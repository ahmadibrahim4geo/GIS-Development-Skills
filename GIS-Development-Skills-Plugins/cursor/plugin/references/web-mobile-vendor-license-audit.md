# Web & Mobile Providers (26 Vendors) & OWASP Security Threat Matrix

> Authoritative Free-First commercial vs OSS vendor decision guide (`26` providers, `§14`) and `10`-class OWASP Web/Mobile GIS Threat Matrix (`ASVS`/`MASVS`/`MASTG`, `REQ-WM-029`, `REQ-WM-035`). Check live upstream pricing & terms at selection time; code license NEVER grants free tile/API hosting rights.

---

## 1. Twenty-Six Web & Mobile Providers (`18-Field Decision Model`, `§14`)

Always evaluate **Code/SDK License** separately from **Hosted API Quota/Billing**, **Offline Caching Terms**, **Attribution Requirements**, and **Hard Stop Safeguards**:

| Group | Providers Indexed (`26 Total`) | Free-First / Offline Boundary & Mandatory Checks |
|---|---|---|
| **Fully Open / Free Data & Self-Hostable (`7`)** | `OpenStreetMap` (`ODbL` data != public tiles!), `Protomaps` (`PMTiles`, BSD-3/ODbL), `OpenFreeMap` (MIT/ODbL fair-use), `Natural Earth` (Public Domain), `geoBoundaries` (`CC-BY-4.0`), `OpenTopography` (`DEM` public/keyed), `NASA Earthdata / GIBS / CMR` (public science data; free account for bulk) | **Best Free-First Defaults.** Self-host `PMTiles` / `Natural Earth` / `geoBoundaries` for `WEB-01..18` & `MOB-01..20` offline runs without paid keys |
| **Public EO / Earth Science Portals (`4`)** | `USGS M2M / Landsat`, `Copernicus Data Space`, `Microsoft Planetary Computer` (SAS signed), `Google Earth Engine` (`non-commercial free / commercial billed`) | Disclose account registration, token expiry, egress limits & non-commercial clauses on GEE |
| **Commercial Mapping / Platform APIs (`9`)** | `Esri ArcGIS Location Platform`, `Google Maps Platform`, `Mapbox`, `MapTiler` *(free personal/non-commercial dev tier)*, `Apple MapKit / JS` *(Apple Dev account)*, `HERE`, `Azure Maps`, `AWS Location Service`, `TomTom` | Require API keys/tokens, strict HTTP Referrer or App-ID/SHA1 restrictions, billing caps, **explicit ban on unauthorized offline tile redistribution** |
| **Conditional / Niche Geocoding, Routing & Street View (`6`)** | `Stadia Maps` *(free dev tier, attribution)*, `Geoapify` *(free tier, key)*, `OpenRouteService` *(free quota / OSS self-host)*, `GraphHopper Directions` *(keyed API / OSS engine)*, `Mapillary` *(keyed images; CC-BY-SA attribution)*, `Cesium ion` *(free dev quota; paid commercial)* | Prefer self-hosted `OSRM`/`Valhalla`/`GraphHopper`/`Nominatim`/`Photon` for offline or unbounded production |

**18-Field Vendor Decision Checklist:** `(1)` Product/SKU name, `(2)` SDK code license, `(3)` Hosted data/tile license, `(4)` Auth mechanism (`none/API key/OAuth/SAS`), `(5)` Free-tier cap, `(6)` Commercial/production trigger, `(7)` Billing card required upfront?, `(8)` Academic/non-commercial clause, `(9)` Offline storage/cache allowed?, `(10)` Offline expiry window, `(11)` Max offline feature/tile cap, `(12)` Mandatory visual attribution string, `(13)` Telemetry/tracking opt-out, `(14)` Origin/Referer/BundleID key lock, `(15)` `401/403/429` graceful fallback path, `(16)` Hard monthly quota alarm/circuit breaker, `(17)` Self-hosted OSS drop-in analog, `(18)` Review date (`V1/V2/V3`).

---

## 2. Ten OWASP Web & Mobile GIS Threat Classes (`ASVS / MASVS`, `REQ-WM-035`)

| # | Threat Class | Mandatory Mitigation & Acceptance Verification |
|---|---|---|
| 1 | **Client-Exposed Secrets & Billing Keys** | Never ship private/billing server keys in static JS/HTML/APK/IPA bundles (`security_audit.py`). Route paid APIs through authenticated backend proxy or strictly origin/bundle-locked public map tokens; enforce `401/403/429` key-redacting error UI (`WEB-QA-08`) |
| 2 | **Untrusted KML / KMZ / GeoJSON / ZIP Bombs & XXE** | Enforce uncompressed byte caps, zip-entry path traversal guards, XML `<!DOCTYPE`/`<!ENTITY` rejection (`security_guardian.py` / `kml-kmz-engineering`) |
| 3 | **Popup / Attribute HTML XSS Injection** | Escape or construct DOM safely (`textContent`, DOM nodes — never `innerHTML = feature.properties.name`) and reject `javascript:` links (`WEB-QA-10`) |
| 4 | **Geolocation, Tracking & EXIF PII Leakage** | Obtain explicit foreground user consent before `navigator.geolocation` or photo GPS capture; strip/disclose EXIF GPS on public uploads; forbid plain HTTP location streaming (`https://` / `wss://` only) |
| 5 | **Prohibited Bulk Tile Scraping** | Block `tile.openstreetmap.org` prefetch patterns at code review & runtime router level (`WEB-QA-07`); use `PMTiles`/self-hosted sources |
| 6 | **Token Storage, CORS Wildcards & CSRF** | Web: avoid `Access-Control-Allow-Origin: *` on authenticated APIs, use `HttpOnly; SameSite` cookies or short-lived OAuth PKCE; Mobile: use Android `EncryptedSharedPreferences`/Keystore & iOS `Keychain`, NEVER `AsyncStorage`/`SharedPreferences` plaintext |
| 7 | **Supply-Chain & External Agent Skill Poisoning** | Pin npm/Gradle/CocoaPods/SwiftPM lockfiles, audit CVEs, keep external agent skills (`external-agent-skills-registry.json`) strictly quarantined `candidate-review-only` |
| 8 | **PostGIS / API SQL Injection & SSRF** | Parameterized PostGIS queries only (`ST_Intersects($1, ...)` — zero SQL string interpolation); strict URL/host allowlist on backend tile/STAC proxies (no SSRF to `169.254.169.254` / LAN) |
| 9 | **Unconsented Sensitive Layer Cloud Upload (GeoAI)** | Default GeoAI to local WASM/WebGPU/on-device or isolated private server; require explicit consent modal before sending layers externally |
| 10 | **Offline Sync Queue Corruption & Silent Overwrite** | Use immutable `client_op_id` + `payload_sha256` + `base_revision` optimistic lock (`conflict` UI instead of blind LWW) plus encrypted/checksummed manual JSON export backup (`WEB-QA-06`, `WEB-QA-14`) |
