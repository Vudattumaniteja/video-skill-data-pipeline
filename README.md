# Video Skill Data Pipeline

Architecture, PRD, ADRs, and prompt contracts for a staged pipeline that learns reusable AI video-production skills from short Instagram/Reels-style video samples.

The pipeline separates:

1. dataset manifests and provenance,
2. deterministic preprocessing into evidence bundles,
3. per-video evidence collection,
4. pilot review and prompt revision,
5. channel synthesis,
6. global per-category skill synthesis.

Current source-of-truth documents:

- `CONTEXT.md`
- `docs/architecture/video-skill-data-pipeline-architecture.md`
- `docs/prd/video-skill-data-pipeline-prd.md`
- `docs/adr/`
- `prompts/`

Runtime data, downloaded videos, generated evidence, analysis outputs, and synthesis outputs are intentionally ignored until the implementation stage defines safe artifact handling.
