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
        """An incompatible host blocks adaptation even when a recipe has a license."""
        candidate = {
            "title": "QGIS Python Plugin",
            "domain": "pyqgis",
            "language": "Python",
            "license": "GPL-2.0-or-later"
        }
        eval_mismatch = cd.evaluate_candidate(candidate, "create button", target_platform="arcgis-pro-sdk")
        self.assertTrue(any("Platform mismatch: expected arcgis-pro-sdk" in issue for issue in eval_mismatch["issues"]))
        self.assertFalse(eval_mismatch["applicable"])
        self.assertFalse(eval_mismatch["is_safe_to_adapt"])
        self.assertEqual(eval_mismatch["score"], 0)

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

    def test_14_generic_ui_terms_do_not_identify_arcgis(self):
        for query in ("ribbon", "button", ".NET add-in", "C# dockpane", "plugin"):
            with self.subTest(query=query):
                self.assertEqual(cd.detect_platforms(query), ["generic-gis"])

    def test_15_qgis_ribbon_never_returns_arcgis_implementation(self):
        for query in (
            "Convert QGIS tools to a ribbon",
            "Create QGIS ribbon button",
            "حول أدوات QGIS إلى ribbon واربطها بمحرك UI.js",
        ):
            with self.subTest(query=query):
                res = cd.search_knowledge_base(query)
                self.assertEqual(res["selected_platforms"], ["pyqgis"])
                # No catalog recipe implements this migration. Neither a Pro button
                # nor an unrelated QGIS Processing stub is a ribbon implementation.
                self.assertEqual(res["matching_recipes"], [])
                arcgis = next(r for r in res["research_recipes"]
                              if r["id"] == "recipe-arcgis-pro-sdk-button")
                self.assertEqual(arcgis["use"], "reference-only")
                self.assertFalse(arcgis["is_safe_to_adapt"])
                self.assertNotIn("code_snippet", arcgis)

    def test_16_unknown_ui_engine_does_not_choose_an_implementation(self):
        res = cd.search_knowledge_base("Use UI.js for the interface of my GIS app")
        self.assertEqual(res["platform_resolution"], "unresolved")
        self.assertEqual(res["status"], "unresolved")
        self.assertEqual(res["selected_platforms"], [])
        self.assertEqual(res["matching_recipes"], [])
        self.assertEqual(res["matching_sources"], [])

    def test_17_declared_target_blocks_incompatible_query_hints(self):
        res = cd.search_knowledge_base("Create ArcGIS Pro SDK ribbon button", platform="qgis")
        self.assertEqual(res["selected_platforms"], ["pyqgis"])
        self.assertEqual(res["platform_resolution"], "declared")
        self.assertEqual(res["matching_recipes"], [])
        self.assertNotIn("esri-arcgis-pro-sdk-snippets",
                         [s["id"] for s in res["matching_sources"]])
        self.assertIn("esri-arcgis-pro-sdk-snippets",
                      [s["id"] for s in res["research_sources"]])

    def test_18_unknown_declared_target_cannot_fall_back_to_arcgis(self):
        res = cd.search_knowledge_base("Create ArcGIS Pro SDK ribbon button", platform="UI.js")
        self.assertEqual(res["platform_resolution"], "unknown-target")
        self.assertEqual(res["matching_recipes"], [])
        self.assertEqual(res["matching_sources"], [])

    def test_observed_pro_release_selects_a_matching_reviewed_reference(self):
        query = "Create ArcGIS Pro SDK ribbon button and dockpane"
        inventory = {"native_inventory": {"installer_file_versions": [
            {"product": "ArcGIS Pro", "version": "3.6.0.59527", "status": "VERSION_RESOURCE_READ"}
        ]}}
        result = cd.search_knowledge_base(query, platform="arcgis-pro-sdk", native_inventory=inventory)
        sources = {entry["id"]: entry for entry in result["matching_sources"]}
        samples = sources["esri-arcgis-pro-sdk-community-samples"]
        self.assertEqual(result["observed_arcgis_pro_version"], "3.6.0.59527")
        self.assertEqual(samples["reviewed_revision"]["host_release"], "3.6")
        self.assertEqual(samples["runtime_status"], "NOT RUN")
        self.assertNotIn("esri-arcgis-pro-sdk-snippets", sources)
        self.assertIn("esri-arcgis-pro-sdk-snippets",
                      {entry["id"] for entry in result["research_sources"]})
        self.assertEqual(result["matching_recipes"], [])

    def test_19_conflicting_hosts_need_an_explicit_target(self):
        query = "Compare QGIS processing algorithm with ArcGIS Pro SDK button"
        unresolved = cd.search_knowledge_base(query)
        self.assertEqual(unresolved["platform_resolution"], "ambiguous-host")
        self.assertEqual(unresolved["matching_recipes"], [])
        resolved = cd.search_knowledge_base(query, platform="qgis")
        self.assertEqual([r["id"] for r in resolved["matching_recipes"]],
                         ["recipe-qgis-processing-algorithm"])

    def test_20_known_platform_aliases_remain_usable(self):
        for platform, query, expected in (
            ("qgis", "processing algorithm", "recipe-qgis-processing-algorithm"),
            ("gdal", "sample raster elevation", "recipe-sample-raster-at-points"),
        ):
            with self.subTest(platform=platform):
                res = cd.search_knowledge_base(query, platform=platform)
                self.assertEqual(res["matching_recipes"][0]["id"], expected)

    def test_21_compatible_ribbon_recipe_can_be_selected(self):
        recipes = copy.deepcopy(self.recipes)
        recipes["recipes"].append({
            "recipe_id": "fixture-qgis-ribbon", "title": "QGIS Ribbon Command",
            "domain": "pyqgis", "target_environment": "QGIS 3.x",
            "language": "Python", "license": "MIT", "code_snippet": "fixture only",
        })
        res = cd.search_knowledge_base("Create QGIS ribbon button", recipes_data=recipes)
        self.assertEqual([r["id"] for r in res["matching_recipes"]], ["fixture-qgis-ribbon"])

    def test_22_gpl_notice_does_not_promise_an_isolation_exemption(self):
        candidate = next(r for r in self.recipes["recipes"]
                         if r["recipe_id"] == "recipe-qgis-processing-algorithm")
        result = cd.evaluate_candidate(candidate, "QGIS processing algorithm")
        self.assertTrue(result["applicable"])
        notice = next(issue for issue in result["issues"] if "GPL" in issue)
        self.assertIn("process isolation is not an automatic exemption", notice)


if __name__ == "__main__":
    unittest.main()
