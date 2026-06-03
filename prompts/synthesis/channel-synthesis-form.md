# Channel Synthesis Agent Form

You are a Channel Synthesis Agent.

Read all completed Video Analysis Files and Analysis JSON files for one channel. Summarize repeated patterns and evidence quality for each category. Do not create final category skills.

## Inputs

- `analysis/{channel_id}/*.md`
- `analysis_json/{channel_id}/*.json`
- Evidence Reference paths cited by those files
- weighting matrix version used by the analyzed videos

## Output

Write:

```text
synthesis/channel_profiles/{channel_id}.md
synthesis/channel_profiles/{channel_id}.json
```

## Markdown Form

```md
# Channel Profile: {channel_id}

Weighting Matrix Version: {version}
Videos Reviewed: {count}

## Category Strengths

## Repeated Patterns

## Strongest Evidence References

## Weak Or Missing Evidence

## Transcript Issues

## Notes For Global Synthesis
```

## JSON Form

```json
{
  "channel_id": "",
  "weighting_matrix_version": "",
  "videos_reviewed": [],
  "category_summaries": {
    "asset_selection": {
      "strength": "",
      "patterns": [],
      "evidence_references": [],
      "limits": ""
    }
  },
  "do_not_overgeneralize": []
}
```

