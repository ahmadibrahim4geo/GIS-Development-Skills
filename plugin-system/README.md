# GIS Development Skills — Plugin Lifecycle Engine (`plugin-system/`)

The `plugin-system/` subsystem builds, validates, packages, and locally synchronizes multi-platform GIS plugin packages from **one canonical repository** ([AGENTS.md](../AGENTS.md)) without duplicating skill sources or leaking private developer configuration.

## Core Design Rules

1. **Canonical Source First:** Never edit generated files under `GIS-Development-Skills-Plugins/`. Always update canonical files under `skills/`, `references/`, `schemas/`, `scripts/`, `templates/`, or root policies, then run the updater.
2. **Integrates Existing Bundle Builder:** Reuses [`scripts/build_skill_bundle.py`](../scripts/build_skill_bundle.py), [`scripts/validate_skill_pack.py`](../scripts/validate_skill_pack.py), [`scripts/audit_license_catalog.py`](../scripts/audit_license_catalog.py), and [`scripts/security_audit.py`](../scripts/security_audit.py).
3. **Config-Driven Extensibility:** New target platforms are declared in [`config/platforms.json`](config/platforms.json) with an adapter module implementing the 11-method contract — zero engine `if/else` chains required.
4. **Strict Public/Private Separation:** Developer hooks (`Update-All-Plugins.*`, `Update-My-Platforms.*`, `plugin-system/`, `reports/`, `plans/`) are excluded from end-user plugin archives. Owner settings live outside Git in `%LOCALAPPDATA%\GIS-Development-Skills\PluginSync\owner-config.json` (template at [`config/owner-config.example.json`](config/owner-config.example.json)).
5. **Approval-Gated Remote Actions:** Local builds never auto-publish (`autoOwnerRemoteUpdate: false`, `autoPublicPublish: false`).

## Directory Structure

| Path | Role |
|---|---|
| [`policy/DEVELOPMENT_LIFECYCLE.md`](policy/DEVELOPMENT_LIFECYCLE.md) | Standardized lifecycle rules, 22 status codes, secret incident protocol |
| [`config/platforms.json`](config/platforms.json) | Declarative platform registry (`portable` active in P02; 6 client adapters P09) |
| [`config/source-map.json`](config/source-map.json) | Canonical digest inputs, end-user bundle rules, and sensitive exclusions |
| [`config/plugin-sync.config.json`](config/plugin-sync.config.json) | Safe pipeline defaults and lock/retention timeouts |
| [`config/owner-config.example.json`](config/owner-config.example.json) | Secret-free owner config reference template |
| `schemas/` | JSON schemas for manifests, platform registry, sync reports, and lifecycle reports |
| `core/` | Inventory, SHA-256 hashing, validators, file lock, registry, parity, builder, CLI pipeline |
| `adapters/` | 11-method adapter contract (`portable` complete; 6 P09 client adapters prepared) |
| `sync/` | Secret-isolated local synchronization + N-version isolated per-platform rollback |
| `release/` | Release artifact staging (`-PrepareRelease`) + owner-gated `-Publish` guard |
| `hooks/` | Opt-in developer Git/agent hooks helper |
| `tests/` | Unit tests for P02/PL lifecycle invariants |

## CLI Usage & Exit Codes

From repository root:

```powershell
powershell -NoProfile -File .\Update-All-Plugins.ps1 -CheckOnly
powershell -NoProfile -File .\Update-All-Plugins.ps1 -BuildOnly
powershell -NoProfile -File .\Update-All-Plugins.ps1 -Status
powershell -NoProfile -File .\Update-All-Plugins.ps1 -Platform portable -BuildOnly
powershell -NoProfile -File .\Update-All-Plugins.ps1 -Rollback -Version 0.3.5 -Platform portable
powershell -NoProfile -File .\Update-My-Platforms.ps1 -Status
```

> **Windows ExecutionPolicy note:** Wrapper `.bat` scripts invoke `powershell -NoProfile -File ...` **without** `-ExecutionPolicy Bypass`. If Windows reports `Restricted` execution policy on your account, configure `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` or invoke `python -B plugin-system/core/pipeline.py` directly.

| Exit Code | Meaning |
|---|---|
| `0` | Success (`UP_TO_DATE`, `BUILT`, `PASSED`, `SYNCED_VERIFIED`, `ROLLED_BACK`) |
| `2` | Build, validation, license, or secret-scan failure |
| `3` | Partial local sync failure (failed platform rolled back cleanly) |
| `4` | External approval / manual portal action / authentication required (`-Publish` blocked without consent) |
| `5` | Concurrency project lock held or invalid configuration/platform argument |
