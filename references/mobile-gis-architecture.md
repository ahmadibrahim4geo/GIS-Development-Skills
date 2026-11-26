# Mobile GIS Architecture, Runtime and Engine Selection

**Scope:** Android and iOS field applications; not desktop-shell or responsive-web-only development. Entry point: [Mobile GIS skill](../skills/gis-mobile-application-development/SKILL.md). See the [canonical source catalog](project-catalog.json) and [source registry](gis-software-source-registry.md) for current upstream records.

## Choose independently

| Concern | Options to evaluate | Verification evidence |
| --- | --- | --- |
| OS and UI | Android Kotlin; iOS Swift; Qt/QGIS mobile; Flutter; .NET MAUI | Supported OS versions, build ABI, SDK license, actual device UI |
| 2D render | MapLibre Native, verified native framework, QGIS map canvas | Tiles, styles, offline fallback, projection, GPU, attribution |
| Editing and I/O | Version-matched QGIS/GDAL if deployable; suitable native spatial adapters | Real editable GeoPackage/GeoJSON/KML round-trip; transaction safety |
| CRS | PROJ or version-tested mobile CRS API | Known reference control points, axis order, datum grid availability |
| Storage | GeoPackage/SQLite, OS app sandbox, selected-file URI | WAL/transactions, schema migration, encrypted sensitive data, backup |
| Sensor | Android location services, Apple Core Location, supported external GNSS | Foreground/background permission state, accuracy/fix age, no spoofed live claim |
| Synchronization | API with idempotent outbox, content version and per-feature revisions | Offline/restart/retry/conflict and login expiry acceptance |
| Maps | Licensed self-hosted raster/vector packages or verified downloadable packages | Attribution, bounds, update rules, cache and redistribution rights |

