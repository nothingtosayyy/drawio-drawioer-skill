#!/usr/bin/env python3
"""Render a .drawio file to a canvas-only PNG with headless system Edge/Chrome.

Builds a self-contained viewer page (viewer.diagrams.net), serves it on
127.0.0.1, takes a headless screenshot, and writes a PNG next to the input
(or to --output). No in-app browser panel or MCP tooling is required.

By default the viewport auto-fits the diagram bounds (diagram fills the
image); pass --width/--height to force a fixed viewport.

Usage:
  python render_png.py diagram.drawio
  python render_png.py diagram.drawio -o shots/d1.png --width 1920 --height 1200
  python render_png.py diagram.drawio --scale 1.5
  python render_png.py diagram.drawio --browser "C:/Program Files/Google/Chrome/Application/chrome.exe"
"""

from __future__ import annotations

import argparse
import functools
import html
import json
import os
import shutil
import struct
import subprocess
import sys
import tempfile
import threading
import xml.etree.ElementTree as ET
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# Windows consoles default to a narrow codepage; force UTF-8 output.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

MARGIN = 64
MIN_SIDE = 480
MAX_SIDE = 3000


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def build_html(xml: str, title: str) -> str:
    cfg = {"highlight": "#0000ff", "nav": False, "resize": True, "toolbar": None, "xml": xml}
    attr = json.dumps(cfg).replace("&", "&amp;").replace("'", "&#39;")
    escaped_title = html.escape(title)
    return f"""<!doctype html>
<html>
<head>
<meta charset="utf-8" />
<title>{escaped_title}</title>
<style>
  html, body {{ margin: 0; padding: 0; background: #ffffff; }}
  body {{ display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
  .mxgraph {{ width: 100vw; }}
</style>
</head>
<body>
<div class="mxgraph" data-mxgraph='{attr}'></div>
<script src="https://viewer.diagrams.net/js/viewer-static.min.js"></script>
</body>
</html>
"""


def content_bounds(drawio_path: Path) -> tuple[float, float, float, float] | None:
    """Approximate diagram bounds in user units, resolving nested offsets."""
    try:
        root = ET.parse(drawio_path).getroot()
    except ET.ParseError:
        return None

    cells: dict[str, tuple[float, float, float, float, str]] = {}
    for cell in root.iter("mxCell"):
        cid = cell.get("id")
        if not cid:
            continue
        geometry = None
        for child in cell:
            if child.tag == "mxGeometry" and child.get("as") == "geometry":
                geometry = child
                break
        if geometry is None:
            continue
        try:
            x = float(geometry.get("x") or 0)
            y = float(geometry.get("y") or 0)
            w = float(geometry.get("width") or 0)
            h = float(geometry.get("height") or 0)
        except ValueError:
            continue
        cells[cid] = (x, y, w, h, cell.get("parent") or "1")

    def absolute(cid: str) -> tuple[float, float]:
        x = y = 0.0
        guard = 0
        while cid in cells and guard < 50:
            cx, cy, _, _, parent = cells[cid]
            x += cx
            y += cy
            if parent in ("0", "1", ""):
                break
            cid = parent
            guard += 1
        return x, y

    min_x = min_y = float("inf")
    max_x = max_y = float("-inf")
    for cid, (_, _, w, h, _) in cells.items():
        if w <= 0 or h <= 0:
            continue
        x, y = absolute(cid)
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + w)
        max_y = max(max_y, y + h)
    if min_x == float("inf"):
        return None
    return min_x, min_y, max_x, max_y


def find_browser(explicit: str | None) -> Path | None:
    if explicit:
        candidate = Path(explicit)
        return candidate if candidate.exists() else None
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


def png_dimensions(path: Path) -> tuple[int, int] | None:
    try:
        data = path.read_bytes()[:24]
        if data[:8] != b"\x89PNG\r\n\x1a\n":
            return None
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    except OSError:
        return None


