import unittest
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

class ReadmeLayoutTests(unittest.TestCase):
    def test_banner_and_six_real_navigation_cards(self):
        md = (ROOT / "README.md").read_text(encoding="utf-8")
        ar = (ROOT / "README.ar.md").read_text(encoding="utf-8")
        ET.parse(ROOT / "assets/readme-banner.svg")
        self.assertIn("assets/readme-banner.svg", md)
        self.assertIn("assets/readme-banner.svg", ar)
        self.assertEqual(md.count("<td align=\"center\" valign=\"top\""), 6)
        self.assertNotIn("<strong>The Heart of Geospatial Innovation</strong>", md)
        self.assertIn("Build GIS tools, plugins and geospatial applications with a verifiable development workflow.", md)
        links = [
           "skills/arcgis-toolbox-engineering/SKILL.md",
           "references/free-geospatial-apis.md",
           "skills/gis-development/SKILL.md",
           "skills/geospatial-web-mapping/SKILL.md",
           "skills/gis-desktop-application-development/SKILL.md",
           "references",
        ]
        for link in links:
            self.assertIn('href="' + link + '"', md)
            self.assertTrue((ROOT / link).exists(), link)
        for name in ("tools", "apis", "development", "maps", "desktop", "guides"):
            ET.parse(ROOT / "assets" / ("readme-" + name + ".svg"))
        self.assertNotIn("v1.0.0", md.split("## What makes this different")[0])

    def test_header_banner_tight_word_spacing_and_no_white_edges(self):
        """Prevent the huge Development/Skills gap from reappearing in the README SVG."""
        root = ET.parse(ROOT / "assets/readme-banner.svg").getroot()
        self.assertEqual(root.attrib.get("viewBox"), "0 0 1600 330")
        self.assertEqual(root.attrib.get("width"), "1600")
        self.assertEqual(root.attrib.get("height"), "330")
        svg = "{http://www.w3.org/2000/svg}"
        labels = {
            (node.text or "").strip(): node for node in root.iter(svg + "text")
        }
        for word in ("GIS", "Development", "Skills"):
            self.assertIn(word, labels)
        # Approximate word widths for the declared DejaVu Sans bold sizing
        # and -3 letter-spacing. Both inter-word gaps are ~30 SVG units.
        gis_gap = float(labels["Development"].get("x")) - float(labels["GIS"].get("x")) - 174
        dev_gap = float(labels["Skills"].get("x")) - float(labels["Development"].get("x")) - 532
        self.assertGreater(gis_gap, 15)
        self.assertLess(gis_gap, 45)
        self.assertGreater(dev_gap, 15)
        self.assertLess(dev_gap, 45)
        self.assertLessEqual(abs(gis_gap - dev_gap), 12)
        svg_text = (ROOT / "assets/readme-banner.svg").read_text(encoding="utf-8")
        self.assertIn('<rect width="1600" height="330" fill="url(#background)"/>', svg_text)
        self.assertNotIn('fill="#FFFFFF"', svg_text)
        self.assertNotIn('fill="white"', svg_text)


if __name__ == "__main__":
    unittest.main()
