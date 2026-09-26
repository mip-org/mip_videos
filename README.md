# mip videos

A small static site that hosts screencasts and other videos about [mip](https://mip.sh). It is deployed to GitHub Pages at https://mip-org.github.io/mip_videos/ on every push to `main`.

## Adding a video

1. Copy the `.mp4` file into `videos/`. The filename (without extension) becomes the video's URL slug, so use lowercase words separated by hyphens, for example `videos/installing-mip.mp4`.
2. Optionally add a sidecar file with the same name and a `.yaml` extension, for example `videos/installing-mip.yaml`:

   ```yaml
   title: Installing mip
   description: How to install mip
   thumbnail_time: 20
   date: 2026-09-26
   ```

3. Commit and push. CI builds the site and deploys it.

All sidecar keys are optional:

| Key | Default | Meaning |
| --- | --- | --- |
| `title` | Derived from the filename (`installing-mip` becomes "Installing mip") | Title shown on the card and in the player |
| `description` | Empty | Plain text; line breaks are preserved in the player |
| `thumbnail_time` | `1` | Time in seconds of the frame used as the thumbnail |
| `date` | Date the `.mp4` was first committed | `YYYY-MM-DD`; videos are listed newest first |
| `order` | None | Number; videos with an `order` are listed first, in ascending order |

The build fails on unknown keys, on a `thumbnail_time` past the end of the video, and on files in `videos/` other than `.mp4` and `.yaml`.

Videos are stored in plain git. GitHub rejects files over 100 MB, and a Pages site is limited to about 1 GB in total, so keep screencasts compressed (720p H.264 is plenty).

## Building locally

Requires `ffmpeg` and Python with PyYAML.

```bash
python3 build.py
python3 -m http.server -d _site 8000
```

Then open http://localhost:8000. To preview a thumbnail frame before committing, run `ffmpeg -ss 20 -i videos/installing-mip.mp4 -frames:v 1 /tmp/thumb.jpg`, or just rebuild and reload.

## Layout

- `videos/`: the `.mp4` files and their optional `.yaml` sidecars
- `site/`: the static front end (`index.html`, `app.js`, `style.css`)
- `build.py`: copies `site/` to `_site/`, extracts thumbnails, and writes `_site/videos.json`
- `.github/workflows/deploy.yml`: builds and deploys to GitHub Pages
