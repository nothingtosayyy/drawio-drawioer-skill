#!/usr/bin/env python3
"""One-shot environment preflight for the drawioer pipeline.

Run once per session before authoring. Reports which capabilities are
available (preview server, headless screenshot channel, network, optional
draw.io desktop) and the resulting working mode, so pipeline steps never
rediscover the environment one failure at a time.

Usage:
  python preflight.py
  python preflight.py --json
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

# Windows consoles default to a narrow codepage; force UTF-8 output.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

SKILL_DIR = Path(__file__).resolve().parents[1]
REQUIRED_SCRIPTS = (
    "validate_drawio.py",
    "validate_visual_quality.py",
    "serve_drawio_preview.py",
    "make_drawio_preview.py",
    "render_png.py",
)
VIEWER_URL = "https://viewer.diagrams.net/js/viewer-static.min.js"
EMBED_URL = "https://embed.diagrams.net/"


def find_browser() -> Path | None:
    for name in ("msedge", "chrome", "chromium"):
        found = shutil.which(name)
        if found:
            return Path(found)
    roots = (
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("ProgramFiles"),
        os.environ.get("LOCALAPPDATA"),
    )
    for root in roots:
        if not root:
            continue
        for rel in (
            "Microsoft/Edge/Application/msedge.exe",
            "Google/Chrome/Application/chrome.exe",
        ):
            candidate = Path(root) / rel
            if candidate.exists():
                return candidate
    return None


def find_drawio_desktop() -> Path | None:
    for name in ("draw.io", "drawio"):
        found = shutil.which(name)
        if found:
            return Path(found)
    roots = (
        os.environ.get("ProgramFiles(x86)"),
        os.environ.get("ProgramFiles"),
        os.environ.get("LOCALAPPDATA"),
    )
    for root in roots:
        if not root:
            continue
        for rel in ("draw.io/draw.io.exe", "Programs/draw.io/draw.io.exe"):
            candidate = Path(root) / rel
            if candidate.exists():
                return candidate
    return None


def probe(url: str, timeout: float) -> int | None:
    """Return the HTTP status if the host responded, else None."""
    request = urllib.request.Request(url, headers={"User-Agent": "drawio-preflight"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            response.read(512)
            return response.status
    except urllib.error.HTTPError as exc:
        return exc.code
    except OSError:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print a JSON report instead of text.")
    parser.add_argument("--timeout", type=float, default=6.0, help="Network probe timeout in seconds.")
    args = parser.parse_args()

    python_ok = sys.version_info >= (3, 7)
    missing = [name for name in REQUIRED_SCRIPTS if not (SKILL_DIR / "scripts" / name).exists()]
    browser = find_browser()
    viewer_status = probe(VIEWER_URL, args.timeout)
    embed_status = probe(EMBED_URL, args.timeout)
    desktop = find_drawio_desktop()

    if python_ok and not missing:
        mode = "FULL" if (browser and viewer_status and embed_status) else "DEGRADED"
    else:
        mode = "BROKEN"

    report = {
        "skill_dir": str(SKILL_DIR),
        "python": sys.version.split()[0],
        "python_ok": python_ok,
        "scripts_missing": missing,
        "headless_browser": str(browser) if browser else None,
        "viewer_status": viewer_status,
        "embed_status": embed_status,
        "drawio_desktop": str(desktop) if desktop else None,
        "mode": mode,
    }

    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        return 0 if mode != "BROKEN" else 1

    def line(tag: str, text: str) -> str:
        return f"  [{tag}] {text}"

    print("drawio pipeline preflight")
    print(line("PASS" if python_ok else "FAIL", f"python {sys.version.split()[0]} (>= 3.7 required)"))
    if missing:
        print(line("FAIL", f"scripts missing: {', '.join(missing)}"))
    else:
        print(line("PASS", f"scripts: {len(REQUIRED_SCRIPTS)}/{len(REQUIRED_SCRIPTS)} present"))
    if browser:
        print(line("PASS", f"headless browser: {browser}"))
    else:
        print(line("FAIL", "headless browser: no Edge/Chrome found (screenshots unavailable)"))
    if viewer_status and embed_status:
        print(line("PASS", f"network: viewer.diagrams.net {viewer_status}, embed.diagrams.net {embed_status}"))
    else:
        print(line("WARN", f"network: viewer={viewer_status or 'unreachable'}, embed={embed_status or 'unreachable'}"))
    if desktop:
        print(line("INFO", f"draw.io desktop: {desktop} (CLI --export also available)"))
    else:
        print(line("INFO", "draw.io desktop: not found (optional; only needed for CLI export)"))
    print(line("INFO", "in-app browser panel screenshots are not used by this pipeline (they require a visible panel)"))

    if mode == "FULL":
        print("mode: FULL  (preview server + headless screenshot available)")
        print("next: python scripts/validate_visual_quality.py <file>.drawio --quick")
        print("      python scripts/render_png.py <file>.drawio")
    elif mode == "DEGRADED":
        print("mode: DEGRADED  (static pre-flight only; hand the preview URL to the user)")
        print("next: python scripts/serve_drawio_preview.py <file>.drawio --no-open")
    else:
        print("mode: BROKEN  (fix the FAIL lines before authoring)")
    return 0 if mode != "BROKEN" else 1


if __name__ == "__main__":
    raise SystemExit(main())
