# Editing Layout Skill

## Purpose
Enforce spatial sequencing, composition consistency, and layout frameworks that optimize content for widescreen (16:9) and vertical mobile (9:16) viewing, ensuring clear spatial relationships and visual depth.

## When To Use
- Designing the spatial layout and composition of visual elements.
- Organizing split-screen reactions, interview feeds, and floating overlays.
- Keyframing motion graphics, 3D camera drift, and spatial transitions.
- Formatting chapter slates, cards, and grid arrangements.

## Core Rules

### Rule 1: Vertically Stacked Split-Screen (9:16 Optimization)

- Instruction: Convert landscape webcams, guest feeds, or product videos into vertical 9:16 layouts by stacking elements (e.g. host reaction below, guest video above). Utilize a clean center divider with a rounded pill interface to house subtitles.
- Use when: Editing podcast clips, remote interviews, or reaction clips for mobile-first platforms (TikTok, YouTube Shorts).
- Avoid when: Editing widescreen-only horizontal (16:9) cinematic videos.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_001/references/obs_006` (Satya Nadella / Varun stacked split-screen layout)
  - `evidence/channel_4_varunmaya/channel_4_video_002/references/obs_001` (Sam Altman / Varun webcam split-screen)
- Confidence: 0.95

### Rule 2: Rounded Floating Overlay Cards

- Instruction: Frame tweets, news article cards, and guest feeds inside clean, rounded-corner cards floating in the upper half of the frame, keeping the presenter's talking head visible in the lower half.
- Use when: overlaying social proof, quotes, and web article screenshots without losing eye contact between presenter and viewer.
- Avoid when: Displaying full-screen spec sheets, tables, or system diagrams.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_006/references/obs_003` (Tim Sweeney video card overlay)
  - `evidence/channel_3_aevy_tv/channel_3_video_007/references/obs_004` (Floating card checklists)
- Confidence: 0.92

### Rule 3: Geometric Grid & Shape Containment

- Instruction: Place product cutouts, icons, or visual assets inside circular zones with gradient fills or rounded backing boxes on top of grid backgrounds to create immediate alignment, structure, and contrast.
- Use when: Arranging clean grids of products, software features, or logo collections.
- Avoid when: Showing immersive, full-screen live-action footage or keynote video feeds.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_001/references/obs_004` (Cutouts placed inside circular zones on grids)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_003/references/obs_006` (Product assets enclosed in yellow backing shapes)
- Confidence: 0.90

### Rule 4: Chronological Open-Book Spreads & Spatial Sequencing

- Instruction: Sequence chronological timelines or regional comparisons using open-book layouts (e.g., geography/map on the left page, brand details/dates on the right page) or vertical/horizontal image strips.
- Use when: Narrating corporate histories, evolution of products, or multi-step processes.
- Avoid when: Displaying single standalone statistics or quick, transient tweets.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_004/references/obs_005` (McDonald's historical open-book layout)
  - `evidence/channel_3_aevy_tv/channel_3_video_008/references/obs_003` (Step-by-step spatial sequencing using horizontal image strips)
- Confidence: 0.90

### Rule 5: Branded Cinematic Reset Slates

- Instruction: Insert brief (1-2s), heavily-textured, high-contrast branded slates (e.g., custom textures, dark UI boards) to divide major sections and reset visual pacing.
- Use when: Transitioning between major narrative chapters or moving from an introductory hook to the technical body.
- Avoid when: Splitting rapid, consecutive talking points within the same sub-chapter.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_005/references/obs_003` (Textured branded chapter slates)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_009/references/obs_004` (Cinematic section resets)
- Confidence: 0.88

### Rule 6: 3D Spatial Parallax Layouts

- Instruction: Arrange text layers, isolated product cutouts, and background plates at varying depths on the Z-axis in a 3D workspace. Add soft camera drift, rotation, and keyframed focal changes to create spatial depth.
- Use when: Animating static images, diagrams, or title cards to prevent flat, static slides.
- Avoid when: Displaying real-time screen recordings of software tool interfaces.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_004/references/obs_006` (3D spatial depth assets)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_004/references/obs_008` (Z-axis keyframing camera path)
- Confidence: 0.93

## Decision Checklist
1. [ ] Is the composition format matched to the viewer's platform (e.g., vertically stacked feeds for mobile vertical)?
2. [ ] Are floating cards rounded and positioned to keep the talking head visible?
3. [ ] Are isolated assets placed on backing grids with shape containment (e.g., circles, pods) to prevent floating alignment errors?
4. [ ] Does the chronological progression use an open-book spread or spatial sequencing strip?
5. [ ] Is a textured chapter slate used to reset visual pacing between chapters?
6. [ ] Do static graphics utilize Z-axis depth and 3D camera drift to create parallax?

## Failure Modes
- **Sub-optimal Mobile Splits**: Exporting 16:9 widescreen footage inside a vertical 9:16 layout without modifying the spatial positioning, resulting in tiny, unreadable feeds.
- **Flat Layout Drabness**: Placing images directly on default solid backgrounds with zero 3D separation or camera drift.
- **Uncontained Asset Clutter**: Letting multiple cutouts and logos float freely on screen without grounding them on grids or shapes.

## Example Execution Pattern
1. *Input*: Widescreen webcam footage of host interviewing a guest. Target format: TikTok.
2. *Layout Execution*: Stack host webcam at the bottom. Stack guest webcam at the top. Insert a dark divider bar with a rounded black pill containing subtitles. Float relevant tweet cards in the upper margins next to the guest's webcam feed.

## Source Evidence Index
- `synthesis/channel_profiles/channel_1_upgrido_retro_doc.md`
- `synthesis/channel_profiles/channel_2_100x_engineers.md`
- `synthesis/channel_profiles/channel_3_aevy_tv.md`
- `synthesis/channel_profiles/channel_4_varunmaya.md`
