# Cognitive Methods, Research Governance & Decision Intelligence

> Canonical specification for AAREF requirements `REQ-COG-01..18`, `REQ-RES-01..09`, and `REQ-DEC-01..09`. Complements domain owners without adding redundant skills or mandatory model chains.

## 1. Selective Cognitive Method Toolkit (18 Protocols)

These 18 protocols are **on-demand cognitive patterns**, NOT 18 subagents to spawn per prompt. Activate only what matches the current problem; record concise evidence and rationales—never private model deliberation.

| Method | Activation Trigger | Core Action | Verifiable Output |
|---|---|---|---|
| **Adaptive Reasoning** | Every intake | Calibrate `L0–L5` depth separately from `I0–I4` risk | Justified depth + impact pair |
| **Critical Thinking** | Weak evidence, high stakes, review | Seek falsifying evidence, hidden assumptions, over-generalization | Severity-ranked findings |
| **First Principles** | Ambiguous problem or greenfield design | Separate user outcome from tool labels; isolate hard physics/math constraints | Problem definition without tool lock-in |
| **Systems Thinking** | Coupled UI/engine/data pipelines | Trace data flow, command flow, state ownership, failure cascades | Component boundary & dependency map |
| **Strategic Planning** | Multi-phase scope (`L4`, `0007`) | Partition into vertical slices, critical path, rollback checkpoints | DAG plan checked for cycles |
| **Research Intelligence** | Missing/volatile specs, APIs, licenses | Check primary docs, release versions, license terms directly | Source evidence record |
| **Decision Intelligence** | Multiple viable libraries/engines | Eliminate on hard constraints first; compare surviving options | Decision Capsule / ADR |
| **Root Cause Analysis** | Recurring bug, test fail, CRS drift | Reproduce, pinpoint first divergence, run discriminating test | Causal proof + regression check |
| **Scientific Reasoning** | CRS, RS indices, DEM, statistics | State hypothesis, units, equations, validation vs confounding factors | Reproducible scientific check |
| **Counterfactual Analysis** | Major engine/API/dependency choice | Ask what breaks if connectivity, license, or dependency version fails | Fallback / sensitivity check |
| **Predictive Thinking** | Migrations, packaging, field deploy | Anticipate blast radius, offline edge cases, rollback triggers | Pre-change mitigation list |
| **Creative Problem Solving** | Conventional pattern blocked by constraint | Generate strictly compliant alternatives; discard incompatible ones first | Testable safe workaround |
| **Metacognition** | Stalled loop or shrinking signal/noise | Judge progress from test observations; pivot or stop cleanly | Replan or `BLOCKED` disposition |
| **Uncertainty Management** | Unresolved component (`UI.js`) or missing metadata | Tag `material_unknowns` vs reversible assumptions | Targeted question or inspection step |
| **Failure Recovery** | Build, runtime, tool, or data error | Classify failure mode; alter hypothesis/tool/input cleanly | Recovery path or `PARTIAL`/`NOT_RUN` |
| **Learning & Adaptation** | Fixed defect or validated user correction | Draft environment-scoped `CANDIDATE` lesson for human/peer review | Quarantined lesson record |
| **Context Intelligence** | Multi-turn resume or large repository | Load task-critical lines first; write compact checkpoints | Verified checkpoint ref |
| **Resource Intelligence** | Large batches, strict budget/latency | Batch independent reads safely; avoid redundant re-reads/retries | Honest `actual`/`estimated`/`UNKNOWN` usage |

**Reviewable Reasoning Loop (`L2–L5`):**
`Frame -> Ground -> Hypothesize -> Compare -> Decide -> Act -> Observe -> Revise -> Verify`.
- Formulate **genuinely distinct hypotheses** (not three rewordings of the same guess).
- Design the smallest discriminating experiment that preserves protected inputs.
- Revise the hypothesis immediately when observations falsify it; never cherry-pick logs.

## 2. Concise Decision Capsule Schema

For non-trivial technical choices (`L2+`), record a lightweight Decision Capsule in `.agent-development-log` or the active ADR:
`decision_id`, `task_id`, `question`, `facts_and_evidence_refs`, `material_assumptions`, `alternatives`, `hard_constraints`, `selection` (or `DEFERRED` / `UNRESOLVED`), `short_rationale`, `risks`, `verification`, `review_mode`, `reopen_when`.

## 3. Anti-Overthinking & Anti-Underthinking Guards

- Never run a full ADR or scientific checklist for a typo fix or `L0` glossary question.
- Never classify an unknown-cause failure as "simple (`L1`)" merely because the final patch touches one line; route unknown bugs through `L3 Root Cause Analysis`.
- Never cite fabricated numerical confidence percentages or request private hidden chain-of-thought extraction.

## 4. Research Intelligence & Source Conflict Resolution

1. **Source Priority Order:** (1) Primary repository code, official specs/EPSG/PROJ/GDAL/OGC standards, release notes; (2) peer-reviewed papers & agency docs (USGS, Copernicus); (3) reproducible local experiments; (4) community issues/blogs (symptom discovery only—never sole proof).
2. **Evidence States:** Tag claims honestly as `verified`, `supported`, `provisional`, `unknown`, or `contradicted`. Never average contradictory formulas or invent missing citations/licenses.
3. **Catalog Reuse Discipline:** Search `references/project-catalog.json` via `scripts/search_catalog.py` before proposing custom stacks. Keep GUI framework (`Qt`, `WPF`, `HTML/JS`), map renderer (`CesiumJS`, `MapLibre`), and GIS compute engine (`GDAL`, `QGIS Processing`) cleanly separated, and leave ambiguous names (`UI.js`) `unresolved` until source inspection.
4. **Blast-Radius & Clean-Room Check:** Before public API/schema/CRS shifts, verify backward compatibility, license boundaries (`MIT/BSD/Apache` vs `GPL/AGPL/SSPL` vs proprietary), and clean-room separation (never copy protected binaries, DAML, or icons).
