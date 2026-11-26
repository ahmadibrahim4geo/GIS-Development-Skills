"""Regression checks for the new public hub and the preserved full GIS Explorer."""
import json
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.links = []
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if a.get("id"):
            self.ids.add(a["id"])
        if tag == "a" and a.get("href"):
            self.links.append(a["href"])


class InteractiveHubTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.explorer = (ROOT / "explorer.html").read_text(encoding="utf-8")
        cls.parse = LinkParser()
        cls.parse.feed(cls.site)

    def test_interactive_sections_and_full_explorer_links(self):
        for section in ("home", "capabilities", "earth-kml", "cartography",
                        "security", "author", "pathwaysContainer", "mobileMenu"):
            self.assertIn(section, self.parse.ids, section)
        self.assertIn("explorer.html", self.parse.links)
        self.assertIn("explorer.html#all-skills", self.parse.links)
        for feature in ("pathwaySearch", "timelineSlider", "skillModal", "langToggleBtn"):
            self.assertIn(feature, self.parse.ids, feature)

    def test_complete_existing_explorer_is_not_lost(self):
        for section in ("all-skills", "catalog", "repositoriesTab",
                        "licenseAuditProgress", "skillDirectory"):
            self.assertIn('id="' + section + '"', self.explorer)
        self.assertIn("references/project-catalog.json", self.explorer)
        self.assertIn("references/free-geospatial-apis.json", self.explorer)

    def test_original_developer_data_remains_in_footer(self):
        author = self.site.split('<section id="author"', 1)[1].split("</section>", 1)[0]
        for value in ('class="author-panel mirsad-author"',
                      'ahmad_ibrahim_original.png',
                      'أحمد إبراهيم',
                      'Ahmad Ibrahim',
                      'mailto:ahmadibrahim.geo@gmail.com',
                      'https://wa.me/201111915925',
                      'https://github.com/ahmadibrahim4geo',
                      'feature-request.yml',
                      'class="consultation"'):
            self.assertIn(value, author)
        self.assertIn('html[lang="ar"] .mirsad-author', self.site)
        self.assertIn('html[lang="en"] .mirsad-author', self.site)

    def test_main_page_metrics_match_live_manifests(self):
        expected = {
            "projectsCount": len(json.loads((ROOT / "references/project-catalog.json").read_text(encoding="utf-8"))["projects"]),
            "apisCount": len(json.loads((ROOT / "references/free-geospatial-apis.json").read_text(encoding="utf-8"))["services"]),
            "dataCount": len(json.loads((ROOT / "references/geospatial-data-repositories.json").read_text(encoding="utf-8"))["repositories"]),
            "skillsCount": len(tuple((ROOT / "skills").glob("*/SKILL.md")))
        }
        import re
        for name, number in expected.items():
            m = re.search(r'id="' + name + r'"[^>]*>(\d+)</strong>', self.site)
            self.assertIsNotNone(m, name)
            self.assertEqual(int(m.group(1)), number, name)

    def test_no_embedded_raster_inside_primary_logo(self):
        master = (ROOT / "assets/brand/logo-dark.svg").read_text(encoding="utf-8")
        self.assertNotIn("data:image/", master)
        self.assertIsNotNone(ET.fromstring(master))
        self.assertIn('src="assets/brand/logo-dark.svg"', self.site)
        self.assertIn('src="assets/brand/logo-compact-dark.svg"', self.site)

    def test_bilingual_and_accessible_interactions(self):
        self.assertIn('data-lang="ar"', self.site)
        self.assertIn('data-lang="en"', self.site)
        self.assertIn('aria-expanded="false"', self.site)
        self.assertIn("toggleLanguage()", self.site)
        self.assertIn("closeMobileMenu()", self.site)
        self.assertIn("document.addEventListener('keydown'", self.site)


if __name__ == "__main__":
    unittest.main()
