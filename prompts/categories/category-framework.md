# Category Framework

The pipeline generates final skills per category, not per channel.

## Categories

### 1. How To Select Assets

Extract rules about choosing the right visual material for a point in the script.

Look for:

- before/after asset replacement
- weak asset diagnosis
- foreground cutouts
- product screenshots
- 3D objects
- archival imagery
- mockups
- when the creator avoids generic stock visuals

### 2. Sourcing Great Assets

Extract rules about where strong assets come from and how they are prepared.

Look for:

- high-quality image sourcing
- isolated PNGs
- screen recordings
- custom 3D renders
- UI captures
- historical/archival images
- asset cleanup or masking

### 3. What Makes A Good Video

Extract high-level principles about retention, clarity, pacing, and information intent.

Look for:

- hooks
- payoff setup
- visual reset timing
- clarity improvements
- information hierarchy
- when the edit changes because the idea changes

Reduce confidence when transcript is unavailable.

### 4. Editing Framework / Layout

Extract rules about screen organization.

Look for:

- split screens
- cards
- grids
- side-by-side comparisons
- z-axis depth
- mockup placement
- camera movement
- layout transitions

### 5. Sound Design Sync

Extract rules about sound events tied to visual actions.

Look for:

- clicks on asset pops
- whooshes on transitions
- risers before reveals
- bass hits on cuts
- sound accents on text changes
- silence before important moments

### 6. Data & Text Density

Extract rules about using visible words, numbers, labels, captions, and dense information.

Look for:

- text overlays
- callouts
- labels
- charts
- stats
- comparison tables
- high-density but readable layouts

## Weight Thresholds

- `>= 8.0`: primary category. Extract deeply.
- `6.5-7.9`: optional category. Extract only when strong evidence appears.
- `< 6.5`: low priority. Ignore unless exceptional.

## Weighting Matrix v1

| Category | Channel 1 Upgrido / Retro Doc | Channel 2 100X engineers | Channel 3 Aevy TV | Channel 4 VarunMaya |
|---|---:|---:|---:|---:|
| How to Select Assets | 9.0 | 7.0 | 8.0 | 8.5 |
| Sourcing Great Assets | 9.5 | 8.0 | 7.5 | 8.5 |
| What Makes a Good Video | 6.5 | 9.5 | 8.5 | 9.0 |
| Editing Framework / Layout | 7.5 | 9.0 | 8.0 | 9.5 |
| Sound Design Sync | 7.0 | 9.5 | 8.0 | 9.0 |
| Data & Text Density | 6.0 | 9.5 | 8.5 | 9.0 |
