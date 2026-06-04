# Sound Design & Sync Skill

## Purpose
Align audio peaks, sound-effect layers, and dialogue markers with visual cuts, layout transitions, and asset reveals to maintain conversational momentum and increase tactile impact.

## When To Use
- Aligning visual transition cuts to background music beats or sound effects.
- Synchronizing the appearance of text cards, floating overlays, and graphic highlights.
- Timing rapid-fire lists or repetitive questions.
- Sequencing split-screen changes or talking-head resets in relation to spoken dialogue.

## Core Rules

### Rule 1: Sync Audio Peak Clusters with Visual Cuts and Chapter Reveals

- Instruction: Place high-amplitude audio peaks (hits, wooshes, swooshes, or sub-drops) exactly on visual scene changes, layout transitions, and new chapter headings to add visceral weight.
- Use when: Transitioning between major narrative chapters, changing scenes, or moving from talking heads to graphic layouts.
- Avoid when: Running quiet, reflective dialogue or during steady screen-recordings.
- Evidence References:
  - `evidence/channel_3_aevy_tv/channel_3_video_010/references/obs_007` (Audio peak transition accent)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_002/references/obs_008` (Peak on visual cut)
  - `evidence/channel_2_100x_engineers/channel_2_video_010/references/obs_003` (Peak aligned with layout reset)
- Confidence: 0.92

### Rule 2: Graphic Entrance Syncing (Overlay Beats)

- Instruction: Make floating card overlays, social tweets, and text highlights enter the frame exactly in sync with localized audio peaks, sound effects (e.g. paper tear, swoosh, click), or vocal emphasis.
- Use when: Introducing floating cards, tweets, pricing sheets, or highlighting key text lines.
- Avoid when: Graphic assets are already established on screen or are meant for subtle background detail.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_006/references/obs_003` (Tim Sweeney overlay sync)
  - `evidence/channel_4_varunmaya/channel_4_video_001/references/obs_006` (DiscussingFilm tweet entry sync)
- Confidence: 0.90

### Rule 3: Rhythmic List Pacing

- Instruction: Pace rapid sequences of questions, logo grids, or list items in sync with a steady progression of local audio beats or vocal spikes to create a driving rhythm.
- Use when: Presenting lists of tools, partners, features, or quick-fire questions.
- Avoid when: Delivering detailed, slow-paced explanations or presenting high-density datasheets.
- Evidence References:
  - `evidence/channel_3_aevy_tv/channel_3_video_002/references/obs_009` (Rhythmic list pacing sync)
  - `evidence/channel_3_aevy_tv/channel_3_video_009/references/obs_006` (Rapid-fire sequence)
- Confidence: 0.88

### Rule 4: Dialogue-Driven Layout Transitions

- Instruction: Execute layout resets, webcam splits, or presenter transitions immediately following vocal emphasis spikes, sentence pauses, or conversational pivots.
- Use when: Cutting between presenter feeds, moving to full-screen tool captures, or transitioning themes.
- Avoid when: The speaker is in the middle of a continuous, rapid-fire sentence.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_004/references/obs_006` (Dialogue cut transition)
  - `evidence/channel_2_100x_engineers/channel_2_video_007/references/obs_005` (Task analysis screen reset)
- Confidence: 0.90

## Decision Checklist
1. [ ] Do major visual cuts or chapter reveals land exactly on a beat or audio peak (swoosh, sub-drop)?
2. [ ] Do floating card entries sync with localized sound effects?
3. [ ] Are rapid list items or logos appearing sequentially in sync with a rhythmic beat track?
4. [ ] Does the transition to a presenter reset occur directly after a conversational pause or vocal spike?

## Failure Modes
- **Subjective / Unaligned Sync**: Placing visual edits 2-3 frames off the audio peak, creating a jarring, unpolished viewer experience.
- **Timeline-End Gaps**: Experiencing gaps in sync data or audio peaks towards the end of long timelines (a common production issue, where late-stage visual assets lose sound design integration).
- **Over-sync Fatigue**: Syncing every single minor text element to a loud sound effect, which causes cognitive overload.

## Example Execution Pattern
1. *Timeline Layout*: Music track has a heavy beat drop at 00:15.5.
2. *Sync Design*: Cut from the presenter's talking head to a full-screen layout containing a custom system diagram precisely at 00:15.5. Play a low-frequency sub-drop sound effect that peaks at the same millisecond.

## Source Evidence Index
- `synthesis/channel_profiles/channel_1_upgrido_retro_doc.md`
- `synthesis/channel_profiles/channel_2_100x_engineers.md`
- `synthesis/channel_profiles/channel_3_aevy_tv.md`
- `synthesis/channel_profiles/channel_4_varunmaya.md`
