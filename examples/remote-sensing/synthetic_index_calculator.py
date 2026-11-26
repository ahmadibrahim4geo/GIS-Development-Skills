#!/usr/bin/env python3
"""Synthetic Remote Sensing Index Calculator and Evaluation Engine.

Provides exact, deterministic calculations for core optical and SAR spectral indices,
sensor Level-2 unpacking, alias disambiguation, and contextual threshold guards.
Uses Python standard library (no mandatory third-party requirements).
"""
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

ROOT = Path(__file__).resolve().parents[2]
INDICES_PATH = ROOT / "references" / "remote-sensing-indices.json"
THRESHOLDS_PATH = ROOT / "references" / "remote-sensing-threshold-profiles.json"
SOURCES_PATH = ROOT / "references" / "remote-sensing-index-source-registry.json"


def load_json_resource(path: Path) -> Dict[str, Any]:
    """Load and parse a JSON resource safely."""
    if not path.is_file():
        raise FileNotFoundError(f"Required resource not found: {path}")
    return json.loads(path.read_text(encoding="utf-8"))


# --- Level-2 Radiometric Unpacking ---

def unpack_landsat_c2_l2_sr(raw_dn: Union[int, float]) -> float:
    """Unpack USGS Landsat Collection 2 Level-2 Surface Reflectance.
    
    Formula: Reflectance = DN * 0.0000275 - 0.2
    Valid surface reflectance range: 0.0 to 1.0 (slight negatives may occur over water/shadow).
    """
    if raw_dn == 0 or raw_dn is None:
        return float("nan")
    return raw_dn * 0.0000275 - 0.2


def unpack_landsat_c2_l2_st(raw_dn: Union[int, float]) -> float:
    """Unpack USGS Landsat Collection 2 Level-2 Surface Temperature.
    
    Formula: ST = DN * 0.00341802 + 149.0 (Kelvin)
    """
    if raw_dn == 0 or raw_dn is None:
        return float("nan")
    return raw_dn * 0.00341802 + 149.0


def unpack_sentinel2_l2a_sr(raw_dn: Union[int, float], processing_baseline_above_04: bool = True) -> float:
    """Unpack Copernicus Sentinel-2 MSI Level-2A Bottom-Of-Atmosphere (BOA) Reflectance.
    
    For PB >= 04.00: Reflectance = (DN - 1000) / 10000.0 (BOA_ADD_OFFSET = -1000)
    For older PB: Reflectance = DN / 10000.0
    """
    if raw_dn == 0 or raw_dn is None:
        return float("nan")
    offset = 1000.0 if processing_baseline_above_04 else 0.0
    return (raw_dn - offset) / 10000.0


def db_to_linear_power(backscatter_db: float) -> float:
    """Convert SAR backscatter from decibels (dB) to linear intensity power.
    
    Formula: Power = 10^(dB / 10.0)
    """
    if math.isnan(backscatter_db) or math.isinf(backscatter_db):
        return float("nan")
    return 10.0 ** (backscatter_db / 10.0)


# --- Core Scientific Index Calculations ---

def calc_ndvi(nir: float, red: float) -> float:
    """Calculate Normalized Difference Vegetation Index (Rouse et al. 1974).
    
    Formula: (NIR - RED) / (NIR + RED)
    """
    if math.isnan(nir) or math.isnan(red):
        return float("nan")
    denom = nir + red
    if abs(denom) < 1e-7:
        return float("nan")
    return (nir - red) / denom


