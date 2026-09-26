#!/usr/bin/env python3
"""Build the mip videos site into _site/.

For each videos/<slug>.mp4, reads the optional sidecar videos/<slug>.yaml,
extracts a thumbnail with ffmpeg, and writes a videos.json manifest that the
static front end in site/ renders.

Requires ffmpeg, ffprobe, and PyYAML.
"""

import json
import math
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
VIDEOS_DIR = ROOT / "videos"
SITE_SRC = ROOT / "site"
OUT = ROOT / "_site"

ALLOWED_KEYS = {"title", "description", "thumbnail_time", "date", "order"}
DEFAULT_THUMBNAIL_TIME = 1.0
THUMBNAIL_WIDTH = 640


def fail(msg):
    print(f"error: {msg}", file=sys.stderr)
    sys.exit(1)


def title_from_slug(slug):
    words = slug.replace("_", "-").split("-")
    text = " ".join(w for w in words if w)
    return text[:1].upper() + text[1:]


def probe_duration(path):
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(path)],
        capture_output=True, text=True, check=True,
    )
    return float(result.stdout.strip())


def extract_thumbnail(video, time, dest):
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-ss", f"{time:.3f}", "-i", str(video),
         "-frames:v", "1", "-vf", f"scale={THUMBNAIL_WIDTH}:-2", "-q:v", "3",
         str(dest)],
        check=True,
    )
    if not dest.exists() or dest.stat().st_size == 0:
        fail(f"ffmpeg produced no thumbnail for {video.name} at {time}s")


def git_added_date(path):
    """Date the file was first committed, or None if untracked / no git."""
    try:
        result = subprocess.run(
            ["git", "log", "--diff-filter=A", "--follow", "--format=%aI", "--", str(path)],
            capture_output=True, text=True, cwd=ROOT,
        )
    except FileNotFoundError:
        return None
    lines = result.stdout.strip().splitlines()
    return lines[-1][:10] if result.returncode == 0 and lines else None


def load_meta(sidecar):
    if not sidecar.exists():
        return {}
    with open(sidecar, encoding="utf-8") as f:
        meta = yaml.safe_load(f)
    if meta is None:
        return {}
    if not isinstance(meta, dict):
        fail(f"{sidecar.name}: expected a mapping of keys to values")
    unknown = set(meta) - ALLOWED_KEYS
    if unknown:
        fail(f"{sidecar.name}: unknown keys {sorted(unknown)}; allowed: {sorted(ALLOWED_KEYS)}")
    return meta


def build_entry(video, thumbs_dir):
    slug = video.stem
    meta = load_meta(video.with_suffix(".yaml"))
    duration = probe_duration(video)
    if not duration > 0:
        fail(f"{video.name}: could not determine duration")

    thumb_time = meta.get("thumbnail_time", DEFAULT_THUMBNAIL_TIME)
    if not isinstance(thumb_time, (int, float)) or isinstance(thumb_time, bool) or thumb_time < 0:
        fail(f"{video.name}: thumbnail_time must be a non-negative number of seconds")
    if thumb_time >= duration:
        fail(f"{video.name}: thumbnail_time {thumb_time}s is past the end of the video ({duration:.1f}s)")
    extract_thumbnail(video, float(thumb_time), thumbs_dir / f"{slug}.jpg")

    date = meta.get("date")
    if date is not None:
        date = str(date)
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            fail(f"{video.name}: date must be YYYY-MM-DD, got {date!r}")
    else:
        date = git_added_date(video) or datetime.fromtimestamp(
            video.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")

    order = meta.get("order")
    if order is not None and (not isinstance(order, (int, float)) or isinstance(order, bool)):
        fail(f"{video.name}: order must be a number")

    return {
        "slug": slug,
        "title": str(meta.get("title") or title_from_slug(slug)),
        "description": str(meta.get("description") or "").strip(),
        "date": date,
        "duration": round(duration, 2),
        "order": order,
        "video": f"videos/{video.name}",
        "thumbnail": f"thumbs/{slug}.jpg",
    }


def main():
    if not VIDEOS_DIR.is_dir():
        fail(f"{VIDEOS_DIR} does not exist")
    for tool in ("ffmpeg", "ffprobe"):
        if shutil.which(tool) is None:
            fail(f"{tool} not found on PATH")

    videos = sorted(VIDEOS_DIR.glob("*.mp4"))
    for sidecar in VIDEOS_DIR.glob("*.yaml"):
        if not sidecar.with_suffix(".mp4").exists():
            fail(f"{sidecar.name} has no matching .mp4")
    for other in VIDEOS_DIR.iterdir():
        if other.suffix not in (".mp4", ".yaml") and not other.name.startswith("."):
            fail(f"unexpected file in videos/: {other.name} (only .mp4 and .yaml are supported)")

    if OUT.exists():
        shutil.rmtree(OUT)
    shutil.copytree(SITE_SRC, OUT)
    thumbs_dir = OUT / "thumbs"
    thumbs_dir.mkdir()
    (OUT / "videos").mkdir()

    entries = []
    for video in videos:
        entries.append(build_entry(video, thumbs_dir))
        shutil.copy2(video, OUT / "videos" / video.name)
        print(f"  {video.name}")

    # Explicit order first (ascending), then newest first.
    entries.sort(key=lambda e: e["title"])
    entries.sort(key=lambda e: e["date"], reverse=True)
    entries.sort(key=lambda e: e["order"] if e["order"] is not None else math.inf)

    with open(OUT / "videos.json", "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)
    print(f"Built {len(entries)} video(s) into {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
