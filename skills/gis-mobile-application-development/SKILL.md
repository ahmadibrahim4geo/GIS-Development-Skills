---
name: gis-mobile-application-development
description: Plan, engineer, validate and release genuine offline-first Android and iOS GIS field applications with GNSS, spatial data, secure sign-in, synchronization, touch UX and real-device verification.
license: MIT
compatibility: Cross-platform engineering guidance; Android/iOS builds and permissions require SDKs, simulators or physical devices. Documentation and offline fixtures do not prove native behavior.
---

# GIS Mobile Application Development

**Use this specialist for native or cross-platform mobile GIS applications** (Android, iOS, tablets, rugged field devices). A responsive website, a desktop WebView, an APK screenshot or a static map mockup is not a completed mobile GIS application. An existing field app (QField/Mergin Maps) is a reference, not a preinstalled engine.

## Mandatory route and ownership

Follow [Prompt Intent Orchestrator](../prompt-intent-orchestrator/SKILL.md) -> [GIS Development Router](../gis-development/SKILL.md) -> this mobile specialist. Apply [repository orchestration contract](../../references/repository-wide-skill-orchestration.md), [GIS Security Guardian](../gis-security-guardian/SKILL.md), and the [free-first policy](../../references/free-first-policy.md) at preflight, implementation and release. Only approved work may execute; reading this document grants no device privileges.

| Responsibility | Owner and handoff |
| --- | --- |
| Mobile application navigation, lifecycle, packaging and platform integration | This specialist |
| Spatial CRS, datum and units | [Coordinate Reference Systems](../coordinate-reference-systems/SKILL.md) |
| Vector/raster operations, deterministic GIS outputs | [Geospatial Data Processing](../geospatial-data-processing/SKILL.md) |
| KML/KMZ import/export, original symbology and safe archives | [KML/KMZ Engineering](../kml-kmz-engineering/SKILL.md) |
| Renderers, vector tiles, terrain and WebView caveats | [Geospatial Web Mapping](../geospatial-web-mapping/SKILL.md), remembering `PWA != Native` |
| Framework / SDK comparison (`M01–M10`, 12×10 matrix) | [Geospatial Engine Selection](../geospatial-engine-selection/SKILL.md) + [`mobile-gis-stack-decision.md`](../../references/mobile-gis-stack-decision.md) |
| GNSS/time semantics, RTK & Z datum provenance | [GIS Device Context](../gis-device-context/SKILL.md) + [`mobile-gis-device-gnss-rtk.md`](../../references/mobile-gis-device-gnss-rtk.md) |
| OS permission and sensor adapters | [System Capabilities and Permissions](../system-capabilities-and-permissions/SKILL.md) |
| Authentication threat model and protected secrets | [GIS Security Guardian](../gis-security-guardian/SKILL.md) + [`web-mobile-vendor-license-audit.md`](../../references/web-mobile-vendor-license-audit.md) |
| Touch UX (`48dp`/`44pt`), Arabic RTL + LTR coords & A11y | [GIS UI/UX](../gis-ui-ux-design-testing/SKILL.md), [GIS Arabic i18n](../gis-internationalization-arabic/SKILL.md), [`web-mobile-testing-release-guide.md`](../../references/web-mobile-testing-release-guide.md) |
| Import -> map -> edit -> queue -> sync -> export trace | [GIS Data Flow Diagnostics](../gis-data-flow-diagnostics/SKILL.md) |
| Source-code upstream catalog | [GIS Software Registry](../../references/gis-software-source-registry.md); do not duplicate it |

Never route mobile work to Desktop E2E/Windows UIA, never treat `WebView`/`Expo Go` as tested native GIS, and **strictly block `iOS` PASS on Windows/Linux without macOS + Xcode**.

## Architecture selection (`M01–M10`, `20` frameworks, `21` map SDKs)

Use [mobile architecture guide](../../references/mobile-gis-architecture.md) (12-component model & 19 benchmark apps), [platform selection](../../references/mobile-gis-platform-selection.md), and [12×10 decision matrix](../../references/mobile-gis-stack-decision.md):
- **Native Android / iOS:** Kotlin + Compose + MapLibre Native; SwiftUI + MapLibre/MapKit (`macOS/Xcode` required).
- **Cross-platform:** Flutter (use official `maplibre` `maplibre-flutter-maplibre`, not legacy `maplibre_gl`), React Native / Expo Dev Build (BG location PoC), `KMP` (`commonMain` SQLDelight/Sync), `.NET MAUI` (`Mapsui`), or Capacitor with GPU/memory bounds.
- **QGIS mobile & GeoAI:** Evaluate `QField` / `Mergin Maps` via [QGIS Engine Integration](../qgis-engine-integration/SKILL.md) under `GPL` and native Qt checks; pair [GeoAI options](../../references/web-mobile-geoai-options.md) with metric CRS & confirmation. Never prefetch bulk tiles from `tile.openstreetmap.org`.

