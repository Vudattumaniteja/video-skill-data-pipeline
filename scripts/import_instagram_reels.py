#!/usr/bin/env python3
"""
Import Instagram reel/post exports into the Video Skill Data Pipeline.

Default mode writes manifests only. Use --download to fetch media with yt-dlp.
Runtime folders are intentionally ignored by git.
"""

from __future__ import annotations

import argparse
import json
import random
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHANNELS = [
    {
        "channel_id": "channel_1_upgrido_retro_doc",
        "display_name": "Upgrido / Retro Doc",
        "source_filename": "upgridolear.json",
        "prompt_module": "prompts/channels/channel-1-upgrido-retro-doc.md",
        "extraction_mission": "Learn asset selection and asset sourcing for premium retro/documentary-style videos.",
    },
    {
        "channel_id": "channel_2_100x_engineers",
        "display_name": "100X engineers",
        "source_filename": "100x Engine.json",
        "prompt_module": "prompts/channels/channel-2-100x-engineers.md",
        "extraction_mission": "Learn fast retention, editing layout, sound-design sync, and dense text/data delivery.",
    },
    {
        "channel_id": "channel_3_aevy_tv",
        "display_name": "Aevy TV",
        "source_filename": "AEVTV.json",
        "prompt_module": "prompts/channels/channel-3-aevy-tv.md",
        "extraction_mission": "Learn essay-style pacing, broad good-video principles, layout support, sound rhythm, and text/data clarity.",
    },
    {
        "channel_id": "channel_4_varunmaya",
        "display_name": "VarunMaya",
        "source_filename": "varunmay 6(only continas 6 reels.json",
        "prompt_module": "prompts/channels/channel-4-varunmaya.md",
        "extraction_mission": "Learn UI/design-focused asset selection, layout systems, sound sync, good-video principles, and high-density visual explanation.",
    },
]

CATEGORIES = [
    "asset_selection",
    "asset_sourcing",
    "good_video_principles",
    "editing_layout",
    "sound_design_sync",
    "data_text_density",
]

WEIGHTS = {
    "channel_1_upgrido_retro_doc": {
        "asset_selection": 9.0,
        "asset_sourcing": 9.5,
        "good_video_principles": 6.5,
        "editing_layout": 7.5,
        "sound_design_sync": 7.0,
        "data_text_density": 6.0,
    },
    "channel_2_100x_engineers": {
        "asset_selection": 7.0,
        "asset_sourcing": 8.0,
        "good_video_principles": 9.5,
        "editing_layout": 9.0,
        "sound_design_sync": 9.5,
        "data_text_density": 9.5,
    },
    "channel_3_aevy_tv": {
        "asset_selection": 8.0,
        "asset_sourcing": 7.5,
        "good_video_principles": 8.5,
        "editing_layout": 8.0,
        "sound_design_sync": 8.0,
        "data_text_density": 8.5,
    },
    "channel_4_varunmaya": {
        "asset_selection": 8.5,
        "asset_sourcing": 8.5,
        "good_video_principles": 9.0,
        "editing_layout": 9.5,
        "sound_design_sync": 9.0,
        "data_text_density": 9.0,
    },
}


@dataclass(frozen=True)
class ChannelConfig:
    index: int
    channel_id: str
    display_name: str
    source_json: Path
    prompt_module: str
    extraction_mission: str


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def clean_text(value: Any) -> Any:
    if isinstance(value, str):
        text = value
        if any(marker in text for marker in ("â", "ð", "Ã")):
            try:
                repaired = text.encode("latin1").decode("utf-8")
                if repaired.count("�") <= text.count("�"):
                    return repaired
            except UnicodeError:
                pass
        return text
    if isinstance(value, list):
        return [clean_text(item) for item in value]
    if isinstance(value, dict):
        return {key: clean_text(item) for key, item in value.items()}
    return value


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def shortcode_from_url(url: str) -> str:
    match = re.search(r"instagram\.com/(?:p|reel|reels)/([^/?#]+)/?", url)
    if not match:
        raise ValueError(f"Cannot extract Instagram shortcode from URL: {url}")
    return match.group(1)


def iso_now() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def channel_configs(source_dir: Path) -> list[ChannelConfig]:
    configs = []
    for index, item in enumerate(CHANNELS, start=1):
        configs.append(
            ChannelConfig(
                index=index,
                channel_id=item["channel_id"],
                display_name=item["display_name"],
                source_json=source_dir / item["source_filename"],
                prompt_module=item["prompt_module"],
                extraction_mission=item["extraction_mission"],
            )
        )
    return configs