def landsat8_l2_ndvi(collection, bands, qa_name, qa_value):
    """NDVI for a paired Landsat 8 L2 SR fixture pixel; None represents a mask.

    Expects aligned, calibrated product inputs identified from the actual scene
    metadata. It does not infer the collection from acquisition date or filenames.
    This narrow vegetation fixture masks snow, cloud and shadow; saturation and
    aerosol screening are separate scene-level requirements.
    """
    if type(collection) is not int or collection not in (1, 2):
        raise ValueError("Landsat 8 Collection 1 or 2 Level-2 SR is required")
    expected_qa = "pixel_qa" if collection == 1 else "QA_PIXEL"
    if qa_name != expected_qa or type(qa_value) is not int or not 0 <= qa_value <= 65535:
        raise ValueError("QA band or encoded value does not match the selected collection")
    if not isinstance(bands, dict) or not {"B4", "B5"} <= bands.keys():
        raise ValueError("Landsat 8 requires named B4 red and B5 near-infrared inputs")
    red, nir = bands["B4"], bands["B5"]
    minimum, maximum = (-32768, 32767) if collection == 1 else (0, 65535)
    if any(type(dn) is not int or not minimum <= dn <= maximum for dn in (red, nir)):
        raise ValueError("Reflectance DN does not fit the declared product encoding")
    if collection == 1:
        rejected_bits = 1 | 8 | 16 | 32 | 1024
        if red in (-9999, 20000) or nir in (-9999, 20000) or qa_value & rejected_bits or (qa_value >> 8) & 3 == 3:
            return None
        value = calc_ndvi(nir * 0.0001, red * 0.0001)
    else:
        if red == 0 or nir == 0 or qa_value & 0b111111:
            return None
        value = calc_ndvi(unpack_landsat_c2_l2_sr(nir), unpack_landsat_c2_l2_sr(red))
    return value if math.isfinite(value) else None


def calc_evi(nir: float, red: float, blue: float, g: float = 2.5, c1: float = 6.0, c2: float = 7.5, l: float = 1.0) -> float:
    """Calculate Enhanced Vegetation Index (Huete et al. 2002).
    
    Formula: G * (NIR - RED) / (NIR + C1 * RED - C2 * BLUE + L)
    """
    if any(math.isnan(x) for x in (nir, red, blue)):
        return float("nan")
    denom = nir + c1 * red - c2 * blue + l
    if abs(denom) < 1e-7:
        return float("nan")
    return g * (nir - red) / denom


def calc_evi2(nir: float, red: float, g: float = 2.5, c: float = 2.4, l: float = 1.0) -> float:
    """Calculate Two-Band Enhanced Vegetation Index (Jiang et al. 2008).
    
    Formula: G * (NIR - RED) / (NIR + C * RED + L)
    """
    if math.isnan(nir) or math.isnan(red):
        return float("nan")
    denom = nir + c * red + l
    if abs(denom) < 1e-7:
        return float("nan")
    return g * (nir - red) / denom


def calc_savi(nir: float, red: float, l: float = 0.5) -> float:
    """Calculate Soil-Adjusted Vegetation Index (Huete 1988).
    
    Formula: ((NIR - RED) / (NIR + RED + L)) * (1.0 + L)
    """
    if math.isnan(nir) or math.isnan(red):
        return float("nan")
    denom = nir + red + l
    if abs(denom) < 1e-7:
        return float("nan")
    return ((nir - red) / denom) * (1.0 + l)


def calc_msavi(nir: float, red: float) -> float:
    """Calculate Modified Soil-Adjusted Vegetation Index (Qi et al. 1994).
    
    Formula: (2 * NIR + 1 - sqrt((2 * NIR + 1)^2 - 8 * (NIR - RED))) / 2
    """
    if math.isnan(nir) or math.isnan(red):
        return float("nan")
    term = 2.0 * nir + 1.0
    discriminant = term * term - 8.0 * (nir - red)
    if discriminant < 0:
        return float("nan")
    return (term - math.sqrt(discriminant)) / 2.0


def calc_ndwi_water(green: float, nir: float) -> float:
    """Calculate Normalized Difference Water Index for Open Surface Water (McFeeters 1996).
    
    Formula: (GREEN - NIR) / (GREEN + NIR)
    """
    if math.isnan(green) or math.isnan(nir):
        return float("nan")
    denom = green + nir
    if abs(denom) < 1e-7:
        return float("nan")
    return (green - nir) / denom


