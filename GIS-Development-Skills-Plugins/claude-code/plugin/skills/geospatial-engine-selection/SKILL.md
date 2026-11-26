---
name: geospatial-engine-selection
description: Select, compare, compose, and reuse GIS engines, kernels, renderers, frameworks, and open-source codebases without inventing nonexistent libraries or forcing a single stack. Use for new GIS apps, engine selection/replacement, source forks (QGIS cleanup), Clean-Room reference UIs, multi-engine compositions, اختيار محرك, بناء برنامج جديد, اشتقاق/فورك, or واجهة مثل ArcGIS Pro/Google Earth.
license: MIT
---

# Geospatial Engine Selection & Architecture Intelligence

Follow **Discover Before Building · Reuse Before Reinventing · Free and Open Source First · Verify Before Claiming · Integrate Without Regression**. Apply the [free-first policy](../../references/free-first-policy.md) and coordinate intake via [GIS Development](../gis-development/SKILL.md), [Prompt Intent Orchestrator](../prompt-intent-orchestrator/SKILL.md), [Security Guardian](../gis-security-guardian/SKILL.md), [DoneProof](../completion-evidence/SKILL.md), and [Development Journal](../agent-development-journal/SKILL.md).

## Core Responsibilities & Strict Boundaries

1. **Entity & Role Disambiguation:** Separate the 24 software types (`Application`, `Engine`, `Core`, `Kernel`, `Library`, `Framework`, `Renderer`, `SDK`, `Service`, `Fork`, etc.) per [engine-architecture-taxonomy.md](../../references/engine-architecture-taxonomy.md). A UI shell or map renderer is never a full GIS analysis engine; ambiguous names like `UI.js` remain `unresolved` until source repo, version, and license are verified.
2. **Bilingual Intent & 21-Slot Extraction:** Parse Arabic (including Egyptian/regional colloquial) and English requests into the 21 architectural slots defined in [engine-selection-request.schema.json](../../schemas/engine-selection-request.schema.json) without unsafe silent assumptions.
3. **Existing Project Gate First:** Inspect the target workspace's existing shell, renderers, libraries, CRS logic, and tests before recommending replacement, addition, or cleanup (`build-vs-reuse`). Skip full architectural ceremony for trivial localized label/color edits.
4. **Offline-First 9-Step Discovery:** Run `scripts/discover_engines.py` over [project-catalog.json](../../references/project-catalog.json), [engine-capability-profiles.json](../../references/engine-capability-profiles.json), and [engine-capability-taxonomy.json](../../references/engine-capability-taxonomy.json). Never invent libraries; optional read-only GitHub metadata (`scripts/engine_repo_metadata.py`) stays `state: metadata-only`. Treat [external-agent-skills-registry.json](../../references/external-agent-skills-registry.json) strictly as quarantined `reference-only` until audited.
5. **Hard Gates & Per-Function Selection:** Run `scripts/compare_engines.py` using [engine-comparison-guide.md](../../references/engine-comparison-guide.md). Apply platform, license, security, capability, and `free_only` hard gates before weighted `0–5` scoring; treat `unknown` as `needs-evidence`, never `eligible`. Choose the best engine per function rather than forcing one engine everywhere.
6. **Multi-Engine Composition & Build Modes:** Select and combine from the 11 build modes (`extend-host`, `configure-host`, `source-fork`, `source-component-reuse`, `embedded-engine`, `ui-shell-migration`, `reference-inspired-ui`, `multi-engine-composition`, `worker-service`, `custom-component`, `custom-engine`) behind explicit contracts (`ui-engine-architecture-contract.md`) and [technology-compatibility.md](../../references/technology-compatibility.md).
7. **Open-Source Fork & Clean-Room Reference UI:** For `source-fork` (`KEEP/HIDE/DISABLE/REMOVE/REPLACE/DEFER`), inventory Qt UI declarations via `scripts/inventory_ui_actions.py`, hand off native QGIS integration to [QGIS Engine Integration](../qgis-engine-integration/SKILL.md) and command auditing to [UI Command Audit](../gis-ui-command-audit/SKILL.md). For behavioral inspiration (`ArcGIS Pro`, `Google Earth Pro`), delegate Clean-Room design to [Clean-Room Reference Implementation](../clean-room-reference-implementation/SKILL.md) with zero copied vendor binaries, DAML, or icons.
8. **ADR Gate & Free-First Separation:** Custom components require an approved Architecture Decision Record ([ARCHITECTURE_DECISION_RECORD.md](../../templates/ARCHITECTURE_DECISION_RECORD.md)) proving why reuse failed (`build-vs-reuse-policy.md`). Separate developer build dependencies from end-user runtime requirements; never auto-install heavy SDKs without user approval.

**Out of Scope:** Do not replace `gis-development` routing, write host-specific plugin/app code owned by Web/Mobile/Desktop/QGIS/ArcGIS specialists, grant install/network permissions owned by Security Guardian, or report `T0/T1` architectural output as `T2–T4` native runtime proof.

## Standard Workflow & CLI Helpers

1. Validate profile registry health (optional sanity check): `python scripts/validate_engine_profiles.py`.
2. Discover candidates bilingually: `python scripts/discover_engines.py --query "<AR/EN goal>" --platform <os> --format json`.
3. Evaluate candidates through hard gates & weights: `python scripts/compare_engines.py --request <request.json> --format json`.
4. Emit 10-part stack recommendation & setup separation: `python scripts/recommend_stack.py --request <request.json> --format markdown`.
5. For Qt `.ui` fork cleanup, inspect declarations safely: `python scripts/inventory_ui_actions.py --root <src_ui_dir> --format json`.
6. Delegate snippet/cookbook lookup to [GIS Code Discovery](../gis-code-discovery/SKILL.md) (`scripts/gis_code_discovery.py`) and record outputs using:
   - [TECHNOLOGY_SELECTION_REPORT.md](../../templates/TECHNOLOGY_SELECTION_REPORT.md) · [ENGINE_EVALUATION_REPORT.md](../../templates/ENGINE_EVALUATION_REPORT.md)
   - [SOURCE_FORK_FEATURE_INVENTORY.md](../../templates/SOURCE_FORK_FEATURE_INVENTORY.md) · [REFERENCE_UI_COMMAND_MAPPING.md](../../templates/REFERENCE_UI_COMMAND_MAPPING.md)
   - [engine-selection-report.schema.json](../../schemas/engine-selection-report.schema.json) · [ui-engine-architecture-contract.md](../../references/ui-engine-architecture-contract.md)
