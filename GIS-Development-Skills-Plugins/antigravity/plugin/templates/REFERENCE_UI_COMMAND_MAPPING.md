# Clean-Room Reference UI Command Mapping

> Behavioral parity specification mapping a reference product's workflows (e.g., `ArcGIS Pro`, `Google Earth Pro`) to an original open-source UI shell and engine (`clean-room-reference-implementation`, `ui-engine-architecture-contract.md`). Zero proprietary DLLs, `.daml`, binary shaders, or trademarked icons may be copied.

- **Behavioral Reference Product(s):** *(Studied functionally only; no restricted assets reused)*
- **Target Original UI Framework & Shell:**
- **Target Underlying GIS Engine(s) & Adapters:**
- **Static Source Inventory Reference:** *(Output of `scripts/inventory_ui_actions.py` / `scripts/gis_ui_command_audit.py`)*

## Before / After Command Parity Table (`source_commands` ↔ `command_mappings`)

| `command_id` | Behavioral Source Group/Tab (`before`) | Clean-Room Target Surface (`after`) | Original Handler / Service (`handler_state`) | Shortcut | Enabled / Checked Context Rules | Disposition (`preserved` / `excluded`) | Rationale / Native Verification (`NOT RUN`) |
|---|---|---|---|---|---|---|---|
| | | | `unresolved` | | | | `NOT RUN` |

## Clean-Room & Compliance Checklist
- [ ] All icons, stylesheets, and ribbon definitions are original or properly licensed (`MIT` / `Apache-2.0` / Lucide / Fluent Icons) with attribution.
- [ ] Flow graph validates cleanly via `python scripts/validate_architecture_flow.py <flow.json>`.
- [ ] Async GIS operations specify cancellation, progress feedback, and error recovery without freezing the UI thread.