def choose_viewport(drawio_path: Path, width: int | None, height: int | None) -> tuple[int, int, str]:
    if width and height:
        return width, height, "explicit"
    bounds = content_bounds(drawio_path)
    if bounds:
        min_x, min_y, max_x, max_y = bounds
        w = max(MIN_SIDE, min(MAX_SIDE, round(max_x - min_x) + MARGIN))
        h = max(MIN_SIDE, min(MAX_SIDE, round(max_y - min_y) + MARGIN))
        return w, h, "auto"
    return 1920, 1200, "fallback"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("drawio", type=Path, help="Path to the .drawio XML file.")
    parser.add_argument("-o", "--output", type=Path, default=None, help="Output PNG path. Defaults to <input>.png.")
    parser.add_argument("--width", type=int, default=None, help="Force viewport width (default: auto-fit).")
    parser.add_argument("--height", type=int, default=None, help="Force viewport height (default: auto-fit).")
    parser.add_argument("--scale", type=float, default=1.0, help="Device scale factor for the output. Default 1.0.")
    parser.add_argument("--budget", type=int, default=20000, help="Headless render budget in milliseconds. Default 20000.")
    parser.add_argument("--browser", default=None, help="Explicit browser executable path.")
    args = parser.parse_args()

    drawio_path = args.drawio.resolve()
    if not drawio_path.exists():
        print(f"[FAIL] input does not exist: {drawio_path}", file=sys.stderr)
        return 2

    browser = find_browser(args.browser)
    if browser is None:
        print(
            "[FAIL] no Edge/Chrome found. Pass --browser <path>, or use "
            "scripts/serve_drawio_preview.py and ask the user to review the preview.",
            file=sys.stderr,
        )
        return 2

    png_path = (args.output or drawio_path.with_suffix(".png")).resolve()
    png_path.parent.mkdir(parents=True, exist_ok=True)
    xml = drawio_path.read_text(encoding="utf-8")
    width, height, size_source = choose_viewport(drawio_path, args.width, args.height)

    work_dir = Path(tempfile.mkdtemp(prefix="drawio-render-"))
    profile_dir = Path(tempfile.mkdtemp(prefix="drawio-profile-"))
    try:
        (work_dir / "preview.html").write_text(build_html(xml, drawio_path.name), encoding="utf-8")
        server = ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(work_dir)))
        port = server.server_address[1]
        threading.Thread(target=server.serve_forever, daemon=True).start()
        url = f"http://127.0.0.1:{port}/preview.html?rev=1"

        screenshot_ok = False
        last_mode = "--headless=new"
        stderr_tail = ""
        for mode in ("--headless=new", "--headless"):
            last_mode = mode
            if png_path.exists():
                png_path.unlink()
            cmd = [
                str(browser),
                mode,
                "--disable-gpu",
                "--hide-scrollbars",
                "--no-first-run",
                "--no-default-browser-check",
                "--disable-extensions",
                f"--force-device-scale-factor={args.scale:g}",
                f"--user-data-dir={profile_dir}",
                f"--window-size={width},{height}",
                f"--virtual-time-budget={args.budget}",
                "--run-all-compositor-stages-before-draw",
                f"--screenshot={png_path}",
                url,
            ]
            try:
                proc = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    errors="replace",
                    timeout=args.budget / 1000 + 40,
                )
                stderr_tail = (proc.stderr or "").strip()[-400:]
            except subprocess.TimeoutExpired:
                stderr_tail = "browser timed out"
                continue
            if png_path.exists() and png_path.stat().st_size >= 10000:
                screenshot_ok = True
                break

        server.shutdown()
        server.server_close()

        if not screenshot_ok:
            if png_path.exists() and png_path.stat().st_size > 4096:
                size_kb = png_path.stat().st_size // 1024
                print(f"[WARN] screenshot is small ({size_kb} KB) - verify it is not blank: {png_path}")
                return 0
            print(f"[FAIL] screenshot was not produced ({last_mode}).", file=sys.stderr)
            if stderr_tail:
                print(f"  browser output: {stderr_tail}", file=sys.stderr)
            print("  hint: increase --budget, or try --browser with another Chrome/Edge build.", file=sys.stderr)
            return 3

        dims = png_dimensions(png_path)
        dims_text = f"{dims[0]}x{dims[1]}" if dims else "unknown size"
        size_kb = png_path.stat().st_size // 1024
        print(f"[OK] browser: {browser}")
        print(f"[OK] viewport: {width}x{height} ({size_source})")
        print(f"[OK] screenshot: {png_path} ({dims_text}, {size_kb} KB)")
        return 0
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
        shutil.rmtree(profile_dir, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
