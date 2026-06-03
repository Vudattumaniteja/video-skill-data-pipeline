# Video Skill Data Pipeline PRD

## Problem Statement

The user wants to turn a curated dataset of short Instagram/Reels-style videos into reliable AI video-production skills. The current challenge is that raw multimodal video analysis can easily consume too much context, produce vague observations, overgeneralize from small samples, and generate skills that feel like generic editing advice rather than evidence-backed rules.

The system needs to learn from roughly 40 downloaded Video Samples across four channels, with each channel contributing differently through a Weighting Matrix. Some channels teach asset selection and sourcing better, while others teach pacing, layout, sound sync, text density, or broader good-video principles. The pipeline must preserve this difference instead of treating every video and every channel equally.

## Solution

Build a staged Video Skill Data Pipeline that preprocesses each Video Sample into an Evidence Bundle before AI analysis, uses Video Analysis Agents to create per-video observations and Evidence References, uses a Pilot Run to improve prompts before scaling, and finally produces reusable Category Skills backed by timestamped evidence.

The system uses these stages:

1. Dataset organization and manifests.
2. Evidence Bundle generation before AI analysis.
3. Proactor transcript extraction with three attempts.
4. Segment Discovery and Deep Extraction by Video Analysis Agents.
5. Per-video Markdown and JSON analysis outputs.
6. Evidence References created during video analysis.
7. Pilot Review Agent review after two videos per channel.
8. Prompt Revision Agent changes only from documented pilot failures.
9. Full rollout for remaining videos after pilot approval or revision.
10. Channel Synthesis Agent intermediate summaries.
11. Global Synthesis Agent final per-category Category Skills.

The final product is not a channel clone. The final product is a set of reusable Category Skills:

- Asset selection.
- Asset sourcing.
- Good video principles.
- Editing framework and layout.
- Sound design sync.
- Data and text density.

## User Stories

1. As the pipeline owner, I want each downloaded video to have a stable Video ID, so that folders, manifests, evidence, and analysis files stay traceable.
2. As the pipeline owner, I want each Video ID paired with a Platform ID, so that the original Instagram source can be traced later.
3. As the pipeline owner, I want the manifest to record source URLs and local video paths, so that transcript automation and local preprocessing both have the data they need.
4. As the pipeline owner, I want channel metadata separated from video metadata, so that channel-level weighting and prompt modules are easy to revise.
5. As the pipeline owner, I want a versioned Weighting Matrix, so that future revisions do not erase the weights used by older analysis runs.
6. As the pipeline owner, I want every analysis file to record the Weighting Matrix version, so that later synthesis can audit why categories were extracted or skipped.
7. As the pipeline owner, I want every video to be preprocessed before AI analysis, so that agents reason from compact evidence rather than raw videos alone.
8. As the pipeline owner, I want each Evidence Bundle to contain transcript metadata, frame grids, scene changes, audio peaks, keyframes, and a video index, so that the agent has multiple evidence types.
9. As the pipeline owner, I want transcript extraction to use Proactor from the Instagram URL, so that transcript handling matches the current planned workflow.
10. As the pipeline owner, I want Proactor transcript extraction to retry three times, so that temporary website failures do not immediately remove narration evidence.
11. As the pipeline owner, I want videos with Transcript Failure to continue through analysis, so that visual and audio evidence is still useful.
12. As the pipeline owner, I want missing transcripts to reduce confidence for narration-dependent categories, so that the system does not overclaim.
13. As the pipeline owner, I want per-video Evidence Bundles, so that sub-agents can receive one complete handoff folder.
14. As a Video Analysis Agent, I want a base prompt plus a channel-specific prompt module, so that shared rules stay consistent while extraction focus changes per channel.
15. As a Video Analysis Agent, I want the category framework and weights included in my instructions, so that I prioritize high-value categories.
16. As a Video Analysis Agent, I want to perform Segment Discovery before Deep Extraction, so that I focus only on useful Timeline Segments.
17. As a Video Analysis Agent, I want to write one Video Analysis File per video, so that context stays clean and later synthesis can read independent artifacts.
18. As a Video Analysis Agent, I want to write one analysis JSON file per video, so that synthesis can aggregate data without parsing Markdown.
19. As a Video Analysis Agent, I want to create 5 to 12 Evidence References per 3-minute video, so that final skills have strong proof without excessive noise.
20. As a Video Analysis Agent, I want Evidence References to include before, at, and after frames, so that timestamped claims are visually inspectable.
21. As a Video Analysis Agent, I want Evidence References to include audio and transcript windows when relevant, so that sound sync and narration-dependent observations can be checked.
22. As a Video Analysis Agent, I want to avoid cross-video conclusions, so that evidence does not become contaminated by early generalization.
23. As a Channel Synthesis Agent, I want to read completed video analysis outputs for one channel, so that I can summarize repeated channel patterns.
24. As a Channel Synthesis Agent, I want to avoid creating final Category Skills, so that final synthesis remains a separate stage.
25. As a Global Synthesis Agent, I want to read channel outputs and category evidence, so that I can create final per-category skills.
26. As a Global Synthesis Agent, I want every major skill rule backed by Evidence References, so that final skills are not generic advice.
27. As a Pilot Review Agent, I want to audit two videos per channel before full rollout, so that weak prompts or schemas do not contaminate all 40 videos.
28. As a Pilot Review Agent, I want to identify weaknesses that affect the remaining 32 videos, so that the pilot improves the pipeline rather than merely repairing pilot files.
29. As a Pilot Review Agent, I want objective quality gates, so that approval to continue is not based only on vibes.
30. As a Pilot Review Agent, I want to output improvement plans for prompts, schemas, preprocessing, evidence references, and weighting, so that fixes are targeted.
31. As a Prompt Revision Agent, I want to revise prompts only from documented pilot failures, so that prompt changes do not become vague or harmful.
32. As a Prompt Revision Agent, I want to patch the base prompt only for global failures, so that channel-specific issues do not bloat every prompt.
33. As a Prompt Revision Agent, I want to patch channel modules for channel-specific failures, so that extraction missions remain sharp.
34. As the pipeline owner, I want the final output to be per-category only, so that the system produces reusable skills rather than channel clones.
35. As the pipeline owner, I want channel profiles to remain intermediate artifacts, so that they inform synthesis without becoming final products.
36. As the pipeline owner, I want the system to continue without transcript when needed, so that the dataset is resilient.
37. As the pipeline owner, I want confidence to reflect missing evidence types, so that weak observations do not look as reliable as strong ones.
38. As the pipeline owner, I want the folder structure to separate input videos, evidence, analysis, analysis JSON, pilot outputs, synthesis, prompts, and manifests, so that every stage has a clean boundary.
39. As the pipeline owner, I want the first version to use a pilot gate, so that the pipeline can become reliable before scale.
40. As the pipeline owner, I want future runs to preserve matrix versions and review outcomes, so that revisiting old decisions is possible.

