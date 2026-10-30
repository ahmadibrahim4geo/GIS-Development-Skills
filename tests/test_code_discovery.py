"""Tests for GIS Code Discovery & Reuse (Deterministic offline unit tests)."""
import copy
import json
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import gis_code_discovery as cd
import intent_router as router


class GISCodeDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.sources = cd.load_registry(ROOT / "references" / "gis-code-sources.json")
        self.recipes = cd.load_registry(ROOT / "references" / "gis-code-recipes.json")

    def test_01_arcgis_pro_sdk_button_routing(self):
        """Scenario 1: ArcGIS Pro SDK ribbon button routes to C# with QueuedTask constraint."""
        query = "Create ArcGIS Pro SDK ribbon button with QueuedTask in C#"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        self.assertIn("arcgis-pro-sdk", res["detected_platforms"])
        top_recipe = res["matching_recipes"][0]
        self.assertEqual(top_recipe["id"], "recipe-arcgis-pro-sdk-button")
        self.assertEqual(top_recipe["language"], "C#")
        self.assertIn("QueuedTask.Run", top_recipe["code_snippet"])
        self.assertTrue(top_recipe["is_safe_to_adapt"])

    def test_02_pyqgis_processing_algorithm_subclassing(self):
        """Scenario 2: PyQGIS algorithm subclassing returns QgsProcessingAlgorithm template."""
        query = "PyQGIS processing algorithm plugin script"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        self.assertIn("pyqgis", res["detected_platforms"])
        top_recipe = res["matching_recipes"][0]
        self.assertEqual(top_recipe["id"], "recipe-qgis-processing-algorithm")
        self.assertEqual(top_recipe["language"], "Python")
        self.assertIn("QgsProcessingAlgorithm", top_recipe["code_snippet"])
        self.assertTrue(any("GPL" in issue for issue in top_recipe["issues"]))

    def test_03_gdal_rasterio_elevation_sampling(self):
        """Scenario 3: GDAL/Rasterio raster elevation sampling with CRS and NoData."""
        query = "sample raster elevation at points geotiff nodata dem"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        self.assertIn("gdal-rasterio", res["detected_platforms"])
        top_recipe = res["matching_recipes"][0]
        self.assertEqual(top_recipe["id"], "recipe-sample-raster-at-points")
        self.assertIn("src.nodata", top_recipe["code_snippet"])
        self.assertEqual(top_recipe["state"], "tested")

    def test_04_web_gis_maplibre_initialization(self):
        """Scenario 4: Web GIS MapLibre vector tile initialization."""
        query = "web gis maplibre vector tiles interactive map"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        self.assertIn("web-gis", res["detected_platforms"])
        top_recipe = res["matching_recipes"][0]
        self.assertEqual(top_recipe["id"], "recipe-maplibre-vector-tiles")
        self.assertEqual(top_recipe["language"], "JavaScript")
        self.assertIn("maplibregl.Map", top_recipe["code_snippet"])

    def test_05_kml_kmz_hex_inversion(self):
        """Scenario 5: KML placemark color hex inversion aabbggrr -> rrggbbaa."""
        query = "kml placemark style color aabbggrr"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        self.assertIn("kml-kmz", res["detected_platforms"])
        top_recipe = res["matching_recipes"][0]
        self.assertEqual(top_recipe["id"], "recipe-kml-style-preservation")
        self.assertIn("aabbggrr", top_recipe["code_snippet"])

    def test_06_unverified_license_rejection(self):
        """Scenario 6: Candidate with unverified license is blocked from direct copy."""
        synthetic_candidate = {
            "title": "Unverified GIS Algorithm",
            "domain": "raster-analysis",
            "language": "Python",
            "license": "unverified",
            "code_snippet": "def algo(): pass"
        }
        evaluation = cd.evaluate_candidate(synthetic_candidate, "raster analysis python")
        self.assertFalse(evaluation["is_safe_to_adapt"])
        self.assertTrue(any("Unverified license" in issue for issue in evaluation["issues"]))

    def test_07_missing_source_fallback(self):
        """Scenario 7: Queries with empty or absent sources handle gracefully without error."""
        empty_sources = {"sources": []}
        empty_recipes = {"recipes": []}
        res = cd.search_knowledge_base("unmatched query", sources_data=empty_sources, recipes_data=empty_recipes)
        self.assertEqual(len(res["matching_recipes"]), 0)
        self.assertEqual(len(res["matching_sources"]), 0)

    def test_08_version_and_platform_mismatch_detection(self):
        """Scenario 8: Candidate evaluated against mismatched target platform is penalized."""
        candidate = {
            "title": "QGIS Python Plugin",
            "domain": "pyqgis",
            "language": "Python",
            "license": "GPL-2.0-or-later"
        }
        eval_mismatch = cd.evaluate_candidate(candidate, "create button", target_platform="arcgis-pro-sdk")
        self.assertTrue(any("Platform mismatch: expected arcgis-pro-sdk" in issue for issue in eval_mismatch["issues"]))

    def test_09_no_hallucinated_libraries_on_nonsense_query(self):
        """Scenario 9: Bogus nonsense query yields low scores without making up metadata."""
        query = "xyzzy99nonsensefakequery123"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        for r in res["matching_recipes"]:
            self.assertLessEqual(r["score"], 40)
        for s in res["matching_sources"]:
            self.assertLessEqual(s["score"], 40)

    def test_10_router_integration_bilingual(self):
        """Scenario 10: Intent router suggests gis-code-discovery for bilingual prompts."""
        en_prompt = "Find a GIS code snippet for raster elevation sampling"
        ar_prompt = "ابحث عن كود جغرافي لاستخراج قيم الارتفاع"
        
        en_hints = router.route_hints(en_prompt)["suggested_skills"]
        ar_hints = router.route_hints(ar_prompt)["suggested_skills"]
        
        self.assertIn("gis-code-discovery", en_hints)
        self.assertIn("gis-code-discovery", ar_hints)

    def test_11_opengeohub_scikit_map_source_retrieval(self):
        """Scenario 11: scikit-map is discovered for spatial prediction with MIT license."""
        query = "spatial prediction machine learning scikit-map"
        res = cd.search_knowledge_base(query, sources_data=self.sources, recipes_data=self.recipes)
        top_source = res["matching_sources"][0]
        self.assertEqual(top_source["id"], "openlandmap-scikit-map")
        self.assertEqual(top_source["license"], "MIT")
        self.assertIn("spatial-modeling", res["detected_platforms"])

    def test_12_unverified_license_flagged_for_soildb(self):
        """Scenario 12: soildb research reference has unverified license and limitation warnings."""
        soildb = next((s for s in self.sources["sources"] if s["source_id"] == "openlandmap-soildb"), None)
        self.assertIsNotNone(soildb)
        self.assertFalse(soildb["license_verified"])
        self.assertEqual(soildb["license"], "unknown")
        self.assertIn("no copying", soildb["limitations"])

    def test_13_router_scenarios_from_user_guidelines(self):
        """Scenario 13: The five user routing scenarios route to appropriate skills."""
        s1 = router.route_hints("ابحث عن كود Python للتنبؤ المكاني")["suggested_skills"]
        self.assertIn("gis-code-discovery", s1)

        s2 = router.route_hints("اكتشف خرائط خصائص التربة لمنطقة جغرافية محددة")["suggested_skills"]
        self.assertIn("geospatial-data-discovery", s2)

        s3 = router.route_hints("ابحث عن منتجات Land Cover ذات تغطية زمنية")["suggested_skills"]
        self.assertIn("geospatial-data-discovery", s3)
        self.assertIn("remote-sensing-pipelines", s3)

        s4 = router.route_hints("حدد إمكانية استعراض طبقة COG داخل تطبيق GIS")["suggested_skills"]
        self.assertIn("remote-sensing-pipelines", s4)

        s5 = router.route_hints("قارن بين مصدر بيانات مفتوح ومستودع يضم كودًا بحثيًا")["suggested_skills"]
        self.assertIn("gis-code-discovery", s5)
        self.assertIn("geospatial-data-catalogs", s5)


if __name__ == "__main__":
    unittest.main()
