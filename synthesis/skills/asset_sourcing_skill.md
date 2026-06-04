# Asset Sourcing Skill

## Purpose
Define workflows for gathering, organizing, and preparing raw visual assets (both design mockups and generative AI outputs) to ensure they are structured correctly for layout integration and animation pipelines.

## When To Use
- Initiating a new design sequence from a raw script.
- Writing prompts for generative image engines (Midjourney, DALL-E).
- Organizing reference designs and color schemes.
- Preparing graphic assets (PSD, PNG) for motion graphics and editing software (After Effects, Premier).

## Core Rules

### Rule 1: Convert Script Keywords into Visual Search Queries & Figma Moodboards

- Instruction: Do not download random images directly. Convert key script keywords into targeted search terms for Pinterest/Cosmos, gather candidate designs in a Figma workspace, and run the collection through Adobe Color to extract hex-coded visual palettes.
- Use when: Establishing the visual direction, color theme, and aesthetic layout of a new video.
- Avoid when: Using first-party screenshots or developer-provided terminal outputs.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_002/references/obs_003` (Pinterest visual search compile)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_002/references/obs_004` (Figma design moodboard)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_002/references/obs_005` (Adobe Color palette extraction)
- Confidence: 0.95

### Rule 2: AI-Generative Prompt Recipes with Subject Isolation

- Instruction: Specify subject, era, materials, colors, lens/lighting, and strict negative constraints (e.g. empty background, no people, solid backdrop) in prompts to ensure clean background removal and layered subject extraction.
- Use when: Generating custom illustrations, character assets, or metaphorical objects where stock photos do not exist.
- Avoid when: Real screenshots, actual branding assets, or factual corporate history are required.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_004/references/obs_003` (Detailed Midjourney prompt specifying textures, era, colors, and negatives)
- Confidence: 0.90

### Rule 3: Show Active CLI Terminal / Software UI Sourcing

- Instruction: When explaining developer or software workflows, capture and show the actual CLI command execution, terminal run, or software configuration screens instead of using placeholder B-roll.
- Use when: Narrating code development, database querying, tool setups, or command runs.
- Avoid when: Discussing general business strategies or historical narratives.
- Evidence References:
  - `evidence/channel_2_100x_engineers/channel_2_video_009/references/obs_004` (Direct terminal run and Graphify UI screen)
- Confidence: 0.88

### Rule 4: Multi-Layer Separation Asset Preparation

- Instruction: Prepare imported graphic assets (PSD/PNG) as separated layers linked to null objects in the timeline. Ensure the subject is separated from the background plate to support multi-depth 3D camera drift.
- Use when: Preparing layered designs for motion graphics and camera transitions in After Effects.
- Avoid when: Displaying flat, full-screen static screenshots or raw text tables.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_004/references/obs_004` (Separated subject layer)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_004/references/obs_007` (Background plate separation)
- Confidence: 0.92

## Decision Checklist
1. [ ] Have script keywords been mapped to Pinterest/Cosmos search queries instead of a general Google Image search?
2. [ ] Is the generated AI image prompt configured with negative constraints to facilitate background removal?
3. [ ] If explaining a software tool, does the timeline show a real CLI run or direct software UI?
4. [ ] Are the PSD/PNG files split into separate layers (subject, shadow, background) before importing into the compositor?

## Failure Modes
- **Undocumented Sourcing (Sourcing Gaps)**: Presenting final assets on the timeline without validating or showing the active sourcing tool/CLI interface (a recurring gap across multiple reviewed channels).
- **Flat Image Compositions**: Importing a single flat image where subject and backdrop cannot be moved independently, resulting in lifeless keyframe motion.
- **Unconstrained AI Generations**: Generating images with complex backgrounds that cannot be easily cropped, keyed, or isolated.

## Example Execution Pattern
1. Script says: "We run a Python script to index files."
2. *Bad sourcing*: Show a generic code graphic.
3. *Good sourcing*: Open a terminal window, type `python index.py`, record the visual output of the command running, and embed the recorded frame directly on the screen.

## Source Evidence Index
- `synthesis/channel_profiles/channel_1_upgrido_retro_doc.md`
- `synthesis/channel_profiles/channel_2_100x_engineers.md`
- `synthesis/channel_profiles/channel_3_aevy_tv.md`
- `synthesis/channel_profiles/channel_4_varunmaya.md`