## Implementation Decisions

- Use Timeline Segments as the atomic learning unit.
- Use Channel Profiles only as aggregate intermediate artifacts.
- Use a Weighting Matrix to decide which categories each channel should emphasize.
- Version Weighting Matrix revisions instead of overwriting them.
- Use `weight >= 8.0` as deep extraction, `6.5-7.9` as optional extraction, and `< 6.5` as generally skipped.
- Generate Evidence Bundles before any AI agent analyzes a Video Sample.
- Use FFmpeg plus Python helper scripts for v1 local preprocessing artifacts.
- Require Video Analysis Agents to use Evidence Bundles first and inspect raw local video only for targeted timestamp verification.
- Use Proactor as the required Transcript Provider for Instagram transcript extraction.
- Retry Proactor transcript extraction three times.
- Store successful transcript output as structured timestamped `transcript.json`, not as a human-readable transcript artifact.
- If transcript extraction fails after three attempts, mark Transcript Failure and continue without narration evidence.
- Lower Evidence Confidence for narration-dependent categories when transcript is missing.
- Store Evidence Bundles per video, not in global helper-type folders.
- Produce both Markdown and JSON analysis outputs per video.
- Use strict mandatory fields in v1 analysis JSON, plus a regulated flexible `extensions.notes` field for uncertainties, edge cases, extra observations, synthesis hints, schema gaps, and references that the Global Synthesis Agent may inspect as supporting context.
- Create Evidence References during video analysis, after important observations are identified.
- Let Video Analysis Agents select teachable timestamps, then use local helper/orchestration to assemble Evidence Reference folders.
- Keep helper preprocessing broad and deterministic; keep focused proof creation inside Video Analysis Agent work.
- Use one local Pipeline Orchestrator to own stage state, assemble Agent Packets, validate outputs, and advance stages only from explicit artifacts.
- Require 5 to 12 Evidence References per 3-minute video.
- Keep Video Analysis Agents evidence-only.
- Reserve channel-level conclusions for Channel Synthesis Agents.
- Reserve final Category Skills for the Global Synthesis Agent.
- Use a Pilot Run of two videos per channel before full rollout.
- Use one Video Analysis Agent per Video Sample during the 8-video Pilot Run.
- Select pilot videos randomly within each channel for v1 because each channel's videos are expected to be similar enough.
- Use the Pilot Review Agent primarily to improve the pipeline before analyzing the remaining 32 videos.
- Preserve failed pilot outputs as diagnostic artifacts and write revised outputs separately.
- Let the Pilot Review Agent automatically decide whether the pipeline can proceed or must be revised.
- Require all pilot hard gates to pass before full rollout; allow minor warnings only when they do not threaten full-rollout quality.
- Use the Prompt Revision Agent only after documented pilot findings.
- Generate final skills per category only, not per channel.
- Require Channel Synthesis before Global Synthesis.
- Produce v1 final Category Skills as Markdown skill specs first; convert to Codex or Claude skill directories later only after the evidence-backed rules mature.
- Keep v1 final Category Skills as prompt-style rules, with any helper commands or tool ideas limited to a clearly marked future automation hooks section.
- Handle overlapping final rules by assigning one primary Category Skill home and cross-referencing related categories.
- Convert conflicting channel evidence into conditional guidance rather than forcing one universal rule.
- Use existing prompt artifacts as the initial operational prompt layer.
- Use the project glossary terms consistently in prompts, schemas, reports, and synthesis outputs.

