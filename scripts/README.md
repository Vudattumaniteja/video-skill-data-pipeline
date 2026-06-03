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

The runtime output folders are ignored by git.
