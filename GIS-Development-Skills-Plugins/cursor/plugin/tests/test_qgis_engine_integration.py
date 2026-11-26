"""Offline integrity tests; does not import QGIS or imply a native host run."""
import ast
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class QGISEngineTests(unittest.TestCase):
    def test_skill_and_routing(self):
        skill = (ROOT / "skills/qgis-engine-integration/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("name: qgis-engine-integration", skill)
        for label in ("QGIS Server", "GIS Desktop Development", "GPL", "KML/KMZ", "T2"):
            self.assertIn(label, skill)
        self.assertIn("qgis-engine-integration/SKILL.md", (ROOT / "skills/gis-development/SKILL.md").read_text(encoding="utf-8"))

    def test_example_syntax_and_safety(self):
        source = (ROOT / "examples/qgis-engine/standalone_roundtrip.py").read_text(encoding="utf-8")
        ast.parse(source)
        self.assertIn("Refusing to overwrite", source)
        self.assertIn("TemporaryDirectory", source)
        self.assertIn("writeAsVectorFormatV3", source)

    def test_bilingual_manifest_and_site(self):
        data = json.loads((ROOT / "references/repository-manifest.json").read_text(encoding="utf-8"))
        self.assertIn("qgis-engine-integration", data["skill_ids"])
        self.assertEqual(data["skill_count"], len(data["skill_ids"]))
        for file in ("README.md", "README.ar.md", "index.html", "explorer.html"):
            self.assertIn("qgis-engine-integration", (ROOT / file).read_text(encoding="utf-8"))
        self.assertIn("qgis-engine", (ROOT / "project-wizard.html").read_text(encoding="utf-8"))
        explorer = (ROOT / "explorer.html").read_text(encoding="utf-8")
        self.assertIn('qgis-engine-integration":"QGIS engine & standalone apps"', explorer)
        self.assertIn('qgis-engine-integration":"محرك QGIS والتطبيقات المستقلة"', explorer)


if __name__ == "__main__":
    unittest.main()
