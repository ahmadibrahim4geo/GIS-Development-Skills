"""Runtime-parseable JavaScript and reachable fragment navigation in public GIS pages.

Offline smoke checks only; do not claim real browser/device or GIS engine QA.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PAGES = (
    "index.html",
    "explorer.html",
    "project-wizard.html",
    "examples/icon-manager/index.html",
)


class NavigationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids = set()
        self.fragment_links = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if isinstance(attrs.get("id"), str):
            self.ids.add(attrs["id"])
        if tag == "a" and isinstance(attrs.get("href"), str):
            href = attrs["href"]
            if href.startswith("#") and len(href) > 1:
                self.fragment_links.append(href[1:])


class WebsiteRuntimeIntegrityTests(unittest.TestCase):
    def test_local_navigation_ids_resolve(self):
        bad = []
        for path in PAGES:
            html = (ROOT / path).read_text(encoding="utf-8")
            parser = NavigationParser()
            parser.feed(html)
            for frag in parser.fragment_links:
                if frag not in parser.ids:
                    bad.append(f"{path} -> #{frag}")
        self.assertEqual([], bad)

    def test_inline_javascript_is_syntactically_valid(self):
        node = shutil.which("node")
        if node is None:
            self.skipTest("Node not installed; GitHub Actions provides a real Node.js gate")
        checked = 0
        with tempfile.TemporaryDirectory() as tmp:
            for page in PAGES:
                data = (ROOT / page).read_text(encoding="utf-8")
                for index, (attributes, source) in enumerate(
                    re.findall(r"<script\b([^>]*)>(.*?)</script>", data, flags=re.I | re.S)
                ):
                    if "src=" in attributes.lower():
                        continue
                    if "application/json" in attributes.lower() or "application/ld+json" in attributes.lower():
                        continue
                    if not source.strip():
                        continue
                    filepath = Path(tmp) / f"{Path(page).stem}-{index}.js"
                    filepath.write_text(source, encoding="utf-8")
                    run = subprocess.run([node, "--check", str(filepath)],
                                         capture_output=True, text=True, timeout=20)
                    self.assertEqual(run.returncode, 0, f"{page} inline script {index}: {run.stderr}")
                    checked += 1
        self.assertGreaterEqual(checked, 4)


if __name__ == "__main__":
    unittest.main()
