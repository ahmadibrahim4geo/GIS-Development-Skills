# Web & Mobile Testing, Accessibility, Build-Signing & Release Guide

> Shared verification, UX accessibility (`REQ-WM-033`), signing/privacy (`REQ-WM-034`), and 16-tool QA handbook (`REQ-WM-048`) covering `Web_Mobile_r3 §16.2–§16.4 & §19.4`.

---

## 1. Nine-Stage Android vs iOS Build, Signing & Privacy Pipeline (`§16.3`, `REQ-WM-034`)

| Stage | Android Contract (`Google Play / Sideload`) | iOS / iPadOS Contract (`App Store / TestFlight`) |
|---|---|---|
| **1. Host Toolchain Gate** | JDK 17+, Android SDK/Build-Tools, Gradle wrapper (Win/Lin/Mac) | **macOS + Xcode + Apple SDK required** — NEVER mark `PASS` on Windows/Linux (`MOB-QA-02`) |
| **2. Manifest & Privacy** | `AndroidManifest.xml` least-privilege permissions + **Play Data Safety** form match | `Info.plist` usage descriptions (`WhenInUse`, `Camera`, `BT`) + **`PrivacyInfo.xcprivacy`** |
| **3. Secrets & Deep Links** | Verified `App Links` (`assetlinks.json`), Keystore-encrypted tokens only | `Associated Domains` (`apple-appsite-association`), Keychain-only tokens, PKCE browser flow |
| **4. License & SBOM Check** | Scan Gradle/CMake/NDK `.so` transitive licenses (`GPL` vs `MIT/Apache`) | Scan SwiftPM/CocoaPods/XCFramework transitive licenses & binary provenance |
| **5. Contract Tests (`T1–T2`)** | JVM JUnit + SQLite schema/outbox + GeoPackage readback | `XCTest` unit tests + SQLite/GRDB migration + GeoJSON/GPX readback |
| **6. UI & Lifecycle (`T3`)** | Emulator (`Espresso` / `Compose UI Test` / `UIAutomator`): deny GPS, rotate, process kill | Simulator (`XCUITest`): permission deny, rotation, low memory warnings |
| **7. Physical Hardware (`T3`)** | Real handset: physical GNSS, camera EXIF strip, BLE RTK, battery saver (`MOB-QA-05, 10, 16`) | Physical iPhone/iPad: real `CoreLocation`, camera, `ARKit GeoAnchor`, Keychain unlock |
| **8. Signed Release (`T4`)** | Release **`AAB`** (or APK) signed via upload key outside repo, SHA-256 recorded (`MOB-QA-17`) | Signed **`IPA`** via Apple certificate/provisioning in macOS Keychain -> TestFlight |
| **9. Upgrade & Uninstall (`T4`)** | `v1 -> v2` Room/GPKG migration intact; uninstall clears internal sandbox (`MOB-QA-12, 19`) | `v1 -> v2` CoreData/GRDB migration intact; uninstall purges Keychain/container items as documented |

**Web Delivery Security Parity (`§16.4`):** Always serve static maps safely behind relative `./` subpaths (`GitHub Pages`), enforce `CSP` (no inline unsanitized feature HTML), keep secret provider keys off client JS bundles (`WEB-QA-08`), and document `COOP`/`COEP` needs for multi-thread WASM OPFS (`REQ-WM-047`).

---

## 2. Touch UX, Arabic RTL + LTR Coordinates & Accessibility (`REQ-WM-033`, `MOB-QA-14`)

- **Minimum Touch Targets:** `≥ 48dp × 48dp` on Android and `≥ 44pt × 44pt` on iOS; honor OS safe areas (`WindowInsets`, notch, home indicator) and draggable bottom sheets for one-handed field entry.
- **Bilingual Arabic RTL Layout + LTR Numeric Isolation:** Mirror panels and form labels in `RTL` (`dir="rtl"` / `supportsRtl="true"`), while wrapping **coordinates (`30.0444, 31.2357`), EPSG codes (`EPSG:4326`), accuracy (`±3.2 m`), and timestamps (`2026-11-25T20:00Z`)** in `LTR` (`unicode-bidi: isolate; direction: ltr`).
- **Accessible Map Alternative (`WEB-QA-15` / `MOB-QA-14`):** Every interactive map screen must expose a keyboard-reachable / TalkBack / VoiceOver-navigable feature list & search table + state announcements (offline/syncing/conflict/stale GNSS) without relying solely on canvas gestures or color alone.

---

## 3. Sixteen-Tool QA & Verification Matrix (`§19.4`, `REQ-WM-048`)

| Domain | Curated Verification Tools (`T0–T4`) | Evidence Validator / Honesty Gate |
|---|---|---|
| **Web E2E & Accessibility** | `Playwright`, `Cypress`, `axe-core`, `Lighthouse` | Browser binary required -> else `NOT_RUN` |
| **Web Unit, API & Data Readback** | `Vitest`, `Jest`, Node `node:test`, `Newman`, `pytest`, Python/GDAL `ogr2ogr` | `T1`/`T2` local contracts (`tests/web-gis/`) |
| **Android Instrumented & Unit** | `JUnit`, `Espresso`, `UIAutomator`, `Compose UI Test` | Android SDK/Emulator/Device -> else `NOT_RUN` |
| **iOS Automated & Unit** | `XCTest`, `XCUITest` | **macOS + Xcode mandatory** -> else `NOT_RUN` |
| **Cross-Platform Mobile QA** | `flutter_test` (`integration_test`), `React Native Testing Library` (`RNTL`), `Maestro`, `Detox`, `Appium` | Separate Android & iOS PASS records in [validate_mobile_device_evidence.py](../scripts/validate_mobile_device_evidence.py) |
| **Security & Performance** | `OSV-Scanner`, `OWASP ZAP`, `Chrome DevTools`, `Android Profiler`, `Xcode Instruments` | External scans `NOT_RUN` unless actually executed |

**Truthful Reporting Rule:** Validate machine-readable mobile evidence with `python scripts/validate_mobile_device_evidence.py <report.json>` and `python scripts/validate_evidence.py <report.json>`; physical hardware checks (`MOB-03, 04, 06, 11, 15`) are rejected if marked `PASS` under `mode="ci-fixture"` or emulator/simulator.
