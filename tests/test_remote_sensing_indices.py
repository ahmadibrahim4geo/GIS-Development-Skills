#!/usr/bin/env python3
"""Unit tests for Remote Sensing Indices, Sensor Band Mappings, and Interpretation Rules.

Verifies mathematical accuracy, Level-2 scaling, edge case handling,
alias collision resolution, threshold safety guards, and schema integrity.
"""
import importlib.util
import json
import math
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CALC_SCRIPT = ROOT / "examples" / "remote-sensing" / "synthetic_index_calculator.py"

spec = importlib.util.spec_from_file_location("synthetic_index_calculator", CALC_SCRIPT)
calc_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(calc_mod)


class RemoteSensingIndicesTests(unittest.TestCase):
    """Test mathematical formulas and scientific edge cases."""

    def test_ndvi_exact_calculation(self):
        # Rouse et al. 1974: (NIR - RED) / (NIR + RED)
        result = calc_mod.calc_ndvi(nir=0.6, red=0.2)
        self.assertAlmostEqual(result, 0.5, places=5)

    def test_ndvi_zero_denominator_returns_nan(self):
        result = calc_mod.calc_ndvi(nir=0.0, red=0.0)
        self.assertTrue(math.isnan(result))

    def test_ndvi_negative_inputs_or_shadow(self):
        # Dark shadow or uncorrected water where Red > NIR
        result = calc_mod.calc_ndvi(nir=0.05, red=0.15)
        self.assertAlmostEqual(result, -0.5, places=5)

    def test_ndwi_water_mcfeeters(self):
        # McFeeters 1996: (GREEN - NIR) / (GREEN + NIR)
        result = calc_mod.calc_ndwi_water(green=0.3, nir=0.1)
        self.assertAlmostEqual(result, 0.5, places=5)

    def test_ndwi_moisture_gao(self):
        # Gao 1996: (NIR - SWIR) / (NIR + SWIR)
        result = calc_mod.calc_ndwi_moisture(nir=0.5, swir1=0.3)
        self.assertAlmostEqual(result, 0.25, places=5)

    def test_savi_soil_adjustment(self):
        # Huete 1988: ((NIR - RED) / (NIR + RED + L)) * (1 + L) with L=0.5
        # ((0.6 - 0.2) / (0.6 + 0.2 + 0.5)) * 1.5 = (0.4 / 1.3) * 1.5 = 0.461538...
        result = calc_mod.calc_savi(nir=0.6, red=0.2, l=0.5)
        expected = (0.4 / 1.3) * 1.5
        self.assertAlmostEqual(result, expected, places=5)

    def test_evi_three_band_formulation(self):
        # Huete et al. 2002: 2.5 * (NIR - RED) / (NIR + 6*RED - 7.5*BLUE + 1)
        result = calc_mod.calc_evi(nir=0.6, red=0.2, blue=0.05)
        # Denominator: 0.6 + 6(0.2) - 7.5(0.05) + 1.0 = 0.6 + 1.2 - 0.375 + 1.0 = 2.425
        # Numerator: 2.5 * 0.4 = 1.0
        # Result: 1.0 / 2.425 ~ 0.41237
        expected = 1.0 / 2.425
        self.assertAlmostEqual(result, expected, places=4)

    def test_msavi_radical_protection(self):
        # Normal canopy
        result = calc_mod.calc_msavi(nir=0.5, red=0.1)
        self.assertTrue(0.0 <= result <= 1.0)
        # Input causing negative discriminant (e.g. nir=0.5, red=-0.2 -> 4 - 5.6 = -1.6 < 0)
        result_noisy = calc_mod.calc_msavi(nir=0.5, red=-0.2)
        self.assertTrue(math.isnan(result_noisy))

    def test_dnbr_unscaled_and_scaled(self):
        # Key & Benson 2006
        unscaled = calc_mod.calc_dnbr(nbr_pre=0.8, nbr_post=0.1, scale_by_1000=False)
        self.assertAlmostEqual(unscaled, 0.7, places=5)
        scaled = calc_mod.calc_dnbr(nbr_pre=0.8, nbr_post=0.1, scale_by_1000=True)
        self.assertAlmostEqual(scaled, 700.0, places=2)

    def test_ndsi_snow_with_nir_gate(self):
        # Hall et al. 1995: Snow requires NDSI >= 0.4 AND NIR >= 0.11
        # Test 1: True snow (high Green, low SWIR, adequate NIR)
        val, is_snow = calc_mod.calc_ndsi_snow(green=0.7, swir1=0.2, nir=0.5)
        self.assertTrue(is_snow)
        self.assertGreater(val, 0.4)

        # Test 2: Water body (high Green, low SWIR, but VERY LOW NIR ~ 0.05)
        val_water, is_snow_water = calc_mod.calc_ndsi_snow(green=0.3, swir1=0.05, nir=0.04)
        self.assertGreater(val_water, 0.4)  # NDSI alone is positive
        self.assertFalse(is_snow_water)    # But NIR condition fails, preventing water misclassification

    def test_rvi_sar_linear_vs_db(self):
        # Charbonneau et al. 2005: 4 * VH / (VV + VH) in LINEAR power
        vv_lin = 0.1
        vh_lin = 0.03
        rvi = calc_mod.calc_rvi_sar(vv_linear=vv_lin, vh_linear=vh_lin)
        expected = (4.0 * 0.03) / (0.1 + 0.03)
        self.assertAlmostEqual(rvi, expected, places=5)

        # Verify db to linear conversion: -10 dB = 0.1 linear power
        self.assertAlmostEqual(calc_mod.db_to_linear_power(-10.0), 0.1, places=5)
        self.assertAlmostEqual(calc_mod.db_to_linear_power(0.0), 1.0, places=5)

    def test_rvi_optical_simple_ratio(self):
        # Jordan 1969: NIR / Red
        rvi_opt = calc_mod.calc_rvi_optical(nir=0.8, red=0.2)
        self.assertAlmostEqual(rvi_opt, 4.0, places=5)
        # Red near zero
        self.assertTrue(math.isnan(calc_mod.calc_rvi_optical(nir=0.8, red=0.0)))


