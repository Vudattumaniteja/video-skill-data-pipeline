# Data & Text Density Skill

## Purpose
Optimize the visual presentation of complex information, data points, and technical specifications, balancing high informational value with readable layout organization to prevent viewer cognitive overload.

## When To Use
- Presenting articles, studies, screenshots, and text highlights.
- Formatting lists of companies, platforms, partners, or software features.
- Displaying technical benchmarks, specification sheets, and hardware comparisons.
- Designing statistical highlights, pricing charts, or system architectures.

## Core Rules

### Rule 1: Highlighted Document & Article Receipts

- Instruction: Display screenshots of actual research papers, articles, or databases on screen. Overlay bright yellow or high-contrast highlights on key paragraphs or numbers to focus the viewer's attention on the precise proof.
- Use when: Establishing credibility, quoting sources, or referencing official data.
- Avoid when: Illustrating general concepts or highly abstract narratives.
- Evidence References:
  - `evidence/channel_3_aevy_tv/channel_3_video_010/references/obs_002` (Highlighted budget receipts)
  - `evidence/channel_3_aevy_tv/channel_3_video_008/references/obs_008` (Highlighted reports)
  - `evidence/channel_3_aevy_tv/channel_3_video_001/references/obs_004` (Highlighted article screenshots)
- Confidence: 0.95

### Rule 2: Centered Large-Scale Metrics (Payoffs)

- Instruction: Isolate a single massive statistic or percentage (e.g. "71x", "40L/1Cr", "26%") in clean, oversized text centered on a dark screen to establish the primary takeaway.
- Use when: Introducing a major financial cost, industry growth metric, or performance multiplier.
- Avoid when: Displaying multiple comparative values or detailed lists.
- Evidence References:
  - `evidence/channel_3_aevy_tv/channel_3_video_001/references/obs_005` (Goldman Sachs 26% card)
  - `evidence/channel_2_100x_engineers/channel_2_video_006/references/obs_003` (Electrical capacity numbers centered)
- Confidence: 0.92

### Rule 3: Logo and Card Clustering for Lists

- Instruction: Avoid presenting long spoken lists (such as partners, platforms, or tools) as boring text bullet points. Cluster them into visual grids of logos, horizontal carousels, or icon groups.
- Use when: Summarizing integrations, compatible platforms, client portfolios, or toolkit checklists.
- Avoid when: Comparing complex numeric data that requires structured rows and columns.
- Evidence References:
  - `evidence/channel_2_100x_engineers/channel_2_video_007/references/obs_002` (Diagnostic UI check grid)
  - `evidence/channel_3_aevy_tv/channel_3_video_007/references/obs_004` (Floating card checklist)
- Confidence: 0.90

### Rule 4: Tabular Datasheet Comparisons & Spec Sheets

- Instruction: Present comparative specifications, benchmarks, or budgets in structured tables (e.g., using colored row backgrounds to separate data) or labeled block diagrams.
- Use when: Comparing hardware components, pricing tiers, or complex system workflows.
- Avoid when: Presenting simple, single-metric highlights.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_005/references/obs_005` (RTX 5070 specification comparison table)
  - `evidence/channel_3_aevy_tv/channel_3_video_010/references/obs_008` (Budget forecast chart)
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_005/references/obs_007` (Color row-background table)
- Confidence: 0.93

### Rule 5: Visual-Only Parallel Data (Self-Paced Text)

- Instruction: Insert secondary specs, prices, or details directly into the visual layout (e.g., stylized yellow ticket stubs with torn edges, card tags) without reading them aloud. This permits self-paced viewer reading without cluttering the audio track.
- Use when: Displaying product price tags, micro-metadata, or accessory specs.
- Avoid when: Presenting the primary thesis or critical script claims.
- Evidence References:
  - `evidence/channel_1_upgrido_retro_doc/channel_1_video_003/references/obs_003` (Price tag ticket texture)
  - `evidence/channel_4_varunmaya/channel_4_video_004/references/obs_004` (Radar visual UI spec)
- Confidence: 0.88

### Rule 6: Stylized Large Italic Text Punches

- Instruction: Emphasize core spoken statements or shocking claims by overlaying giant, bold, white, italicized uppercase text (e.g., "SaaS is DEAD", "SEEING") across the center of the screen.
- Use when: punctuating conversational pivots, narrative climaxes, or bold predictions.
- Avoid when: Explaining details, listing specs, or showing proof documents.
- Evidence References:
  - `evidence/channel_4_varunmaya/channel_4_video_001/references/obs_008` ("SaaS is DEAD" text overlay)
- Confidence: 0.90

## Decision Checklist
1. [ ] Are screenshots of source articles or reports highlighted to direct the viewer's eye?
2. [ ] Is the primary statistic isolated as a single massive metric card?
3. [ ] Are long lists converted into visual logo grids or icon cards instead of bulleted lists?
4. [ ] Does the comparative hardware data use a structured table or labeled diagram?
5. [ ] Are accessory details embedded as visual-only props (e.g. ticket stubs) to keep the narration clean?
6. [ ] Is a bold center-screen text punch used for the climax of the script's argument?

## Failure Modes
- **Text Slop / Paragraph Dumps**: Dumping blocks of unhighlighted text or full article screenshots, forcing the viewer to scan the screen.
- **Narrative Overload**: Reading every single number, spec, and price aloud instead of offloading minor details to visual cards.
- **Low-Contrast Grids**: Organizing text overlays without containers or background contrast, making numbers bleed into B-roll.

## Example Execution Pattern
1. *Script*: "The RTX 5070 runs on the Blackwell architecture and costs $599, yielding a 1.4x gain in ray tracing."
2. *Visual Execution*: Show a huge centered "1.4x" on screen. Transition to a clean 2-column table comparing RTX 5070 vs RTX 4070 specs. Place a small, stylized yellow ticket stub in the corner showing "$599" without saying it aloud.

## Source Evidence Index
- `synthesis/channel_profiles/channel_1_upgrido_retro_doc.md`
- `synthesis/channel_profiles/channel_2_100x_engineers.md`
- `synthesis/channel_profiles/channel_3_aevy_tv.md`
- `synthesis/channel_profiles/channel_4_varunmaya.md`
