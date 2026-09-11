# Reference Image Replication Protocol

Use this protocol whenever the user provides a reference image and asks to reproduce, redraw, copy, replicate, or closely match it in draw.io. See the Gate Matrix in `SKILL.md` for which gates apply at each fidelity level (L1 / L2 / L3) — this file never overrides it.

The goal is to make replication an evidence-driven process without turning it into an unbounded one: turn the image into a specification (as deep as the level requires), draw from that specification, verify with rendered screenshots, and stop at the exit checklist or the iteration budget.

## Hard Rules

1. The primary output is a `.drawio` file. Preview HTML is derived and must not be treated as the source of truth.
2. Start authoring at the depth the level requires:
   - **L1**: no intermediate files; the reference defines content and rough layout only.
   - **L2**: a short (inline or written) spec of regions, palette, and typography before XML.
   - **L3**: do not begin `.drawio` XML until the required artifacts exist (see below).
3. Never silently omit a visible component. At L3, log omissions in `asset-ledger.md`; at L1/L2, state approximations and omissions in the handoff.
4. Do not reproduce only the geometry. Identify connector semantics: source, target, direction, fan-in/fan-out, feedback, grouping, and arrowhead placement.
5. Avoid "close enough" language for L3 work — record every remaining mismatch in `defect-log.md` or the gap list. For L1/L2, documented approximations are acceptable and must be stated.
6. Run `scripts/validate_visual_quality.py` before the first preview. Fix FAILs, or waive a specific rule with `--waive <rule>` and log the reason (waiving is normal at L1, unusual at L2, rare at L3).
7. Respect the iteration budget: at most the level default (L1: 1, L2: 2, L3: 3) or the user-specified cap. Stop when the exit checklist passes — even after one cycle — or when the budget is spent (hand off with the gap list).
8. Do not judge fidelity from a full browser screenshot. The diagram must fill ≥80% of the screenshot image. A screenshot showing the diagrams.net toolbar, sidebar, or browser chrome is invalid — crop to the canvas rectangle or zoom the viewport.
9. If the screenshot shows large structural errors, repair the plan before more XML patches: update `visual-spec.md` / `layout-grid.md` at L3, or re-inspect the reference and restate the plan at L1/L2.
10. Do not overwrite screenshot review history. After the first review row exists, append new passes and corrections instead of replacing the file.
11. Do not run artifact validation in parallel with generation, preview creation, screenshot capture, or scripts that write the same workdir. Validate only after those writes complete so the result reflects one coherent artifact state.

## Required Artifacts By Level

| File | L1 | L2 | L3 |
|------|----|----|----|
| `visual-spec.md` | — | optional | required |
| `layout-grid.md` | — | — | required |
| `asset-ledger.md` | — | — | required |
| `defect-log.md` | — | recommended | required |

For L3, create these files next to the working `.drawio` file and run:

```powershell
python scripts/validate_replication_artifacts.py <workdir> --level L3
```

After the latest screenshot pass and before handoff (L2/L3):

```powershell
python scripts/validate_replication_artifacts.py <workdir> --level L3 --require-screenshot-review
```

The final check fails if the log still contains placeholder screenshot rows.

## 1. visual-spec.md (L3; raw material for L2 specs)

This file captures what is visible.

```markdown
# Visual Spec

## Source
- Reference image:
- Target drawio:
- Canvas:
- Font policy:

## Global Style
- Background:
- Primary font:
- Stroke style:
- Arrow style:
- Color palette:

## Regions
| id | bbox x,y,w,h | role | visual notes |

## Text Blocks
| id | bbox x,y,w,h | text | font | alignment | priority |

## Shapes
| id | bbox x,y,w,h | type | fill | stroke | notes |

## Connectors
| id | from | to | route | arrowheads | label | notes |

## Semantic Relations And Flow
| id | source | target | meaning | direction/cardinality | visual evidence |

## Icons And Images
| id | bbox x,y,w,h | meaning | exact/approx/missing | replacement plan |
```

For complex research figures, use region IDs such as `top_problem_statement`, `bottom_method_overview`, `memory_hierarchy`, `routing_controller`.

## 2. layout-grid.md (L3)

This file turns the visual spec into coordinates. High-fidelity drawing needs explicit geometry, not vague relative placement.

