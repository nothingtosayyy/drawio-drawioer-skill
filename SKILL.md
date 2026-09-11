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

The skill writes `.drawio` files — plain XML. No runtime dependencies, no browser, no network, no Python. All validation scripts are optional tools, not gates.

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

## Exit Checklists (finalization only)

These apply when the user finalizes, not during the draft phase.

**L1:** all required entities/labels present, connector semantics correct, no display-blocking defects (overlap, arrow-through-box, severe text overflow).
**L2:** L1 + palette/typography follow the style contract + region layout approximates the reference + a side-by-side comparison was reviewed (style/replication tasks).
**L3:** L2 + a red-team pass was done (or explicitly skipped with a stated reason).

**Final gate in all cases:** every finding from the finalization pass is presented with its priority, and the user has acknowledged the disposition of each item (fix or consciously skip). Skipped items move to the gap list.

## Failure Handling

- **Twice-failed fix** — stop retrying; report the defect, what was tried, the suspected cause, and the options.
- **Ugly loop arrows** — use editable curved connectors, not Unicode glyphs.
- **Missing icons** — check `assets/icons/ICON-MANIFEST.md` and `references/primitive-icons.md` before downloading anything.
- **User says stop** — stop immediately; hand off the current state.

## Bundled Helpers

- `VERSION` — installed skill version (see `CHANGELOG.md`).
- `scripts/validate_visual_quality.py` — static pre-render checking (arrow–box collisions, text overflow risk, spacing, palette, decorations, density). Supports `--quick`, `--json`, `--strict`.
- `scripts/validate_drawio.py` — structural validation; supports `--strict` and `--json`.
- Reference files: `references/drawio-workflow.md`, `references/self-supervision-and-intake.md`, `references/primitive-icons.md`, `references/xml-authoring.md`.
- Assets: `assets/icons/ICON-MANIFEST.md` (bundled MIT Tabler SVGs).

## Editing Rules

- Edit `.drawio` files by writing or patching XML directly. Keep a working copy and a handoff copy only when useful.
- Preserve user files and unrelated generated files.
- When the user reports a defect: fix it and re-deliver. Do not re-run full audits unless the user asks.
- For "100% reproduction", treat it as a bounded target: keep fixing visible mismatches until the user accepts. Report remaining mismatches honestly — never claim perfection.