def calc_ndwi_moisture(nir: float, swir1: float) -> float:
    """Calculate Normalized Difference Water Index for Canopy Moisture / NDMI (Gao 1996).
    
    Formula: (NIR - SWIR1) / (NIR + SWIR1)
    """
    if math.isnan(nir) or math.isnan(swir1):
        return float("nan")
    denom = nir + swir1
    if abs(denom) < 1e-7:
        return float("nan")
    return (nir - swir1) / denom


def calc_mndwi(green: float, swir1: float) -> float:
    """Calculate Modified Normalized Difference Water Index (Xu 2006).
    
    Formula: (GREEN - SWIR1) / (GREEN + SWIR1)
    """
    if math.isnan(green) or math.isnan(swir1):
        return float("nan")
    denom = green + swir1
    if abs(denom) < 1e-7:
        return float("nan")
    return (green - swir1) / denom


def calc_nbr(nir: float, swir2: float) -> float:
    """Calculate Normalized Burn Ratio (Key & Benson 2006).
    
    Formula: (NIR - SWIR2) / (NIR + SWIR2)
    """
    if math.isnan(nir) or math.isnan(swir2):
        return float("nan")
    denom = nir + swir2
    if abs(denom) < 1e-7:
        return float("nan")
    return (nir - swir2) / denom


def calc_dnbr(nbr_pre: float, nbr_post: float, scale_by_1000: bool = False) -> float:
    """Calculate Differenced Normalized Burn Ratio (Key & Benson 2006).
    
    Formula: NBR_pre - NBR_post
    """
    if math.isnan(nbr_pre) or math.isnan(nbr_post):
        return float("nan")
    diff = nbr_pre - nbr_post
    return diff * 1000.0 if scale_by_1000 else diff


def calc_ndsi_snow(green: float, swir1: float, nir: Optional[float] = None, require_nir_condition: bool = True) -> Tuple[float, bool]:
    """Calculate Normalized Difference Snow Index (Hall et al. 1995).
    
    Returns (ndsi_value, is_snow_classified).
    Condition: NDSI >= 0.4 AND (NIR >= 0.11 if require_nir_condition is True)
    """
    if math.isnan(green) or math.isnan(swir1):
        return float("nan"), False
    denom = green + swir1
    if abs(denom) < 1e-7:
        return float("nan"), False
    ndsi = (green - swir1) / denom
    is_snow = ndsi >= 0.4
    if require_nir_condition and nir is not None:
        is_snow = is_snow and (nir >= 0.11)
    return ndsi, is_snow


def calc_ndci(red_edge: float, red: float) -> float:
    """Calculate Normalized Difference Chlorophyll Index for Water Quality (Mishra & Mishra 2012).
    
    Formula: (RedEdge - Red) / (RedEdge + Red)
    """
    if math.isnan(red_edge) or math.isnan(red):
        return float("nan")
    denom = red_edge + red
    if abs(denom) < 1e-7:
        return float("nan")
    return (red_edge - red) / denom


def calc_rvi_sar(vv_linear: float, vh_linear: float) -> float:
    """Calculate Radar Vegetation Index from Dual-Pol SAR linear power intensity.
    
    Formula: (4.0 * VH) / (VV + VH)
    Inputs MUST be in linear power, NOT decibels (dB)!
    """
    if math.isnan(vv_linear) or math.isnan(vh_linear) or vv_linear < 0 or vh_linear < 0:
        return float("nan")
    denom = vv_linear + vh_linear
    if abs(denom) < 1e-7:
        return float("nan")
    return (4.0 * vh_linear) / denom


def calc_rvi_optical(nir: float, red: float) -> float:
    """Calculate Optical Ratio Vegetation Index (Jordan 1969 Simple Ratio).
    
    Formula: NIR / Red
    """
    if math.isnan(nir) or math.isnan(red) or red <= 1e-7:
        return float("nan")
    return nir / red


# --- Alias Disambiguation Resolver ---

