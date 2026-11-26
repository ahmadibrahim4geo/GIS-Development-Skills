# Architecture Decision Record (`ADR`): Custom Component or Stack Choice

> Required by [`build-vs-reuse-policy.md`](../references/build-vs-reuse-policy.md) before authoring custom components or replacing an existing engine/framework.

- **ADR ID:** `ADR-XXXX`
- **Date:** `YYYY-MM-DD`
- **Status:** `Proposed` | `Accepted` | `Superseded`
- **Decision Owners:**

## 1. Context & Problem Statement
Describe the exact geospatial/architectural problem, target platforms, CRS/precision constraints, and existing codebase invariants.

## 2. Existing & Open-Source Candidates Evaluated
| Candidate (`project_id`) | Outcome (`rejected` / `needs-evidence` / `partial-fit`) | Observed Evidence / License / Technical Gap |
|---|---|---|
| | | |

## 3. Justified Reason for Original Code / Chosen Architecture
Select at least one policy-valid justification from `build-vs-reuse-policy.md` (§2):
- [ ] Capability absent in compatible catalog / OSS ecosystem
- [ ] Irreconcilable OS/ABI/runtime incompatibility across verified candidates
- [ ] License mismatch prevents legal distribution under target terms
- [ ] Reproducible PoC benchmark failure against documented accuracy/latency/memory budget
- [ ] Unacceptable binary footprint bloat for a narrow verified primitive
- [ ] Explicit strategic ownership / clean-room behavioral parity goal

## 4. Consequences, Contracts & Security Boundaries
- Interface contracts exposed (`DatasetRef`, `ICrsTransformer`, etc.)
- Licensing & attribution impact (`THIRD_PARTY_NOTICES`, LGPL/GPL isolation)
- Rollback / replaceability path and required `T0–T4` acceptance tests
