#!/usr/bin/env python3
"""
Generate deterministic Evidence Bundles for the Video Skill Data Pipeline.

This creates visual, audio, scene-change, keyframe, and merged timeline artifacts
from the local videos listed in manifest/videos.json.
"""

from __future__ import annotations

import argparse
import json
import math
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw, ImageFont


SCENE_THRESHOLD = 0.22
MAX_KEYFRAME_EVENTS = 12
AUDIO_WINDOW_SECONDS = 0.25
AUDIO_PEAK_MIN_GAP_SECONDS = 0.75
MAX_AUDIO_PEAKS = 80
SCENE_MIN_GAP_SECONDS = 0.35


@dataclass(frozen=True)
class VideoRecord:
    video_id: str
    channel_id: str
    source_url: str
    local_file: Path
    evidence_dir: Path
    dataset_split: str


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def run_command(cmd: list[str], cwd: Path | None = None, capture: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        cmd,
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE if capture else None,
        stderr=subprocess.PIPE if capture else None,
    )


def load_manifest(root: Path) -> list[dict[str, Any]]:
    manifest_path = root / "manifest" / "videos.json"
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    return payload["videos"]


def to_records(root: Path, videos: list[dict[str, Any]], split: str) -> list[VideoRecord]:
    records: list[VideoRecord] = []
    for video in videos:
        if split != "all" and video["dataset_split"] != split:
            continue
        records.append(
            VideoRecord(
                video_id=video["video_id"],
                channel_id=video["channel_id"],
                source_url=video["source_url"],
                local_file=root / video["local_file"],
                evidence_dir=root / video["evidence_dir"],
                dataset_split=video["dataset_split"],
            )
        )
    return records


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_fraction(value: str | None) -> float | None:
    if not value or value == "0/0":
        return None
    if "/" in value:
        numerator, denominator = value.split("/", 1)
        try:
            denominator_float = float(denominator)
            return float(numerator) / denominator_float if denominator_float else None
        except ValueError:
            return None
    try:
        return float(value)
    except ValueError:
        return None


