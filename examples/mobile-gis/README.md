# Mobile GIS Offline/Sync Contract — Demonstration Fixture

This is a deliberately small **offline deterministic example**, not an Android or iOS app, map renderer, encrypted database, authentication server, geoprocessing engine, network synchronization client, or publishable package.

- Run from the repository root: python -m unittest tests.test_gis_mobile_application -v
- Verify truthful device evidence: python scripts/validate_mobile_device_evidence.py examples/mobile-gis/device-acceptance.example.json
- Modules:
  - `offline_sync_contract.py` (in-memory sync state-machine fixture)
  - `shared/mobile_field_core.py` (SQLite WAL durable store, 15-field `REQ-WM-042` outbox, v1→v2 migration, GNSS/RTK + `GIS-015` vertical datum, EXIF GPS strip, OSM scrape guard, atomic GeoJSON & GPX 1.1 export)
- Structured templates (`M01–M10`): `templates/MOB-01` .. `templates/MOB-20` (with 6-subfolder layout `fixtures/`, `spec/`, `tests/`, `evidence/`, `docs/`, `safety/` and representative scaffold slices in `MOB-01`, `MOB-02`, `MOB-03`, `MOB-08`).
- Tests: `tests/test_gis_mobile_application.py`, `tests/test_mobile_gis_expansion.py`, `tests/mobile-gis/`.
- Scope: immutable client operation IDs, revisions, deduplicated replay, server-side conflicts, and rejection of remote writes when disconnected or without verified authentication.
- No real Android/iOS APK/IPA binary, OAuth flow, macOS/Xcode build, physical GNSS receiver, or RTK checkpoint is exercised in workstation CI — inspect [MOBILE_GIS_GUIDE.md](../../docs/MOBILE_GIS_GUIDE.md).

For architecture, [read mobile architecture](../../references/mobile-gis-architecture.md), [platform selection](../../references/mobile-gis-platform-selection.md), [12×10 stack matrix](../../references/mobile-gis-stack-decision.md), [GNSS/RTK & sensors](../../references/mobile-gis-device-gnss-rtk.md), [offline data and sync](../../references/mobile-gis-offline-sync.md), [login/session privacy](../../references/mobile-gis-authentication.md), and the [device test matrix](../../references/mobile-gis-device-test-matrix.md). Follow the [mobile skill](../../skills/gis-mobile-application-development/SKILL.md).
