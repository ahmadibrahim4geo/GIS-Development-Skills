# Engine Evaluation Report

> Compare candidate GIS engines/libraries against verified hard exclusion gates and the 100-point weighted rubric (`references/engine-comparison-guide.md`).

| Field | Value |
|---|---|
| Evaluation ID | |
| Request / Workload | |
| Target OS / Architecture | |
| License Policy (`free-first`, `oss-only`, `lgpl-dynamic-ok`, `gpl-ok`, `commercial-host-explicit`) | |
| Offline / No-Key Constraint | |
| Evidence Tier (`T0` metadata / `T1` offline test / `T2` PoC runtime) | |

## 1. Required & Optional Atomic Capabilities

- Required `capability_id`s: ``
- Optional `capability_id`s: ``

## 2. Hard Exclusion Gate Screening

| Candidate (`project_id`) | Entity Type | License SPDX / Cost Class | Security Status | Gate Result (`eligible` / `needs-evidence` / `rejected`) | Failed Gates / Missing Evidence |
|---|---|---|---|---|---|
| | | | | | |

## 3. Weighted Scoring Breakdown (Eligible / Conditional Only)

| Candidate (`project_id`) | Func (25) | Geod (20) | Perf (15) | Lic (15) | Integ (10) | Deploy (10) | Maint (5) | Total /100 | Missing Metrics (`NOT RUN`) |
|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | |

## 4. Compatibility, Isolation & Provenance Notes

- Separate native C++/GDAL/PROJ boundaries cleanly (never mix PyPI wheels and OSGeo4W/conda DLLs).
- Quarantined external agent skills remain strictly `reference-only` until audited.
- No candidate rated `unknown` / `needs-evidence` is declared production-ready without verified evidence.