class SensorLevel2UnpackingTests(unittest.TestCase):
    """Test Level-2 radiometric unpacking and scaling equations."""

    def test_landsat_c2_l2_sr_unscale(self):
        # Official USGS formula: SR = DN * 0.0000275 - 0.2
        # Example from brief: DN=18639 -> ~0.3125725
        sr = calc_mod.unpack_landsat_c2_l2_sr(18639)
        self.assertAlmostEqual(sr, 0.3125725, places=5)

    def test_landsat_c2_l2_st_unscale(self):
        # Official USGS formula: ST = DN * 0.00341802 + 149.0 (Kelvin)
        # Example: DN=44180 -> ~300.008 K
        st = calc_mod.unpack_landsat_c2_l2_st(44180)
        self.assertAlmostEqual(st, 300.00812, places=3)

    def test_sentinel2_l2a_offset_handling(self):
        # PB 04.00+ introduces -1000 BOA_ADD_OFFSET: SR = (DN - 1000) / 10000.0
        sr_new = calc_mod.unpack_sentinel2_l2a_sr(raw_dn=4125, processing_baseline_above_04=True)
        self.assertAlmostEqual(sr_new, 0.3125, places=5)

        # Older PB: SR = DN / 10000.0
        sr_old = calc_mod.unpack_sentinel2_l2a_sr(raw_dn=3125, processing_baseline_above_04=False)
        self.assertAlmostEqual(sr_old, 0.3125, places=5)


