# UI and GIS engine architecture contract

Use this contract through [Intent intake](../skills/prompt-intent-orchestrator/SKILL.md) and the [GIS router](../skills/gis-development/SKILL.md) for ribbon/tool reorganization, UI shell migration, or a new UI/engine boundary. Preserve the user's architectural goal before choosing skills or libraries. It complements the [UI command/data quality contract](gis-ui-quality-coordination.md) and [Archify handoff](archify-integration.md); it does not grant execution permissions.

## Decide what changes and what remains

Record source host, target host, UI framework, map renderer and GIS computation engine separately. Classify the requested change as `ui-reorganization`, `ui-shell-migration`, `engine-integration` or `engine-replacement`. A ribbon describes a command layout; it does not choose an engine. A named JavaScript library does not establish that the deliverable is a web map.

| Intended outcome | Architecture owner and boundary |
| --- | --- |
| Regroup existing actions inside QGIS | QGIS Plugin Development owns supported plugin integration; UI/UX designs groups and Command Audit inventories bindings/state. Determine whether supported APIs cover the requested scope. |
| Replace QGIS application chrome or alter core-only UI | QGIS Engine Integration evaluates source/fork feasibility with the platform owner; do not promise that a plugin can replace the complete QGIS shell. Review distribution, upgrade and GPL obligations. |
| Independent desktop shell using QGIS libraries | Desktop Development owns shell/packaging; QGIS Engine Integration owns QGIS embedding or a worker boundary. Distinguish in-process Qt integration from worker IPC or service deployment. |
| New JavaScript UI around an existing GIS renderer/engine | Target platform owner owns the shell/bridge. Keep the renderer and computation engine unless the reviewed request changes them. Add Web Mapping only for an actual map renderer requirement. |
| A different GIS engine | Treat as engine replacement with an explicit compatibility, license, data fidelity and native acceptance decision. A UI framework alone cannot satisfy this outcome. |

If the user names **UI.js**, discover its exact local project/package/repository, version, source and license. The spelling alone is ambiguous. Until verified, record it as unresolved, preserve the name supplied by the user, and propose no invented adapter, API, installation or replacement engine. Read-only project discovery and architecture drafting can continue. Dependent implementation waits for source/compatibility preflight; existing host authorization remains authoritative.

## Task architecture declaration

An optional `task.architecture` uses `schema_version: "1.0"` with these fields only. It is required by the host's architectural intake for these outcomes; the offline helper validates a declaration, not the semantic meaning of arbitrary prompts.

| Field | Contract |
| --- | --- |
| `change_type` | One of the four change types above. |
| `source_host`, `target_host` | Nonempty descriptions. Say unknown explicitly when not established; do not silently change the delivery target. |
| `ui_framework`, `renderer`, `gis_engine` | Each has `name`, `role`, `status`, `source_ref`, `version`. Roles are respectively `ui-shell`, `map-renderer`, `geospatial-engine`. |
| Component `status` | `unresolved` or `source-reviewed`. A proposed name is unresolved until the actual source/version is reviewed. `source-reviewed` requires a source reference and version; it does not assert runtime success. Unknown source/version may be `null` only for unresolved identities. |
| `integration_mode` | `in-process`, `worker-ipc`, `service`, or `unresolved`. This records a reviewed/proposed boundary rather than an available runtime claim. |
| `preserved_invariants` | Nonempty list of protected host, renderer, data, command, CRS/unit or license behavior. Distinguish user requirements from proposed design choices in the task description. |
| `command_inventory_ref`, `flow_spec_ref` | Local project-relative paths, or `null` while missing. No absolute paths, traversal, network resources or executable bindings. Resolve against the target project and inspect referenced contents. |

Unknown declaration fields fail validation. The compiler preserves the typed declaration rather than silently dropping it. Unresolved identities or required missing contracts prevent dependent execution readiness, not compilation of a reviewable draft. Even a fully source-reviewed declaration cannot authorize tools or prove native integration.

## Renderer-independent flow specification

Use a local JSON document with `schema_version: "1.0"`, `change_type`, optional descriptive `purpose`, `persistence_required`, `nodes`, `edges`, and `command_mappings`. UI migrations also require `source_commands`. This schema belongs to this repository. It is neither an executable workflow nor an external Archify schema. The [QGIS ribbon flow](../examples/architecture-visualization/qgis-ribbon.flow.json) is a proposed example. Check declared consistency with `python scripts/validate_architecture_flow.py <flow.json>`; the checker does not establish source truth or runtime behavior.

Each node has a unique `id` and nonempty `role`. Each edge has:

| Field | Required meaning |
| --- | --- |
| `id`, `from`, `to` | Stable unique edge ID and existing endpoint node IDs. |
| `kind` | `request`, `result`, `error`, `state`, `persist`, `readback`, `progress` or `cancel`. |
| `contract` | Nonempty schema/contract description or local reference: payload identity, validation, result/error/state semantics, CRS/units when relevant. Carry opaque dataset references instead of private coordinates or raw layers across serialization boundaries. |
| `execution`, `thread_owner` | `sync` or `async`, and an explicit owning thread/process. Do not pass a live Qt/QGIS object across a worker/JS boundary without verified support. |
| `command_id` | A mapped stable command ID, or `null` for an uncorrelated design edge. Proposed IDs must be labeled illustrative; never present them as discovered native IDs. |
| `evidence_basis`, `source_ref` | `proposed`, `source-reviewed` or `runtime-observed`. Reviewed/observed edges require an actual source/evidence reference; proposed edges may use `null`. An observed label alone is not proof. |

