# Mobile GIS Engineering Guide (`M01–M10`, `MOB-01..MOB-20`)

> Arabic summary companion: [`docs/WEB_MOBILE_GUIDE.ar.md`](WEB_MOBILE_GUIDE.ar.md).

> Companion engineering handbook to [`skills/gis-mobile-application-development/SKILL.md`](../skills/gis-mobile-application-development/SKILL.md) and [`examples/mobile-gis/README.md`](../examples/mobile-gis/README.md).

## 1. Platform Selection & Architecture (`M01–M10`, `REQ-WM-007`)

- **Strict Platform Boundaries:** `PWA != Native`, `WebView != Native Tested`, and **`Expo Go` cannot replace an `Expo Dev Build`** when native `MapLibre` or background GNSS is needed.
- **Native Android (`MOB-01`):** Prefer `Kotlin + Jetpack Compose + MapLibre Native Android + Room/SQLite WAL` for direct access to `LocationManager`/`GnssMeasurements`, BLE/USB RTK, `CameraX`, and `Android Keystore`.
- **Native iOS (`MOB-02`):** Prefer `SwiftUI + MapLibre Native/MapKit + CoreLocation + GRDB/SQLite + Keychain + PrivacyInfo.xcprivacy`. **Never mark iOS `MOB-QA-02` as `PASS` on Windows or Linux — macOS + Xcode + Apple signing are mandatory.**
- **Cross-Platform (`MOB-03..05`):**
  - Use official Flutter `maplibre` (`maplibre-flutter-maplibre`), **not** unmaintained legacy `maplibre_gl` (`REQ-WM-018`).
  - Use `KMP` (`commonMain` shared 15-field SQLite sync + CRS domain) for shared Kotlin domain logic paired with native Compose/SwiftUI canvases.
- **Standalone vs QGIS Mobile (`MOB-07`):** Evaluate `QField` / `Mergin Maps` for desktop QGIS symbology/form parity after verifying `GPLv2+` licensing and native mobile Qt builds.

## 2. Offline Durability, GNSS Provenance & Security Rules

- **15-Field Sync & Zero Blind LWW (`REQ-WM-026`, `REQ-WM-042`):** Every vector mutation must persist atomically to local SQLite before UI confirmation using `project_id, layer_id, feature_id, op_id, base_revision, geometry, attributes, crs, client_timestamp, server_timestamp, device_id, attachment_manifest, deletion_tombstone, checksum, sync_state`. Conflicts preserve both versions cleanly.
- **OSM Bulk Scrape Ban (`MOB-QA-20`):** Never download or cache tiles from `tile.openstreetmap.org` for offline packs; bundle permitted self-hosted `PMTiles`/`MBTiles` with visible attribution.
- **GNSS, Z Datum & Photos (`GIS-015`, `MOB-QA-04, 05, 10`):** Distinguish `ellipsoidal_wgs84` vs `orthometric_egm2008`, track `fix_age_s` / `is_mock`, reject false cm claims unless `RTK_FIXED` with checkpoint verification, keep `deny`/`ask_later` manual coordinate capture usable, and strip EXIF GPS tags from field photos by default (`strip_exif_gps=True`).
- **Arabic RTL & Accessibility (`MOB-QA-14`):** Mirror RTL labels cleanly while wrapping lat/lon/accuracy numbers in Unicode LTR isolates (`\u2066...\u2069`) and meeting `>=48dp` Android / `>=44pt` iOS touch targets.

## 3. T0–T1 Offline Verification Commands & Host Honesty Gate

```bash
python -B -m unittest tests.test_gis_mobile_application tests.test_gis_mobile_device_evidence tests.test_mobile_gis_expansion -v
python -B examples/mobile-gis/templates/MOB-08/run_gnss_logger_contract.py
python -B scripts/validate_mobile_device_evidence.py examples/mobile-gis/device-acceptance.example.json
```

> **Verification Boundary:** Above commands prove **`T0/T1`** durable SQLite outbox persistence, schema v1→v2 migration, GNSS provenance logic, EXIF stripping, and atomic GeoJSON/GPX export readback. Native Android Gradle builds (`MOB-QA-01`), iOS macOS/Xcode builds (`MOB-QA-02`), physical GNSS/BLE/Camera runs (`MOB-QA-05, 10`), and signed store releases (`MOB-QA-17, 19`) remain **`NOT_RUN`** whenever target SDKs or handsets are absent.