class AliasDisambiguationTests(unittest.TestCase):
    """Test alias collision resolution."""

    def test_ndwi_resolves_to_mcfeeters_for_surface_water(self):
        res = calc_mod.resolve_index_alias("NDWI", "delineate open water lake boundaries")
        self.assertEqual(res["id"], "NDWI_McFeeters_1996")
        self.assertIn("GREEN - NIR", res["formula"])

    def test_ndwi_resolves_to_gao_for_canopy_moisture(self):
        res = calc_mod.resolve_index_alias("NDWI", "measure vegetation canopy moisture and crop drought")
        self.assertEqual(res["id"], "NDWI_Gao_1996")
        self.assertIn("NIR - SWIR", res["formula"])

    def test_ndwi_ambiguous_without_domain(self):
        res = calc_mod.resolve_index_alias("NDWI", "")
        self.assertEqual(res["id"], "AMBIGUOUS_NDWI")
        self.assertIn("clarification_needed", res)

    def test_ndsi_resolves_to_snow_vs_salinity(self):
        res_snow = calc_mod.resolve_index_alias("NDSI", "mountain snow cover extent")
        self.assertEqual(res_snow["id"], "NDSI_Hall_1995")
        res_salinity = calc_mod.resolve_index_alias("NDSI", "soil salinity detection in arid farmland")
        self.assertEqual(res_salinity["id"], "NDSI_Salinity")

    def test_rvi_resolves_to_sar_vs_optical(self):
        res_sar = calc_mod.resolve_index_alias("RVI", "sentinel-1 sar polarimetric vegetation")
        self.assertEqual(res_sar["id"], "RVI_Radar_Charbonneau_2005")
        res_opt = calc_mod.resolve_index_alias("RVI", "optical multispectral simple ratio")
        self.assertEqual(res_opt["id"], "RVI_Ratio_Jordan_1969")


class SchemaAndSafetyGuardTests(unittest.TestCase):
    """Test JSON resource schemas and threshold safety guards."""

    def test_indices_catalog_schema(self):
        path = ROOT / "references" / "remote-sensing-indices.json"
        data = calc_mod.load_json_resource(path)
        self.assertEqual(data.get("schema_version"), "1.0")
        indices = data.get("indices", [])
        self.assertGreaterEqual(len(indices), 15)

        ids = [idx["id"] for idx in indices]
        self.assertEqual(len(ids), len(set(ids)), "Index IDs must be strictly unique")

        for idx in indices:
            self.assertIn("acronym", idx)
            self.assertIn("formula", idx)
            self.assertIn("domain", idx)
            self.assertIn("mathematical_range", idx)
            self.assertIn("science_references", idx)
            self.assertGreater(len(idx["science_references"]), 0)

    def test_threshold_profiles_safety_guard(self):
        path = ROOT / "references" / "remote-sensing-threshold-profiles.json"
        data = calc_mod.load_json_resource(path)
        profiles = data.get("profiles", [])
        self.assertGreaterEqual(len(profiles), 2)

        for profile in profiles:
            # Check that profiles are NOT automatically approved for uncalibrated global use
            self.assertFalse(
                profile.get("approved_for_automatic_classification", False),
                f"Profile {profile['id']} must not claim uncalibrated universal automatic classification"
            )
            # Evaluate against the safety guard
            guard_result = calc_mod.evaluate_threshold_profile_guard(profile, test_value=0.5)
            self.assertEqual(guard_result["status"], "REJECTED_UNAPPROVED")
            self.assertIn("caveats", guard_result)

    def test_source_registry_schema(self):
        path = ROOT / "references" / "remote-sensing-index-source-registry.json"
        data = calc_mod.load_json_resource(path)
        sources = data.get("sources", [])
        self.assertGreaterEqual(len(sources), 10)

        source_ids = [s["id"] for s in sources]
        self.assertEqual(len(source_ids), len(set(source_ids)), "Source IDs must be strictly unique")

        for s in sources:
            self.assertIn("title", s)
            self.assertIn("organization", s)
            self.assertIn("url", s)
            self.assertIn("authoritative_for", s)
            self.assertIn("license_status", s)


if __name__ == "__main__":
    unittest.main()