def format_timestamp(seconds: float) -> str:
    minutes = int(seconds // 60)
    remainder = seconds - (minutes * 60)
    return f"{minutes:02d}:{remainder:04.1f}"


def parse_timestamp_seconds(value: Any) -> float:
    if isinstance(value, int | float):
        return float(value)
    if value is None:
        return 0.0
    text = str(value).strip()
    if not text:
        return 0.0
    try:
        return float(text)
    except ValueError:
        pass

    parts = text.split(":")
    try:
        if len(parts) == 2:
            minutes, seconds = parts
            return (float(minutes) * 60) + float(seconds)
        if len(parts) == 3:
            hours, minutes, seconds = parts
            return (float(hours) * 3600) + (float(minutes) * 60) + float(seconds)
    except ValueError:
        return 0.0
    return 0.0


def probe_video(record: VideoRecord) -> dict[str, Any]:
    cmd = [
        "ffprobe",
        "-v",
        "error",
        "-print_format",
        "json",
        "-show_format",
        "-show_streams",
        str(record.local_file),
    ]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed for {record.video_id}: {result.stderr}")
    payload = json.loads(result.stdout)
    video_stream = next((stream for stream in payload.get("streams", []) if stream.get("codec_type") == "video"), {})
    audio_stream = next((stream for stream in payload.get("streams", []) if stream.get("codec_type") == "audio"), {})
    duration = float(payload.get("format", {}).get("duration") or video_stream.get("duration") or 0)
    return {
        "video_id": record.video_id,
        "channel_id": record.channel_id,
        "local_file": str(record.local_file),
        "duration_seconds": round(duration, 3),
        "size_bytes": int(payload.get("format", {}).get("size") or record.local_file.stat().st_size),
        "video": {
            "codec": video_stream.get("codec_name"),
            "width": video_stream.get("width"),
            "height": video_stream.get("height"),
            "display_aspect_ratio": video_stream.get("display_aspect_ratio"),
            "avg_frame_rate": parse_fraction(video_stream.get("avg_frame_rate")),
            "pix_fmt": video_stream.get("pix_fmt"),
        },
        "audio": {
            "codec": audio_stream.get("codec_name"),
            "sample_rate": int(audio_stream["sample_rate"]) if audio_stream.get("sample_rate") else None,
            "channels": audio_stream.get("channels"),
        },
        "created_at": iso_now(),
    }


def build_frame_grid(
    record: VideoRecord,
    duration: float,
    thumb_width: int,
    columns: int,
    jpeg_quality: int,
    overwrite: bool,
) -> dict[str, Any]:
    output = record.evidence_dir / "frame_grid_1fps.jpg"
    if output.exists() and not overwrite:
        return {"path": str(output), "status": "exists"}

    with tempfile.TemporaryDirectory(prefix=f"{record.video_id}_frames_") as tmp_name:
        tmp = Path(tmp_name)
        pattern = tmp / "frame_%05d.jpg"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(record.local_file),
            "-vf",
            f"fps=1,scale={thumb_width}:-1:flags=lanczos",
            "-q:v",
            "2",
            str(pattern),
        ]
        result = run_command(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"frame extraction failed for {record.video_id}: {result.stderr}")

        frame_paths = sorted(tmp.glob("frame_*.jpg"))
        if not frame_paths:
            raise RuntimeError(f"no 1fps frames created for {record.video_id}")

        font = ImageFont.load_default()
        labeled_frames: list[Image.Image] = []
        for index, frame_path in enumerate(frame_paths):
            image = Image.open(frame_path).convert("RGB")
            label_h = 22
            canvas = Image.new("RGB", (image.width, image.height + label_h), "black")
            canvas.paste(image, (0, label_h))
            draw = ImageDraw.Draw(canvas)
            draw.text((6, 5), format_timestamp(float(index)), fill="white", font=font)
            labeled_frames.append(canvas)

        cell_w = max(frame.width for frame in labeled_frames)
        cell_h = max(frame.height for frame in labeled_frames)
        rows = math.ceil(len(labeled_frames) / columns)
        grid = Image.new("RGB", (cell_w * columns, cell_h * rows), "white")
        for index, frame in enumerate(labeled_frames):
            x = (index % columns) * cell_w
            y = (index // columns) * cell_h
            grid.paste(frame, (x, y))

        output.parent.mkdir(parents=True, exist_ok=True)
        grid.save(output, quality=jpeg_quality, subsampling=0, optimize=True)
        for frame in labeled_frames:
            frame.close()
        grid.close()

    return {
        "path": str(output),
        "status": "created",
        "fps": 1,
        "frames": len(frame_paths),
        "duration_seconds": duration,
        "columns": columns,
        "thumb_width": thumb_width,
        "jpeg_quality": jpeg_quality,
    }


def detect_scene_changes(record: VideoRecord, overwrite: bool) -> dict[str, Any]:
    output = record.evidence_dir / "scene_changes.json"
    if output.exists() and not overwrite:
        return json.loads(output.read_text(encoding="utf-8"))

    metadata_file = record.evidence_dir / "_scene_metadata.txt"
    cmd = [
        "ffmpeg",
        "-y",
        "-i",
        str(record.local_file),
        "-vf",
        f"select='gt(scene,{SCENE_THRESHOLD})',metadata=print:file=_scene_metadata.txt",
        "-an",
        "-f",
        "null",
        "-",
    ]
    result = run_command(cmd, cwd=record.evidence_dir)
    if result.returncode != 0:
        raise RuntimeError(f"scene detection failed for {record.video_id}: {result.stderr}")

    raw_events: list[dict[str, Any]] = []
    current_time: float | None = None
    pts_re = re.compile(r"pts_time:([0-9.]+)")
    score_re = re.compile(r"lavfi\.scene_score=([0-9.]+)")
    if metadata_file.exists():
        for line in metadata_file.read_text(encoding="utf-8", errors="ignore").splitlines():
            pts_match = pts_re.search(line)
            if pts_match:
                current_time = float(pts_match.group(1))
            score_match = score_re.search(line)
            if score_match and current_time is not None:
                score = float(score_match.group(1))
                raw_events.append(
                    {
                        "timestamp": format_timestamp(current_time),
                        "time_seconds": round(current_time, 3),
                        "change_type": "scene_change",
                        "confidence": round(min(1.0, score), 4),
                    }
                )
        metadata_file.unlink(missing_ok=True)

    events: list[dict[str, Any]] = []
    for event in sorted(raw_events, key=lambda item: (-float(item["confidence"]), float(item["time_seconds"]))):
        if all(abs(float(event["time_seconds"]) - float(existing["time_seconds"])) >= SCENE_MIN_GAP_SECONDS for existing in events):
            events.append(event)
    events.sort(key=lambda item: float(item["time_seconds"]))

    payload = {
        "video_id": record.video_id,
        "threshold": SCENE_THRESHOLD,
        "min_gap_seconds": SCENE_MIN_GAP_SECONDS,
        "scene_changes": events,
        "count": len(events),
        "created_at": iso_now(),
    }
    write_json(output, payload)
    return payload


def analyze_audio_peaks(record: VideoRecord, duration: float, overwrite: bool) -> dict[str, Any]:
    output = record.evidence_dir / "audio_peaks.json"
    if output.exists() and not overwrite:
        return json.loads(output.read_text(encoding="utf-8"))

    sample_rate = 16000
    with tempfile.TemporaryDirectory(prefix=f"{record.video_id}_audio_") as tmp_name:
        raw_path = Path(tmp_name) / "audio.f32"
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            str(record.local_file),
            "-vn",
            "-ac",
            "1",
            "-ar",
            str(sample_rate),
            "-f",
            "f32le",
            str(raw_path),
        ]
        result = run_command(cmd)
        if result.returncode != 0:
            raise RuntimeError(f"audio extraction failed for {record.video_id}: {result.stderr}")
        audio = np.fromfile(raw_path, dtype=np.float32)

    if audio.size == 0:
        payload = {
            "video_id": record.video_id,
            "window_seconds": AUDIO_WINDOW_SECONDS,
            "audio_peaks": [],
            "summary": {"rms_mean": 0, "rms_p95": 0, "rms_max": 0},
            "created_at": iso_now(),
        }
        write_json(output, payload)
        return payload

    window_size = max(1, int(sample_rate * AUDIO_WINDOW_SECONDS))
    window_count = math.ceil(audio.size / window_size)
    padded = np.pad(audio, (0, window_count * window_size - audio.size))
    windows = padded.reshape(window_count, window_size)
    rms = np.sqrt(np.mean(np.square(windows), axis=1))
    p85 = float(np.percentile(rms, 85))
    p95 = float(np.percentile(rms, 95))
    p75 = float(np.percentile(rms, 75))
    threshold = max(p85, p75 * 1.15, float(np.mean(rms)) * 1.35)

    candidate_indices = np.where(rms >= threshold)[0]
    sorted_candidates = sorted(candidate_indices, key=lambda idx: float(rms[idx]), reverse=True)
    selected: list[int] = []
    min_gap_windows = max(1, int(AUDIO_PEAK_MIN_GAP_SECONDS / AUDIO_WINDOW_SECONDS))
    for idx in sorted_candidates:
        if all(abs(int(idx) - existing) >= min_gap_windows for existing in selected):
            selected.append(int(idx))
        if len(selected) >= MAX_AUDIO_PEAKS:
            break
    selected.sort()

    max_rms = float(np.max(rms)) or 1.0
    peaks = []
    for idx in selected:
        start = idx * AUDIO_WINDOW_SECONDS
        end = min(duration, start + AUDIO_WINDOW_SECONDS)
        peaks.append(
            {
                "timestamp": format_timestamp(start),
                "time_seconds": round(start, 3),
                "end_seconds": round(end, 3),
                "event_type": "audio_peak",
                "intensity": round(float(rms[idx]) / max_rms, 4),
                "rms": round(float(rms[idx]), 6),
            }
        )

    payload = {
        "video_id": record.video_id,
        "window_seconds": AUDIO_WINDOW_SECONDS,
        "sample_rate": sample_rate,
        "audio_peaks": peaks,
        "count": len(peaks),
        "summary": {
            "rms_mean": round(float(np.mean(rms)), 6),
            "rms_p75": round(p75, 6),
            "rms_p85": round(p85, 6),
            "rms_p95": round(p95, 6),
            "rms_max": round(max_rms, 6),
            "threshold": round(float(threshold), 6),
        },
        "created_at": iso_now(),
    }
    write_json(output, payload)
    return payload


