# Remote Sensing Sensor Band Mappings, Levels, and Scaling Specifications

> **Target:** `skills/remote-sensing-pipelines` and multidisciplinary GIS workflows.  
> **Source hierarchy:** Official USGS Landsat Product Guides, ESA Copernicus Data Space, NASA HLS, and CEOS ARD specifications.

---

## 1. Optical Sensor Band Mapping Matrix

Never rely on sequential band numbers (e.g. Band 4 is Red on Landsat 8 and Sentinel-2, but Near-Infrared on Landsat 4–7). Always resolve bands by physical spectral role and wavelength.

| Spectral Role | Nominal Wavelength ($\mu\text{m}$) | Landsat 4–5 TM & Landsat 7 ETM+ | Landsat 8–9 OLI / TIRS | Sentinel-2 MSI (S2A / S2B) | MODIS (Terra/Aqua) | Notes & Spatial Resolution |
|---|---|---|---|---|---|---|
| **Coastal Aerosol** | ~0.43 – 0.45 | — | **B1** (30m) | **B1** (60m) | — | Atmospheric correction & bathymetry |
| **Blue** | ~0.45 – 0.51 | **B1** (30m) | **B2** (30m) | **B2** (10m) | **B3** (500m) | Deep water, EVI denominator |
| **Green** | ~0.53 – 0.59 | **B2** (30m) | **B3** (30m) | **B3** (10m) | **B4** (500m) | McFeeters NDWI, NDSI snow, GNDVI |
| **Red** | ~0.64 – 0.67 | **B3** (30m) | **B4** (30m) | **B4** (10m) | **B1** (250m) | NDVI, SAVI, EVI, chlorophyll absorption |
| **Red Edge 1** | ~0.705 | — | — | **B5** (20m) | — | NDRE, NDCI, early stress detection |
| **Red Edge 2** | ~0.740 | — | — | **B6** (20m) | — | Canopy chlorophyll content |
| **Red Edge 3** | ~0.783 | — | — | **B7** (20m) | — | Red edge transition zone |
| **NIR (Broad)** | ~0.83 – 0.88 | **B4** (30m) | **B5** (30m) | **B8** (10m) | **B2** (250m) | Standard vegetation reflectance |
| **NIR (Narrow)** | ~0.865 | — | — | **B8A** (20m) | — | Vegetation water & narrow band ratios |
| **Water Vapour** | ~0.945 | — | — | **B9** (60m) | — | Atmospheric column water vapour |
| **Cirrus / SWIR** | ~1.37 | — | **B9** (30m) | **B10** (60m) | **B26** (1000m) | High-altitude cirrus cloud detection |
| **SWIR 1** | ~1.57 – 1.65 | **B5** (30m) | **B6** (30m) | **B11** (20m) | **B6** (500m) | NDMI, MNDWI, NDBI, soil & leaf moisture |
| **SWIR 2** | ~2.11 – 2.29 | **B7** (30m) | **B7** (30m) | **B12** (20m) | **B7** (500m) | NBR burn severity, clay minerals, geology |
| **Thermal 1** | ~10.4 – 11.3 | **B6** (60m TM / 120m ETM+) | **B10** (100m resampled to 30m) | — | **B31** (1000m) | Surface Temperature (LST) calculation |
| **Thermal 2** | ~11.5 – 12.5 | — | **B11** (100m resampled to 30m) | — | **B32** (1000m) | Split-window atmospheric correction |

> [!IMPORTANT]
> **Spatial Resolution Co-registration:**  
> When calculating indices like **NDMI** or **MNDWI** on Sentinel-2, combining **10m bands** (B3, B4, B8) with **20m bands** (B11, B12, B8A) requires an explicit resampling step (typically bilinear or nearest-neighbor) to a unified target grid. Never combine different pixel grids implicitly.

---

## 2. Product Scaling Factors and Radiometric Levels

### A. USGS Landsat Collection 2 Level-2 Surface Reflectance (L2 SR)
Raw stored Digital Numbers (DN) in Collection 2 L2 SR files are scaled integer numbers. They must be unpacked to true surface reflectance ($0.0 \text{ to } 1.0$) using the official formula:

$$\text{Reflectance} = \text{DN} \times 0.0000275 - 0.2$$

* **Sample verification:**
  * Raw stored $\text{DN} = 18639$
  * $\text{Reflectance} = 18639 \times 0.0000275 - 0.2 = 0.5125725 - 0.2 = 0.3125725$
* **Surface Temperature (Band 10):**
  $$\text{ST} = \text{DN} \times 0.00341802 + 149.0 \quad (\text{Kelvin})$$

> [!WARNING]
> **DO NOT confuse band scaling with Ready-Made USGS Index products:**  
> If using pre-computed USGS spectral index products (e.g. Landsat NDVI or NDMI geotiffs), the values are stored as 16-bit signed integers with a scale factor of `0.0001`:  
> $\text{NDVI} = \text{DN} \times 0.0001$ (stored range $-10000 \text{ to } +10000$). Never apply the band scaling equation ($0.0000275 - 0.2$) to an index product!

