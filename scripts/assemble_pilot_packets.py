#!/usr/bin/env python3
"""
Assemble paste-ready Video Analysis Agent packets for the pilot run.

The script does not call an LLM. It reads the manifest, prompt modules, and
pilot run definition, then writes one RUN_PROMPT.md packet per pilot video.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


CHANNEL_PROMPTS = {
    "channel_1_upgrido_retro_doc": "channel-1-upgrido-retro-doc.md",
    "channel_2_100x_engineers": "channel-2-100x-engineers.md",
    "channel_3_aevy_tv": "channel-3-aevy-tv.md",
    "channel_4_varunmaya": "channel-4-varunmaya.md",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fenced_json(payload: Any) -> str:
    return "```json\n" + json.dumps(payload, indent=2, ensure_ascii=False) + "\n```"


def load_pilot_records(root: Path, run_id: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    runs = read_json(root / "manifest" / "runs.json")["runs"]
    run = next((item for item in runs if item["run_id"] == run_id), None)
    if not run:
        raise SystemExit(f"Run not found: {run_id}")

    manifest = read_json(root / "manifest" / "videos.json")["videos"]
    by_id = {video["video_id"]: video for video in manifest}
    missing = [video_id for video_id in run["video_ids"] if video_id not in by_id]
    if missing:
        raise SystemExit(f"Pilot run references missing videos: {', '.join(missing)}")
    return run, [by_id[video_id] for video_id in run["video_ids"]]


def build_packet(root: Path, run: dict[str, Any], video: dict[str, Any]) -> str:
    prompts_dir = root / "prompts"
    channel_prompt = CHANNEL_PROMPTS.get(video["channel_id"])
    if not channel_prompt:
        raise SystemExit(f"No channel prompt mapping for {video['channel_id']}")

    evidence_dir = root / video["evidence_dir"]
    required = [
        "source_metadata.json",
        "caption.txt",
        "transcript_meta.json",
        "transcript.json",
        "video_metadata.json",
        "frame_grid_1fps.jpg",
        "scene_changes.json",
        "audio_peaks.json",
        "keyframes/keyframes.json",
        "video_index.json",
    ]
    availability = {name: (evidence_dir / name).exists() for name in required}

    return f"""# Pilot Video Analysis Packet: {video["video_id"]}

Run ID: {run["run_id"]}
Prompt Version: {run["prompt_version"]}
Weighting Matrix Version: {run["weighting_matrix_version"]}

## Operating Instruction

Run one Video Analysis Agent for this video only. Produce the two required output files and the Evidence Reference folders. Do not make cross-video, cross-channel, synthesis, or final-skill claims.

## Required Output Paths

- Markdown analysis: `{video["analysis_file"]}`
- JSON analysis: `{video["analysis_json"]}`
- Evidence references: `evidence/{video["channel_id"]}/{video["video_id"]}/references/obs_###/`

## Source Video

- Local file: `{video["local_file"]}`
- Use the raw video only for timestamp-specific zoom-in verification.

## Evidence Bundle

- Evidence directory: `{video["evidence_dir"]}`
- Availability:

{fenced_json(availability)}

## Prompt Stack

### Base Video Analysis Prompt

{read_text(prompts_dir / "base-video-analysis-prompt.md")}

### Category Framework

{read_text(prompts_dir / "categories" / "category-framework.md")}

### Channel Module

{read_text(prompts_dir / "channels" / channel_prompt)}

## Weighting Matrix v1

{fenced_json(read_json(root / "manifest" / "weighting_matrix_v1.json"))}

## Video Manifest Record

{fenced_json(video)}

## Evidence Files To Read First

1. `{video["evidence_dir"]}transcript_meta.json`
2. `{video["evidence_dir"]}video_metadata.json`
3. `{video["evidence_dir"]}video_index.json`
4. `{video["evidence_dir"]}transcript.json`
5. `{video["evidence_dir"]}frame_grid_1fps.jpg`
6. `{video["evidence_dir"]}keyframes/keyframes.json`
7. `{video["evidence_dir"]}scene_changes.json`
8. `{video["evidence_dir"]}audio_peaks.json`

## Extra Pilot Notes

- Target 5-12 observations.
- Create one Evidence Reference folder for each selected observation.
- Include `extensions.notes` for uncertainty, prompt/schema problems, transcript quality issues, or evidence gaps.
- Record edge cases explicitly; they are useful for the Pilot Review Agent.
"""


def main() -> None:
    parser = argparse.ArgumentParser(description="Assemble pilot analysis packets.")
    parser.add_argument("--run-id", default="pilot_v1_001")
    parser.add_argument("--out-dir", default="pilot/agent_packets")
    args = parser.parse_args()

    root = Path.cwd()
    run, videos = load_pilot_records(root, args.run_id)
    out_dir = root / args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    index_lines = [
        f"# Pilot Agent Packets",
        "",
        f"Created: {datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')}",
        f"Run ID: {run['run_id']}",
        "",
    ]

    for video in videos:
        packet_dir = out_dir / video["video_id"]
        packet_dir.mkdir(parents=True, exist_ok=True)
        packet_path = packet_dir / "RUN_PROMPT.md"
        packet_path.write_text(build_packet(root, run, video), encoding="utf-8")
        index_lines.append(f"- `{video['video_id']}`: `{packet_path.relative_to(root)}`")

    index_path = out_dir / "README.md"
    index_path.write_text("\n".join(index_lines) + "\n", encoding="utf-8")
    print(f"wrote {len(videos)} pilot packets to {out_dir}")
    print(f"index: {index_path}")


if __name__ == "__main__":
    main()
