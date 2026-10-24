import json
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class LinkCollector(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if "id" in values:
            self.ids.add(values["id"])
        if tag in ("img", "script", "link", "a") and "src" in values:
            self.links.append(values["src"])
        if tag in ("img", "script", "link", "a") and "href" in values:
            self.links.append(values["href"])


class LandingPageTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.parser = LinkCollector()
        cls.parser.feed(cls.html)

    def test_page_has_navigation_and_search_controls(self):
        for element in ("main", "capabilities", "catalog", "get-started",
                        "contribute", "searchInput", "categoryFilter",
                        "catalogResults", "langBtn"):
            self.assertIn(element, self.parser.ids)

    def test_local_assets_exist(self):
        self.assertIn("assets/logo.svg", self.parser.links)
        self.assertIn("assets/icon.svg", self.parser.links)
        for asset in ("assets/logo.svg", "assets/icon.svg"):
            tree = ET.parse(ROOT / asset)
            self.assertTrue(tree.getroot().tag.endswith("svg"))

    def test_catalog_endpoints_and_shapes(self):
        for path, key in (("references/project-catalog.json", "projects"),
                          ("references/free-geospatial-apis.json", "services")):
            self.assertIn(path, self.html)
            contents = json.loads((ROOT / path).read_text(encoding="utf-8"))
            self.assertTrue(contents[key])

    def test_language_and_accessibility_features(self):
        for term in ("lang=\"en\"", "aria-selected",
                     "document.documentElement.dir", "prefers-reduced-motion",
                     "data-i18n", "role=\"tablist\""):
            self.assertIn(term, self.html)


if __name__ == "__main__":
    unittest.main()