For archived Landsat 8 Collection 1 Level-2 surface reflectance, the scale
is 0.0001, the offset is zero and the fill value is -9999. Its pixel_qa bits
differ from Collection 2 QA_PIXEL. Identify the product from its metadata
before choosing a scale or mask. The synthetic paired-pixel fixture covers
both collections with B4 red and B5 near-infrared. Level-1 TOA products and
pre-collection scenes require their own calibration and QA interpretation.
[USGS scaling comparison](https://www.usgs.gov/faqs/why-are-fill-values-and-scaling-factors-landsat-collection-2-level-2-products-different-those) · [Collection 1 LaSRC Product Guide](https://www.usgs.gov/media/files/landsat-8-collection-1-land-surface-reflectance-code-product-guide) · [Collection 2 QA bands](https://www.usgs.gov/landsat-missions/landsat-collection-2-quality-assessment-bands)

### B. Copernicus Sentinel-2 MSI Level-2A (Bottom-Of-Atmosphere Reflectance)
* **Processing Baselines prior to 04.00 (before 25 Jan 2022):**
  $$\text{Reflectance} = \frac{\text{DN}}{10000.0}$$
* **Processing Baseline 04.00+ (from 25 Jan 2022 onwards):**
  To prevent clipping of negative surface reflectance over dark surfaces and water, an offset of $-1000$ DN was introduced (`BOA_ADD_OFFSET = -1000`):
  $$\text{Reflectance} = \frac{\text{DN} + \text{BOA\_ADD\_OFFSET}}{10000.0} = \frac{\text{DN} - 1000}{10000.0}$$
  * Check image metadata XML (`MTD_MSIL2A.xml` or STAC asset metadata) for `BOA_ADD_OFFSET` to ensure seamless multi-year time-series alignment.

### C. NASA Harmonized Landsat and Sentinel-2 (HLS v2.0)
* **Products:** `HLSL30` (Landsat 8-9 30m) and `HLSS30` (Sentinel-2 30m).
* **NBAR (Nadir BRDF-Adjusted Reflectance):**
  * Bandpass adjusted and normalized to nadir viewing geometry at local solar noon.
  * Stored with scale factor `0.0001` and offset `0.0`. Valid reflectance is $\text{DN} \times 0.0001$.

---

## 3. Cloud, Shadow, and Quality Pixel Masking (QA)

Relying on scene-level metadata (e.g. `CLOUD_COVER < 10%`) is insufficient for scientific workflows. Per-pixel QA bitmasks must be interrogated.

### A. Landsat Collection 2 `QA_PIXEL` Bitmask Table
| Bit Position | Bit Value | Flag Interpretation | Required Filter Action |
|---|---|---|---|
| **Bit 0** | 1 | Fill (NoData) | Mask out |
| **Bit 1** | 2 | Dilated Cloud | Mask out |
| **Bit 2** | 4 | Cirrus Cloud (High Confidence) | Mask out |
| **Bit 3** | 8 | Cloud (High Confidence) | Mask out |
| **Bit 4** | 16 | Cloud Shadow | Mask out |
| **Bit 5** | 32 | Snow / Ice | Evaluate per application |
| **Bit 6** | 64 | Clear (no cloud, shadow, or snow) | Retain |
| **Bit 7** | 128 | Water body | Retain / Mask depending on target |

### B. Sentinel-2 Scene Classification Layer (`SCL`)
| Class Value | Class Description | Quality Status for Land Vegetation |
|---|---|---|
| **0** | No Data (missing pixel) | Mask out |
| **1** | Saturated or Defective | Mask out |
| **2** | Dark Area Pixels | Evaluate (shadow risk) |
| **3** | Cloud Shadows | Mask out |
| **4** | Vegetation | Retain |
| **5** | Not Vegetated / Bare Soil | Retain |
| **6** | Water | Mask out for vegetation / Retain for water |
| **7** | Unclassified | Mask out or inspect |
| **8** | Cloud Medium Probability | Mask out |
| **9** | Cloud High Probability | Mask out |
| **10** | Thin Cirrus | Mask out |
| **11** | Snow / Ice | Mask out for vegetation |

---

## 4. SAR Polarimetry: Linear Intensity vs Decibels (dB)

For Sentinel-1, ALOS PALSAR, and Radarsat SAR imagery:

$$\text{Power (Linear Intensity)} = 10^{\frac{\text{dB}}{10}}$$
$$\text{dB} = 10 \times \log_{10}(\text{Linear Intensity})$$

* **Ratio Operations:**
  * In linear intensity units: $\text{Ratio} = \frac{\text{VH}_{\text{lin}}}{\text{VV}_{\text{lin}}}$
  * In logarithmic dB units: $\text{Ratio}_{\text{dB}} = \text{VH}_{\text{dB}} - \text{VV}_{\text{dB}}$
* **Radar Vegetation Index (RVI):**
  $$\text{RVI} = \frac{4 \times \text{VH}_{\text{lin}}}{\text{VV}_{\text{lin}} + \text{VH}_{\text{lin}}}$$
  > [!CAUTION]
  > Never calculate Radar RVI using values in decibels ($\text{dB}$). You must convert $\text{dB}$ to linear intensity power before calculating ratios or fractions.
