# Asset Selection Skill

## Purpose
Guide editors and prompt engineers in choosing topic-congruent, high-credibility, and brand-aligned visual assets that replace generic stock B-roll, establishing visual proof and immediate topic context.

## When To Use
- Selecting visual B-roll, graphics, and stills for video compositions.
- Framing historical, cultural, design, or technical concepts.
- Embedding social proof (such as tweets or articles) or first-party developer assets.

## Core Rules

### Rule 1: Concrete Visual Anchors over Generic Stock B-Roll

- Instruction: Avoid using generic B-roll (e.g., standard stock office handshakes or typing). Select specific, high-credibility visual anchors that represent concepts (e.g., Studio Ghibli stills for illustrative/artistic mood, classical statues for historical context, and custom vector diagrams for technical anatomy).
- Use when: Visualizing abstract script references, emotional states, historical events, or artistic categories.
- Avoid when: Explaining direct, active software tool actions that require real-time screen captures.
- Evidence References: 
  - `evidence/channel_3_aevy_tv/channel_3_video_001/references/obs_002` (Studio Ghibli visual anchor)
  - `evidence/channel_3_aevy_tv/channel_3_video_008/references/obs_002` (Historical painted portrait)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_005/references/obs_004` (Topic-specific movie genre stills)
- Confidence: 0.90

### Rule 2: Embedded First-Party / Third-Party Evidence (Social & Authority Proof)

- Instruction: Use actual screenshots or screencasts of product interfaces, company homepages, tweet embeds, and keynote presentation footage to back up claims rather than relying on abstract illustrations.
- Use when: Introducing named platforms, quoting industry figures, reference-checking news articles, or highlighting technical updates.
- Avoid when: The script covers generic historical principles or highly conceptual/fictional narratives.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_001/references/obs_006` (Tweet overlays as proof surfaces)
  - `evidence/channel_4_varunmaya/channel_4_video_006/references/obs_003` (Tim Sweeney developer keynote footage)
  - `evidence/channel_3_aevy_tv/channel_3_video_007/references/obs_005` (Product interface screenshots)
  - `evidence/channel_3_aevy_tv/channel_3_video_009/references/obs_002` (Company homepage cards)
- Confidence: 0.95

### Rule 3: Brand-Congruent Palettes and Visual Themes

- Instruction: Align visual backdrops, text fields, and asset colors directly with the brand identity of the subject being discussed (e.g., Apple's black-and-white theme instead of generic blue fills).
- Use when: Discussing brand strategies, product releases, or corporate case studies.
- Avoid when: Sourcing generic historical references or non-branded industry-wide topics.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_001/references/obs_002` (Apple's black-and-white theme)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_001/references/obs_003` (High-contrast corporate brand colors)
- Confidence: 0.88

### Rule 4: Cultural & Historical Reference Stills

- Instruction: Ground historical style discussions with authentic artifacts, such as classical statues, vintage newspaper front pages, or large letterform crops.
- Use when: Discussing typographic heritage, cultural eras, or historical case studies.
- Avoid when: Visualizing futuristic tech, modern SaaS interfaces, or contemporary tutorials.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_007/references/obs_002` (Classical art statue and vintage front pages)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_007/references/obs_005` (Serif letterform crops)
- Confidence: 0.90

## Decision Checklist
1. [ ] Is the candidate asset generic B-roll? (If yes, replace it with a concrete visual anchor or direct proof).
2. [ ] Does the asset have immediate credibility (e.g., first-party screenshot or tweet vs. stock vector)?
3. [ ] Does the color palette of the selected asset match the brand guidelines of the target company?
4. [ ] If historical or cultural concepts are mentioned, are they anchored by authentic, high-quality images (statues, newspapers, paintings)?

## Failure Modes
- **Generic B-Roll Overuse**: Slipping into standard stock footage of offices/keyboards, making the video feel like "slop."
- **Low-Contrast Palette Choices**: Selecting blue or gray default backgrounds that dilute brand identity.
- **Vague Visuals for Specific Claims**: Using abstract graphics to represent specific tools or tweets instead of showing the actual interface.

## Example Execution Pattern
1. Script says: "Apple launched the iPhone in 2007."
2. *Bad selection*: Generic hand holding a random smartphone.
3. *Good selection*: A crisp crop of the original 2007 Steve Jobs keynote video feed, or the original Apple 2007 homepage announcement archive screenshot, framed in a clean card.

## Source Evidence Index
- `synthesis/channel_profiles/channel_1_upgrido_retro_doc.md`
- `synthesis/channel_profiles/channel_2_100x_engineers.md`
- `synthesis/channel_profiles/channel_3_aevy_tv.md`
- `synthesis/channel_profiles/channel_4_varunmaya.md`
