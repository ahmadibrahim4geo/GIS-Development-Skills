import json
import base64
import re
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
        self.assertIn("assets/icon.svg", self.parser.links)
        self.assertIn("assets/readme-banner.svg", (ROOT / "README.md").read_text(encoding="utf-8"))
        for asset in ("assets/logo.svg", "assets/icon.svg"):
            tree = ET.parse(ROOT / asset)
            self.assertTrue(tree.getroot().tag.endswith("svg"))

    def test_api_expansion_and_skill_path(self):
        catalog=json.loads((ROOT/'references/free-geospatial-apis.json').read_text(encoding='utf-8'))
        self.assertIn('id="apisCount">{}<'.format(len(catalog['services'])),self.html)
        self.assertIn('data-i18n="apiExpansion"',self.html)
        self.assertIn('data-i18n="dataSkill"',self.html)
        self.assertIn('data-i18n="apiSkill"',self.html)
        self.assertTrue((ROOT/'skills/geospatial-api-integration/SKILL.md').exists())

    def test_catalog_endpoints_and_shapes(self):
        for path, key in (("references/project-catalog.json", "projects"),
                          ("references/free-geospatial-apis.json", "services")):
            self.assertIn(path, self.html)
            contents = json.loads((ROOT / path).read_text(encoding="utf-8"))
            self.assertTrue(contents[key])

    def test_brand_tagline_and_original_mission_statement(self):
        self.assertIn("The Heart of Geospatial Innovation", self.html)
        self.assertIn(
            "Build GIS tools, plugins and geospatial applications with a verifiable development workflow.",
            self.html,
        )
        self.assertIn('class="hero-symbol" src="assets/icon.svg"', self.html)
        self.assertIn('class="hero-wordmark"', self.html)
        self.assertIn('class="word-development"', self.html)
        self.assertIn('href="assets/brand-refresh.css"', self.html)
        self.assertTrue((ROOT / "assets/brand-refresh.css").is_file())

    def test_readme_header_has_only_one_slogan_and_balanced_wordmark(self):
        logo = ET.parse(ROOT / "assets/logo.svg").getroot()
        svg_ns = "{http://www.w3.org/2000/svg}"
        text_elements = logo.findall(f".//{svg_ns}text")
        wordmark = [
            element for element in text_elements
            if (element.text or "").startswith("Development")
        ]
        self.assertEqual(len(wordmark), 1)
        skills = wordmark[0].find(f"{svg_ns}tspan")
        self.assertIsNotNone(skills)
        self.assertEqual(skills.text, "Skills")
        self.assertEqual(skills.attrib.get("dx"), "17")

        for path in ("README.md", "README.ar.md"):
            readme = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn('src="assets/readme-banner.svg"', readme)
            self.assertNotIn("<strong>The Heart of Geospatial Innovation</strong>", readme)
            self.assertIn("GIS Development Skills", readme)
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "Build GIS tools, plugins and geospatial applications with a verifiable development workflow.",
            english,
        )

    def test_approved_layered_g_brand_used_consistently(self):
        full_logo = (ROOT / "assets/logo.svg").read_text(encoding="utf-8")
        icon_logo = (ROOT / "assets/icon.svg").read_text(encoding="utf-8")
        self.assertIn("The Heart of Geospatial Innovation", full_logo)
        # Both assets embed the same scaled approved G photographically, avoiding
        # a structurally different hand-redrawn symbol that distorted the G.
        logos = []
        for asset in (full_logo, icon_logo):
            match = re.search(r'data:image/png;base64,([A-Za-z0-9+/=]+)', asset)
            self.assertIsNotNone(match)
            data = base64.b64decode(match.group(1), validate=True)
            self.assertTrue(data.startswith(bytes([137, 80, 78, 71, 13, 10, 26, 10])))
            logos.append(data)
        self.assertEqual(logos[0], logos[1])
        self.assertIn('class="scene-logo" src="assets/icon.svg"', self.html)
        self.assertNotIn('class="globe-art"', self.html)

    def test_public_creator_section_and_contacts(self):
        self.assertIn("author", self.parser.ids)
        self.assertIn("ahmad_ibrahim_original.png", self.html)
        self.assertIn('class="author-panel mirsad-author"', self.html)
        self.assertIn('class="portrait-frame"', self.html)
        self.assertIn('class="contact-actions"', self.html)
        self.assertIn('class="consultation"', self.html)
        self.assertIn("https://github.com/ahmadibrahim4geo", self.html)
        self.assertIn("mailto:ahmadibrahim.geo@gmail.com", self.html)
        self.assertIn("https://wa.me/201111915925", self.html)
        self.assertIn("feature-request.yml", self.html)

    def test_author_name_and_profile_are_fully_bilingual(self):
        section = self.html.split('<section id="author"', 1)[1].split("</section>", 1)[0]
        self.assertIn('<span class="lang-ar" lang="ar">أحمد إبراهيم</span>', section)
        self.assertIn('<span class="lang-en" lang="en">Ahmad Ibrahim</span>', section)
        self.assertNotIn('Ahmad Ibrahim <span', section)
        self.assertIn('data-i18n-alt="authorPortraitAlt"', section)
        for token in ('class="lang-ar" lang="ar"', 'class="lang-en" lang="en"'):
            self.assertGreaterEqual(section.count(token), 6)
        self.assertIn("document.querySelectorAll(\"[data-i18n-alt]\")", self.html)
        self.assertIn("document.querySelectorAll(\"[data-i18n-aria]\")", self.html)
        css = (ROOT / "assets/brand-refresh.css").read_text(encoding="utf-8")
        self.assertIn('html[lang="ar"] .mirsad-author{direction:rtl}', css)
        self.assertIn('html[lang="en"] .mirsad-author{direction:ltr}', css)

    def test_language_and_accessibility_features(self):
        for term in ("lang=\"en\"", "aria-selected",
                     "document.documentElement.dir", "prefers-reduced-motion",
                     "data-i18n", "role=\"tablist\""):
            self.assertIn(term, self.html)


if __name__ == "__main__":
    unittest.main()