## End-to-end mobile GIS contract

1. **Open/create project:** show local workspace, stable IDs, schema/CRS, layers, provenance, file permissions and dataset version. Do not silently upload user data.
2. **Map and data:** pan/zoom/rotate/identify/select/edit point-line-polygon, read supported GeoPackage/GeoJSON/GPX/KML/KMZ and raster/tile sources. Explicitly declare per-driver read/write limits and unsupported styles. Preserve feature IDs, timestamps, original CRS and UTF-8 Arabic attributes through round-trip tests.
3. **GNSS:** foreground consent; show horizontal accuracy, fix time, coordinate system, altitude source and stale status; record manual or external GNSS provenance separately. Background tracking needs a second explicit platform policy review.
4. **Field forms:** validation, required fields, media links, attachments, transaction rollback, undo, crash recovery and image EXIF/location minimization. Never let photo capture, microphone or location be a prerequisite unless the actual workflow needs it.
5. **Offline-first:** local durable transactions (8 storage resilience layers), download scope, storage estimates, basemap license/attribution, data version, 15-field outbox (`project_id..sync_state`, no blind `LWW`) before remote acknowledgment. Follow [offline sync protocol](../../references/mobile-gis-offline-sync.md) and [shared 15-field contract](../../references/web-mobile-offline-sync-contract.md).
6. **Sign-in and session:** allow local-only guest use where appropriate; distinguish offline unlocked state from online authenticated state; never claim login succeeded without server verification. Follow [sign-in and privacy contract](../../references/mobile-gis-authentication.md).
7. **Sync:** explicit upload/download triggers or documented background policy; immutable operation IDs, retries, idempotency, conflict detection, partial failure, permission-denied and logged-out handling. Avoid last-write-wins without an approved conflict rule.
8. **Export/share:** atomic local export, independent readback, retention of geometry, CRS, fields and eligible symbology/attachments, provenance, user-chosen share intent and safe filename/path handling.
9. **UI/UX:** `48dp`/`44pt` touch targets, safe area, orientation, tablet layout, accessibility, localization RTL + LTR isolated coordinates, focus and keyboard, network/offline status, storage and battery controls, system font scale and high-contrast.
10. **Privacy/security:** least privileges, no secret in repo/logs/project/KML, OS keychain/keystore, TLS, validated deep links, scoped storage, secure backup and deletion. No automatic geographic telemetry or plaintext tokens.

## Native acceptance and release gates

Read [mobile device testing matrix](../../references/mobile-gis-device-test-matrix.md) and [testing/signing guide](../../references/web-mobile-testing-release-guide.md). T0 checks contracts and links (`MOB-01..MOB-20`); T1 uses deterministic offline permission/sync/auth SQLite fixtures; T2 tests real GIS file readback and adapters; T3 uses Android emulator/device plus iOS simulator/device (`macOS/Xcode` required) with real map, permissions and lifecycle interaction; T4 signs, installs, launches, updates and uninstalls packages (`AAB` vs `IPA`) with release evidence. Mark unavailable native gates **NOT RUN**, never PASS.

An [offline contract example + `MOB-01..20`](../../examples/mobile-gis/README.md), [English Mobile Guide](../../docs/MOBILE_GIS_GUIDE.md), [Arabic Web/Mobile Guide](../../docs/WEB_MOBILE_GUIDE.ar.md), [scientific GIS invariants](../../references/agent-reasoning/scientific-gis-reasoning.md), and [mobile regression tests](../../tests/test_gis_mobile_application.py) prove only reference policy and deterministic SQLite/sync semantics, **not** that an Android/iOS binary or device driver has been built.

## Visual assets (conditional)

When the reviewed project needs thumbnails, official logos, photographs, illustrations or screenshots, compose [Visual Asset Discovery & Integration](../visual-asset-discovery-integration/SKILL.md). It owns internet/source discovery, asset suitability, source credits and prepared local variants; keep layout, target resource binding, packaging and actual UI acceptance with this platform/UX owner. Do not silently replace requested images with generic icons or claim a source URL proves local integration.
