"""Offline first-party GIS case-study contract tests (not native ArcGIS execution)."""
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OWNER = "https://github.com/ahmadibrahim4geo/"
REPOS = (
    "MIRSAD",
    "Create-FlowArrow-Tool",
    "GeologicalCrossSectionToolbox",
    "ArcMap-Style-Collection",
    "gis-data-repositories-professional-2026",
)

class AuthorGISCaseStudyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads(
            (ROOT / "references" / "project-catalog.json").read_text(encoding="utf-8")
        )
        cls.entries = {entry["url"]: entry for entry in cls.catalog["projects"]}

    def test_required_author_repositories(self):
        for repo in REPOS:
            with self.subTest(repo=repo):
                url = OWNER + repo
                self.assertIn(url, self.entries)
                self.assertIn("source_availability", self.entries[url])
                self.assertIn("reviewed", self.entries[url]["provenance"])

    def test_excluded_unready_software(self):
        self.assertNotIn(OWNER + "GeoVision", self.entries)
        guide = (ROOT / "references" / "ahmad-ibrahim-gis-case-studies.md").read_text(encoding="utf-8")
        self.assertNotIn("GeoVision", guide)

    def test_scope_separates_tools_and_assets(self):
        styles = self.entries[OWNER + "ArcMap-Style-Collection"]
        self.assertIn("reference-only", styles["integration"])
        self.assertNotEqual(styles["license"], "MIT")
        flow = self.entries[OWNER + "Create-FlowArrow-Tool"]
        self.assertIn("arcgis-pro", flow["platforms"])
        self.assertIn("arcmap", flow["platforms"])

    def test_skill_frontmatter_and_case_study(self):
        skill = (ROOT / "skills" / "arcgis-toolbox-engineering" / "SKILL.md").read_text(encoding="utf-8")
        guide = (ROOT / "references" / "ahmad-ibrahim-gis-case-studies.md").read_text(encoding="utf-8")
        self.assertTrue(skill.startswith("---\n"))
        self.assertIn("name: arcgis-toolbox-engineering", skill)
        self.assertIn("ArcPy", skill)
        self.assertIn("T3", guide)
        self.assertIn("auto-flip", guide.lower())
        self.assertIn("Desktop", guide)
        self.assertIn("headless", guide)

    def test_no_overclaim_native_tests(self):
        text = (ROOT / "references" / "ahmad-ibrahim-gis-case-studies.md").read_text(encoding="utf-8")
        self.assertIn("not proof", text.lower())
        self.assertIn("licensed GIS", text)
        self.assertIn("no approved stable desktop release", text.lower())

if __name__ == "__main__":
    unittest.main()
