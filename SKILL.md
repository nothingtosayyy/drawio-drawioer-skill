---
name: drawioer
description: Create, edit, replicate, and iteratively refine editable diagrams in diagrams.net/draw.io (.drawio XML) from prompts, papers, repositories, screenshots, or existing diagrams. Use when asked to generate a scientific figure, paper method diagram, ML/system architecture diagram, draw.io file, reference-figure replication, flowchart, browser-screenshot review loop, Windows-safe draw.io preview, or layout fixes for overlapping text, arrows, colors, icons, fonts, and component alignment.
---

# Research Draw.io Diagram Builder

## Overview

Turn prompts, papers, repositories, and reference images into editable `.drawio` diagrams. The workflow starts with the fastest path that can produce a useful first result, then refines on demand.

Core principles:

1. **Editable output first.** The `.drawio` file is the primary artifact. Never present an embedded screenshot as the final answer when the user asked for an editable or vector result.
2. **Fit the process to the task.** A 15-box flowchart does not need the ceremony of a pixel-faithful conference-figure replica. The fidelity level decides which gates apply.
3. **Deliver before checking.** The first visible result must reach the user as fast as possible — no script-based checks block the draft. XML is written, file is handed over; refinement and validation happen after the first look, not before.
4. **Zero external tools in the fast path.** For a simple diagram, the entire pipeline is: write XML → hand over. Python scripts, preview servers, and browser screenshots are optional tools scoped to specific needs, not gates for every diagram.
5. **The user signals "done."** The finalization pass (full pre-flight + issue list) runs only when the user says "finalize" — never as a mandatory post-draft step. The draft exists to be reacted to, not audited.
6. **Checks serve the user, not the process.** Quick check, preview, and screenshot are available on demand. Their absence must never block delivery.

## Prerequisites

Check what is available before starting. If something is missing, degrade gracefully (see Failure Handling) instead of stopping.

| Requirement | Why | If missing |
|---|---|---|
| Python 3.7+ | preview/validation scripts | author XML by hand; skip script-based checks and say so |
| System Edge/Chrome (any recent build) | agent screenshots via `scripts/render_png.py` (headless; no browser panel or MCP tooling needed) | degraded mode: static pre-flight + ask the user to review the rendered preview once |
| Vision / image reading (for reference images) | style extraction, fidelity comparison | ask the user for palette hex codes; state that pixel-level fidelity cannot be verified |
| Internet access | preview/screenshot pages load `https://viewer.diagrams.net/` and `https://embed.diagrams.net/` | XML authoring still works; preview/screenshot unavailable |
| File write access | creating `.drawio` files | — |

Script paths are relative to the skill directory. **Run `preflight.py` lazily** — execute it only before the first use of a Python script. If no script is needed (simple diagram, fast path), preflight never runs.

## Step 0 — Task Intake

**Minimal intake rule: the simplest path has zero questions.** Infer the level from the request and proceed. Only ask when the request is ambiguous or explicitly about replication.

**Fast path (no questions, no ceremony):**
- Freeform diagram (flowchart, architecture, process) — silently assume L1 structure-only, `.drawio` only. State the plan in one sentence and write XML immediately.
- "Draw a simple X" — same fast path.
- "Like this" / provides a drawn reference → this is replication; **ask once** about fidelity.

**Replication intake** (one question only):

> 你想要什么精细度？(1) 结构和内容正确，最快出图 —— (2) 布局和配色贴近，推荐 —— (3) 尽量一模一样，最费时

Answer 1→L1, 2→L2, 3→L3. No answer → L2 default.

**For any task:** do not ask about deliverables (`.drawio` vs PNG), delivery strategy (draft vs polish), or iteration budget. Default to `.drawio` only, deliver immediately after first XML, and let the user signal when they want the full pass.

## Fidelity Levels — Gate Matrix

This table is the single source of truth for which gates apply at each level. Reference files defer to it.

| Stage | L1 Structure | L2 Layout | L3 Pixel |
|---|---|---|---|
| Intermediate docs | none | optional (visual-spec, defect-log) | full set: visual-spec, layout-grid, asset-ledger, defect-log |
| Draft phase (same for all levels) | no blocking gates. XML is written → hand off to user. Quick check (`--quick`) is available on demand but never blocks delivery. Small defects wait for finalization. |
| Finalization check | full pre-flight + prioritized issue list | full pre-flight + issue list | full pre-flight + one red-team pass + issue list |
| Issue handling | the user chooses what to fix from the issue list; skipped items move to the gap list |
| Finding quotas | none | none | none |
| Exit gate | the user has acknowledged the issue list (fix or skip per item) |

## Standard Workflow

1. **Assess** — classify the request: is it a freeform diagram (fast path) or replication/style-matching?
   - Fast path: skip to step 3. No intake, no preflight, no plan docs.
   - Replication: Step 0 one-question intake first.
2. **Author XML** — write mxGraph XML into a `.drawio` file. Simple geometry, editable primitives, icons from `assets/icons/tabler/outline/`.
3. **Hand off (no ceremony).** Tell the user the file path in one sentence. Do not spell out options — let the user react naturally.
4. **Iterate on feedback** — user says what to change → edit XML → hand off again. Quick check and preview are available on demand if the user asks for verification.
5. **Finalization (only when the user says "finalize")** — run the full pre-flight, compile a prioritized issue list, present it to the user, fix what they choose, and hand off the final `.drawio`.