A request-bearing flow needs explicit result, error and state return paths. Inspect connectivity and command correlation, not merely the presence of three edge labels somewhere in the graph. Show validation/rejection at the boundary, enabled/checked state, selection/layer context, visible map change and error recovery where applicable. An abstract responsibilities diagram needs none of these GIS-specific fields.

Asynchronous edges also require `async_policy` with nonempty `progress`, `cancellation`, `error`, `recovery` descriptions. Model supported progress/cancel edges, or explicitly state unsupported behavior and its user-visible fallback. Record thread ownership, bounded work, stale/out-of-order results, cancellation completion and UI state restoration; never block the GUI while waiting on an unbounded worker. Supported APIs and threading rules must be reviewed in the actual target runtime before implementation.

If `persistence_required` is true, include `persist` and independent `readback` paths and the output identity/semantic checks. If false, state why persistence is outside this flow. Do not infer that project save/export works from a render or dialog.

## Before/after command parity

`ui-reorganization` and `ui-shell-migration` require nonempty `source_commands` and `command_mappings`. `source_commands` declares the in-scope inventory IDs; each ID must have exactly one mapping, with no duplicates or extra mapped IDs. Each mapping contains `command_id`, `before`, `after`, `handler`, `shortcut`, `enabled_state`, `checked_state`, `disposition` (`preserved` or `excluded`) and `reason` (string or `null`). Exclusions need a reviewed reason and `after: null`. Keep all in-scope commands accounted for, or mark the inventory incomplete. A conceptual sample must say which IDs and handlers are uninspected.

Inventory equality is a structural check over the declared IDs. It cannot detect a command omitted from both lists or attest that the declared inventory matches the actual host. Reconcile it against `command_inventory_ref` and the reviewed scope before claiming parity; an illustrative `source_commands` list is design metadata, not runtime evidence.

Preserve QAction/handler identity when supported, command availability, toggle state, shortcuts, active layer/selection context, error behavior and undo semantics. Update UI locator mappings when controls move. Before/after descriptions and an unchanged command name alone do not prove behavioral parity.

## Acceptance and evidence

- T0/T1: typed declaration/reference validation, graph integrity, command mappings, contract preservation through compilation, unresolved identities and denied approval paths. A lexical hint or valid JSON is not semantic understanding.
- T2: actual target engine/runtime, supported adapters and thread rules, fixture operations, errors/cancellation and independent GIS result checks.
- T3: real ribbon/keyboard interaction, context-sensitive enabled/checked behavior, progress/cancellation, visible map state and before/after command parity.
- T4 when distribution is in scope: packaging, launch on a clean supported environment, dependencies/licenses and project reopen/readback.

Report native evidence **NOT RUN** when unavailable. Archify schema/render/browser checks concern the diagram only. Apply [DoneProof](../skills/completion-evidence/SKILL.md), keep original data unchanged, and retain per-edge source/evidence references without secrets or invented trace IDs.

## Schema `v2.0` Extension (Backward Compatible with `v1.0`)

`v1.0` declarations remain **strictly unchanged** so existing fixtures (`examples/architecture-visualization/qgis-ribbon.flow.json`, `qgis-ribbon.plan.json`) and `scripts/validate_architecture_flow.py` continue to pass without modification.

For multi-engine composition, open-source fork cleanup (`KEEP / HIDE / DISABLE / REMOVE / REPLACE / DEFER`), or clean-room `reference-inspired-ui` workflows, use the additive `v2.0` contract defined in [architecture-v2.schema.json](../schemas/architecture-v2.schema.json):

- **Preserved `v1.0` guarantees:** `source_host`, `target_host`, `preserved_invariants`, `flow_spec_ref`, `command_mappings`, and strict `unresolved` blockers for unverified components (such as `UI.js`).
- **Additive `v2.0` declarations:** Multi-value `intent` array aligned with [engine-architecture-taxonomy.md](engine-architecture-taxonomy.md), `reference_products` (behavior reference metadata without implying code reuse), `source_base` (upstream repo, pinned ref, SPDX license when forked), structured `ui` (`framework`, `reference_reuse_mode`, `status`), typed `components[]` (per-component `project_id`, `role`, `integration_mode`, atomic `capabilities`, `license_evidence`, `runtime_evidence`, `dependency_refs`, `data_contract_ref`, `owner`), `capability_requirements`, `feature_inventory_ref`, `command_mapping_ref`, `license_policy`, and `decision_ref`.
- **`v1.0` to `v2.0` Migration Rule:** Never drop fields from `v1.0`; promote `ui_framework`, `renderer`, and `gis_engine` into typed entries inside `components[]` while retaining `source_host`, `target_host`, `preserved_invariants`, and `flow_spec_ref` identically. `unresolved` components continue to block execution readiness.

