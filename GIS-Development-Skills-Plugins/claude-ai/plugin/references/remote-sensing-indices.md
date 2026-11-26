# Remote Sensing Indices, Formulas, and Scientific Interpretation Guide

> **Target:** Scientific Earth observation workflows in `skills/remote-sensing-pipelines`.  
> **Complements:** [`remote-sensing-sensor-band-mappings.md`](remote-sensing-sensor-band-mappings.md), [`remote-sensing-indices.json`](remote-sensing-indices.json), [`remote-sensing-threshold-profiles.json`](remote-sensing-threshold-profiles.json), and [`remote-sensing-index-source-registry.json`](remote-sensing-index-source-registry.json).

---

## 1. Fundamental Scientific Rules for Index Interpretation

1. **Four Separate Layers:**
   * **Mathematical Range:** The theoretical bounds given strictly by formula algebra (e.g. `[-1, 1]` for normalized difference with non-negative inputs).
   * **Observed / Typical Field Range:** The empirical interval typically encountered in realistic landscapes (e.g. dense vegetation NDVI is ~0.6 to 0.85; clear water is < 0.0).
   * **Classification Thresholds:** Contextual, conditional ranges tied to a specific biome, sensor, season, and validated scientific study. **No universal classification threshold exists.**
   * **Storage Encoding:** The integer representation on disk (e.g. USGS packaged NDVI scaled by `0.0001` stored as `int16` from `-10000` to `+10000`).
2. **Values Are Not Percentages:**
   * $\text{NDVI} = 0.65$ **does not** equal 65% vegetation cover. Fractional Vegetation Cover (FVC) requires a calibrated dimidiate pixel model ($FVC = \frac{NDVI - NDVI_0}{NDVI_v - NDVI_0}$).
   * $\text{NDWI} = 0.40$ **does not** mean 40% water depth or 40% water fraction.
   * $\text{NDBI} > 0$ **does not** prove an urban built-up area; dry arid soil routinely produces positive NDBI.
3. **Denominator and Domain Protection:**
   * Guard every normalized difference or ratio against $\text{denominator} = 0$, near-zero values ($|\text{den}| < 10^{-6}$), $\text{NaN}$, and $\text{Inf}$.
   * In Google Earth Engine, `ee.Image.normalizedDifference()` silently masks pixels where either input is negative. In calibrated Surface Reflectance (SR), slight negative reflectance can occur over dark water or cloud shadows; use explicit `expression()` when you need to preserve or analyze negative inputs.
4. **Temporal Change & Trend Integrity:**
   * Multi-temporal difference: $\Delta \text{Index} = \text{Index}_{t2} - \text{Index}_{t1}$.
   * Relative change: $\% \Delta = \frac{\text{Index}_{t2} - \text{Index}_{t1}}{\text{Index}_{t1}} \times 100$ (only valid when $\text{Index}_{t1}$ is strictly positive and non-zero).
   * Never compare scenes from different seasons without phenological normalization, and never compare raw unharmonized scenes from different sensors (e.g. Landsat 8 and Sentinel-2 require HLS or cross-sensor regression).
5. **Optical Proxies vs Physical Quantities:**
   * Indices like NDCI (chlorophyll proxy) or LST (thermal proxy) are optical indicators. Converting them to physical concentrations ($\text{mg/m}^3$) or exact degrees Celsius requires documented atmospheric corrections and local empirical calibration.

---

## 2. Resolving Alias Collisions and Naming Ambiguities

| Ambiguous Term | Candidate 1 (Primary) | Candidate 2 (Alternative) | Disambiguation Strategy |
|---|---|---|---|
| **NDWI** | **NDWI (McFeeters 1996):**  <br>$\frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}}$  <br>Target: **Open Surface Water bodies** | **NDWI (Gao 1996):**  <br>$\frac{\text{NIR} - \text{SWIR}}{\text{NIR} + \text{SWIR}}$  <br>Target: **Plant Canopy Liquid Water (NDMI / LSWI)** | Check user goal: if mapping lakes, rivers, or coastlines $\rightarrow$ McFeeters. If assessing plant moisture, crop drought, or canopy hydration $\rightarrow$ Gao / NDMI. |
| **NDSI** | **NDSI Snow (Hall 1995):**  <br>$\frac{\text{Green} - \text{SWIR1}}{\text{Green} + \text{SWIR1}}$  <br>Target: **Snow & Ice** (requires $\text{NIR} \ge 0.11$) | **NDSI Salinity (Major et al.):**  <br>$\frac{\text{Red} - \text{NIR}}{\text{Red} + \text{NIR}}$ or specialized soil ratios  <br>Target: **Soil Salinization** | Snow mapping is default in cryosphere/mountain contexts. If agricultural soil salinization is requested, invoke specialized salinity ratios. |
| **RVI** | **Radar Vegetation Index (Charbonneau 2005):**  <br>$\frac{4 \times \text{VH}_{\text{lin}}}{\text{VV}_{\text{lin}} + \text{VH}_{\text{lin}}}$  <br>Target: **Microwave canopy volume scattering** | **Ratio Vegetation Index (Jordan 1969):**  <br>$\frac{\text{NIR}}{\text{Red}}$  <br>Target: **Optical Simple Ratio (SR)** | Check data modality: SAR backscatter (linear power) $\rightarrow$ Radar RVI. Optical multispectral reflectance $\rightarrow$ Jordan Simple Ratio. |
| **NBR vs dNBR** | **NBR (Single Date):**  <br>$\frac{\text{NIR} - \text{SWIR2}}{\text{NIR} + \text{SWIR2}}$ | **dNBR (Bi-temporal Difference):**  <br>$\text{NBR}_{\text{pre}} - \text{NBR}_{\text{post}}$ | NBR reflects single-date fuel/ash condition; dNBR measures true fire burn severity. Verify whether values are unscaled ($-1 \text{ to } 1$) or scaled by 1000. |