def extract_frame_at(video_path: Path, timestamp: float, output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",
        "-ss",
        f"{max(0.0, timestamp):.3f}",
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(output),
    ]
    result = run_command(cmd)
    if result.returncode != 0:
        raise RuntimeError(f"frame extraction failed at {timestamp}: {result.stderr}")


def build_keyframes(record: VideoRecord, duration: float, scene_payload: dict[str, Any], overwrite: bool) -> dict[str, Any]:
    keyframes_dir = record.evidence_dir / "keyframes"
    index_path = keyframes_dir / "keyframes.json"
    if index_path.exists() and not overwrite:
        return json.loads(index_path.read_text(encoding="utf-8"))

    if keyframes_dir.exists() and overwrite:
        shutil.rmtree(keyframes_dir)
    keyframes_dir.mkdir(parents=True, exist_ok=True)

    scene_events = sorted(
        scene_payload.get("scene_changes", []),
        key=lambda event: (-float(event.get("confidence", 0)), float(event["time_seconds"])),
    )
    scene_times = [float(event["time_seconds"]) for event in scene_events[:MAX_KEYFRAME_EVENTS]]
    scene_times.sort()
    if not scene_times:
        if duration <= 0:
            scene_times = [0.0]
        else:
            scene_times = sorted({0.0, duration / 3, (duration * 2) / 3, max(0.0, duration - 1.0)})

    records = []
    for event_index, scene_time in enumerate(scene_times, start=1):
        event_name = f"scene_{event_index:03d}"
        samples = [
            ("before", max(0.0, scene_time - 0.5)),
            ("at", max(0.0, scene_time)),
            ("after", min(max(0.0, duration - 0.05), scene_time + 0.5)),
        ]
        files = {}
        for label, timestamp in samples:
            output = keyframes_dir / f"{event_name}_{label}.jpg"
            extract_frame_at(record.local_file, timestamp, output)
            files[label] = {
                "path": str(output.relative_to(record.evidence_dir)),
                "timestamp": format_timestamp(timestamp),
                "time_seconds": round(timestamp, 3),
            }
        records.append(
            {
                "event_id": event_name,
                "source_time_seconds": round(scene_time, 3),
                "source_timestamp": format_timestamp(scene_time),
                "frames": files,
            }
        )

    payload = {"video_id": record.video_id, "keyframes": records, "count": len(records), "created_at": iso_now()}
    write_json(index_path, payload)
    return payload