A mobile map renderer alone is **not** a complete GIS engine. A source repository URL is **reference-only** until matching versions, licenses and native builds are independently verified. Evaluate [QField](https://github.com/opengisch/QField), [Mergin Maps](https://github.com/MerginMaps/mobile), [MapLibre Native](https://github.com/maplibre/maplibre-native), and [Mapsui](https://github.com/Mapsui/Mapsui) without assuming commercial cloud access or copying upstream trademark/assets. QGIS integration requires GPL and Qt/plugin/provider packaging review; desktop ABI proof does not prove mobile ABI compatibility.

## Component contract

- Project service: stable project ID, version, layer descriptors, CRS, geometry and field schema, attribution and migrations.
- Data service: import/probe/export/readback, sandboxed documents, explicit format fidelity and typed errors.
- Map service: camera, layers, selection and diagnostics; never silently change original imported KML/KMZ styling.
- Field service: validated forms, local transaction, attachment hash, editor identity and immutable client operation IDs.
- Device service: location permission, GNSS reading age/accuracy, pause/resume, battery/storage policy and precise denial fallback.
- Auth service: keychain/keystore, server verification, refresh and revoked/offline session transitions.
- Sync service: durable outbox, server revision comparison, conflict queue, retry with idempotency, no silent deletion.
- Release service: platform manifests, permission strings, signed package, clean-install/migration and third-party notices.

## Selection and proof

Before coding, record target API/minimum OS; device CPU/ABI; required GPS, camera, storage and BLE; expected maximum offline map size; CRS/vertical accuracy; scope of feature edits; login requirement; retention/deletion; map source rights; transitive licenses; and deployment channel. Build one independently verifiable vertical slice on each target OS. Never declare Android/iOS compatibility based on CI source checks alone.

---

## Ten Mobile Product Classes (`M01–M10`, `REQ-WM-007`) & 8-Layer Separation (`REQ-WM-008`)

Always distinguish **`PWA != Native`** and **`WebView != Native Tested`**:
`M01` Native Android (`Kotlin/Compose + MapLibre Native`), `M02` Native iOS (`SwiftUI + MapLibre/MapKit`, macOS/Xcode required), `M03` Cross-Platform Field Collector (`Flutter` official MapLibre / `RN` / `KMP`), `M04` Hybrid Bridge App (`Capacitor`), `M05` Offline Survey/Form Collector (`XLSForm`/`ODK`), `M06` Precision GNSS/RTK Survey (`BLE/USB NMEA/NTRIP`), `M07` Offline Navigation & Geofencing (`OSRM`/`Valhalla` packs), `M08` Mobile 3D/AR Field Viewer (`ARCore Geospatial` / `ARKit ARGeoAnchor`), `M09` Photo Asset & Inspection Logger (`CameraX`/`AVFoundation` + EXIF strip), and `M10` Enterprise Synchronized Field Suite (`QField`/`Mergin`/PostGIS sync).

Maintain strict **8-layer separation (`L1–L8`)** shared with [Web GIS Products Map](web-gis-products-map.md): `L1` Shell/Nav, `L2` Map Scene Adapter, `L3` GIS Domain Core, `L4` Data Access & Format Codecs, `L5` Offline Storage & Sync Queue, `L6` Security/Auth/Licensing Gate, `L7` Device Capabilities & GNSS/Sensors, and `L8` Diagnostics & QA.

---

## Standardized 12-Component Field GIS Architecture (`REQ-WM-019`)

1. **Project Home & Workspace Manager** *(UUID, local paths, dataset version, storage estimate)*
2. **Map Canvas Adapter** *(pan/zoom/rotate/identify, attribution overlay, zero business state in tiles)*
3. **Vector CRUD & Snapping Engine** *(point/line/polygon, undo/redo, topology validity check)*
4. **Dynamic Bilingual Forms** *(schema-driven validation, required/conditional fields, RTL UI + LTR numbers)*
5. **Provenanced Location Capture** *(foreground opt-in, horizontal/vertical accuracy, fix age, stale warning, mock flag)*
6. **Local Atomic Database** *(`SQLite`/WAL/`GeoPackage`/`Room`/`GRDB`, crash-safe writes & schema migrations)*
7. **Layer & Format Adapters** *(GeoJSON, GeoPackage, GPX, KML/KMZ, COG/MBTiles/PMTiles with readback)*
8. **Offline Map Manager** *(licensed region downloads only, quota checks, explicit OSM bulk-scrape ban)*
9. **Outbox Sync Engine** *(immutable `op_id`, 15-field contract, `base_revision` conflict queue, no blind `LWW`)*
10. **Security, Keystore/Keychain & Guest Mode** *(no secrets in APK/IPA, isolated `GUEST_LOCAL` vs `OFFLINE_UNLOCKED` vs `AUTHENTICATED`)*
11. **Safe Share & Independent Export** *(atomic file write, EXIF privacy stripping default, external readback)*
12. **Signed Release & Device Diagnostics** *(platform signing provenance, `NOT_RUN` honest reporting on missing SDKs/devices)*

---

## Nineteen Benchmark Mobile Field Applications (`REQ-WM-024`)

Consult upstream licenses and terms before reusing patterns or formats (full profiles in [project-catalog.json](project-catalog.json) & [platform selection guide](mobile-gis-platform-selection.md)):
`QField` (`GPL`), `Mergin Maps` (`GPL`), `Input (legacy/archived — prefer Mergin Maps)`, `ODK Collect`, `ODK Central`, `Enketo`, `KoboToolbox`, `OpenMapKit`, `OsmAnd`, `Organic Maps`, `CoMaps`, `StreetComplete`, `Every Door`, `Vespucci`, `MapSwipe`, `Transistorsoft Background Geolocation` *(commercial SDK license required; never treat as free open source)*, `ArcGIS Field Maps`, `ArcGIS Survey123`, and `ArcGIS QuickCapture` *(commercial Esri licensing required)*.

**Integrated 9-Step Mobile Field Reference Workflow (`examples/mobile-gis/`):**
`(1) Open/init local SQLite project -> (2) Load licensed offline vector layer -> (3) Check foreground location permission & GNSS provenance -> (4) Capture/edit feature + form attributes -> (5) Attach media w/ EXIF strip option -> (6) Persist atomically + enqueue 15-field outbox op -> (7) Survive simulated process death / reopen DB -> (8) Reconnect & resolve revision conflict cleanly (no blind LWW) -> (9) Export GeoJSON/GPX atomically for independent Python/GDAL readback.`

**See also:** [Mobile Platform Selection](mobile-gis-platform-selection.md) · [12×10 Stack Matrix](mobile-gis-stack-decision.md) · [GNSS, RTK & Sensors](mobile-gis-device-gnss-rtk.md) · [Testing & Release Guide](web-mobile-testing-release-guide.md) · [Geospatial Engine Selection](../skills/geospatial-engine-selection/SKILL.md).
