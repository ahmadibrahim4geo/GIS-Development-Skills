# Mobile GIS Stack Decision Matrix (12 Criteria × 10 Platforms)

> Quantitative selection companion (`REQ-WM-017`, `REQ-WM-022`) to [`mobile-gis-platform-selection.md`](mobile-gis-platform-selection.md) and [`scripts/compare_engines.py`](../scripts/compare_engines.py).
> Never infer cross-platform parity without a mandatory **Platform PoC** testing real offline vector storage, OS permissions, and native lifecycle termination.

---

## 1. Twelve Criteria × Ten Platforms Decision Matrix (`§7.3`, Scale `1–5` + Mandatory Caveats)

| Platform / Approach | 1. Native Speed | 2. MapLibre / Tiles | 3. GPKG / SQLite Edit | 4. BG GNSS & BLE/RTK | 5. Camera / Sensors | 6. Keystore & Storage | 7. AR RTL + A11y | 8. CI Build Portability | 9. Shared Code % | 10. App Footprint | 11. Maintenance Health | 12. Mandatory PoC Gate before Build |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **1. Kotlin + Jetpack Compose (Android)** | `5` | `5` | `5` | `5` | `5` | `5` | `5` | `5` *(Win/Lin/Mac)* | `1` *(Android only)* | `5` | `5` | Emulator + real GNSS deny/kill + Room tx |
| **2. Swift + SwiftUI (iOS/iPadOS)** | `5` | `4` *(UIKit wrap)* | `5` | `5` *(BLE MFi/GATT)* | `5` *(ARKit)* | `5` | `5` | `1` *(macOS/Xcode only)* | `1` *(iOS only)* | `5` | `5` | macOS Xcode sim + physical GPS/Keychain |
| **3. KMP (`commonMain` + Compose/SwiftUI)** | `5` | `4` | `5` (`SQLDelight`) | `5` | `5` | `5` | `5` | `3` *(iOS needs Mac)* | `4` *(Domain 70%+)* | `4` | `4` | Shared sync unit tests + Android & iOS shell PoC |
| **4. Flutter + Dart** | `4` | `4` *(official `maplibre`)* | `4` (`sqlite3`) | `4` *(plugin channels)* | `4` | `4` | `4` | `3` *(iOS needs Mac)* | `5` *(85–95%)* | `3` | `5` | Verify `maplibre` != legacy `maplibre_gl`, APK+IPA separately |
| **5. React Native (Bare)** | `4` | `4` | `4` (`op-sqlite`) | `3` *(JSI/native bridge)* | `4` | `4` | `4` | `3` | `4` | `3` | `4` | Custom native MapLibre + process-kill queue PoC |
| **6. Expo Dev Build (`prebuild`)** | `4` | `4` | `4` (`expo-sqlite`) | `3` *(Dev Build only)* | `4` | `4` | `4` | `3` *(EAS/Mac for iOS)* | `4` | `3` | `5` | **Mandatory Dev Build BG Location PoC** (ban `Expo Go`) |
| **7. `.NET MAUI` (`Mapsui`)** | `4` | `4` *(Skia/Mapsui)* | `4` | `3` | `3` | `4` | `3` | `3` | `4` *(C# Desktop share)* | `3` | `4` | Validate target Android API / iOS linker trimming |
| **8. Qt / QML (`QField` / `Mergin` stack)** | `4` | `5` *(QGIS Core)* | `5` *(GDAL/GPKG full)* | `4` | `3` | `4` | `3` | `2` *(heavy NDK/Qt)* | `4` *(Desktop+Mobile)* | `2` | `4` | Verify `GPLv2+` obligations & mobile Qt ABI build |
| **9. Capacitor Hybrid (`Web + Plugins`)** | `2` | `3` *(WebGL cap)* | `3` (`@capacitor-community/sqlite`) | `2` | `3` | `3` | `4` | `4` | `5` *(Web+Mobile)* | `4` | `4` | Benchmark `5k` features + iOS `WKWebView` background purge |
| **10. Mobile PWA *(Non-Native Baseline)*** | `3` | `4` | `2` *(IndexedDB quota)* | `1` *(No BLE/BG GNSS)* | `2` *(No raw EXIF/CameraX)* | `2` *(No Keystore)* | `4` | `5` *(Static Web)* | `5` | `5` | `5` | Never classify as native app (`PWA != Native`) |

---

## 2. Deterministic Selection Rules (`compare_engines.py` + `recommend_stack.py`)

1. **Both Android & iOS + Deep Field Sync + Clean Native Feel:** Choose **KMP (`commonMain` shared core + Compose/SwiftUI)** or **Flutter (official `maplibre` + `sqlite3`)** depending on team language (`Kotlin/Swift` vs `Dart`).
2. **Android-First Survey / Rugged Field Hardware (USB/BLE RTK, Raw GNSS, Scoped Storage):** Choose **Kotlin + Jetpack Compose** directly for zero JNI latency on GNSS/BLE streams.
3. **Full QGIS Project Styles / Forms / Expressions Parity Needed Offline:** Choose **Qt / QGIS Mobile architecture** (`QField` / `Mergin` pattern) after passing the `GPL` & mobile `QGIS` build gate.
4. **Purely Public/Simple Viewer or Light Offline Form without Background GNSS or BLE:** Prefer **Web GIS / PWA** (`WEB-12` / `WEB-17`) instead of forcing native Play/App Store distribution overhead.