---

## 3. Core Thematic Index Catalog & Formulation

### A. Vegetation Greenness & Biophysical Canopy

#### 1. Normalized Difference Vegetation Index (NDVI)
* **Citation:** Rouse et al. (1974)
* **Formula:**
  $$\text{NDVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red}}$$
* **Mathematical Range:** $[-1.0, 1.0]$
* **Typical Field Range:** Water $< 0$; Bare soil $0.05 - 0.20$; Sparse vegetation $0.20 - 0.40$; Dense healthy canopy $0.60 - 0.85$.
* **Limitations:** Saturates at high leaf area index ($\text{LAI} > 3 - 4$); sensitive to soil background reflectance in arid zones.

#### 2. Enhanced Vegetation Index (EVI & EVI2)
* **Citation:** Huete et al. (2002); Jiang et al. (2008)
* **Formula (EVI - 3 bands):**
  $$\text{EVI} = 2.5 \times \frac{\text{NIR} - \text{Red}}{\text{NIR} + 6.0 \times \text{Red} - 7.5 \times \text{Blue} + 1.0}$$
* **Formula (EVI2 - 2 bands):**
  $$\text{EVI2} = 2.5 \times \frac{\text{NIR} - \text{Red}}{\text{NIR} + 2.4 \times \text{Red} + 1.0}$$
* **Mathematical Range:** Approximates $[-1.5, 1.5]$ (denominator has added constants; not bound to $[-1, 1]$).
* **Advantage:** Resists saturation in high-biomass forests; decouples canopy signal from atmospheric aerosol background.

#### 3. Soil-Adjusted Vegetation Index (SAVI) & MSAVI
* **Citation:** Huete (1988); Qi et al. (1994)
* **Formula (SAVI):**
  $$\text{SAVI} = \frac{\text{NIR} - \text{Red}}{\text{NIR} + \text{Red} + L} \times (1.0 + L)$$
  * Default adjustment factor $L = 0.5$ for intermediate canopy density ($L=1.0$ for very low density, $L=0.25$ for higher density).
* **Formula (MSAVI self-adjusting):**
  $$\text{MSAVI} = \frac{2 \times \text{NIR} + 1 - \sqrt{(2 \times \text{NIR} + 1)^2 - 8 \times (\text{NIR} - \text{Red})}}{2}$$
* **Advantage:** Drastically reduces soil background brightness variations in arid, semi-arid, and emergent agricultural fields.

#### 4. Normalized Difference Red Edge Index (NDRE)
* **Citation:** Barnes et al. (2000)
* **Formula:**
  $$\text{NDRE} = \frac{\text{NIR} - \text{RedEdge}}{\text{NIR} + \text{RedEdge}}$$
* **Sensor Suitability:** Sentinel-2 (B8 or B8A vs B5), RapidEye, PlanetScope SuperDove.
* **Advantage:** The red-edge band penetrates deeper into dense canopies than red light, diagnosing chlorophyll and nitrogen status before chlorosis appears in broad red bands.

---

### B. Water Bodies, Soil Moisture, and Snow

#### 1. Open Water: NDWI (McFeeters 1996) & MNDWI (Xu 2006)
* **McFeeters Formula:**
  $$\text{NDWI}_{\text{water}} = \frac{\text{Green} - \text{NIR}}{\text{Green} + \text{NIR}}$$
* **Xu Modified Formula (MNDWI):**
  $$\text{MNDWI} = \frac{\text{Green} - \text{SWIR1}}{\text{Green} + \text{SWIR1}}$$
* **Scientific Distinction:**
  * McFeeters NDWI reflects water when $> 0$, but asphalt, built-up concrete, and urban shadows often yield false positives.
  * Xu MNDWI substitutes SWIR1 for NIR. Since built-up land reflects much higher in SWIR1 than Green, MNDWI drives urban values negative, sharply delineating open water bodies in city landscapes.

#### 2. Vegetation Canopy Moisture: NDMI / Gao NDWI (1996)
* **Formula:**
  $$\text{NDMI} = \frac{\text{NIR} - \text{SWIR1}}{\text{NIR} + \text{SWIR1}}$$
