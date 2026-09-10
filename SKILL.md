---
name: drawio-diagram-builder
description: Create, edit, replicate, and iteratively refine editable diagrams in diagrams.net/draw.io (.drawio XML) from prompts, papers, repositories, screenshots, or existing diagrams. Use when asked to generate a scientific figure, paper method diagram, ML/system architecture diagram, draw.io file, reference-figure replication, flowchart, browser-screenshot review loop, Windows-safe draw.io preview, or layout fixes for overlapping text, arrows, colors, icons, fonts, and component alignment.
---

# Research Draw.io Diagram Builder

## Overview

Turn prompts, papers, repositories, and reference images into editable `.drawio` diagrams. The workflow is sized to the task: ask for a fidelity level and an iteration budget up front, run the smallest process that reaches the target, and stop when the target is met or the budget is spent.

Core principles:

1. **Editable output first.** The `.drawio` file is the primary artifact. Never present an embedded screenshot as the final answer when the user asked for an editable or vector result.
2. **Fit the process to the task.** A 15-box flowchart does not need the ceremony of a pixel-faithful conference-figure replica. The fidelity level decides which gates apply.
3. **Deliver early, then refine.** Most users want to see something quickly and react to it, not wait out a long black box. Under the default draft-first strategy, the first version whose quick check is clean is revealed to the user immediately (file + preview link); refinement continues afterward. Never bury the first reveal behind the full review cycle. Long stretches of invisible work are the original failure mode this skill exists to avoid.
4. **Check lightly in draft, fully at finalization.** Until the user finalizes, run only the quick check (display-blocking defects: overlap, arrow-through-box, severe text overflow) and ignore small imperfections — a draft exists to be reacted to, not audited. When the user is ready to finalize (or asks for a final pass), run the full check, compile every finding into a prioritized issue list (P0/P1/P2), and let the user choose what to fix. Never dump full technical findings on an unfinished draft; never skip the full pass at finalization.
5. **The user holds the controls — and must know what they can say.** Ask about fidelity, budget, and delivery strategy at intake; report progress after each cycle; hand off at the target or when the budget runs out. **Never assume the user knows the available commands: at every contact point (draft handoff, progress reports, final handoff), spell out the concrete next actions in the user's language** — e.g. "send feedback / say 'finalize' to run the full check and get the issue list / say nothing and I'll keep refining". The user may stop the loop or redirect at any time.
6. **Objective checks over self-declared quality.** Prefer the static pre-flight checker, rendered screenshots, and side-by-side comparison with the reference. Fix by severity (P0/P1), never by finding counts.

## Prerequisites

Check what is available before starting. If something is missing, degrade gracefully (see Failure Handling) instead of stopping.

| Requirement | Why | If missing |
|---|---|---|
| Python 3.7+ | preview/validation scripts | author XML by hand; skip script-based checks and say so |
| Browser automation (Playwright MCP, Puppeteer MCP, browser tools) | screenshots for the review loop | degraded mode: static pre-flight + ask the user to review the rendered preview once |
| Vision / image reading (for reference images) | style extraction, fidelity comparison | ask the user for palette hex codes; state that pixel-level fidelity cannot be verified |
| Internet access | the preview loads `https://embed.diagrams.net/` in an iframe | XML authoring still works; preview/screenshot unavailable |
| File write access | creating `.drawio` files | — |

Script paths are relative to the skill directory. If Playwright reports a missing bundled browser, try an installed channel first: `npx playwright screenshot --channel chrome ...` or `--channel msedge ...`.

## Step 0 — Task Intake

Ask once, in one batch. Do not drip questions.

1. **Fidelity level**
   - L1 Structure — content, labels, and semantics correct; layout may differ
   - L2 Layout — approximate placement, palette, and typography match the reference
   - L3 Pixel — maximum-fidelity replication
2. **Iteration budget** — default by level: L1 = 1 cycle, L2 = 2, L3 = 3. The user may set a different cap. "Keep going until it's perfect" is not a number — cap it at the level default and say so.
3. **Deliverables** — `.drawio` only / + PNG export / + both
4. **Delivery strategy** — draft-first (recommended default) or polish-first:
   - Draft-first: the moment the first version passes pre-flight, you get the file and a preview link; refinement continues after your first look. Best for avoiding a long black box.
   - Polish-first: nothing is revealed until the exit checklist passes or the budget ends.

**Blocking gate: for replication, style-matching, or any diagram derived from a reference image, do not author anything until the user has answered — or explicitly delegated the choice ("you decide" / "up to you"). Proposing a default level and "confirming" it yourself is still not an answer: the ask must go to the user and the reply must come from the user. The user's first message rarely contains the level; the default action on "replicate this" is to ASK, not to draw. A test run, an automated pipeline, or your own judgment never removes this gate.**

Request-specific rules:

- "redraw / replicate / reproduce" without a level → **ask the user**, proposing L2 as the recommended default. Never silently assume L2 or L3.
- "exact / 100% / pixel-perfect" → level is L3; still **ask** for the budget.
- Freeform diagram with no reference image → L1 is a safe default; state the plan in one sentence and proceed unless the user objects.
- User delegates ("you decide") → record the choice as user-delegated, apply the level defaults, and say what you chose.

Also record without asking: output path, canvas size, caption policy, label language.

## Fidelity Levels — Gate Matrix

This table is the single source of truth for which gates apply at each level. Reference files defer to it.

