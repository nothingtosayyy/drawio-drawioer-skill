# Diagram Intake And Self-Supervision Protocol

Use this protocol for non-trivial diagrams, mixed inputs (prompts, project context, papers, screenshots, style references), and any iterative visual work. Effort is matched to the fidelity level: L1 runs the light path, L2 the standard path, L3 the full discipline. See the Gate Matrix in `SKILL.md` — it is the single source of truth for what applies at each level.

The failure to prevent is **false completion**: claiming the diagram is done while visible problems remain. The fix is not more ceremony — it is honest, scoped review backed by objective evidence (pre-flight output, screenshots, side-by-side comparison).

## 1. Diagram Brief (depth by level)

- **L1**: state the plan in one or two sentences (entities, flow, canvas). No file.
- **L2**: keep a short brief in your working notes; write `diagram-brief.md` only if the task spans sessions.
- **L3**: write `diagram-brief.md` with the full tables below.

Required sections (L3):

```markdown
# Diagram Brief

## User Goal
- Output:
- Audience:
- Must communicate:
- Must not do:

## Source Inventory
| id | source | type | role | priority | notes |

## Requirement Traceability
| id | requirement | source evidence | must/should/may | planned visual encoding |

## Semantic Model
| id | entity or relationship | direction / hierarchy / cardinality | visual encoding | uncertainty |

## Style Contract
| id | font | palette | stroke | icon style | layout density | reference source |

## Open Assumptions
| assumption | risk | how to verify |
```

Source roles are different and must not be mixed:

- **content source**: what the diagram must say.
- **structure source**: how components relate.
- **style source**: colors, typography, icon language, spacing.
- **layout source**: approximate placement, density, or composition.
- **asset source**: exact icons, logos, images, or symbols.

When multiple images are provided, classify each image by role. Do not copy layout from a style-only image unless the user asked for that. If sources conflict, write the decision in the brief before drawing.

## 2. Preserve Semantics Before Styling

Every arrow, loop, bracket, and group must have a meaning before it is drawn.

For each connector, answer:

- What is the source?
- What is the target?
- Is the relation data flow, control flow, feedback, update, selection, dependency, or annotation?
- Is it one-to-one, fan-in, fan-out, bidirectional, loop, or grouping?
- Where should the arrowhead be?
- Can the route cross labels or boxes without changing meaning?

If you cannot answer these questions from the prompt, paper, code, or reference image, mark the connector as uncertain in the brief, or ask the user when the risk is high. Do not infer connector direction from convenience. A semantically wrong arrow is a P0 blocker even if it looks neat.

## 3. Style Extraction (by level)

When the user provides reference images as style guides:

- **L1**: one-line style statement (dominant colors, general shape language).
- **L2**: the compact table — palette, typography, spacing rhythm.
- **L3**: the full extraction table in `references/style-extraction.md`.

"Looking" at a reference is not extraction. Write down concrete values (hex codes, font sizes, gaps) before authoring XML, and treat them as your style contract. If you cannot read exact values (no vision tool), ask the user for the palette instead of guessing.

## 3.5 Pre-Flight: Static XML Quality Check

After writing the `.drawio` XML and before generating the first preview:

- **L2 / L3**: required. Run the checker, fix every FAIL, or waive a specific rule with `--waive <rule>` and log the reason.
- **L1**: recommended. Review the output; fix what is cheap to fix.

```powershell
python <skill-dir>/scripts/validate_visual_quality.py <file>.drawio --json --output preflight-report.json
```

The checker computes geometry defects you cannot perceive from XML alone:

- arrows passing through boxes or text
- text that will overflow its container
- font sizes mismatched to box sizes
- overlapping shapes
- inconsistent spacing
- palette scatter
- meaningless decorative blocks

Read the report before rendering. A pre-flight report is cheaper than a garbage screenshot cycle. Load `references/xml-preflight.md` for what each rule catches.

## 4. The Review Loop (finalization phase)

**Phase model:** during the draft phase (the user has not finalized), do NOT run this loop. Use the quick check (`--quick`: overlap, arrow-through-box, severe text overflow) and user feedback only — small defects are noise until finalization. Run the full loop when the user is ready to finalize or asks for a final pass, and compile its findings into the prioritized issue list the user chooses from. The iteration budget caps full review cycles; draft-phase quick fixes do not consume it.

After each rendered screenshot, review the whole current output — not only the region you just changed.

### 4.1 Zone Checklist (scan scope by level)

**Scan every zone in scope. Record what you actually see. A zone with no findings gets "no findings" — never invent entries to look thorough.**

Scope: L1 = zones 1–4 and 7 (core hygiene). L2 / L3 = all nine zones.

| Zone | What to look for |
|------|------------------|
| 1. Text readability | Text too small? Clipped by container? Hidden behind a shape or arrow? Overflowing an edge? |
| 2. Arrow hygiene | Arrow passing through a box, text, or icon? Overlapping another arrow? Wrong direction? Missing or misplaced arrowhead? |
| 3. Box integrity | Box overlapping another box or icon? Far too large for its content? Too small for its text? |
| 4. Spacing consistency | Unequal gaps between adjacent elements? Misaligned rows or columns? Uneven padding? |
| 5. Color & palette | Colors deviating from the style contract? Clashing neighbors? Missing fills where the reference has them? |
| 6. Typography | Font family, size, or weight inconsistent within the same element type? |
| 7. Layout & composition | Region placement or flow direction wrong? Density far from the reference? Missing labels, legend, or caption? |
| 8. Icons | Missing, wrong, oversized/undersized, or miscolored icons? Icons overlapping text or borders? |
| 9. Style coherence | Does the whole diagram feel like the reference family, or like a different genre? Answer honestly. |

