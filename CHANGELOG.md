# Changelog

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

Upstream project: https://github.com/Will-hxw/drawio-diagram-builder-skill
Do not overwrite this build by reinstalling upstream without merging.
