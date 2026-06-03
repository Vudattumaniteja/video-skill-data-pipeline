# Scripts

## `import_instagram_reels.py`

Imports four Instagram JSON exports into the pipeline manifest layer and optionally downloads the referenced videos with `yt-dlp`.

Manifest-only run:

```powershell
py scripts\import_instagram_reels.py --source-dir "C:\path\to\exports"
```

Download all videos:

```powershell
py scripts\import_instagram_reels.py --source-dir "C:\path\to\exports" --download
```

Download only pilot videos:

```powershell
py scripts\import_instagram_reels.py --source-dir "C:\path\to\exports" --download --download-split pilot
```

Safe test download:

```powershell
py scripts\import_instagram_reels.py --source-dir "C:\path\to\exports" --download --limit 1
```

If Instagram requires login cookies:

```powershell
py scripts\import_instagram_reels.py --source-dir "C:\path\to\exports" --download --cookies-from-browser chrome
```

Outputs:

- `manifest/channels.json`
- `manifest/videos.json`
- `manifest/weighting_matrix_v1.json`
- `manifest/runs.json`
- `manifest/draft_import_report.md`
- `input_videos/{channel_id}/{video_id}.mp4` when `--download` is used
- `evidence/{channel_id}/{video_id}/source_metadata.json`
- `evidence/{channel_id}/{video_id}/caption.txt`

The runtime output folders are ignored by git.

## `preprocess_evidence.py`

Generates deterministic Evidence Bundle helper artifacts from downloaded videos.

Run all videos:

```powershell
py scripts\preprocess_evidence.py --overwrite
```

Run only pilot videos:

```powershell
py scripts\preprocess_evidence.py --split pilot --overwrite
```

Main outputs per video:

- `video_metadata.json`
- `transcript_meta.json` placeholder until Proactor transcript import runs
- `frame_grid_1fps.jpg`
- `scene_changes.json`
- `audio_peaks.json`
- `keyframes/keyframes.json`
- `keyframes/*.jpg`
- `video_index.json`

Run-level outputs:

- `manifest/preprocessing_report.json`
- `manifest/preprocessing_summary.md`