## Screenshot Standard

Applies whenever a screenshot is used as review evidence:

- Canvas-only crop; the diagram must occupy ≥80% of the image. A full browser window is invalid evidence.
- `scripts/render_png.py` output is canvas-only by construction (no browser chrome) and auto-fits the diagram — prefer it as the agent-side review screenshot; `--width/--height` force a fixed viewport when needed.
- Cache-bust with `?rev=N`; wait for the iframe to render (3–5 s).
- If cropping is unavailable: resize the viewport to 1920×1400+, zoom out until the full canvas fits, then screenshot. If text is unreadable in the result, the screenshot is invalid.

## Exit Checklists (finalization only)

These apply when the user finalizes, not during the draft phase.

**L1:** all required entities/labels present, connector semantics correct, no display-blocking defects (overlap, arrow-through-box, severe text overflow).
**L2:** L1 + palette/typography follow the style contract + region layout approximates the reference + a side-by-side comparison was reviewed (style/replication tasks).
**L3:** L2 + a red-team pass was done (or explicitly skipped with a stated reason).

**Final gate in all cases:** every finding from the finalization pass is presented with its priority, and the user has acknowledged the disposition of each item (fix or consciously skip). Skipped items move to the gap list.

## Failure Handling And Degradation

- **Twice-failed fix** — stop retrying; report the defect, what was tried, the suspected cause (rendering difference, tool limit), and the options.
- **Unavoidable renderer differences** — record them in the gap list; do not loop on them.
- **Windows long URLs** — never open large diagrams via `.url` shortcuts or `#create=` URLs; use the local preview helpers (short URL via postMessage).
- **No screenshot channel** — never build a bespoke rendering pipeline. Run `preflight.py`; if the screenshot channel is unavailable, switch to degraded mode (static pre-flight + hand the preview URL to the user) and state exactly what was not verified.
- **Stale preview** — the preview HTML embeds the XML at generation time; regenerate after every XML edit and bump `?rev=N`.
- **Saving from preview** — the blue Save button downloads a `.drawio`; move it back into the working path before further edits.
- **Text overlap or overflow** — split cells, reduce font size, widen containers; verify by screenshot.
- **Ugly loop arrows** — use editable curved connectors, not Unicode glyphs.
- **Missing icons** — check `assets/icons/ICON-MANIFEST.md` and `references/primitive-icons.md` before downloading anything.
- **User says stop** — stop immediately; hand off the current state + gap list.

## Bundled Helpers

- `VERSION` — installed skill version (this is a locally customized build; see `CHANGELOG.md`).
- `scripts/validate_visual_quality.py` — static pre-render checking (arrow–box collisions, text overflow risk, spacing, palette, decorations, density). Supports `--quick` (draft phase: display-blocking rules only), `--waive <rule>` to downgrade specific FAIL rules to non-blocking WAIVED findings (the reason still needs to be logged), `--json`, `--strict`, `--rules`.
- `scripts/validate_drawio.py` — structural validation before handoff; supports `--strict` and `--json` for CI.
- `scripts/validate_replication_artifacts.py <workdir> --level L2|L3 [--require-screenshot-review]` — artifact completeness by level. L1 requires no intermediate files.
- `scripts/serve_drawio_preview.py` / `scripts/make_drawio_preview.py` — local short-URL preview that loads the XML into diagrams.net via `postMessage`.
- `scripts/render_png.py` — headless canvas-only PNG render (system Edge/Chrome; auto-fit viewport; `--width/--height`/`--scale`/`--budget`/`--browser` overrides).
- `scripts/preflight.py` — one-shot environment report (Python, script set, headless browser, network, optional draw.io desktop) plus the working mode; run once per session.
- `scripts/check_skill_update.py` — compares the local VERSION with the upstream repository. This is a locally customized build: reinstalling from upstream overwrites local changes.
- Reference files: `references/drawio-workflow.md` (end-to-end workflow), `references/self-supervision-and-intake.md` (intake, review zones, exit discipline), `references/xml-preflight.md` (pre-flight rules), `references/style-extraction.md` (style capture), `references/topconf-paper-style.md` (paper-figure style), `references/primitive-icons.md` (editable icon recipes), `references/reference-replication-protocol.md` (replication protocol), `references/xml-authoring.md` (XML patterns).
- Assets: `assets/icons/ICON-MANIFEST.md` (bundled MIT Tabler SVGs), `assets/reference-images/REFERENCE-IMAGES.md` (style fallback images).

## Editing Rules

- Edit `.drawio` files by writing or patching XML directly. Keep a working copy and a handoff copy only when useful.
- Preserve user files and unrelated generated files.
- Never claim completion without visual verification when a screenshot loop was possible. In degraded mode, state exactly what was and was not verified.
- When the user reports a defect: fix it, show the focused crop plus the full canvas, and append to the defect log. Do not re-run full audits unless the user asks.
- For "100% reproduction", treat it as a bounded target: keep fixing visible mismatches until the budget is spent or the user accepts. Report remaining mismatches honestly — never claim perfection.
