#!/usr/bin/env python3
"""Python + Node.js cross-runtime tests for Phase P05 Web GIS Expansion (W01-W12, WEB-01..18, GIS-001..014)."""

import json
import shutil
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
WEB_EXAMPLES = ROOT / "examples" / "web-gis"
SHARED_FIXTURES = ROOT / "tests" / "shared-gis-fixtures"
NODE_TEST_FILE = ROOT / "tests" / "web-gis" / "web_gis_contract.test.mjs"


class WebGISExpansionP05Tests(unittest.TestCase):
    """Verifies P05 Web GIS manuals, 18 6-folder templates, shared fixtures, and JS+Python readback."""

    def test_web_references_guides_and_skill_wiring(self):
        expected_refs = (
            "web-gis-products-map.md",
            "web-gis-architecture-selection.md",
            "browser-geospatial-js-runtime.md",
            "geospatial-3d-ar-mobile-web.md",
            "web-mobile-offline-sync-contract.md",
            "web-mobile-geoai-options.md",
            "web-mobile-vendor-license-audit.md",
        )
        skill_text = (ROOT / "skills" / "geospatial-web-mapping" / "SKILL.md").read_text(encoding="utf-8")
        for ref in expected_refs:
            fpath = REFERENCES / ref
            self.assertTrue(fpath.is_file(), f"Missing P05 reference: {ref}")
            self.assertGreater(fpath.stat().st_size, 1000, f"Reference {ref} suspiciously sparse")
            self.assertIn(ref, skill_text, f"SKILL.md must link {ref}")

        for token in (
            "geospatial-engine-selection",
            "W01",
            "W12",
            "WEB_GIS_GUIDE.md",
            "tile.openstreetmap.org",
            "earth-view-architecture.md",
            "blue-marble-global-mapper.md",
            "google-earth-pro-engineering.md",
            "historical-imagery-timeline.md",
        ):
            self.assertIn(token, skill_text)

        self.assertTrue((ROOT / "docs" / "WEB_GIS_GUIDE.md").is_file())
        perf = (ROOT / "docs" / "PERFORMANCE_RELIABILITY.md").read_text(encoding="utf-8")
        self.assertIn("10-Domain Measured Budget Matrix", perf)

    def test_all_18_web_templates_have_six_subfolders_and_specs(self):
        self.assertTrue((WEB_EXAMPLES / "README.md").is_file())
        self.assertTrue((WEB_EXAMPLES / "shared" / "spatial-core.mjs").is_file())
        self.assertTrue((WEB_EXAMPLES / "shared" / "pwa-sync.mjs").is_file())

        for num in range(1, 19):
            tid = f"WEB-{num:02d}"
            tdir = WEB_EXAMPLES / "templates" / tid
            self.assertTrue(tdir.is_dir(), f"Missing template directory {tid}")
            for sub in ("fixtures", "spec", "tests", "evidence", "docs", "safety"):
                self.assertTrue((tdir / sub).is_dir(), f"{tid} missing required subfolder '{sub}'")
            spec = json.loads((tdir / "spec" / "template-spec.json").read_text(encoding="utf-8"))
            self.assertEqual(spec["template_id"], tid)
            self.assertIn("NOT RUN", spec["status"]["headless_browser_e2e"])

        for runnable_id in ("WEB-01", "WEB-03", "WEB-12"):
            self.assertTrue((WEB_EXAMPLES / "templates" / runnable_id / "index.html").is_file())
        self.assertTrue((WEB_EXAMPLES / "templates" / "WEB-12" / "sw.js").is_file())
        self.assertTrue((WEB_EXAMPLES / "templates" / "WEB-12" / "manifest.webmanifest").is_file())

    def test_node_syntax_unit_tests_and_independent_python_geojson_readback(self):
        node = shutil.which("node")
        if not node:
            self.skipTest("Node.js runtime not installed")

        for mod_path in (
            WEB_EXAMPLES / "shared" / "spatial-core.mjs",
            WEB_EXAMPLES / "shared" / "pwa-sync.mjs",
            WEB_EXAMPLES / "templates" / "WEB-12" / "sw.js",
        ):
            chk = subprocess.run([node, "--check", str(mod_path)], capture_output=True, text=True, timeout=20)
            self.assertEqual(0, chk.returncode, f"Syntax check failed for {mod_path}: {chk.stderr}")

        run_js = subprocess.run(
            [node, "--test", str(NODE_TEST_FILE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(0, run_js.returncode, f"Node test failure:\n{run_js.stdout}\n{run_js.stderr}")

        # GIS-012 & WEB-QA-05: Execute JS SpatialEditorStore -> export GeoJSON -> independently verify via Python json.
        js_roundtrip = r"""
        import fs from "node:fs";
        import { SpatialEditorStore } from "./examples/web-gis/shared/spatial-core.mjs";
        const raw = fs.readFileSync("./tests/shared-gis-fixtures/geojson_epsg4326_bilingual.geojson", "utf8");
        const store = new SpatialEditorStore(raw);
        store.updateProperties("pt-cairo-01", { verified_by: "node-js-edit" });
        store.createFeature({
          type: "Feature",
          id: "pg-added-05",
          properties: { name_ar: "مضلع مضاف", name_en: "Added Polygon", notes: null },
          geometry: { type: "Polygon", coordinates: [[[31.21, 30.01], [31.22, 30.01], [31.22, 30.02], [31.21, 30.02], [31.21, 30.01]]] }
        });
        store.deleteFeature("mp-sensors-04");
        store.undo();
        process.stdout.write(store.exportGeoJson());
        """
        exp = subprocess.run(
            [node, "--input-type=module", "-e", js_roundtrip],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=20,
        )
        self.assertEqual(0, exp.returncode, exp.stderr)
        exported = json.loads(exp.stdout)
        self.assertEqual(exported["type"], "FeatureCollection")
        self.assertEqual(len(exported["features"]), 5)
        by_id = {f["id"]: f for f in exported["features"]}
        self.assertEqual(by_id["pt-cairo-01"]["properties"]["name_ar"], "نقطة معاينة القاهرة")
        self.assertEqual(by_id["pt-cairo-01"]["properties"]["verified_by"], "node-js-edit")
        self.assertIsNone(by_id["pt-cairo-01"]["properties"]["notes"])
        self.assertEqual(by_id["pg-added-05"]["properties"]["name_ar"], "مضلع مضاف")
        self.assertIn("mp-sensors-04", by_id)


if __name__ == "__main__":
    unittest.main()