### 4.2 Severity

- **P0** — makes the diagram wrong or unreadable: wrong connector semantics, arrow through a box, hidden/clipped text, accidental overlap, missing required content.
- **P1** — clearly visible defect a reviewer would flag: mismatched style, uneven spacing, hollow boxes, wrong icon.
- **P2** — polish: sub-pixel alignment, 1–2px size differences.

Pre-flight FAIL findings are P0-class; WARN findings are P1-class unless explicitly waived with a reason.

### 4.3 Fix And Verify

Fix **all P0/P1 found this cycle** (scope by level: L1 fixes P0 only; L2/L3 fix P0 + P1; P2 is logged, not fixed).

After fixing and regenerating the preview, verify each fix against the new screenshot:

1. Take the new screenshot.
2. For each defect, compare the old and new screenshot at that location.
3. Mark it: FIXED / NOT FIXED / PARTIAL / REGRESSION.

If a P0/P1 is NOT FIXED, retry it once. If it fails a second time, report it to the user with the suspected cause — do not retry forever.

```markdown
## Fix Verification — Cycle N

| defect id | claimed fix | old screenshot | new screenshot | status |
|-----------|-------------|---------------|---------------|--------|
| arr-03 | moved waypoints up 40px to bypass `attention` box | pass-3 zone-2 crop | pass-4 zone-2 crop | FIXED |
| box-07 | reduced height 180→80px, font to 14pt | pass-3 zone-3 crop | pass-4 zone-3 crop | PARTIAL — text fits, box still 20px too wide |
```

### 4.4 Cycle Discipline

Each cycle: scan zones → inventory (honest) → fix P0/P1 → regenerate → verify → log (L2 with a log / L3). Stop when the exit checklist for the level passes, the budget is spent, or the user says stop. Do not start another cycle just because a previous one existed — cycles are a budget, not a minimum. In Interactive mode, report progress and ask before continuing.

## 5. Red-Team Pass (L3, once, no quotas)

Before handoff for L3 work, switch roles once: stop being the author, become a hostile reviewer. Its purpose is to catch residual problems a fresh pass sees — not to produce a quota of findings.

Re-scan the nine zones on a canvas-only screenshot. Inspect especially:

- arrow direction, arrowhead placement, fan-in/fan-out, feedback loops
- connectors crossing text or boxes; impossible flows
- text overflow, wrapped titles, labels crossed by lines
- box overlaps, clipped shapes, z-order mistakes
- regressions introduced by the latest fixes

**Finding zero problems is an acceptable outcome if you honestly scanned.** Do not invent findings, do not manufacture trivial entries ("box A is 1px wider than box B") to look thorough. Record real findings and fix P0/P1 as usual. If the budget is exhausted, skip the pass and say so in the handoff — that is better than fabricating it.

## 6. Self-Score Card (optional)

The score card is a self-reflection aid, not a gate. Use it when you are unsure whether quality is acceptable; skip it otherwise. Handoff decisions are made by the exit checklist, never by this score.

| Dimension | Score (1–10) | Evidence / reason for deduction |
|-----------|-------------|-------------------------------|
| Text readability | /10 | |
| Arrow accuracy | /10 | |
| Color coherence | /10 | |
| Layout consistency | /10 | |
| Style match to reference/spec | /10 | |
| **TOTAL** | **/50** | |

If you fill it in, cite concrete screenshot-visible evidence for each deduction.

## 7. Stop Conditions And Handoff

A diagram can be handed off when any of these is true:

- the exit checklist for its level passes (even after one cycle), or
- the iteration budget is spent — hand off the current best, clearly labeled, or
- the user says stop.

Never hand off silently while a known P0/P1 is unresolved. List it in the gap list with a reason. Handoff package:

```markdown
## Handoff
- .drawio: <path>
- latest screenshot: <path>
- side-by-side reference vs result: <path> (style/replication tasks)
- what was verified: <pre-flight / screenshot how>
- gap list (remaining P2s, known mismatches, unverified claims):
  | gap | severity | reason | next action |
```

## 8. Defect Logging (L2 with a log / L3)

```markdown
## Screenshot Review Cycle N
| # | issue | observed screenshot | requirement/source evidence | cells to change | severity | status |

## Red-Team Audit (L3, pre-handoff)
| # | finding | location | severity | fix or accept? |

## Remaining Gaps
| gap | severity | reason | next action |
```

The log must include negative findings, not only confirmations. Do not overwrite earlier cycle records — append new passes so the debugging chain stays visible. Do not pad the log with fabricated entries.

## 9. Responding To User Feedback

When the user points out a visual or semantic mistake:

1. Do not defend the output. If the user can see it and you did not flag it, acknowledge that.
2. Re-open the relevant reference/prompt and the latest screenshot; correct your interpretation in one sentence.
3. Patch the source `.drawio`, not only the preview.
4. Re-render and show a focused crop plus the full canvas.
5. Append the mistake and fix to the defect log ("found by user, missed in cycle N").
6. Do **not** automatically re-run a full audit. Re-run the red-team pass only if the user asks for a thorough re-check, or the task is L3 and the budget allows.

## 10. Completion Standard

Before handing off, confirm:

- the exit checklist for the level passes, or the budget is spent and the gap list is explicit;
- the latest screenshot was reviewed against the brief or references (when a screenshot loop was possible);
- all P0/P1 in scope are fixed and verified, or listed in the gap list with reasons;
- the handoff package (Section 7) is complete.

For "100% reproduction", never claim perfection unless the latest side-by-side review finds no visible mismatch. Otherwise state exactly what remains and what the next patch target is.
