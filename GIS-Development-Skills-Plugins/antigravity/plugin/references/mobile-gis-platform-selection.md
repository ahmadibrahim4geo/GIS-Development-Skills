# Mobile GIS Platform Selection: 20 Frameworks, 21 Map SDKs & Native Deep Dives

> Reference manual for [`gis-mobile-application-development`](../skills/gis-mobile-application-development/SKILL.md) (`REQ-WM-007`, `017`, `018`, `020`, `021`, `022`). Pair with [`mobile-gis-stack-decision.md`](mobile-gis-stack-decision.md) and [`scripts/recommend_stack.py`](../scripts/recommend_stack.py).

---

## 1. Twenty Mobile Frameworks & Approaches (`§7.1`, `REQ-WM-017`)

1. **Kotlin + Jetpack Compose** *(primary open Android choice — declarative Material 3 UI, strong lifecycle & Room integration)*
2. **Kotlin Coroutines + StateFlow** *(structured concurrency for non-blocking GeoPackage/SQLite I/O and GNSS streams)*
3. **Java Android (Legacy View/XML)** *(maintenance only for existing enterprise APKs; avoid for greenfield UI)*
4. **Swift + SwiftUI** *(primary open iOS/iPadOS UI — native dark/RTL, PhotosUI, CoreLocation)*
5. **UIKit Interop (`UIViewRepresentable`)** *(needed on iOS for imperative C++/Metal map canvases like MapLibre Native)*
6. **Flutter + Dart** *(strong shared Android/iOS canvas; verify official MapLibre bindings & native method channels)*
7. **React Native (Bare / Fabric)** *(TypeScript ecosystem; requires native bridging for heavy spatial DB/BT serial)*
8. **Expo Dev Build (`expo prebuild`)** *(mandatory over `Expo Go` for custom native MapLibre & background location modules)*
9. **Kotlin Multiplatform (`KMP`)** *(shared `commonMain` domain/SQLDelight/sync with `androidMain` + `iosMain` native UIs)*
10. **Compose Multiplatform (`CMP`)** *(shared Kotlin UI on Android + experimental/skia iOS; test map view interop carefully)*
11. **Capacitor (Hybrid Web-Native Bridge)** *(good for form-heavy hybrid apps; isolate WebGL memory & large offline raster limits)*
12. **Ionic + Capacitor** *(UI toolkit over Capacitor; enforce `48dp`/`44pt` touch targets & hardware limits)*
13. **`.NET MAUI` (`C#` + `Mapsui`)** *(viable for C# teams sharing GIS domain logic with Windows WPF studios)*
14. **Qt / QML (`QField` / `Mergin` pattern)** *(QGIS Core desktop parity on mobile — triggers `GPLv2+` & heavy mobile Qt build gates)*
15. **NativeScript** *(secondary JS-to-native runtime; smaller mobile GIS plugin ecosystem)*
16. **Android `WebView` Shell** *(NEVER market or test as native Android GIS — lacks native background GNSS resilience)*
17. **iOS `WKWebView` Shell** *(subject to ~7-day idle cache eviction & WebGL teardown under memory pressure)*
18. **Trusted Web Activity (`TWA`)** *(Play Store wrapper around an HTTPS PWA — inherits browser quotas)*
19. **Installable Mobile PWA** *(browser runtime only; `PWA != Native` — document background GPS & file API limits)*
20. **Embedded C++/Rust Core via JNI + Swift C-Interop** *(high-throughput spatial indexing/PROJ/SQLite kernel shared cleanly across Kotlin & Swift)*

---

## 2. Twenty-One Mobile Map SDKs (`§7.2`, `REQ-WM-018`)

- **Open-Source / Self-Hostable Renderers:**
  1. **MapLibre Native Android** (`maplibre-maplibre-native`) · 2. **MapLibre Native iOS** · 3. **MapLibre Compose** (Android / KMP `maplibre-compose`) · 4. **Official Flutter `maplibre`** (`maplibre-flutter-maplibre` — **distinct from unmaintained legacy `maplibre_gl`**) · 5. **Legacy `maplibre_gl` (Flutter)** *(warn before adoption; verify maintenance fork)* · 6. **MapLibre React Native** (`@maplibre/maplibre-react-native`, `maplibre-maplibre-react-native`) · 7. **`flutter_map`** (`fleaflet-flutter-map`) · 8. **`vector_map_tiles`** (`greensopinion-flutter-vector-map-tiles`) · 9. **`osmdroid`** (`osmdroid-osmdroid` Android Java/Kotlin) · 10. **`Mapsforge`** (`mapsforge-mapsforge` offline binary vector maps) · 11. **`Mapsui`** (`mapsui-mapsui` `.NET MAUI`/Android/iOS) · 12. **Qt / QGIS Mobile Canvas** (`opengisch-qfield`, `merginmaps-mobile` — `GPL`).
- **Platform Native / Commercial / Key-Gated SDKs (`REQ-WM-029` license check required):**
  13. **Apple `MapKit` / SwiftUI `Map`** *(iOS-only, Apple ecosystem lock-in, no Android parity)* · 14. **Google Maps Android SDK + Compose** (`googlemaps-android-maps-compose`) · 15. **Google Maps iOS SDK** *(Google billing/ToS + Play Services dependencies)* · 16. **Mapbox Maps SDK Android** (`mapbox-mapbox-maps-android`) · 17. **Mapbox Maps SDK iOS** (`mapbox-mapbox-maps-ios`) · 18. **Mapbox Maps Flutter** · 19. **ArcGIS Maps SDK for Kotlin** (`esri-arcgis-maps-sdk-kotlin-samples`) · 20. **ArcGIS Maps SDK for Swift** (`esri-arcgis-maps-sdk-swift-samples`) · 21. **ArcGIS Maps SDK for Flutter / Qt / `.NET`** (`esri-arcgis-maps-sdk-flutter-samples` — commercial runtime/deployment license required).

---

## 3. Native Android Stack & 13 OS/Hardware Edge Cases (`REQ-WM-020`)

- **18 Core Android Building Blocks:** `Kotlin`, `Jetpack Compose`, `Room` (`SQLite`/WAL), `GeoPackage Android` / native C++ SQLite, `WorkManager`, `Preferences/Proto DataStore`, `CameraX`, Storage Access Framework (`SAF`), `LocationManager`, `FusedLocationProviderClient`, `GnssMeasurements` (Raw GNSS), `BluetoothLeScanner` (`BLE` GATT), `UsbManager` (USB-C OTG Serial), `SensorManager`, `Android Keystore`, `App Links` (Digital Asset Links), `Baseline Profiles`, `Android Emulator + Gradle AAB`.
- **13 Mandatory Android Edge Cases (`MOB-QA-01, 03, 07, 11, 16`):**
  1. Mock/spoofed GPS providers (`isMock()` / Developer Options flagged visibly) · 2. Process death while form/edit sheet open (`SavedStateHandle` + disk draft) · 3. Doze & Battery Saver adaptive GNSS throttling · 4. Missing Google Play Services (AOSP/de-Googled devices falling back to `LocationManager`) · 5. Approximate vs Precise location downgrade (`ACCESS_COARSE_LOCATION` only) · 6. Android 10–14+ Background Location + `FOREGROUND_SERVICE_LOCATION` notification · 7. Scoped Storage / `SAF` document URI permission expiry after reboot · 8. ABI mismatch (`arm64-v8a` vs `armeabi-v7a` vs emulator `x86_64` JNI `.so` load failure) · 9. Configuration change / foldable multi-window resize preserving map state · 10. Low storage `< 5%` pre-check blocking partial tile corruptions (`MOB-QA-09`) · 11. SQLite upgrade migration v1->v2 under crash recovery (`MOB-QA-12`) · 12. OEM aggressive background kill (Samsung/Xiaomi/Huawei warning UX) · 13. Arabic RTL mirroring (`supportsRtl`) keeping lat/lon numeric badges strictly `LTR`.

---

## 4. Native iOS/iPadOS Stack & Strict macOS/Xcode Gate (`REQ-WM-021`)

> [!CAUTION]
> **Windows / Linux Build Block (`MOB-QA-02`):** iOS compilation, `Xcode` archiving, `codesign`, `Provisioning Profiles`, `PrivacyInfo.xcprivacy`, `XCTest/XCUITest`, and `TestFlight` submission **CANNOT execute or be marked `PASS` on Windows or Linux**. Mark `MOB-QA-02` and iOS device checks strictly **`NOT_RUN`** unless executed on an actual macOS + Xcode runner / physical iOS device.

- **16 Core iOS/iPadOS Building Blocks:** `Swift 5/6`, `SwiftUI`, `MapKit` / `MapLibre Native`, `CoreLocation`, `CoreMotion`, `CoreBluetooth`, `AVFoundation`, `PhotosUI`, `UIDocumentPickerViewController`, `SwiftData` / `SQLite` / `GRDB.swift` / `GeoPackage`, Apple `Keychain Services`, `BGTaskScheduler` (`BackgroundTasks`), `ARKit` `ARGeoAnchor` (`GeoTracking`), `Xcode` + `XCTest/XCUITest`, `TestFlight`, `App Store Connect` (`PrivacyInfo.xcprivacy` + purpose strings `NSLocationWhenInUseUsageDescription`, `NSCameraUsageDescription`, `NSBluetoothAlwaysUsageDescription`).

---

## 5. Flutter, React Native / Expo, KMP & Capacitor Profiles (`REQ-WM-022`)

- **Flutter (`23` Curated Ecosystem Packages + PoC Gate):** Distinguish official `maplibre` (`maplibre-flutter-maplibre`) vs legacy `maplibre_gl`; pair `flutter_map`/`vector_map_tiles` for lightweight overlays, `geolocator` + explicit Android/iOS permission strings via `permission_handler`, `drift`/`sqflite`/`sqlite3_flutter_libs`, `flutter_secure_storage` (Keystore/Keychain), `camera`/`image_picker` (with EXIF scrub), `file_picker`, `connectivity_plus`, `flutter_blue_plus` (BLE GNSS), `proj4dart`, `flutter_localizations`/`intl`, `integration_test`/`flutter_test`. **Gate:** Run platform checks separately on Android and macOS/iOS (`flutter test` alone is T1/T2 UI widget logic, NOT native GPS verification).
- **React Native & Expo (`13` Key Packages + Mandatory Expo Dev Build Gate):** `@maplibre/maplibre-react-native`, `expo-location` (with foreground-service task config), `react-native-gesture-handler`, `react-native-reanimated`, `expo-sqlite` / `op-sqlite`, `expo-secure-store`, `expo-camera`, `expo-document-picker` / `expo-file-system`, `@react-native-community/netinfo`, `react-native-ble-plx`, `@testing-library/react-native` (`RNTL`), `Maestro` / `Detox`. **Mandatory Gate:** **`Expo Go` is insufficient** for production mobile GIS — always run an **`Expo Dev Build`** (`npx expo prebuild` / `eas build --profile development`) to verify background location, MapLibre native views, and Keystore/Keychain integration.
- **Kotlin Multiplatform (`KMP`):** Split strictly into `commonMain` (`SQLDelight`, `Ktor` client, CRS/sync 15-field engine, tests) + `androidMain` (`MapLibre Compose` / `Room` / `LocationManager`) + `iosMain` (`MapLibre iOS` / `CoreLocation` / `Keychain`).
- **Capacitor Hybrid:** Wrap UI in `WebView`/`WKWebView` ONLY for form-first workflows; cap GeoJSON layer size (< 5k features without MVT), honor iOS `WKWebView` idle eviction, and verify native Capacitor plugins (`Geolocation`, `Filesystem`, `Camera`) on real Android/iOS builds.
