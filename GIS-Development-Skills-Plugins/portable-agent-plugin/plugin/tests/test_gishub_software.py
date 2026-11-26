"""Offline regression checks for Qiusheng Wu GIS software catalog integration."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ("gis-development", "geospatial-data-discovery",
          "qgis-plugin-development", "geospatial-web-mapping")


class GishubSoftwareTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = json.loads(
            (ROOT / "references" / "project-catalog.json").read_text(encoding="utf-8")
        )["projects"]

    def test_count_and_unique_urls(self):
        self.assertGreaterEqual(len(self.entries), 84)
        urls = [r["url"].rstrip("/").lower() for r in self.entries]
        self.assertEqual(len(urls), len(set(urls)))

    def test_provenance_and_upstream_license_review(self):
        refs = [r for r in self.entries if "gishub.org/software/" in r.get("provenance", "")]
        self.assertEqual(len(refs), 40)
        self.assertTrue(all(
            (r.get("license_verified") is True and bool(r.get("license_evidence_url")))
            or (r.get("license_verified") is not True and r.get("license") == "verify-upstream")
            for r in refs
        ))

    def test_priority_repositories(self):
        urls = {r["url"] for r in self.entries}
        for repo in ("opengeos/WhiteboxTools-ArcGIS", "opengeos/qgis-plugin-template",
                     "opengeos/GeoAgent", "opengeos/whitebox-wasm",
                     "opengeos/geospatial-data-catalogs",
                     "opengeos/maplibre-gl-time-slider"):
            self.assertIn("https://github.com/" + repo, urls)

    def test_skills_have_metadata(self):
        for name in SKILLS:
            content = (ROOT / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertEqual(content.splitlines()[0], "---")
            self.assertIn("name: " + name, content)
            self.assertIn("description:", content)

    def test_guide_legal_and_compatibility_guards(self):
        guide = (ROOT / "references" / "gishub-software.md").read_text(encoding="utf-8")
        self.assertIn("10.6", guide)
        self.assertIn("licens", guide.lower())
        self.assertIn("**not** a free API", guide)

if __name__ == "__main__":
    unittest.main()
