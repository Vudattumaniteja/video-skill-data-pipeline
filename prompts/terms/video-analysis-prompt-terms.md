# Video Analysis Prompt Terms

Use these terms consistently in prompts and outputs.

## Agent Roles

**Video Analysis Agent**: reads Evidence Bundles, writes per-video analysis files, and creates Evidence References. It does not synthesize cross-video conclusions.

**Channel Synthesis Agent**: reads completed per-video files for one channel and summarizes channel-level patterns.

**Global Synthesis Agent**: creates final per-category skills from channel/category evidence.

**Pilot Review Agent**: audits the Pilot Run and writes pipeline improvement plans before full rollout.

**Prompt Revision Agent**: revises prompt files from pilot evidence and documented review findings.

## Evidence Terms

**Evidence Bundle**: pre-AI artifacts generated from one video, including transcript metadata, frame grid, scene changes, audio peaks, keyframes, and video index.

**Evidence Reference**: timestamp-specific proof package created by the Video Analysis Agent for a strong observation.

**Evidence Confidence**: score showing how strongly the available evidence supports an observation.

**Transcript Failure**: Proactor did not produce a usable transcript after three attempts; analysis continues without narration evidence.

## Output Terms

**Video Analysis File**: human-readable Markdown analysis for one video.

**Analysis JSON**: canonical machine-readable extraction record for one video.

**Channel Profile**: intermediate synthesis output for one channel.

**Category Skill**: final reusable skill produced per category.