def build_manifests(
    root: Path,
    source_dir: Path,
    seed: int,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any], dict[str, Any]]:
    rng = random.Random(seed)
    videos: list[dict[str, Any]] = []
    import_report: dict[str, Any] = {
        "created_at": iso_now(),
        "pilot_seed": seed,
        "source_files": [],
        "channels": [],
        "warnings": [],
    }

    channel_manifest = {"channels": []}
    for config in channel_configs(source_dir):
        if not config.source_json.exists():
            raise FileNotFoundError(f"Missing source JSON: {config.source_json}")

        raw_items = read_json(config.source_json)
        if not isinstance(raw_items, list):
            raise ValueError(f"Expected a JSON array in {config.source_json}")

        pilot_indices = set(rng.sample(range(len(raw_items)), k=min(2, len(raw_items))))
        channel_manifest["channels"].append(
            {
                "channel_id": config.channel_id,
                "display_name": config.display_name,
                "extraction_mission": config.extraction_mission,
                "prompt_module": config.prompt_module,
                "status": "active",
                "source_json": str(config.source_json),
            }
        )

        import_report["source_files"].append(str(config.source_json))
        import_report["channels"].append(
            {
                "channel_id": config.channel_id,
                "display_name": config.display_name,
                "source_count": len(raw_items),
                "pilot_count": len(pilot_indices),
            }
        )

        seen_urls: set[str] = set()
        for offset, item in enumerate(raw_items, start=1):
            if not isinstance(item, dict):
                raise ValueError(f"Item {offset} in {config.source_json} is not an object")

            source_url = str(item.get("url", "")).strip()
            if not source_url:
                raise ValueError(f"Item {offset} in {config.source_json} is missing url")
            if source_url in seen_urls:
                import_report["warnings"].append(f"Duplicate URL in {config.source_json}: {source_url}")
            seen_urls.add(source_url)

            platform_id = shortcode_from_url(source_url)
            video_id = f"channel_{config.index}_video_{offset:03d}"
            local_file = f"input_videos/{config.channel_id}/{video_id}.mp4"
            evidence_dir = f"evidence/{config.channel_id}/{video_id}/"

            videos.append(
                {
                    "video_id": video_id,
                    "channel_id": config.channel_id,
                    "platform": "instagram",
                    "platform_id": platform_id,
                    "source_url": source_url,
                    "local_file": local_file,
                    "evidence_dir": evidence_dir,
                    "analysis_file": f"analysis/{config.channel_id}/{video_id}.md",
                    "analysis_json": f"analysis_json/{config.channel_id}/{video_id}.json",
                    "dataset_split": "pilot" if (offset - 1) in pilot_indices else "full_rollout",
                    "status": "registered",
                    "source_export": {
                        "display_url": clean_text(item.get("displayUrl")),
                        "caption": clean_text(item.get("caption")),
                        "owner_full_name": clean_text(item.get("ownerFullName")),
                        "owner_username": clean_text(item.get("ownerUsername")),
                        "comments_count": item.get("commentsCount"),
                        "likes_count": item.get("likesCount"),
                        "timestamp": clean_text(item.get("timestamp")),
                    },
                }
            )

    runs = {
        "runs": [
            {
                "run_id": "pilot_v1_001",
                "run_type": "pilot",
                "weighting_matrix_version": "v1",
                "prompt_version": "v1",
                "pilot_seed": seed,
                "video_ids": [video["video_id"] for video in videos if video["dataset_split"] == "pilot"],
                "status": "pending",
                "created_at": iso_now(),
            }
        ]
    }
    weights = {"version": "v1", "categories": CATEGORIES, "weights": WEIGHTS}
    return videos, channel_manifest, {"videos": videos}, weights, runs, import_report


