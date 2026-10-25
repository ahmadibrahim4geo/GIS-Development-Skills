"""Documentary integration tests; not claims of live Google Earth or ZEarth functionality."""
import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GE = "references/google-earth-pro-engineering.md"
TIME = "references/historical-imagery-timeline.md"


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class GoogleEarthBlogReferenceTests(unittest.TestCase):
    def test_reference_sources_and_claim_limits(self):
        engineering = read(GE)
        timeline = read(TIME)
        self.assertIn("https://www.gearthblog.com/", engineering)
        self.assertIn("https://developers.google.com/kml/documentation/kmlreference", engineering)
        self.assertIn("documentation", engineering.lower())
        self.assertIn("No Google Earth Pro", engineering)
        self.assertIn("not proof of an implemented timeline", timeline)
        self.assertIn("license", timeline.lower())

    def test_time_control_guardrails(self):
        content = read(TIME)
        for detail in ("nonblocking", "available", "acquisition", "mosaic",
                       "camera", "No coverage", "Stale replies", "compare",
                       "401/403/404/429", "Google Earth historical"):
            self.assertIn(detail.lower(), content.lower())

    def test_connected_specialists_and_readmes(self):
        for path in ("README.md", "README.ar.md",
                     "skills/gis-development/SKILL.md",
                     "skills/gis-desktop-application-development/SKILL.md",
                     "skills/geospatial-web-mapping/SKILL.md",
                     "skills/kml-kmz-engineering/SKILL.md",
                     "references/desktop-and-web.md",
                     "references/google-kml-kmz-compatibility.md"):
            document = read(path)
            self.assertIn("google-earth-pro-engineering.md", document, path)
            self.assertIn("historical-imagery-timeline.md", document, path)

    def test_bilingual_website_navigation(self):
        page = read("index.html")
        self.assertIn('id="google-earth-reference"', page)
        self.assertIn('href="' + GE + '"', page)
        self.assertIn('href="' + TIME + '"', page)
        self.assertIn('html[lang="en"] .lang-ar', page)
        self.assertIn('html[lang="ar"] .lang-en', page)
        section = page.split('id="google-earth-reference"', 1)[1].split('</section>', 1)[0]
        self.assertEqual(3, section.count('class="feature"'))
        self.assertGreaterEqual(section.count('class="lang-en"'), 10)
        self.assertGreaterEqual(section.count('class="lang-ar"'), 10)

    def test_reference_internal_markdown_links(self):
        for path in (GE, TIME):
            doc = read(path)
            for target in re.findall(r'\]\(([^)]+)\)', doc):
                if target.startswith(('https://', 'http://', '#', 'mailto:')):
                    continue
                resolved = ((ROOT / path).parent / target).resolve()
                self.assertTrue(resolved.is_relative_to(ROOT.resolve()), (path, target))
                self.assertTrue(resolved.exists(), (path, target))


if __name__ == "__main__":
    unittest.main()