* **Application:** Tracks crop water stress, agricultural drought, and fuel moisture content before wildfire outbreaks.

#### 3. Snow & Ice: NDSI (Hall et al. 1995)
* **Formula:**
  $$\text{NDSI} = \frac{\text{Green} - \text{SWIR1}}{\text{Green} + \text{SWIR1}}$$
* **Co-condition:** Snow has high reflectance in Green and strong absorption in SWIR1, but so does open water.  
  $$\text{Snow} \iff \text{NDSI} \ge 0.40 \quad \mathbf{AND} \quad \text{NIR} \ge 0.11$$

---

### C. Wildfire Burn Severity & Regeneration

#### 1. Normalized Burn Ratio (NBR) & Differenced NBR (dNBR)
* **Citation:** Key & Benson (2006)
* **Formulas:**
  $$\text{NBR} = \frac{\text{NIR} - \text{SWIR2}}{\text{NIR} + \text{SWIR2}}$$
  $$\text{dNBR} = \text{NBR}_{\text{pre}} - \text{NBR}_{\text{post}}$$
* **Scaled Convention:** If working with USGS pre-packaged dNBR products, multiply unscaled dNBR by $1000$.
* **Contextual Severity Guidelines (USFS/NPS Reference):**
  * $\text{dNBR} < 0.10$ (or $< 100$): Unburned / negligible change
  * $0.10 \le \text{dNBR} < 0.27$ ($100 - 270$): Low severity
  * $0.27 \le \text{dNBR} < 0.44$ ($270 - 440$): Moderate-low severity
  * $0.44 \le \text{dNBR} < 0.66$ ($440 - 660$): Moderate-high severity
  * $\text{dNBR} \ge 0.66$ ($> 660$): High severity
* **Caution:** These severity cutoffs were calibrated for western US conifer forests. In Mediterranean scrublands, peatlands, or savannahs, local CBI field plots must be used to adjust threshold boundaries.

---

### D. Urban Impervious & Bare Soil

#### 1. Normalized Difference Built-up Index (NDBI) & Bare Soil Index (BSI)
* **NDBI (Zha et al. 2003):**
  $$\text{NDBI} = \frac{\text{SWIR1} - \text{NIR}}{\text{SWIR1} + \text{NIR}}$$
* **BSI (Rikimaru et al. 2002):**
  $$\text{BSI} = \frac{(\text{SWIR1} + \text{Red}) - (\text{NIR} + \text{Blue})}{(\text{SWIR1} + \text{Red}) + (\text{NIR} + \text{Blue})}$$
* **Scientific Warning:** NDBI has very high confusion with bare dry soil and rock outcrops. Do not classify built-up land automatically with NDBI alone; combine with an NDVI mask ($\text{NDBI} - \text{NDVI}$) or high-resolution nightlights/building footprints.

---

### E. Water Quality & Chlorophyll

#### 1. Normalized Difference Chlorophyll Index (NDCI)
* **Citation:** Mishra & Mishra (2012)
* **Formula:**
  $$\text{NDCI} = \frac{\text{RedEdge1} - \text{Red}}{\text{RedEdge1} + \text{Red}} \quad (\text{Sentinel-2: } \frac{\text{B5} - \text{B4}}{\text{B5} + \text{B4}})$$
* **Scientific Constraint:** NDCI is an optical proxy. Converting to physical concentration ($\text{mg/m}^3$) requires local lake/reservoir water sampling and dedicated aquatic atmospheric correction algorithms (e.g. C2RCC, ACOLITE, Polymer).

---

## 4. Multi-Platform Implementation Recipes

### Python (NumPy / Rasterio)
```python
import numpy as np

def calculate_normalized_difference(band_a: np.ndarray, band_b: np.ndarray) -> np.ndarray:
    """Safe normalized difference with zero-division and invalid input protection."""
    denominator = band_a + band_b
    valid_mask = (denominator != 0) & np.isfinite(denominator) & (band_a >= 0) & (band_b >= 0)
    result = np.full(band_a.shape, np.nan, dtype=np.float32)
    result[valid_mask] = (band_a[valid_mask] - band_b[valid_mask]) / denominator[valid_mask]
    return result
```

### Google Earth Engine
```javascript
// Explicit expression to avoid silent negative input masking:
var ndvi = image.expression(
  '(NIR - RED) / (NIR + RED)', {
    'NIR': image.select('B8').multiply(0.0001),
    'RED': image.select('B4').multiply(0.0001)
  }
).rename('NDVI');
```

### QGIS Raster Calculator
```sql
-- Safe evaluation avoiding division by zero:
( ("B8@1" - "B4@1") / ( ("B8@1" + "B4@1") + (("B8@1" + "B4@1") = 0) ) )
```

### ArcGIS Pro Raster Functions
Use the `Band Arithmetic` function with `Method: User Defined` or built-in index selectors (`NDVI`, `SAVI`, `EVI`). Ensure `Band Indexes` are mapped to spectral wavelengths rather than sequence indices.
