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
        cls.html = (ROOT / "explorer.html").read_text(encoding="utf-8")
        cls.parser = LinkCollector()
        cls.parser.feed(cls.html)

    def test_page_has_navigation_and_search_controls(self):
        for element in ("main", "capabilities", "catalog", "get-started",
                        "contribute", "searchInput", "categoryFilter",
                        "catalogResults", "langBtn"):
            self.assertIn(element, self.parser.ids)

    def test_local_assets_exist(self):
        self.assertIn("assets/brand/favicon.svg", self.parser.links)
        self.assertIn("assets/brand/logo-dark.svg", self.parser.links)
        self.assertIn("assets/brand/logo-compact-dark.svg", self.parser.links)
        self.assertIn("assets/brand/banner-dark.svg", (ROOT / "README.md").read_text(encoding="utf-8"))
        for name in ("icon", "favicon", "logo-dark", "logo-light",
                     "logo-compact-dark", "logo-compact-light", "banner-dark", "banner-light"):
            asset = ROOT / "assets" / "brand" / (name + ".svg")
            self.assertTrue(asset.is_file(), str(asset))
            root = ET.parse(asset).getroot()
            self.assertTrue(root.tag.endswith("svg"))

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
        self.assertIn('class="hero-symbol" src="assets/brand/logo-dark.svg"', self.html)
        self.assertIn('src="assets/brand/logo-compact-dark.svg"', self.html)
        self.assertEqual(1, self.html.count('class="hero-symbol"'))
        self.assertNotIn('class="scene-logo"', self.html)
        self.assertNotIn('class="hero-wordmark"', self.html)
        self.assertIn('href="assets/brand-refresh.css"', self.html)
        self.assertTrue((ROOT / "assets/brand-refresh.css").is_file())

    def test_readme_header_has_only_one_slogan_and_balanced_wordmark(self):
        for path in ("README.md", "README.ar.md"):
            readme = (ROOT / path).read_text(encoding="utf-8")
            self.assertIn('src="assets/brand/banner-dark.svg"', readme)
            self.assertIn('href="assets/brand/README.md"', readme)
            self.assertNotIn("<strong>The Heart of Geospatial Innovation</strong>", readme)
        palette = json.loads((ROOT / "assets/brand/palette.json").read_text(encoding="utf-8"))
        self.assertEqual("The Heart of Geospatial Innovation", palette["tagline"])
        self.assertEqual("#1CC8E8", palette["colors"]["cyan"])
        self.assertEqual("#82D53E", palette["colors"]["green"])
        english = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "Build GIS tools, plugins and geospatial applications with a verifiable development workflow.",
            english,
        )

    def test_approved_layered_g_brand_used_consistently(self):
        svg_ns = "{http://www.w3.org/2000/svg}"
        logo = ET.parse(ROOT / "assets/brand/logo-dark.svg").getroot()
        icon = ET.parse(ROOT / "assets/brand/icon.svg").getroot()
        paths_logo = {node.attrib.get("id") for node in logo.findall(f".//{svg_ns}path")}
        paths_icon = {node.attrib.get("id") for node in icon.findall(f".//{svg_ns}path")}
        for element in ("top-map", "map-route", "middle-layer", "bottom-layer"):
            self.assertIn(element, paths_logo)
            self.assertIn(element, paths_icon)
        self.assertEqual(paths_logo, paths_icon)
        nodes = {node.text: node.attrib.get("fill") for node in logo.iter() if node.tag in (f"{svg_ns}text", f"{svg_ns}tspan") and node.text}
        self.assertEqual("#82D53E", nodes["Heart"])
        self.assertEqual("#398CE3", nodes["Geospatial"])
        self.assertEqual("#1CC8E8", nodes["Innovation"])
        self.assertEqual("#82D53E", nodes["Skills"])
        self.assertIn('class="hero-symbol" src="assets/brand/logo-dark.svg"', self.html)
        self.assertNotIn('class="globe-art"', self.html)

    def test_brand_artwork_is_real_editable_vector_not_raster_wrapped_svg(self):
        svg_ns = "{http://www.w3.org/2000/svg}"
        for asset in (ROOT / "assets" / "brand").glob("*.svg"):
            content = asset.read_text(encoding="utf-8")
            root = ET.fromstring(content)
            self.assertEqual([], root.findall(f".//{svg_ns}image"), asset.name)
            self.assertNotIn("data:image/", content, asset.name)
            self.assertTrue(root.findall(f".//{svg_ns}path"), asset.name)
            self.assertFalse("filter=" in content, asset.name)
        logo = ET.parse(ROOT / "assets/brand/logo-dark.svg").getroot()
        self.assertIsNotNone(logo.find(".//*[@id='gis-i-dot']"))
        self.assertIsNotNone(logo.find(".//*[@id='gis-i-stem']"))
        self.assertEqual(self.html.count('class="hero-symbol"'), 1)
        self.assertIn('class="hero-lockup"', self.html)
        self.assertIn('class="hero-content"', self.html)

    def test_all_brand_variants_use_font_independent_word_flow(self):
        """Prevent word collisions even when browsers substitute SVG fonts."""
        ns = "{http://www.w3.org/2000/svg}"
        names = ("logo-dark", "logo-light", "banner-dark", "banner-light",
                 "logo-compact-dark", "logo-compact-light")
        for filename in names:
            svg = ET.parse(ROOT / "assets/brand" / (filename + ".svg")).getroot()
            name = svg.find(".//*[@id='brand-name']")
            tagline = svg.find(".//*[@id='brand-tagline']")
            self.assertIsNotNone(name, filename)
            self.assertIsNotNone(tagline, filename)
            main_parts = name.findall(ns + "tspan")
            self.assertEqual(["Development", "Skills"],
                             [part.text for part in main_parts], filename)
            self.assertNotIn("x", main_parts[1].attrib, filename)
            self.assertGreater(float(main_parts[1].get("dx")), 0, filename)
            self.assertEqual("#82D53E", main_parts[1].get("fill"))
            tokens = tagline.findall(ns + "tspan")
            self.assertEqual(["The", "Heart", "of", "Geospatial", "Innovation"],
                             [part.text for part in tokens], filename)
            for token in tokens[1:]:
                self.assertNotIn("x", token.attrib, filename)
                self.assertGreater(float(token.get("dx")), 0, filename)
            svg_content = (ROOT / "assets/brand" / (filename + ".svg")).read_text(encoding="utf-8")
            self.assertNotIn("<image", svg_content, filename)

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