def ensure_runtime_dirs(root: Path, videos: list[dict[str, Any]]) -> None:
    for folder in ["manifest", "input_videos", "evidence", "analysis", "analysis_json", "pilot", "synthesis"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    for video in videos:
        (root / Path(video["local_file"]).parent).mkdir(parents=True, exist_ok=True)
        (root / Path(video["evidence_dir"])).mkdir(parents=True, exist_ok=True)
        (root / Path(video["analysis_file"]).parent).mkdir(parents=True, exist_ok=True)
        (root / Path(video["analysis_json"]).parent).mkdir(parents=True, exist_ok=True)


def write_video_evidence_sidecars(root: Path, videos: list[dict[str, Any]]) -> None:
    for video in videos:
        evidence_dir = root / Path(video["evidence_dir"])
        evidence_dir.mkdir(parents=True, exist_ok=True)

        source_metadata = {
            "video_id": video["video_id"],
            "channel_id": video["channel_id"],
            "platform": video["platform"],
            "platform_id": video["platform_id"],
            "source_url": video["source_url"],
            "local_file": video["local_file"],
            "dataset_split": video["dataset_split"],
            "source_export": video["source_export"],
        }
        write_json(evidence_dir / "source_metadata.json", source_metadata)

        caption = video["source_export"].get("caption")
        if caption:
            (evidence_dir / "caption.txt").write_text(str(caption).strip() + "\n", encoding="utf-8")


def download_video(root: Path, video: dict[str, Any], cookies_from_browser: str | None, overwrite: bool) -> str:
    target = root / video["local_file"]
    if target.exists() and not overwrite:
        return "skipped_existing"

    target.parent.mkdir(parents=True, exist_ok=True)
    output_template = str(target.with_suffix(".%(ext)s"))
    cmd = [
        sys.executable,
        "-m",
        "yt_dlp",
        "--no-playlist",
        "--merge-output-format",
        "mp4",
        "-f",
        "bv*+ba/b",
        "-o",
        output_template,
        video["source_url"],
    ]
    if cookies_from_browser:
        cmd[3:3] = ["--cookies-from-browser", cookies_from_browser]

    result = subprocess.run(cmd, cwd=root, text=True)
    if result.returncode != 0:
        return "download_failed"

    possible = sorted(target.parent.glob(target.stem + ".*"))
    if not target.exists():
        mp4s = [path for path in possible if path.suffix.lower() == ".mp4"]
        if mp4s:
            mp4s[0].replace(target)
    return "downloaded" if target.exists() else "download_missing_output"


def write_import_report(root: Path, report: dict[str, Any]) -> None:
    lines = [
        "# Instagram Export Import Report",
        "",
        f"Created: {report['created_at']}",
        f"Pilot seed: {report['pilot_seed']}",
        "",
        "## Channels",
        "",
    ]
    for channel in report["channels"]:
        lines.append(f"- {channel['display_name']} (`{channel['channel_id']}`): {channel['source_count']} records, {channel['pilot_count']} pilot")
    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    else:
        lines.extend(["", "## Warnings", "", "- None"])
    path = root / "manifest" / "draft_import_report.md"
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Import Instagram JSON exports and optionally download media.")
    parser.add_argument("--root", default=".", help="Pipeline workspace root.")
    parser.add_argument("--source-dir", default="source_exports", help="Directory containing the four Instagram JSON exports.")
    parser.add_argument("--seed", type=int, default=20260603, help="Random seed for 2-per-channel pilot selection.")
    parser.add_argument("--download", action="store_true", help="Download videos with py -m yt_dlp.")
    parser.add_argument(
        "--download-split",
        choices=["all", "pilot", "full_rollout"],
        default="all",
        help="Which dataset split to download when --download is set.",
    )
    parser.add_argument("--limit", type=int, help="Maximum number of videos to download for this run.")
    parser.add_argument("--cookies-from-browser", help="Optional yt-dlp browser cookies source, e.g. chrome or edge.")
    parser.add_argument("--overwrite", action="store_true", help="Re-download existing local files.")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    source_dir = Path(args.source_dir).expanduser().resolve()
    videos, channels, videos_manifest, weights, runs, import_report = build_manifests(root, source_dir, args.seed)
    ensure_runtime_dirs(root, videos)
    write_video_evidence_sidecars(root, videos)

    write_json(root / "manifest" / "channels.json", channels)
    write_json(root / "manifest" / "videos.json", videos_manifest)
    write_json(root / "manifest" / "weighting_matrix_v1.json", weights)
    write_json(root / "manifest" / "runs.json", runs)
    write_json(root / "manifest" / "draft_import_report.json", import_report)
    write_import_report(root, import_report)

    print(f"Imported {len(videos)} videos across {len(channels['channels'])} channels.")
    print(f"Pilot videos: {sum(1 for video in videos if video['dataset_split'] == 'pilot')}")

    if args.download:
        statuses: dict[str, str] = {}
        download_set = [video for video in videos if args.download_split == "all" or video["dataset_split"] == args.download_split]
        if args.limit is not None:
            download_set = download_set[: args.limit]
        for video in download_set:
            status = download_video(root, video, args.cookies_from_browser, args.overwrite)
            statuses[video["video_id"]] = status
            print(f"{video['video_id']}: {status}")
        write_json(root / "manifest" / "download_status.json", {"created_at": iso_now(), "statuses": statuses})
    else:
        print("Download not run. Use --download to fetch media.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
