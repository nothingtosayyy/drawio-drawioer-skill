#!/usr/bin/env python3
"""Validate replication artifact completeness by fidelity level.

Levels (see the Gate Matrix in SKILL.md):
- L1: no intermediate artifacts required.
- L2: no required files; a defect-log.md is recommended, and is checked
  lightly when present.
- L3: visual-spec.md, layout-grid.md, asset-ledger.md, and defect-log.md are
  required with their core sections.

With --require-screenshot-review, the defect log must record valid screenshot
evidence (canvas-only capture; L3 also requires a recorded resolution) and
must not contain pending rows.

There are intentionally NO quantity thresholds here: no minimum defect
counts, no self-score gate, no red-team finding quotas. Those were removed
because they pushed agents to fabricate log entries on clean diagrams.
Quality decisions are made by the exit checklist (SKILL.md) and the user,
not by counting rows.

Usage:
  python validate_replication_artifacts.py <workdir> --level L2
  python validate_replication_artifacts.py <workdir> --level L3 --require-screenshot-review
"""

import argparse
import re
import sys
from pathlib import Path

# Windows consoles default to a narrow codepage; force UTF-8 so symbols print
# correctly instead of turning into mojibake.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

L3_REQUIRED = {
    "visual-spec.md": [
        "## Source",
        "## Global Style",
        "## Regions",
        "## Text Blocks",
        "## Shapes",
        "## Connectors",
        "## Semantic Relations And Flow",
        "## Icons And Images",
    ],
    "layout-grid.md": [
        "## Canvas",
        "## Grid Lines",
        "## Region Boxes",
    ],
    "asset-ledger.md": [
        "## Exact Assets",
        "## Editable Primitive Icons",
        "## Approximations",
        "## Missing Assets",
    ],
    "defect-log.md": [
        "## Screenshot Review",
        "## Remaining Gaps",
    ],
}

CAPTURE_TYPES = [
    "full-page",
    "canvas-only",
    "deliberate-crop",
    "editor-full-canvas",
    "editor-partial",
]


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _check_placeholder_values(workdir: Path, errors: list) -> None:
    """Flag placeholder values left in visual-spec.md."""
    visual_spec = workdir / "visual-spec.md"
    if not visual_spec.exists():
        return
    text = _read(visual_spec)
    if "#______" in text or "___pt" in text or "___px" in text:
        errors.append(
            "visual-spec.md contains placeholder values (#______, ___pt, ___px). "
            "Style extraction was not completed - fill actual hex codes and font sizes."
        )


def _check_screenshot_evidence(text: str, level: str) -> list:
    """Check screenshot evidence meets canvas-only (and L3 resolution) rules."""
    errors = []
    lower = text.lower()

    if ".png" not in lower and ".jpg" not in lower and ".jpeg" not in lower and ".webp" not in lower:
        errors.append("defect-log.md does not reference a screenshot image")
        return errors

    if "canvas-only" not in lower:
        errors.append(
            "screenshot is not marked as canvas-only; full-browser screenshots are "
            "invalid evidence. Crop to the canvas rectangle and record 'canvas-only' "
            "in the screenshot evidence table"
        )

    if level == "L3":
        # Accept common notations like 1600x900, 1600×900, or "width 1600".
        has_resolution = bool(re.search(r'(?<!\d)(1[2-9]\d{2}|[2-9]\d{3})(?!\d)', text))
        if not has_resolution:
            errors.append(
                "no pixel resolution recorded for the screenshot - record the screenshot "
                "dimensions in the evidence table (L3)"
            )

    return errors


def main() -> int:
    ap = argparse.ArgumentParser(
        description="Validate replication artifacts by fidelity level (no quantity thresholds)"
    )
    ap.add_argument("workdir", type=Path, help="Working directory with artifact files")
    ap.add_argument(
        "--level",
        choices=["L1", "L2", "L3"],
        default="L2",
        help="Fidelity level deciding which artifacts are required (default: L2)",
    )
    ap.add_argument(
        "--require-screenshot-review",
        action="store_true",
        help="Also validate screenshot evidence in defect-log.md",
    )
    args = ap.parse_args()

    workdir = args.workdir
    level = args.level
    if not workdir.is_dir():
        print(f"ERROR: {workdir} is not a directory", file=sys.stderr)
        return 2

    errors = []

    if level == "L1":
        drawio_files = sorted(workdir.glob("*.drawio"))
        print(f"L1: no intermediate artifacts required for {workdir}")
        if drawio_files:
            print("  found .drawio: " + ", ".join(p.name for p in drawio_files))
        return 0

    if level == "L3":
        for filename, sections in L3_REQUIRED.items():
            path = workdir / filename
            if not path.exists():
                errors.append(f"missing {filename} (required at L3)")
                continue
            text = _read(path)
            if len(text.strip()) < 80:
                errors.append(f"{filename} is too short to be useful")
            for heading in sections:
                if heading not in text:
                    errors.append(f"{filename} missing section heading: {heading}")
        _check_placeholder_values(workdir, errors)
    else:  # L2
        defect_log = workdir / "defect-log.md"
        if defect_log.exists():
            print("L2: defect-log.md found; running light checks")
        else:
            print("L2: no defect-log.md found (recommended but not required at L2)")

    if args.require_screenshot_review:
        defect_log = workdir / "defect-log.md"
        if not defect_log.exists():
            if level == "L2":
                errors.append(
                    "defect-log.md not found; it is required when "
                    "--require-screenshot-review is set"
                )
        else:
            text = _read(defect_log)
            if "pending" in text.lower():
                errors.append("defect-log.md still contains pending screenshot review entries")
            errors.extend(_check_screenshot_evidence(text, level))
            if not any(capture_type in text.lower() for capture_type in CAPTURE_TYPES):
                errors.append(
                    "defect-log.md does not record screenshot capture type "
                    f"(expected one of: {', '.join(CAPTURE_TYPES)})"
                )

    if errors:
        print(f"VALIDATION FAILED for {workdir} (level {level}):")
        for e in errors:
            print(f"  - {e}")
        return 1

    print(f"All level-{level} checks passed for {workdir}")
    print("Reminder: no quantity thresholds are enforced; the honesty of the")
    print("defect log is the agent's responsibility, checked by the user.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
