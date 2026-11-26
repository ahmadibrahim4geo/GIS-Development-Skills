# Web & Mobile Offline Storage, PWA Cache, Tile Policy & Sync State Machine

> Shared Offline-First contract (`REQ-WM-016`, `REQ-WM-047`, `Web_Mobile_r3 §6 & §11`) across `geospatial-web-mapping` (`P05`) and `gis-mobile-application-development` (`P06`).

---

## 1. Seventeen PWA & Local-First Web Technologies (`§6`)

| Layer | Tools & Standards | Critical Caveats & Browser Boundaries |
|---|---|---|
| **PWA Shell & Service Worker** | `MDN PWA Installability`, `Workbox`, `vite-plugin-pwa`, `Web App Manifest` | App shell assets (`HTML/JS/CSS/SVG/fonts`) only; cache-version bust cleanly via immutable asset hashes + update prompt |
| **Browser Databases & File Systems** | `IndexedDB`, `Dexie.js`, `RxDB`, `PouchDB`, `SQLite-Wasm + OPFS` (Origin Private File System), `PowerSync`, `ElectricSQL` | Multi-thread `OPFS` / `SQLite-Wasm` requires **`Cross-Origin-Opener-Policy: same-origin` (`COOP`) + `Cross-Origin-Embedder-Policy: require-corp` (`COEP`)** headers — provide single-thread `IndexedDB`/`Dexie` fallback on static hosts like GitHub Pages! |
| **Quota & Persistence APIs** | `navigator.storage.estimate()`, `navigator.storage.persist()` | `storage.persist()` is **not guaranteed** (especially iOS Safari/WKWebView ~7-day idle eviction). Always inspect `estimate()`, warn before overflow, and offer manual **Export Backup (GeoJSON/Zip)** (`REQ-WM-047`) |
| **Self-Hosted & Permitted Vector Tiles** | `PMTiles` (`Protomaps`), `VersaTiles`, `OpenFreeMap`, `Martin`, local bundled `MBTiles`/slices | Static HTTP `Range` requests work offline when pre-bundled or explicitly permitted; respect dataset license & size |

---

## 2. Mandatory Basemap Policy: Zero Public OSM Tile Scraping (`WEB-QA-07`)

> [!CAUTION]
> **NEVER** prefetch, scrape, or cache bulk map tiles from `https://tile.openstreetmap.org` (`{z}/{x}/{y}.png`) for offline PWAs or mobile apps. That violates the **OpenStreetMap Foundation Tile Usage Policy** (`access blocked / User-Agent ban`), even though OpenStreetMap vector/planet *data* is `ODbL`. Always generate self-hosted `PMTiles` / `VersaTiles` / `Martin` archives with proper attribution for offline workflows.

---

## 3. Shared 15-Field Offline Sync State Machine (`§11`, `REQ-WM-026`, `REQ-WM-042`)

Never resolve multi-user or multi-session geospatial edits with blind **Last-Write-Wins (`LWW`)**, which silently overwrites geometry or deletes peer attributes. Every offline mutation queued in Web (`IndexedDB`/`Dexie`) or Mobile (`SQLite`/`Room`/`GRDB`) aligns to these canonical **15 contract fields**:

| # | Canonical `REQ-WM-042` Field | Web / JSON Equivalent (`pwa-sync.mjs`) | Semantics & Safety Rule |
|---|---|---|---|
| 1 | `project_id` | `layer_id` / workspace scope | Target project/workspace scope isolating tenant data |
| 2 | `layer_id` | `layer_id` | Target dataset/table identifier |
| 3 | `feature_id` | `feature_id` | Stable cross-client UUID/feature identity |
| 4 | `op_id` | `client_op_id` | Immutable UUIDv4/idempotency key reused across retries |
| 5 | `base_revision` | `base_revision` | Server revision read prior to edit (`null` only on `create`) |
| 6 | `geometry` | `geometry_geojson` | Validated GeoJSON / WKB geometry payload |
| 7 | `attributes` | `attributes` | UTF-8 attribute map preserving explicit `null` values |
| 8 | `crs` | `crs_epsg` | Explicit EPSG integer/URN (`4326`, `32636`, etc.) + optional vertical datum |
| 9 | `client_timestamp` | `local_timestamp_utc` | ISO-8601 UTC device clock (informational ONLY, never LWW authority) |
| 10 | `server_timestamp` | `server_timestamp_utc` | Authoritative server receipt timestamp upon ACK/pull |
| 11 | `device_id` | *(device/client provenance)* | Pseudonymous installation ID distinguishing multi-device edits |
| 12 | `attachment_manifest` | `binary_attachment_refs` | Local media paths, MIME, SHA-256 digests & EXIF-strip status |
| 13 | `deletion_tombstone` | `op_type = delete_tombstone` | Boolean/tombstone marker — zero physical silent purge before ACK |
| 14 | `checksum` | `payload_sha256` | SHA-256 digest preventing `op_id` reuse with forged payload |
| 15 | `sync_state` | `state` | `PENDING | IN_FLIGHT | ACKED | CONFLICT | BLOCKED` *(or Web `queued/failed-retryable/dead-letter`)* |

### Eight Storage Resilience Layers (`REQ-WM-026`)
1. **Atomic Local DB Commit (`SQLite WAL` / `IndexedDB` tx)** before optimistic UI confirmation.
2. **Quota & Low-Disk Pre-Flight Guard (`< 5%` free or `QuotaExceededError`)** blocking corrupt partial tile/DB writes (`MOB-QA-09`).
3. **Append-Only Outbox Survival** across app force-kill, OS suspension, and cold reboot (`MOB-QA-07`, `WEB-QA-06`).
4. **Immutable `op_id` + `checksum` Server Deduplication** preventing duplicate geometry on flaky mobile retries.
5. **Versioned Conflict Detection (`base_revision != current`)** preserving BOTH local & server versions for manual resolution (zero blind `LWW`, `MOB-QA-08`).
6. **Auth Expiry (`401/403`) & Offline Isolation (`OFFLINE_UNLOCKED`)** pausing uploads cleanly without losing unsynced field edits (`MOB-QA-18`).
7. **Schema Migration Safety (`v1 -> v2`)** wrapped in transactional DB migrations with pre-migration backup checks (`MOB-QA-12`).
8. **Attachment & Export Recovery** linking hashed media (`MOB-QA-10`) and user-triggered JSON/GeoPackage emergency export (`REQ-WM-047`).

---

## 4. Six Offline & Sync Failure Clusters (Mandatory QA)

| Failure Scenario | Expected Safe Behavior | Verification Target |
|---|---|---|
| **1. Airplane Mode / Network Drop Mid-Flush** | Queue stays `queued` or transitions `in-flight -> failed-retryable`; local edits survive cold browser/app restart | `WEB-QA-06`, `MOB-QA-03` |
| **2. Sudden Tab Close / App Force-Kill** | Mutation persisted to `IndexedDB`/`SQLite` *before* optimistic UI confirmation finishes | `WEB-QA-06`, `MOB-QA-04` |
| **3. Server Revision Conflict (`409` / `base != current`)** | Transitions to **`conflict`** holding BOTH `server_record` and `local_patch` side-by-side for manual user resolution | `WEB-TPL-11`, `MOB-QA-06` |
| **4. Retry Duplicate Delivery** | Server verifies `(client_op_id, payload_sha256)` match and returns identical `server_revision` cleanly without duplicating features | `WEB-QA-14` |
| **5. Auth Expiry (`401`/`403`) or Quota Full (`507`/`QuotaExceededError`)** | Halts queue safely without discarding local edits; triggers re-auth flow or manual JSON backup export | `WEB-QA-08`, `REQ-WM-047` |
| **6. Missing Offline Tiles (`404` / Offline)** | Renders offline base vector GeoJSON + visible tile-unavailable banner rather than blank map or hitting OSM bulk servers | `WEB-QA-07` |