```markdown
# Layout Grid

## Canvas
- width:
- height:
- scale assumption:
- margin:

## Grid Lines
| name | x | y | purpose |

## Region Boxes
| id | x | y | w | h |

## Repeated Components
| family | count | cell size | spacing | start x,y |

## Drawing Order
1. background regions
2. containers
3. internal shapes
4. connectors
5. text
6. icons
7. highlights/overlays
```

If the reference has a dense layout, do not rely on relative placement only. Use explicit x/y/w/h for each major container.

## 3. asset-ledger.md (L3)

This file prevents silent icon loss.

```markdown
# Asset Ledger

## Exact Assets
| id | source | path | usage |

## Editable Primitive Icons
| id | built from | fidelity notes |

## Approximations
| id | reference meaning | approximation | why |

## Missing Assets
| id | reference meaning | blocking issue | user action needed |
```

If using an embedded raster image, state why editability is intentionally reduced. For common paper-figure icons, consult `primitive-icons.md` before inventing one-off approximations.

## 4. defect-log.md (L2 with a log / L3)

Records screenshot-based refinement. Format and append rules are defined in `self-supervision-and-intake.md` Section 8. Each screenshot pass must add concrete observations — write "right-side multimodal panel is 18% too narrow", not "looks bad".

The screenshot evidence table must state the capture type: `full-page`, `canvas-only`, `deliberate-crop`, `editor-full-canvas`, or `editor-partial`. Use `editor-partial` only for debugging; it cannot support final fidelity claims.

The red-team pass (L3, once, budget permitting) inspects for: arrow direction and arrowhead placement; fan-in/fan-out and feedback semantics; bracket orientation; connector paths crossing text or boxes; box overlaps and z-order mistakes; text overflow and labels crossed by lines; regressions from the latest patch.

## Exit Criteria For Replication

Instead of counting defects or cycles, check the exit checklist for the level (see `SKILL.md`). For replication specifically:

- **L1**: content, labels, and connector semantics match the reference; layout is a reasonable simplification.
- **L2**: palette, typography, and region placement approximate the reference; a side-by-side comparison has been reviewed.
- **L3**: every visible mismatch is either fixed or listed in the gap list; artifacts are complete; red-team pass done or explicitly skipped.

Handoff requires: the `.drawio` file exists and is the primary artifact; pre-flight passed (or waivers logged); `validate_drawio.py` passes; preview HTML regenerated after the latest XML edit; the latest screenshot reviewed; remaining mismatches listed. For L3 also: `validate_replication_artifacts.py --level L3 --require-screenshot-review` passes.

For a "100% reproduction" request, the handoff must not claim perfection. It either shows that no visible mismatches remain after side-by-side review, or lists the exact remaining mismatches and next patch targets. If renderer differences make a mismatch impossible to remove, record it in the gap list and stop — do not loop on it.

## High-Fidelity Replication Discipline

If the first draft is messy, do not continue patching randomly. Return to `visual-spec.md` and `layout-grid.md` (L3) or re-inspect the reference and restate the plan (L1/L2), identify which observation or coordinate assumption failed, and repair the plan before editing XML again.

Prefer a simpler but structurally faithful first draft over a visually dense but incoherent drawing:

1. Correct canvas and major regions.
2. Correct container hierarchy.
3. Correct text placement.
4. Correct arrows.
5. Correct icons.
6. Correct colors and polish.

Only after the structure is correct should the agent increase visual density.

When a generated result looks bad, inspect these first-principles failure points:

- canvas scale or browser zoom makes the page clipped
- headings are too large and wrap unexpectedly
- multiline labels overlap nearby annotations
- bottom labels escape or touch the page edge
- connector routes use straight lines where the reference uses loops
- connector routes preserve geometry but invert the meaning, such as drawing a fan-in as five independent arrows
- icons were silently replaced with generic symbols
- background fills, shadows, and dashed borders were skipped
- generated scripts reset evidence files instead of appending new screenshot observations
- validator results were taken while another process was still rewriting the workdir

Use the defect log as an engineering ledger: every visible mismatch should map to either a missing observation, an incorrect coordinate, an unavailable asset, or a draw.io rendering difference.