## Testing Decisions

- Test the highest observable pipeline seams rather than implementation details.
- Validate manifest records against the expected channel, video, source URL, local file, prompt module, and weighting matrix fields.
- Validate that each manifest local file path exists before preprocessing starts.
- Validate that each Evidence Bundle contains required artifacts or explicit failure metadata.
- Validate that Proactor transcript extraction records attempts, success, failure, provider, and source URL.
- Validate that Transcript Failure does not block visual and audio analysis.
- Validate that missing transcript cases do not produce narration claims.
- Validate scene change, audio peak, keyframe, and video index outputs at the artifact level.
- Validate Video Analysis File creation per video.
- Validate analysis JSON against the canonical schema.
- Validate that every observation has a category, timestamp, confidence score, summary, and evidence link.
- Validate that Video Analysis Agents do not include cross-video, cross-channel, or final skill claims.
- Validate that Evidence Reference folders include required frame files and metadata.
- Validate that each video has 5 to 12 Evidence References unless an explicit exception is recorded.
- Validate that high-weight categories receive coverage during pilot analysis.
- Validate that low-weight categories are not forced unless exceptional evidence exists.
- Validate that Pilot Review Agent outputs contain a decision, quality findings, and improvement plans.
- Validate that Prompt Revision Agent changes are traceable to pilot review findings.
- Validate that Global Synthesis Agent final rules cite Evidence References.
- Validate that final Category Skills do not become channel clone profiles.

## Out of Scope

- Training or fine-tuning a model.
- Building the final autonomous video factory.
- Automatically editing videos with FFmpeg or a timeline engine.
- Creating final production videos.
- Implementing a complete browser automation for Proactor in this PRD.
- Implementing local Whisper fallback.
- Replacing Proactor with another transcript provider.
- Publishing results to an external issue tracker.
- Building a UI dashboard.
- Deciding the final video-generation model or editing runtime.
- Creating channel-clone skills as final outputs.

## Further Notes

The current workspace already contains:

- A domain glossary in `CONTEXT.md`.
- ADRs for preprocessing, evidence/conclusion separation, Evidence References, weight thresholds, matrix versioning, and pilot review purpose.
- Prompt artifacts for base video analysis, category framework, channel modules, pilot review, prompt revision, channel synthesis, and global category synthesis.

The current channel prompt filenames use more concrete channel names than the original abstract labels:

- Channel 1: Upgrido / Retro Doc.
- Channel 2: 100X engineers.
- Channel 3: Aevy TV.
- Channel 4: VarunMaya.

The pilot should be treated as a reliability gate. The 8 pilot videos are diagnostic; the remaining 32 videos are the protected full rollout.

## Uncleared Ambiguities

The following items are still not fully resolved and should be clarified before implementation:

1. Whether manifests are the single source of truth or whether folder scanning can create missing manifest records.
2. The exact manifest schema for channels, videos, weighting matrices, preprocessing status, pilot status, and analysis status.
3. The exact current location of downloaded videos.
4. The exact mapping between each downloaded video and its Instagram source URL.
5. Whether every video has an accessible source URL for Proactor transcript extraction.
6. The exact Proactor website automation flow, including selectors, rate limits, download behavior, and failure detection.
7. Exact Proactor extraction mechanism for producing structured timestamped transcript segments.
8. The exact preprocessing helper boundaries and script names.
9. The exact Evidence Bundle schema and file naming convention.
10. The exact Evidence Reference folder naming convention.
11. The exact Evidence Reference helper interface for agent-selected timestamps.
12. The exact analysis JSON schema file and validation mechanism.
13. The exact Pipeline Orchestrator implementation and Agent Packet file schema.
14. The exact raw-video verification interface for timestamp-specific Zoom-In Verification.
15. Full-rollout analysis batch size after the pilot proves stable.
16. Exact random seed and reproducible pilot selection command.
17. Exact warning severity taxonomy for Pilot Review Agent findings.
18. Exact folder naming convention for failed and revised pilot output sets.
19. Exact channel synthesis output schema and validation mechanism.
20. Exact conversion criteria for turning Markdown Category Skill specs into Codex/Claude skill directories later.
21. Exact future automation hook format inside Markdown Category Skill specs.
22. Exact cross-reference format for overlapping final Category Skill rules.
23. Exact conditional-guidance format for conflicting channel evidence.
24. Whether a future mature pipeline can skip the Pilot Review Agent or should always keep it.
25. Where issue tracking should happen, since no issue tracker configuration was available in this workspace.
