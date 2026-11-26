"""Deterministic offline tests for Esri Python version comparison and source intake."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("esri_environment", ROOT / "scripts/check_arcgis_python_env.py")
checker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(checker)

class PythonEnvironmentTests(unittest.TestCase):
    def setUp(self):
        self.baseline = {"3.7": {"arcgispro": "3.7", "numpy": "1.26.4", "my_pkg": "2.0"}}

    def test_name_matching(self):
        items = checker.installed_packages([{"name": "NumPy", "version": "1.26.4"},
                                            {"name": "my-pkg", "version": "2.0"}])
        self.assertEqual(["match", "match"], [r["status"] for r in checker.compare(self.baseline, "3.7", items)])

    def test_missing_and_mismatched(self):
        rows = checker.compare(self.baseline, "3.7", {"numpy": "1.20.0"})
        self.assertEqual(["missing", "mismatch"], [r["status"] for r in rows])

    def test_unknown_release_or_package(self):
        with self.assertRaises(ValueError):
            checker.compare(self.baseline, "3.6", {})
        with self.assertRaises(ValueError):
            checker.compare(self.baseline, "3.7", {}, ["not-listed"])

    def test_invalid_pip_list(self):
        with self.assertRaises(ValueError):
            checker.installed_packages({"numpy": "1.0"})

    def test_cli_codes(self):
        with tempfile.TemporaryDirectory() as t:
            a, b = Path(t) / "distribution.json", Path(t) / "pip.json"
            a.write_text(json.dumps(self.baseline), encoding="utf-8")
            b.write_text(json.dumps([{"name":"numpy","version":"1.26.4"},
                                     {"name":"my_pkg","version":"2.0"}]), encoding="utf-8")
            args = ["--distribution-json", str(a), "--release", "3.7", "--installed-json", str(b)]
            self.assertEqual(0, checker.main(args))
            self.assertEqual(2, checker.main(args + ["--packages", "unlisted"]))
            b.write_text(json.dumps([{"name":"numpy","version":"0.0"}]), encoding="utf-8")
            self.assertEqual(1, checker.main(args))

class EsriCatalogTests(unittest.TestCase):
    def test_ten_sources_and_synchronized_inventory(self):
        from pathlib import Path
        projects = json.loads((ROOT / "references/project-catalog.json").read_text(encoding="utf-8"))["projects"]
        links = [p["url"].lower().rstrip("/") for p in projects]
        self.assertEqual(len(links), len(set(links)))
        for slug in ("arcgis-pro-sdk-snippets", "arcade-expressions", "developer-support",
                     "cad-bim-scripts", "large-network-analysis-tools", "geoportal-server-catalog",
                     "jsapi-resources", "esri-leaflet-geocoder", "elevation-gp-python",
                     "raster-deep-learning"):
            e = next(item for item in projects if item["url"].lower() == "https://github.com/esri/" + slug)
            self.assertTrue(e["license_verified"])
            self.assertFalse(e["native_runtime_verified"])
            self.assertIn("/blob/", e["license_evidence_url"])
        manifest = json.loads((ROOT / "references/repository-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual(len(projects), manifest["reference_count"])

if __name__ == "__main__":
    unittest.main()
