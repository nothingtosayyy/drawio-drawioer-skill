# Changelog

## 0.5.1 — Render pipeline + swimlane-aware checks (2026-09-11)

### Added

- **`scripts/preflight.py`** — one-shot environment preflight (Python, script
  set, headless browser, network reachability, optional draw.io desktop).
  Prints FULL / DEGRADED mode so sessions stop rediscovering the environment
  one failure at a time.
- **`scripts/render_png.py`** — headless canvas-only PNG rendering via system
  Edge/Chrome (no in-app browser panel or MCP tooling needed). Auto-fits the
  viewport to the diagram bounds; `--width/--height`, `--scale`, `--budget`,
  `--browser` overrides.

### Fixed

- **Swimlane false positives in `validate_visual_quality.py`** — nested child
  coordinates are now resolved to absolute canvas space, edge endpoints honor
  `exitX/exitY` / `entryX/entryY` anchors instead of center-to-center lines,
  and lane/group frames are excluded from collision, font-proportionality,
  and spacing-uniformity checks. A clean swimlane diagram now passes with
  0 FAIL / 0 WARN instead of 14 false FAILs.
- **Windows console crash** — `validate_drawio.py` (this skill and
  drawio-generator) now forces UTF-8 stdout/stderr; symbol output no longer
  crashes on GBK consoles.

### Changed

- SKILL.md: preflight step added to the standard workflow; `render_png.py`
  documented as the default agent screenshot channel; explicit "never build a
  bespoke rendering pipeline" rule in Failure Handling.

## 0.5.0 — Locally customized build (2026-09-10)

Reworked from upstream v0.4.1 to fix unbounded iteration and one-size-fits-all
quality gates. Core changes:

### Added

- **Step 0 Task Intake** (SKILL.md): a blocking gate that asks for fidelity
  level (L1/L2/L3), iteration budget, and deliverables before any work
  starts. "Replicate/redraw" triggers a question (with L2 proposed); no
  authoring begins until the user answers or explicitly delegates the
  choice. Test runs and pipelines never remove the gate. L3 is never
  assumed silently.
- **Intuitive intake phrasing** (SKILL.md Step 0): the intake is asked in the
  user's language with outcome-first wording and a stated cost per option —
  no internal codes or jargon exposed to the user (L1/L2/L3, draft-first,
  cycle budgets, ports); the "use your defaults"（按推荐来）shortcut is
  explicitly offered.
- **Draft-first delivery strategy** (SKILL.md): by default the first version
  that passes pre-flight is revealed to the user immediately (file + preview
  link) instead of waiting for the full review cycle; refinement continues
  within the budget after the first look. Polish-first is available as the
  user's explicit choice. "Deliver early, then refine" is a core principle.
- **Phase-based check depth** (SKILL.md + validate_visual_quality.py): the
  draft phase runs only a quick check — new `--quick` flag covering
  display-blocking rules (overlap, arrow-through-box, severe text overflow);
  small defects wait. The full pre-flight, screenshot review, and a
  prioritized issue list (the user chooses what to fix) happen only at
  finalization. The budget caps full-review cycles only.
- **Discoverable options at every contact point** (SKILL.md): the draft
  handoff and progress reports now state the concrete next actions in the
  user's language — including the "finalize" command — instead of assuming
  the user knows them. "The user holds the controls" now includes "and must
  know what they can say".
- **Gate Matrix** (SKILL.md): single source of truth for which gates apply at
  each level. All reference files defer to it.
- **Exit checklists (L1/L2/L3)**: objective pass conditions replace the
  self-score card as the handoff gate.
- **Budgeted loops**: at most N cycles per level (L1: 1, L2: 2, L3: 3, or a
  user-set cap). The loop stops as soon as the checklist passes and hands off
  with a gap list when the budget is spent.
- **Degradation paths**: missing tools (Python, browser automation, vision,
  network) degrade the workflow instead of stopping it.
- **Failure escalation**: a fix failing twice is reported to the user instead
  of being retried forever.
- **`--waive <rule>`** in `validate_visual_quality.py`: specific FAIL rules
  can be downgraded to non-blocking WAIVED findings with a logged reason.
- **`--level L1|L2|L3`** in `validate_replication_artifacts.py`: artifact
  requirements scale with the fidelity level; L1 requires no intermediate
  files.

### Removed

- All defect-finding quotas (C1 ≥ 30 / C2 ≥ 15 / C3 ≥ 8; red-team ≥ 15 / ≥ 10).
- The "minimum 3 screenshot cycles" hard gate.
- The self-score threshold as a handoff blocker (the card is kept as an
  optional reflection aid).
- "Do not ask the user — just keep working" and other anti-ask rules.
- Quantity thresholds hard-coded in `validate_replication_artifacts.py`
  (defect count ≥ 30, self-score ≥ 40, red-team ≥ 30).

### Fixed

- Contradictory quotas (per-zone minimums vs graduated totals) removed.
- Duplicate section numbering (two "4.4" sections) in
  `self-supervision-and-intake.md`.
- Script/documentation threshold mismatches (red-team ≥ 30 in the script vs
  ≥ 15 in the docs).

参考：本项目基于 [drawio-diagram-builder-skill](https://github.com/Will-hxw/drawio-diagram-builder-skill) 进行定制调整，不覆盖上游内容。