def load_optional_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def build_video_index(
    record: VideoRecord,
    metadata: dict[str, Any],
    scene_payload: dict[str, Any],
    audio_payload: dict[str, Any],
    keyframe_payload: dict[str, Any],
) -> dict[str, Any]:
    transcript_meta = load_optional_json(record.evidence_dir / "transcript_meta.json")
    transcript = load_optional_json(record.evidence_dir / "transcript.json")
    transcript_status = "not_started"
    if transcript_meta:
        transcript_status = transcript_meta.get("status", "unknown")

    events: list[dict[str, Any]] = []
    for scene in scene_payload.get("scene_changes", []):
        events.append(
            {
                "timestamp": scene["timestamp"],
                "time_seconds": scene["time_seconds"],
                "event_type": "visual_change",
                "visual_change": scene.get("change_type"),
                "confidence": scene.get("confidence"),
            }
        )
    for peak in audio_payload.get("audio_peaks", []):
        events.append(
            {
                "timestamp": peak["timestamp"],
                "time_seconds": peak["time_seconds"],
                "event_type": "audio_peak",
                "audio_peak": True,
                "intensity": peak.get("intensity"),
            }
        )
    for keyframe in keyframe_payload.get("keyframes", []):
        events.append(
            {
                "timestamp": keyframe["source_timestamp"],
                "time_seconds": keyframe["source_time_seconds"],
                "event_type": "keyframe_set",
                "keyframe_event_id": keyframe["event_id"],
                "keyframes": keyframe["frames"],
            }
        )

    if transcript and transcript.get("segments"):
        for segment in transcript["segments"]:
            start = parse_timestamp_seconds(segment.get("start_seconds", segment.get("start", 0)))
            events.append(
                {
                    "timestamp": format_timestamp(start),
                    "time_seconds": round(start, 3),
                    "event_type": "transcript_segment",
                    "transcript_text": segment.get("text", ""),
                }
            )

    events.sort(key=lambda item: (float(item["time_seconds"]), item["event_type"]))
    payload = {
        "video_id": record.video_id,
        "channel_id": record.channel_id,
        "duration_seconds": metadata["duration_seconds"],
        "transcript_status": transcript_status,
        "evidence_artifacts": {
            "source_metadata": "source_metadata.json",
            "caption": "caption.txt" if (record.evidence_dir / "caption.txt").exists() else None,
            "transcript": "transcript.json" if (record.evidence_dir / "transcript.json").exists() else None,
            "transcript_meta": "transcript_meta.json" if (record.evidence_dir / "transcript_meta.json").exists() else None,
            "frame_grid": "frame_grid_1fps.jpg",
            "scene_changes": "scene_changes.json",
            "audio_peaks": "audio_peaks.json",
            "keyframes": "keyframes/keyframes.json",
        },
        "timeline_events": events,
        "event_counts": {
            "visual_changes": len(scene_payload.get("scene_changes", [])),
            "audio_peaks": len(audio_payload.get("audio_peaks", [])),
            "keyframe_sets": len(keyframe_payload.get("keyframes", [])),
            "transcript_segments": len(transcript.get("segments", [])) if transcript else 0,
        },
        "created_at": iso_now(),
    }
    write_json(record.evidence_dir / "video_index.json", payload)
    return payload


