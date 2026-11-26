# Technology & Architecture Selection Report

> Standardized 10-section recommendation emitted alongside `scripts/recommend_stack.py` (`REQ-EV2-036`, `REQ-EV2-050`).

## 1. Intent Classification & 21 Architectural Slots
- **Original Request:**
- **Identified Intents / Build Models:**
- **Target OS / Arch / Languages / Offline & Free-First Constraints:**

## 2. Entity Role Separation & Existing Project Gate
- **UI Framework / Shell:** (`ui-shell` — separate from rendering and compute)
- **Map / 3D Renderer:** (`map-renderer`)
- **Geospatial Compute Core:** (`geospatial-engine` / `ICrsTransformer` / `IGeometryOps`)
- **Existing Workspace Inspection:** *(Observed working components & preserved invariants)*

## 3. Selected Build Mode(s) & Justification
- Selected modes from the 11 canonical build models + reason simpler reuse modes were kept or insufficient.

## 4. Per-Function Candidate Evaluation & Alternatives
| Function / Capability | Selected Candidate (`project_id`) | Integration Mode | Alternatives Evaluated | Rejected / `needs-evidence` Reasons |
|---|---|---|---|---|
| | | | | |

## 5. Multi-Engine Interfaces & Data Contracts
- `IDataProvider` · `ICrsTransformer` · `IGeometryOps` · `IRasterProcessor` · `IMapRenderer`
- **Serialized Boundary Types:** `DatasetRef`, `FeatureIdentity`, `RasterRef` (avoid passing live Qt/QGIS objects across IPC/JS bridges).

## 6. Developer Toolchain vs End-User Runtime Separation
- **Developer Only (`CI` / Build Machine):** Compilers, SDKs, headers, CMake/NuGet/npm build tools, heavy reference clones *(NEVER auto-installed without approval)*.
- **End-User Deliverable Runtime:** Exact portable/installer dependencies, `PROJ_DATA`/`GDAL_DATA` layout, clean-machine redistributables.

## 7. Algorithmic & Provider Fallback Guardrails
- Disclose semantic differences when switching analysis providers (e.g., `SNAP` vs `OTB` vs `GDAL/Rasterio`; zero silent provider fallback).

## 8. Licensing, Attribution & Security Guardrails
- `SPDX` obligations, LGPL shared linking / GPL process isolation boundaries, API keys/tile TOS boundaries, and `Security Guardian` checks.

## 9. Proof-of-Concept (PoC) Benchmark & ADR Summary
- Minimal slice acceptance test, cold/warm/memory/CRS accuracy checks (`V2 §32.1`), and link to `ADR` if custom code is justified.

## 10. Explicit Capability Gaps & `NOT RUN` Statement
- Missing upstream benchmarks, unavailable target OS toolchains (e.g., iOS without macOS/Xcode), and unverified `T2–T4` native execution remain explicitly `NOT RUN`.