| Stage | L1 Structure | L2 Layout | L3 Pixel |
|---|---|---|---|
| Intermediate docs | none | optional (visual-spec, defect-log) | full set: visual-spec, layout-grid, asset-ledger, defect-log |
| Draft phase (same for all levels) | quick check only (`--quick`): overlap, arrow-through-box, severe text overflow. Small defects wait for finalization. Draft is revealed as soon as the quick check is clean; draft-phase iteration follows user feedback with quick checks only. |
| Finalization check | full pre-flight + prioritized issue list | full pre-flight + screenshot review + issue list | full pre-flight + screenshot review + one red-team pass + issue list |
| Issue handling | the user chooses what to fix from the issue list; skipped items move to the gap list |
| Finding quotas | none | none | none |
| Budget | caps full-review cycles (draft-phase quick fixes do not consume it) |
| Exit gate | the user has acknowledged the issue list (fix or skip per item) |

"Up to N cycles" means the loop stops as soon as the exit checklist passes, even after one cycle. It also stops when the budget is spent: hand off the current best plus a gap list. There is no minimum number of cycles and no minimum number of findings. Never invent defects to justify more iterations, and never keep iterating on a diagram that already passes its checklist.

## Standard Workflow

1. **Intake** (Step 0). For replication tasks, also load `references/reference-replication-protocol.md`.
2. **Plan** — depth by level (see `references/self-supervision-and-intake.md`):
   - Define every connector's meaning before drawing it (source, target, direction, fan-in/out, feedback).
   - If the user provided style references, extract the style first (`references/style-extraction.md`): compact table for L2, full table for L3.
3. **Author XML** (`references/xml-authoring.md`): explicit geometry, editable primitives, icons from `references/primitive-icons.md` or the bundled assets in `assets/icons/`.
4. **Quick check (draft phase)** — run `python <skill-dir>/scripts/validate_visual_quality.py <file>.drawio --quick`. It checks only display-blocking defects (overlap, arrow-through-box, severe text overflow). Fix those; everything else waits for finalization.
5. **Preview** — `python <skill-dir>/scripts/serve_drawio_preview.py <file>.drawio --port 8765` (or `make_drawio_preview.py` + `python -m http.server`). Open `http://127.0.0.1:8765/drawio-preview.html?rev=N` and wait 3–5 s for the embed.
6. **Draft handoff (draft-first strategy — the default).** As soon as the quick check is clean, hand the draft to the user right away: `.drawio` path + preview URL + **the available next actions spelled out explicitly in the user's language** — e.g. "draft 1 is ready. You can: (a) send feedback and I'll adjust; (b) say 'finalize / run the final check' and I'll run the full pass, then give you a prioritized issue list to pick fixes from; (c) say nothing and I'll keep refining." Never assume the user knows the 'finalize' command exists — always announce it. Do NOT run the full pre-flight or the review cycle before this reveal. Under polish-first, skip this step and reveal only at finalization.
7. **Draft-phase iteration** — apply user feedback as light changes; after each change re-run only the quick check. No full reviews during the draft phase.
8. **Finalization (when the user is ready to finalize or asks for a final pass)**:
   - Run the full pre-flight plus the level's finalization checks (screenshot review; L3 also one red-team pass).
   - Compile EVERY finding into a prioritized issue list (P0/P1/P2) and give it to the user to choose what to fix.
   - Fix the selected items, re-verify, and repeat until the user accepts or the budget is spent.
9. **Converge or stop**:
   - Exit checklist satisfied and the user has acknowledged the issue list → final handoff, even right after the first full pass.
   - Budget spent → final handoff of the current best + gap list, clearly labeled.
   - The user may stop or redirect at any time; in Interactive mode, report progress before starting another full cycle, again stating the concrete options (continue / adjust / finalize).
10. **Final handoff** — `.drawio` path + latest screenshot + (replication/style tasks) a side-by-side reference-vs-result image + the final issue list (fixed + consciously skipped) + gap list + a one-line summary of what changed since the draft. The self-score card is optional and never blocks handoff.

## Screenshot Standard

Applies whenever a screenshot is used as review evidence:

- Canvas-only crop; the diagram must occupy ≥80% of the image. A full browser window is invalid evidence.
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
- `scripts/check_skill_update.py` — compares the local VERSION with the upstream repository. This is a locally customized build: reinstalling from upstream overwrites local changes.
- Reference files: `references/drawio-workflow.md` (end-to-end workflow), `references/self-supervision-and-intake.md` (intake, review zones, exit discipline), `references/xml-preflight.md` (pre-flight rules), `references/style-extraction.md` (style capture), `references/topconf-paper-style.md` (paper-figure style), `references/primitive-icons.md` (editable icon recipes), `references/reference-replication-protocol.md` (replication protocol), `references/xml-authoring.md` (XML patterns).
- Assets: `assets/icons/ICON-MANIFEST.md` (bundled MIT Tabler SVGs), `assets/reference-images/REFERENCE-IMAGES.md` (style fallback images).

## Editing Rules

- Edit `.drawio` files by writing or patching XML directly. Keep a working copy and a handoff copy only when useful.
- Preserve user files and unrelated generated files.
- Never claim completion without visual verification when a screenshot loop was possible. In degraded mode, state exactly what was and was not verified.
- When the user reports a defect: fix it, show the focused crop plus the full canvas, and append to the defect log. Do not re-run full audits unless the user asks.
- For "100% reproduction", treat it as a bounded target: keep fixing visible mismatches until the budget is spent or the user accepts. Report remaining mismatches honestly — never claim perfection.
