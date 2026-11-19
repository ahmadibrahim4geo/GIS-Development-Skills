# Shared visualization example

This example explains the **declared** GIS skill routing and optional Archify handoff. It is independently authored from this pack's documented responsibilities. It is not a live agent trace, native GIS test or measured runtime architecture.

- [Specialist](../../skills/gis-architecture-visualization/SKILL.md)
- [Invocation, dependency and delivery guide](../../references/archify-integration.md)
- [Draft plan](plan.example.json)
- [Editable Archify workflow](skill-routing.workflow.json)
- [Generated interactive HTML](skill-routing.html)
- [Actual integration verification report](../../docs/ARCHIFY_INTEGRATION_2026-10-27.md)

Run the offline planning preview from the repository root:

```bash
python scripts/intent_router.py --plan examples/architecture-visualization/plan.example.json --workflow --format json
```

The plan is intentionally unapproved. `--gate` must block it. The preview selects a diagram owner and carries explicit purpose/type/evidence/language; it never starts a tool or grants access.

To render the workflow, the host discovers the reviewed external Archify runtime and Node.js, then invokes `finalize` as described in the integration guide. Keep its real output/check receipts together. Viewer inspection is separate from artifact validation and from actual GIS execution. Upstream's Apache-2.0/component notices must remain embedded in generated HTML.

No spatial data is read or written. CRS, coordinates, units and source datasets are not applicable to this abstract roles/command workflow. Preserve original files; use new output locations and host-authorized installation/network scope.

Evidence levels: the plan/router regression suite is offline T0/T1; an actual Archify render/browser run is diagram evidence only. Native GIS T2–T4 tests are **NOT RUN / not applicable** to this documentation example. Inspect the integration report for the checks actually performed on the published example.

Observed example status: schema/layout, delivery and strict artifact checks **PASS**; browser/visual acceptance **PARTIAL**, because the browser check was skipped (Chrome/Chromium unavailable). The HTML is generated but has not been interactively inspected here.

## Proposed QGIS ribbon and UI/engine flow

The separate [QGIS ribbon draft plan](qgis-ribbon.plan.json) and [renderer-independent flow](qgis-ribbon.flow.json) demonstrate architectural intake for a QGIS-hosted UI reorganization. The [UI/engine architecture contract](../../references/ui-engine-architecture-contract.md) separates source/target host, UI shell, map renderer and GIS engine. Archify consumes the flow reference as explanatory input after conversion to its actual installed schema; the flow is not an Archify candidate or executable workflow.

Run the offline checks from the repository root:

```bash
python scripts/intent_router.py --plan examples/architecture-visualization/qgis-ribbon.plan.json --workflow --format json
python scripts/validate_architecture_flow.py examples/architecture-visualization/qgis-ribbon.flow.json
```

The draft is intentionally unapproved, target component identities remain unresolved, and the native command inventory is missing. `--gate` must reject it. The compiled design retains its architecture and marks the missing preflight; it does not authorize implementation. The illustrative `source_commands: ["sample.buffer"]` covers one proposed vertical slice, not the complete QGIS command inventory. Exact mapping coverage checks compare declared IDs only; review actual actions before claiming full parity.

The flow includes forward request, result/error return, UI/map state, progress/cancellation, thread ownership and recovery contracts. Source data stays read-only, outputs are new, CRS/distance units must be validated, and project persistence is outside this example. Unsupported threading, cancellation or ribbon integration must be resolved against the actual QGIS/Qt/provider APIs before implementation. UI.js remains a separate unresolved identity if a user requests it; this QGIS example neither identifies nor installs such a package.

Evidence for this example is **T0/T1 only**: declaration validation and offline regression checks. Native QGIS T2–T4 and Archify rendering/browser inspection are **NOT RUN**. No generated HTML or native receipt is supplied for this proposed flow. The historical render status of the abstract responsibilities example above does not apply to it.
