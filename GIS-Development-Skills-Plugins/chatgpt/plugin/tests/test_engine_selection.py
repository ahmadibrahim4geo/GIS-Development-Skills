#!/usr/bin/env python3
"""Tests for geospatial-engine-selection skill, templates, schemas, discover, compare, and recommend scripts."""

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
import sys

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import compare_engines, discover_engines, intent_router, recommend_stack  # noqa: E402


PROFILES_DOC = json.loads((ROOT / "references" / "engine-capability-profiles.json").read_text(encoding="utf-8"))
BY_PID = {p["project_id"]: p for p in PROFILES_DOC["profiles"]}


class EngineSelectionTests(unittest.TestCase):
    """Covers skill/templates/schemas plus E01..E20, E33, E35, E37, E40."""

    def test_skill_guide_schemas_and_5_templates_present(self):
        skill = (ROOT / "skills" / "geospatial-engine-selection" / "SKILL.md").read_text(encoding="utf-8")
        self.assertLessEqual(len(skill.splitlines()), 180)
        for token in ("name: geospatial-engine-selection", "free-first-policy.md", "discover_engines.py", "compare_engines.py", "recommend_stack.py"):
            self.assertIn(token, skill)

        guide = (ROOT / "references" / "engine-comparison-guide.md").read_text(encoding="utf-8")
        self.assertIn("hard_gate", guide)
        self.assertIn("PoC Benchmark", guide)

        req_schema = json.loads((ROOT / "schemas" / "engine-selection-request.schema.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(req_schema["properties"]), 21)
        rep_schema = json.loads((ROOT / "schemas" / "engine-selection-report.schema.json").read_text(encoding="utf-8"))
        self.assertIn("developer_vs_enduser_setup", rep_schema["required"])

        for tpl in (
            "ENGINE_EVALUATION_REPORT.md",
            "TECHNOLOGY_SELECTION_REPORT.md",
            "ARCHITECTURE_DECISION_RECORD.md",
            "SOURCE_FORK_FEATURE_INVENTORY.md",
            "REFERENCE_UI_COMMAND_MAPPING.md",
        ):
            self.assertTrue((ROOT / "templates" / tpl).is_file(), f"Missing template: {tpl}")

        hints_ar = intent_router.route_hints("عايز أختار محرك ثلاثي الأبعاد وبناء برنامج جديد")
        self.assertIn("geospatial-engine-selection", hints_ar["suggested_skills"])

    def test_bilingual_arabic_english_discovery_parity_E19_and_empty_gap_E20(self):
        ar = discover_engines.discover(query="تحويل إحداثيات ومساقط crs")
        en = discover_engines.discover(query="coordinate conversion crs projection")
        self.assertEqual(ar["resolved_capabilities"], en["resolved_capabilities"])
        self.assertEqual([c["project_id"] for c in ar["candidates"]], [c["project_id"] for c in en["candidates"]])
        self.assertIn("osgeo-proj", [c["project_id"] for c in ar["candidates"]])

        missing = discover_engines.discover(capabilities=["non.existent.capability.xyz"])
        self.assertEqual(missing["status"], "no-match")
        self.assertEqual(missing["candidates"], [])
        self.assertTrue(missing["gaps"])

    def test_hard_gate_rejects_incompatible_license_paid_api_unsupported_os_E12_to_E16(self):
        # E12: High-scoring GPL engine rejected under permissive-only in-process policy.
        req_perm = {
            "target_os": ["windows"],
            "required_capabilities": ["io.vector.read", "render.2d.projected"],
            "free_only": True,
            "license_policy": "permissive-only",
            "integration_preference": "in-process",
        }
        res_perm = compare_engines.compare_candidates([BY_PID["qgis-qgis"], BY_PID["osgeo-gdal"]], req_perm)
        by_res = {e["project_id"]: e for e in res_perm["evaluations"]}
        self.assertEqual(by_res["qgis-qgis"]["gate_status"], "rejected")
        self.assertNotEqual(res_perm["winner"], "qgis-qgis")

        # E13: Paid / commercial SDK rejected under free_only=True.
        req_free = {"target_os": ["windows"], "required_capabilities": [], "free_only": True}
        res_paid = compare_engines.compare_candidates([BY_PID["esri-arcgis-pro-sdk"], BY_PID["osgeo-gdal"]], req_free)
        paid_eval = next(e for e in res_paid["evaluations"] if e["project_id"] == "esri-arcgis-pro-sdk")
        self.assertEqual(paid_eval["gate_status"], "rejected")
        self.assertNotEqual(res_paid["winner"], "esri-arcgis-pro-sdk")

        # E14: Unknown cost/license returns needs-evidence instead of eligible.
        res_unk = compare_engines.compare_candidates([BY_PID["maplibre-maplibre-gl-js"], BY_PID["openlayers-openlayers"]], {"target_os": ["web"], "required_capabilities": ["render.2d.vector_tiles"], "free_only": True})
        unk_map = {e["project_id"]: e for e in res_unk["evaluations"]}
        self.assertEqual(unk_map["maplibre-maplibre-gl-js"]["gate_status"], "needs-evidence")
        self.assertEqual(unk_map["openlayers-openlayers"]["gate_status"], "eligible")
        self.assertEqual(res_unk["winner"], "openlayers-openlayers")

        # E15: Unsupported target OS blocks direct in-process embedding unless worker possible.
        synthetic_ios_only = dict(BY_PID["osgeo-gdal"])
        synthetic_ios_only = json.loads(json.dumps(synthetic_ios_only))
        synthetic_ios_only["project_id"] = "ios-only-test"
        synthetic_ios_only["platforms"] = ["ios"]
        synthetic_ios_only["build_models"] = ["embedded-engine"]
        synthetic_ios_only["integration_patterns"] = ["static-lib"]
        synthetic_ios_only["verification_metadata"]["supported_os"] = ["ios"]
        gate_os = compare_engines.hard_gate(synthetic_ios_only, {"target_os": ["windows"], "required_capabilities": ["crs.transform"], "free_only": True, "integration_preference": "in-process"})
        self.assertEqual(gate_os["gate_status"], "rejected")

        # E16: Missing empirical benchmarks yield explicit missing_metrics + poc_benchmark_required=True.
        self.assertTrue(all(e["poc_benchmark_required"] and e["missing_metrics"] for e in res_unk["evaluations"]))

    def test_e11_sar_vs_optical_differentiation(self):
        sar_req = {"target_os": ["linux"], "required_capabilities": ["eo.sar.calibration", "rs.sar"], "free_only": True}
        sar_comp = compare_engines.compare_candidates(
            [BY_PID["senbox-org-snap-engine"], BY_PID["orfeotoolbox-otb"], BY_PID["osgeo-gdal"]],
            sar_req,
        )
        by_id = {e["project_id"]: e for e in sar_comp["evaluations"]}
        self.assertEqual(by_id["orfeotoolbox-otb"]["gate_status"], "eligible")
        self.assertEqual(by_id["osgeo-gdal"]["gate_status"], "needs-evidence")

    def test_recommend_scenarios_E03_E08_E09_E10_UIjs_E33_E35_E37(self):
        # Unresolved UI.js guard.
        ujs = recommend_stack.recommend(recommend_stack._infer_request_from_query("Use UI.js to render maps with python"))
        self.assertEqual(ujs["status"], "unresolved")
        self.assertEqual(ujs["entity_role_split"]["ui_framework"]["status"], "unresolved")

        # E03: ArcGIS Pro add-in preserves licensed host explicitly.
        e03 = recommend_stack.recommend(recommend_stack._infer_request_from_query("اعمل Add-in داخل ArcGIS Pro", free_only=False))
        self.assertIn("extend-host", e03["recommended_build_models"])
        self.assertEqual(e03["recommended_stack"][0]["project_id"], "esri-arcgis-pro-sdk")

        # E08: Minimal CRS converter picks lightweight PROJ rather than full desktop QGIS suite.
        e08 = recommend_stack.recommend(recommend_stack._infer_request_from_query("برنامج صغير يحول إحداثيات ومساقط بس"))
        pids_08 = [item["project_id"] for item in e08["recommended_stack"]]
        self.assertIn("osgeo-proj", pids_08)
        self.assertNotIn("qgis-qgis", pids_08)

        # E09: Arbitrary 2D projections separated cleanly from 3D Globe.
        e09 = recommend_stack.recommend(recommend_stack._infer_request_from_query("اعمل Globe و2D بكل المساقط غير Web Mercator"))
        self.assertEqual(len(e09["entity_role_split"]["separated_renderers"]), 2)
        pids_09 = [item["project_id"] for item in e09["recommended_stack"]]
        self.assertIn("osgeo-proj", pids_09)
        self.assertIn("openlayers-openlayers", pids_09)
        self.assertTrue(any(p in pids_09 for p in ("cesiumgs-cesium", "cesiumgs-cesium-native")), pids_09)
        e09_web = recommend_stack.recommend(recommend_stack._infer_request_from_query("2D non-mercator and 3D globe web", target_os="web"))
        self.assertIn("cesiumgs-cesium", [item["project_id"] for item in e09_web["recommended_stack"]])

        # E10: CityEngine decomposition exposes CGA gap & multi-engine composition.
        e10 = recommend_stack.recommend(recommend_stack._infer_request_from_query("اعمل برنامج تصميم مدن زي CityEngine ثلاثي الأبعاد"))
        self.assertTrue(any("CGA" in g or "CityEngine" in g for g in e10["gaps_and_limitations"]))

        # E33 & E37 & Developer/End-user split & T2-T4 NOT RUN boundary.
        self.assertFalse(e09["evidence_boundaries"]["native_runtime_verified"])
        self.assertFalse(e09["evidence_boundaries"]["heavy_installers_executed"])
        self.assertIn("developer_toolchain", e09["developer_vs_enduser_setup"])
        self.assertIn("end_user_runtime", e09["developer_vs_enduser_setup"])
        self.assertTrue(any("silent algorithmic fallback" in g.lower() or "silent fallback" in g.lower() for g in e09["fallback_and_compatibility_guardrails"]))

        # E35: Byte-identical deterministic repeatability.
        r1 = json.dumps(recommend_stack.recommend(recommend_stack._infer_request_from_query("تحويل إحداثيات ومساقط")), sort_keys=True)
        r2 = json.dumps(recommend_stack.recommend(recommend_stack._infer_request_from_query("تحويل إحداثيات ومساقط")), sort_keys=True)
        self.assertEqual(r1, r2)


if __name__ == "__main__":
    unittest.main()
