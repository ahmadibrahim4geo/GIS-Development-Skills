# Build vs Reuse Policy / سياسة البناء مقابل إعادة الاستخدام

> **Principle:** **Discover Before Building. Reuse Before Reinventing. Free and Open Source First. Verify Before Claiming. Integrate Without Regression.**  
> **Scope:** Authoritative architectural decision order (`Engine Architecture Reuse Plan V2` §7, §10–§12).

---

## 1. Mandatory Decision Sequence (Before Writing New Code)

1. **Inspect existing project & invariants:** Identify what already works inside the target codebase (UI shell, renderer, CRS pipeline, tests, persistence). Never replace a working component casually.
2. **Classify intent & entity roles:** Separate UI framework from map renderer from geospatial compute core using the [Unified Taxonomy](engine-architecture-taxonomy.md) and [UI/Engine Contract](ui-engine-architecture-contract.md).
3. **Search canonical catalog first:** Check existing local skills and [project-catalog.json](project-catalog.json) (`references/project-catalog.json`) before proposing external additions.
4. **Apply hard gates before scoring:** Verify target OS/architecture, language/ABI compatibility, verified license compatibility, offline/zero-key requirements under Free-First, mandatory atomic capability evidence, and security posture. Reject failed candidates regardless of popularity. Treat `unknown` as `needs-evidence`, never as `pass`.
5. **Prefer proven reuse paths in order (adapted to lifecycle maintenance cost):**
   - Existing working capability inside the project;
   - Small single-purpose library (`PROJ`, `GEOS`, `Clipper2`, `Turf`, etc.);
   - Specialized engine behind a clean adapter contract;
   - Multi-engine composition (`multi-engine-composition` with explicit `DatasetRef`/CRS boundaries);
   - Approved open-source configuration, plugin, or justified `source-fork` (`KEEP / HIDE / DISABLE / REMOVE`);
   - Original custom component **only when justified below**.

---

## 2. When Writing Original Code Is Justified (Requires an ADR)

Writing original code or custom components is permitted **only** when one or more of the following hold and are documented in an **Architecture Decision Record (`ADR`)**:
1. Required geospatial or domain capability does not exist in compatible OSS candidates;
2. Verified upstream library has irreconcilable runtime, ABI, or platform incompatibility;
3. License mismatch blocks legal distribution under target terms (e.g., proprietary host or incompatible copyleft linkage without approved isolation);
4. Measured benchmark proves existing candidates miss documented accuracy or memory/latency targets;
5. Upstream package imposes unacceptable binary footprint/dependency bloat when a tiny verified primitive suffices;
6. Strategic ownership or clean-room behavioral parity is explicitly requested by the user.

---

## 3. When Replacing or Rebuilding Is Prohibited

Do **not** replace working engines or fork full applications when:
- The user asked only for cosmetic or Ribbon/toolbar reorganization (`ui-reorganization` or `ui-shell-migration`);
- Candidate suitability rests only on unverified claims, README marketing, or GitHub stars without evidence;
- Proposed switch would silently drop user project fidelity (IDs, CRS, Z/M, Arabic UTF-8 attributes, styles, undo stack);
- An unauthorized commercial host or paid cloud API key would be introduced silently under a free-first goal.
