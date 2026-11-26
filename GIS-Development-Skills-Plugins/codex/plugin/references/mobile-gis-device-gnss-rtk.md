# Mobile GNSS Provenance, Vertical Datum, Hardware Sensors & Mobile AR

> Specialist reference (`REQ-WM-023`, `GIS-015`, `MOB-QA-04, 05, 10, 11`, `MOB-TPL-08, 09, 14`) for [`gis-mobile-application-development`](../skills/gis-mobile-application-development/SKILL.md), [`gis-device-context`](../skills/gis-device-context/SKILL.md), and [`system-capabilities-and-permissions`](../skills/system-capabilities-and-permissions/SKILL.md).

---

## 1. Fourteen Location Provenance & Accuracy Layers (`§8.1`)

Never collapse all location inputs into a bare `(lat, lon)` pair or market consumer phone fixes as survey-grade cm accuracy. Track all 14 attributes:

1. **Provider Source Class:** `fused_os` | `raw_gnss_chip` | `external_ble_gnss` | `external_usb_rtk` | `manual_map_tap` | `ip_network_fallback` *(disallowed for field survey save)*
2. **Coordinate System & Epoch:** `EPSG:4326` / `WGS84(G2139)` / local national datum (explicit EPSG integer)
3. **Horizontal Accuracy (`h_acc_m`, 68% RMS / 1-sigma):** Device/receiver-reported horizontal uncertainty in meters
4. **Vertical Accuracy (`v_acc_m`):** Reported altitude uncertainty (usually 1.5×–2.5× worse than `h_acc_m`)
5. **Height Datum Distinction (`GIS-015`):** Explicit **`ellipsoidal_wgs84` (`h`)** vs **`orthometric_egm2008` / `msl` (`H = h - N`)** — never silently mix orthometric and ellipsoidal Z!
6. **UTC Fix Timestamp & Fix Age (`fix_age_s`):** ISO-8601 UTC timestamp + elapsed seconds; mark **`STALE`** if `fix_age_s > max_age_s` (e.g., `15s`)
7. **Mock / Spoofed Location Guard:** Detect Android `Location.isMock()` / Developer mock providers and warn or block verified field capture
8. **External Receiver Identity:** Vendor/Model/Serial over BLE GATT or USB-OTG (e.g., `NMEA 0183 GGA/GSA/GST` or binary `UBX`)
9. **RTK Solution State (`MOB-QA-05`):** `SINGLE` | `DGPS/SBAS` | `RTK_FLOAT` | `RTK_FIXED` (via `RTKLIB` / `NTRIP` RTCM3 caster)
10. **RTCM Correction Age & Mountpoint:** Reject "cm fixed" claim if correction age `> 5s` or solution is `FLOAT`/`SINGLE`
11. **DOP Metrics:** `HDOP`, `VDOP`, `PDOP` + Satellites Used / In View
12. **Constellations Observed:** `GPS`, `GLONASS`, `Galileo`, `BeiDou`, `QZSS`
13. **Antenna Pole Offset (`pole_height_m`):** Documented manual instrument height subtracted from antenna elevation before feature Z storage
14. **Consent & Permission Mode:** `foreground_precise` | `foreground_approximate` | `background_opt_in` | `denied_manual_only`

---

## 2. Nineteen Hardware & Field Interfaces + Privacy Controls (`§8.2`)

| Interface | Use Case | Mandatory Privacy & Fallback Gate |
|---|---|---|
| 1. Foreground Fine GNSS · 2. Approximate Location | Map center, vertex snap | On **Deny / Ask Later** keep manual digitizing usable (`MOB-QA-03`) |
| 3. Background Location (FGS / `Always`) | Track logging | Separate 2nd opt-in + persistent notification + battery-saver throttle (`MOB-QA-11`, `16`) |
| 4. Camera (`CameraX` / `AVFoundation`) · 5. Gallery Picker | Asset photo capture | **Default `strip_exif_gps = true`** unless field workflow & user opt in (`MOB-QA-10`) |
| 6. Scoped File Picker (`SAF`/`DocumentPicker`) · 7. Internal SQLite/GPKG | Import/Export | Never require broad `MANAGE_EXTERNAL_STORAGE`; handle `<5%` disk (`MOB-QA-09`) |
| 8. BLE GATT · 9. Classic SPP BT · 10. USB-C OTG Serial | External RTK NMEA | Auto-reconnect + visible fallback indicator if receiver drops (`MOB-QA-05`) |
| 11. Magnetometer/IMU Compass · 12. Accelerometer/Gyro · 13. Barometer | Bearing, tilt comp. | Calibrate & flag magnetic interference near utility steel |
| 14. LiDAR / Depth Sensor · 15. NFC Tag · 16. Barcode/QR Scanner | Pole/valve IDs, 3D | Graceful software fallback on devices lacking LiDAR/NFC |
| 17. Microphone (Voice Note) · 18. Connectivity Monitor · 19. Biometric Lock | Offline field UX | Explicit consent; local biometric unlock is NOT server authentication |

**Data Deletion Hygiene (`MOB-QA-19`):** Deleting an observation must remove orphan attachments/thumbnails and support user-triggered workspace wipe without touching user-chosen external exports.

---

## 3. Mobile 3D / AR Integration (`§8.3–8.4`, `MOB-TPL-14`)

Pair [Geospatial 3D, AR & Digital Twins](geospatial-3d-ar-mobile-web.md) with 6 mobile AR controls:
1. Check `ARCore Geospatial API` / `ARKit ARGeoTrackingConfiguration` city/VPS availability **before** enabling AR mode (fall back cleanly to 2D map if unsupported).
2. Convert `(Lat, Lon, Orthometric/Ellipsoidal H)` to local **`ENU`** tangent plane with explicit horizontal/vertical uncertainty display (`MOB-TPL-14`).
3. Gate AR overlay calibration on magnetic + visual localization confidence thresholds.
4. Keep background/camera tracking bounded by thermal/battery state (`MOB-QA-16`).
5. Never persist raw camera frames without explicit user confirmation.
6. Declare physical-device AR tests strictly **`NOT_RUN`** on desktop/emulator CI.