def write_transcript_placeholder(record: VideoRecord, overwrite: bool) -> None:
    meta_path = record.evidence_dir / "transcript_meta.json"
    if meta_path.exists() and not overwrite:
        return
    payload = {
        "provider": "proactor",
        "status": "not_started",
        "attempts": 0,
        "source_url": record.source_url,
        "fallback_provider": None,
        "analysis_policy": "pending_transcript",
        "transcript_artifact": None,
        "timestamped": None,
        "created_at": iso_now(),
    }
    write_json(meta_path, payload)


def preprocess_record(
    record: VideoRecord,
    thumb_width: int,
    columns: int,
    jpeg_quality: int,
    overwrite: bool,
) -> dict[str, Any]:
    if not record.local_file.exists():
        raise FileNotFoundError(f"Missing local video for {record.video_id}: {record.local_file}")
    record.evidence_dir.mkdir(parents=True, exist_ok=True)
    write_transcript_placeholder(record, overwrite=False)
    metadata = probe_video(record)
    write_json(record.evidence_dir / "video_metadata.json", metadata)
    duration = float(metadata["duration_seconds"])
    frame_grid = build_frame_grid(record, duration, thumb_width, columns, jpeg_quality, overwrite)
    scene_payload = detect_scene_changes(record, overwrite)
    audio_payload = analyze_audio_peaks(record, duration, overwrite)
    keyframe_payload = build_keyframes(record, duration, scene_payload, overwrite)
    index_payload = build_video_index(record, metadata, scene_payload, audio_payload, keyframe_payload)

    summary = {
        "video_id": record.video_id,
        "channel_id": record.channel_id,
        "duration_seconds": duration,
        "frame_grid": frame_grid,
        "scene_changes": scene_payload.get("count", 0),
        "audio_peaks": audio_payload.get("count", 0),
        "keyframe_sets": keyframe_payload.get("count", 0),
        "timeline_events": len(index_payload.get("timeline_events", [])),
        "status": "ok",
    }
    return summary


