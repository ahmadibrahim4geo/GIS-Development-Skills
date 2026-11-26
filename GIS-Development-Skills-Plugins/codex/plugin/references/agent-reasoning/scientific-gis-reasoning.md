# GIS & Remote Sensing Scientific Reasoning Standards

> Canonical specification for AAREF requirements `REQ-GIS-01..15`. Domain owners apply ONLY the invariants relevant to the task—never apply an unrelated checklist mechanically.

## 1. Core Scientific Guardrails

- **Protected Inputs First:** Treat source datasets and user `testing data/` as read-only protected inputs. Never mutate geometry, pixel values, or spatial reference metadata to mask downstream misalignment.
- **Metadata Repair vs Coordinate Transformation:** `Define Projection` repairs missing/incorrect CRS metadata in place without changing coordinates; `Project` / `Project Raster` mathematically reprojects geometries or resamples pixels from a known source CRS to a target CRS. Back up inputs before in-place metadata edits and verify axis order, datum shifts, PROJ grids, and linear units.
- **No Unfounded Assumptions on Coordinates:** Do not silently assume X/Y order, longitude/latitude ordering, vertical datum (`ellipsoidal_wgs84` vs `orthometric_egm2008`), or meters vs degrees when source metadata is missing or ambiguous.
- **Calculation vs Scientific Interpretation:** Numerically running a formula does not prove physical validity, ecological transferability, or statistical significance.

## 2. Domain Verification Selection Matrix

| Domain | Critical Verification Questions | Concrete Evidence Examples |
|---|---|---|
| **CRS & Datum** | Source & target EPSG/WKT2, axis order, datum shift/PROJ grid/epoch? | Control point transformation within documented tolerance |
| **Geometry** | Topological validity, multipart, Z/M, precision model, antimeridian/poles? | Valid/invalid fixture pairs + independent format readback |
| **Measurement** | Planar vs geodesic/ellipsoidal, linear units, reference surface? | Reference distances/areas + equator/high-latitude sanity checks |
| **Raster** | Pixel resolution, origin/alignment, extent, NoData, pixel center vs corner, resampling? | Grid fixture bounds, affine transform, NoData & histogram check |
| **Remote Sensing** | Sensor/product level, band wavelengths, scale/offset, QA/cloud bitmasks, temporal consistency? | Official product handbook constants + test pixel readback |
| **Spectral Indices** | Exact sign/formula, expected domain (`[-1, 1]` vs physical range), denominator `== 0` guard? | Primary publication + band mapping + zero/NoData edge fixtures |
| **Classification / ML** | Spatial autocorrelation leakage, independent validation, class imbalance, overfitting? | Spatial CV, confusion matrix, OA/F1, uncertainty bounds |
| **Terrain & Hydrology** | DEM source & vertical datum, sink/flow routing model, linear units (m vs ft), Z-factor? | Reference profiles, known watershed boundaries, fill/flow checks |
| **Climate & Interpolation** | Missing values, temporal aggregation, elevation covariates, spatial validation? | Spatial holdout metrics, explicit units & temporal metadata |
| **Spatial Analysis** | Predicates (`intersects` vs `within`), buffers, spatial joins, weighting/normalization? | Small deterministic polygon fixtures + expected counts |
| **Data Acquisition** | License terms, spatial/temporal coverage, pagination completeness, deduplication? | Upstream license record + reconciled record counts |
| **Cartography** | Map scale, generalization, projection distortion, classification breaks, RTL/LTR labels? | Rendered visual inspection + uncorrupted underlying geometry |
| **3D / Globe** | Vertical reference (ellipsoid vs terrain), tile clipping, camera picking, depth precision? | Numeric coordinate readback + captured scene inspection |
| **Web GIS** | Tile scheme (`XYZ` vs `TMS`), view reprojection, CORS, async cancellation, offline cache? | Live browser inspection + network/console logs (`NOT RUN` if absent) |
| **Mobile GIS** | GNSS accuracy/age/mock state, permissions (`deny`/`ask_later`), offline WAL queue, conflict preservation? | Device/emulator status + SQLite durable outbox (`NOT RUN` when absent) |

## 3. Specialized Diagnostic & Empirical Protocols

- **CRS & 2D Rendering Drift:** Compare coordinates step-by-step across raw input -> parsed CRS -> transform output -> renderer input -> view projection -> extent -> screen pixel. Test with a tiny control-point grid; never fix CRS misalignment with hardcoded visual pixel offsets.
- **Remote Sensing & Index Computation:**
  - Verify exact collection/level metadata (e.g., Landsat 8 OLI Collection 2 Level-2 Surface Reflectance uses `SR = DN * 0.0000275 - 0.2` with fill `DN == 0` and bit-level `QA_PIXEL` flags—apply scaling *before* normalized ratios because `-0.2` breaks DN ratio cancellation).
  - Always guard zero/near-zero denominators and NoData before writing output `float32`/`float64` rasters.
  - Disambiguate identically named indices explicitly: e.g., **McFeeters (1996) NDWI** `(Green - NIR)/(Green + NIR)` maps open surface water, whereas **Gao (1996) NDWI/NDMI** `(NIR - SWIR)/(NIR + SWIR)` estimates canopy liquid water; never generalize single-study empirical thresholds globally.
- **Desktop UI / Data Flow:** Use unified `command_id` / `trace_id` across `gis-ui-command-audit`, `gis-desktop-e2e-testing`, `gis-data-flow-diagnostics`, and `gis-ui-ux-design-testing` (`references/gis-ui-quality-coordination.md`). Static XAML/unit tests never prove Windows GUI execution.
- **Algorithm Invariants (`T0–T4`):** When external reference software is unavailable, test deterministic invariants (feature count conservation in non-filtering transforms, idempotence, round-trip tolerance) and explicitly state numeric vs methodological errors and native `NOT RUN` boundaries per `docs/QUALITY_BENCHMARK.md` and `references/evidence-tiers.json`.
