# Video Skill Data Pipeline

This context defines the language for a pipeline that learns editing, asset, layout, visual, and sound patterns from curated video examples and turns those patterns into reusable AI video-production skills.

## Language

**Timeline Segment**:
A timestamped slice of a video sample that contains observable evidence for one or more editing, asset, visual, layout, or sound decisions. Timeline segments are the atomic learning unit; video and channel patterns are aggregated from them.
_Avoid_: Timestamp thing, clip note, moment

**Channel Profile**:
An aggregate description of a channel's repeatable content style, derived from its sampled videos and timeline segments.
_Avoid_: Channel DNA, creator vibe

**Extraction Mission**:
The specific analysis goal assigned to a channel or video sample, such as learning asset selection, sound sync, layout density, or retention pacing.
_Avoid_: Criteria, focus area

**Weighting Matrix**:
The category-by-channel score table that decides which extraction missions matter most for each channel profile.
_Avoid_: Category scores, importance table

**Video Sample**:
A curated video selected from a channel for analysis. A video sample is not analyzed uniformly; it is scanned and segmented according to the channel's extraction mission and weighting matrix.
_Avoid_: Full video, source video

**Segment Discovery**:
The first analysis pass that scans a video sample to find candidate timeline segments worth deeper multimodal extraction.
_Avoid_: Full analysis, rough notes

**Deep Extraction**:
The second analysis pass that turns selected timeline segments into structured observations about assets, layout, pacing, sound, text density, and visual effects.
_Avoid_: Video review, final notes

**Video Analysis File**:
A per-video Markdown artifact written by an analysis agent to store discovered segments, deep observations, and category-specific evidence without carrying the whole video context into later work.
_Avoid_: an.md, notes file, dump

**Analysis Batch**:
The number of video samples assigned to one analysis run, chosen based on context-window capacity and video complexity. An analysis batch may contain multiple videos, but it must still produce one video analysis file per video.
_Avoid_: Agent workload, chunk

**Agent Packet**:
A bounded input package assembled for one agent run, containing the manifest record, evidence paths, prompt stack, weighting matrix version, and output contract needed for that agent to complete its assigned stage.
_Avoid_: Prompt dump, task bundle, agent context

**Evidence Bundle**:
A compact set of helper artifacts generated from one video sample before deep LLM analysis, such as transcripts, frame grids, scene changes, and audio markers.
_Avoid_: Helper files, preprocessing dump

**Zoom-In Verification**:
A targeted check of the raw local video at a specific timestamp after the Evidence Bundle has already identified a moment that needs closer inspection.
_Avoid_: Watching the full video, raw video review, general inspection

**Transcript Provider**:
An external or local service used during preprocessing to produce transcript text from a video link or video file before AI analysis begins.
_Avoid_: Transcript website, caption tool

**Structured Transcript**:
A machine-readable transcript artifact made of timestamped segments. It exists to support timeline alignment, Evidence References, and narration-dependent analysis, not human reading.
_Avoid_: transcript doc, readable transcript, transcript notes

**Transcript Failure**:
A preprocessing state where the transcript provider does not produce usable transcript text after the configured retry attempts. Transcript failure does not remove a video sample from analysis; it marks the video for visual and audio analysis without narration evidence.
_Avoid_: Bad transcript, skipped video

**Evidence Confidence**:
The trust level assigned to an observation based on which evidence types were available. Missing transcripts lower confidence for narration-dependent categories while preserving visual and audio observations.
_Avoid_: Certainty score, guess quality

**Video ID**:
A stable human-readable identifier used for folders, manifests, evidence bundles, and analysis files. A video ID is paired with the original platform ID for provenance.
_Avoid_: File name, reel ID

**Platform ID**:
The original source-platform identifier for a video sample, such as an Instagram Reel shortcode, preserved for traceability.
_Avoid_: Video ID, folder ID

**Evidence Reference**:
A timestamp-specific reference artifact that connects an observation or final skill rule back to the source video, timestamp, surrounding frames, and related transcript/audio markers.
_Avoid_: Citation, proof file

**Extension Note**:
A structured secondary note attached to analysis output for uncertainties, edge cases, extra observations, synthesis hints, schema gaps, or references that may help later synthesis without replacing primary evidence.
_Avoid_: Dump, scratch note, loose note

**Video Analysis Agent**:
An agent assigned to one analysis batch that reads prepared evidence bundles, records per-video observations, and creates focused evidence references. A video analysis agent does not make cross-video, cross-channel, or final skill conclusions.
_Avoid_: Video agent, analyzer, sub-agent

**Channel Synthesis Agent**:
An agent that reads completed video analysis files from one channel and summarizes channel-level patterns for category synthesis. A channel synthesis agent does not create final category skills.
_Avoid_: Channel agent, profile agent

**Global Synthesis Agent**:
An agent that reads channel synthesis outputs and category evidence to create the final per-category skills.
_Avoid_: Skill agent, final agent

**Pilot Review Agent**:
An agent that audits pilot run outputs against objective quality gates and automatically decides whether the pipeline can proceed to full rollout or must be revised. A pilot review agent writes review reports and pipeline improvement plans, but does not directly modify analysis or evidence files.
_Avoid_: Manual reviewer, QA agent

**Prompt Revision Agent**:
An agent that revises prompt files from documented pilot review findings. A prompt revision agent changes prompts only to address specific observed failures, because prompt revisions can make analysis worse when they add vague or competing instructions.
_Avoid_: Prompt improver, prompt fixer

**Pipeline Orchestrator**:
The local controller that owns stage state, assembles Agent Packets, validates outputs, and decides which pipeline stage is eligible to run next based on explicit artifacts.
_Avoid_: Agent manager, master agent, runner

**Pilot Run**:
A small first analysis run, normally two video samples per channel, used to validate preprocessing, prompts, evidence references, schemas, and weighting thresholds before analyzing the full dataset.
_Avoid_: Test batch, trial

**Random Pilot Selection**:
A pilot selection method where a fixed number of video samples are selected randomly from each channel when the channel's videos are similar enough that manual representative selection is unnecessary.
_Avoid_: Arbitrary pilot, cherry-picked pilot, manual sample

**Category Skill**:
A final reusable skill generated for one analysis category, backed by evidence references from the dataset.
_Avoid_: Channel skill, style clone