def validate_bundle(record: VideoRecord) -> dict[str, Any]:
    required = [
        "source_metadata.json",
        "caption.txt",
        "transcript_meta.json",
        "frame_grid_1fps.jpg",
        "scene_changes.json",
        "audio_peaks.json",
        "keyframes/keyframes.json",
        "video_metadata.json",
        "video_index.json",
    ]
    missing = []
    empty = []
    for rel_path in required:
        path = record.evidence_dir / rel_path
        if not path.exists():
            missing.append(rel_path)
        elif path.is_file() and path.stat().st_size == 0:
            empty.append(rel_path)
    return {
        "video_id": record.video_id,
        "channel_id": record.channel_id,
        "missing": missing,
        "empty": empty,
        "status": "ok" if not missing and not empty else "incomplete",
    }


def write_summary_markdown(root: Path, report: dict[str, Any]) -> None:
    summaries = report["summaries"]
    by_channel: dict[str, list[dict[str, Any]]] = {}
    for summary in summaries:
        by_channel.setdefault(summary["channel_id"], []).append(summary)

    lines = [
        "# Preprocessing Summary",
        "",
        f"Created: {report['created_at']}",
        f"Split: {report['split']}",
        f"Videos processed: {report['video_count']}",
        f"Complete Evidence Bundles: {report['success_count']}",
        f"Failures: {report['failure_count']}",
        "",
        "## Totals",
        "",
        f"- Scene changes: {sum(item['scene_changes'] for item in summaries)}",
        f"- Audio peaks: {sum(item['audio_peaks'] for item in summaries)}",
        f"- Keyframe sets: {sum(item['keyframe_sets'] for item in summaries)}",
        f"- Timeline events: {sum(item['timeline_events'] for item in summaries)}",
        "",
        "## By Channel",
        "",
    ]
    for channel_id, channel_items in sorted(by_channel.items()):
        lines.extend(
            [
                f"### {channel_id}",
                "",
                f"- Videos: {len(channel_items)}",
                f"- Scene changes: {sum(item['scene_changes'] for item in channel_items)}",
                f"- Audio peaks: {sum(item['audio_peaks'] for item in channel_items)}",
                f"- Keyframe sets: {sum(item['keyframe_sets'] for item in channel_items)}",
                f"- Timeline events: {sum(item['timeline_events'] for item in channel_items)}",
                "",
            ]
        )

    if report["failures"]:
        lines.extend(["## Failures", ""])
        for failure in report["failures"]:
            lines.append(f"- `{failure['video_id']}`: {failure['error']}")
    else:
        lines.extend(["## Failures", "", "- None"])

    (root / "manifest" / "preprocessing_summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate Evidence Bundle helper artifacts for local videos.")
    parser.add_argument("--root", default=".", help="Pipeline workspace root.")
    parser.add_argument("--split", choices=["all", "pilot", "full_rollout"], default="all")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--thumb-width", type=int, default=360)
    parser.add_argument("--grid-columns", type=int, default=6)
    parser.add_argument("--jpeg-quality", type=int, default=95)
    args = parser.parse_args()

    root = Path(args.root).resolve()
    videos = load_manifest(root)
    records = to_records(root, videos, args.split)
    if args.limit is not None:
        records = records[: args.limit]

    summaries = []
    failures = []
    for index, record in enumerate(records, start=1):
        print(f"[{index}/{len(records)}] preprocessing {record.video_id}")
        try:
            summaries.append(
                preprocess_record(
                    record,
                    thumb_width=args.thumb_width,
                    columns=args.grid_columns,
                    jpeg_quality=args.jpeg_quality,
                    overwrite=args.overwrite,
                )
            )
        except Exception as exc:
            failures.append({"video_id": record.video_id, "error": str(exc)})
            print(f"  failed: {exc}")

    validations = [validate_bundle(record) for record in records]
    report = {
        "created_at": iso_now(),
        "split": args.split,
        "video_count": len(records),
        "success_count": sum(1 for item in validations if item["status"] == "ok"),
        "failure_count": len(failures),
        "summaries": summaries,
        "failures": failures,
        "validations": validations,
    }
    write_json(root / "manifest" / "preprocessing_report.json", report)
    write_summary_markdown(root, report)
    print(f"success_count={report['success_count']} failure_count={report['failure_count']}")
    return 1 if failures or report["success_count"] != len(records) else 0


if __name__ == "__main__":
    raise SystemExit(main())