def resolve_index_alias(acronym: str, target_domain_or_goal: Optional[str] = None) -> Dict[str, Any]:
    """Resolve ambiguous index acronyms based on the scientific application domain."""
    norm_acronym = acronym.strip().upper()
    norm_goal = (target_domain_or_goal or "").strip().lower()

    if norm_acronym == "NDWI":
        if any(term in norm_goal for term in ["water", "flood", "lake", "river", "coast", "مياه", "فيضان", "سطحية"]):
            return {
                "id": "NDWI_McFeeters_1996",
                "formula": "(GREEN - NIR) / (GREEN + NIR)",
                "application": "Open surface water delineation",
                "citation": "McFeeters (1996)",
                "disambiguation": "Selected McFeeters 1996 because target domain is surface water bodies."
            }
        elif any(term in norm_goal for term in ["moisture", "canopy", "vegetation", "drought", "plant", "رطوبة", "نبات", "جفاف"]):
            return {
                "id": "NDWI_Gao_1996",
                "formula": "(NIR - SWIR) / (NIR + SWIR)",
                "application": "Canopy liquid water content (NDMI / LSWI)",
                "citation": "Gao (1996)",
                "disambiguation": "Selected Gao 1996 (NDMI) because target domain is plant canopy moisture."
            }
        else:
            return {
                "id": "AMBIGUOUS_NDWI",
                "candidates": ["NDWI_McFeeters_1996", "NDWI_Gao_1996"],
                "clarification_needed": "Specify whether you want open surface water bodies (McFeeters: Green-NIR) or plant canopy moisture (Gao/NDMI: NIR-SWIR)."
            }

    if norm_acronym == "NDSI":
        if any(term in norm_goal for term in ["salinity", "soil", "salt", "ملوحة", "تربة"]):
            return {
                "id": "NDSI_Salinity",
                "application": "Soil salinity index",
                "disambiguation": "Selected soil salinity index based on soil domain."
            }
        else:
            return {
                "id": "NDSI_Hall_1995",
                "formula": "(GREEN - SWIR1) / (GREEN + SWIR1)",
                "application": "Snow and ice mapping (requires NIR >= 0.11 condition)",
                "citation": "Hall et al. (1995)",
                "disambiguation": "Selected Hall 1995 snow index. Note that NIR >= 0.11 is mandatory to separate snow from open water."
            }

    if norm_acronym == "RVI":
        if any(term in norm_goal for term in ["sar", "radar", "microwave", "polarimetric", "رادار", "سار"]):
            return {
                "id": "RVI_Radar_Charbonneau_2005",
                "formula": "(4.0 * VH_lin) / (VV_lin + VH_lin)",
                "application": "Radar Vegetation Index from linear SAR backscatter",
                "citation": "Charbonneau et al. (2005)",
                "disambiguation": "Selected Polarimetric Radar Vegetation Index. Requires inputs in linear power intensity (not dB)."
            }
        else:
            return {
                "id": "RVI_Ratio_Jordan_1969",
                "formula": "NIR / RED",
                "application": "Optical Simple Ratio (Jordan 1969)",
                "citation": "Jordan (1969)",
                "disambiguation": "Selected optical simple ratio (NIR/Red)."
            }

    return {"id": norm_acronym, "status": "no_collision_detected"}


# --- Threshold Profile Guard ---

def evaluate_threshold_profile_guard(profile: Dict[str, Any], test_value: float) -> Dict[str, Any]:
    """Evaluate a threshold profile against safety constraints.
    
    Prevents automatic uncalibrated classification if the profile is not approved.
    """
    is_approved = profile.get("approved_for_automatic_classification", False)
    if not is_approved:
        return {
            "status": "REJECTED_UNAPPROVED",
            "profile_id": profile.get("id"),
            "reason": "Profile is illustrative or conditional. Automatic classification without local field validation is prohibited.",
            "caveats": profile.get("caveats", [])
        }

    classes = profile.get("classes", [])
    matched_class = None
    for cls in classes:
        if cls.get("min", -float("inf")) <= test_value < cls.get("max", float("inf")):
            matched_class = cls.get("class_name")
            break

    return {
        "status": "EVALUATED",
        "profile_id": profile.get("id"),
        "test_value": test_value,
        "matched_class": matched_class
    }
