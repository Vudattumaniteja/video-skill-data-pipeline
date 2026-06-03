# Prompts

This folder contains the prompt system for the video skill data pipeline.

## Structure

- `base-video-analysis-prompt.md` - shared instructions for every video analysis agent.
- `categories/category-framework.md` - category definitions, weight thresholds, and expected evidence.
- `channels/` - channel-specific prompt modules layered on top of the base prompt.
- `pilot/` - pilot review and prompt revision prompts.
- `synthesis/` - forms for channel synthesis and final per-category skill synthesis.
- `terms/video-analysis-prompt-terms.md` - canonical prompt terms from `CONTEXT.md`.

## Prompt Assembly

For a video analysis run, assemble prompts in this order:

1. Base video analysis prompt.
2. Category framework.
3. Matching channel-specific module.
4. Video manifest record.
5. Evidence bundle paths.

Video analysis agents collect evidence only. They do not make cross-video, cross-channel, or final skill conclusions.

