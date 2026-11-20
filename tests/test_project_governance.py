"""Offline regression tests for GIS project governance.

Tests use disposable projects only. No external downloads, skill execution, GIS
runtime, or changes to real user data.
"""
import json
import tempfile
import unittest
from pathlib import Path

from scripts import project_governance as pg


class ProjectGovernanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "MyGISProject"
        self.root.mkdir()
        (self.root / "main.py").write_text("print('preserve me')\n", encoding="utf-8")

    def test_bootstrap_creates_required_folders_and_preserves_user_data(self):
        user = self.root / "testing data"
        user.mkdir()
        fixture = user / "landcover.geojson"
        fixture.write_bytes(b'{"type":"FeatureCollection","features":[]}')
        before = fixture.read_bytes()
        result = pg.init(self.root)
        self.assertTrue((self.root / "AGENTS.md").is_file())
        self.assertTrue((self.root / "PROJECT_STRUCTURE.md").is_file())
        self.assertTrue((self.root / "testing results").is_dir())
        self.assertTrue((self.root / "New Skill/candidates").is_dir())
        self.assertTrue((self.root / "plans/active").is_dir())
        self.assertTrue((self.root / "plans/archive").is_dir())
        self.assertEqual(fixture.read_bytes(), before)
        self.assertEqual((self.root / "main.py").read_text(encoding="utf-8"), "print('preserve me')\n")
        self.assertIn("testing data", (self.root / "PROJECT_STRUCTURE.md").read_text(encoding="utf-8"))
        self.assertIn("created_directories", result)
        pg.init(self.root)
        self.assertEqual((self.root / "AGENTS.md").read_text(encoding="utf-8").count(pg.MANAGED), 1)

    def test_existing_agent_rules_are_extended_without_overwriting(self):
        original = "# Existing project rules\n\nKeep all old data.\n"
        (self.root / "AGENTS.md").write_text(original, encoding="utf-8")
        pg.init(self.root)
        new = (self.root / "AGENTS.md").read_text(encoding="utf-8")
        self.assertTrue(new.startswith(original))
        self.assertIn(pg.MANAGED, new)
        self.assertIn("testing results/", new)

    def test_user_structure_document_is_preserved(self):
        path = self.root / "PROJECT_STRUCTURE.md"
        original = "# My custom structure\n"
        path.write_text(original, encoding="utf-8")
        pg.init(self.root)
        self.assertEqual(path.read_text(encoding="utf-8"), original)
        self.assertFalse(pg.sync(self.root)["updated"])

    def test_added_directory_is_detected_then_documented(self):
        pg.init(self.root)
        folder = self.root / "assets/custom-symbols"
        folder.mkdir(parents=True)
        self.assertIn("assets", pg.sync(self.root)["undocumented_directories"])
        self.assertIn("assets/custom-symbols", pg.sync(self.root)["undocumented_directories"])
        pg.register_folder(self.root, "assets", "Assets belonging to the user interface")
        result = pg.register_folder(self.root, "assets/custom-symbols", "Project-specific SVG symbols")
        self.assertNotIn("assets/custom-symbols", result["undocumented_directories"])
        text = (self.root / "PROJECT_STRUCTURE.md").read_text(encoding="utf-8")
        self.assertIn("Project-specific SVG symbols", text)

    def test_path_traversal_and_symlink_are_rejected(self):
        pg.init(self.root)
        with self.assertRaises(ValueError):
            pg.safe_path(self.root, "../outside")
        with self.assertRaises(ValueError):
            pg.safe_path(self.root, "/etc/hosts")
        with self.assertRaises(ValueError):
            pg.safe_path(self.root, "C:/Windows")
        with self.assertRaises(ValueError):
            pg.register_folder(self.root, "nonexistent", "Misleading")
        external = Path(self.temp.name) / "outside"
        external.mkdir()
        link = self.root / "pointer"
        try:
            link.symlink_to(external, target_is_directory=True)
        except (OSError, NotImplementedError):
            return
        with self.assertRaises(ValueError):
            pg.safe_path(self.root, "pointer/foreign")

    def test_numbered_plans_archive_with_evidence_but_do_not_claim_runtime(self):
        pg.init(self.root)
        first = pg.new_plan(self.root, "Map Engine", "Implement working camera controls.")
        second = pg.new_plan(self.root, "Raster Processing", "Preserve NoData.")
        self.assertEqual(first["id"], "0001")
        self.assertEqual(second["id"], "0002")
        request = (self.root / first["path"] / "REQUEST.md").read_text(encoding="utf-8")
        self.assertIn("working camera", request)
        with self.assertRaises(ValueError):
            pg.close_plan(self.root, "0001", "reports/missing.md")
        (self.root / "reports/test-evidence.md").write_text("Tests still need actual runtime verification", encoding="utf-8")
        result = pg.close_plan(self.root, "0001", "reports/test-evidence.md")
        self.assertTrue(result["path"].startswith("plans/archive/0001_"))
        state = json.loads((self.root / result["path"] / "STATUS.json").read_text(encoding="utf-8"))
        self.assertEqual(state["status"], "ARCHIVED_WITH_REFERENCED_EVIDENCE")
        self.assertIn("NOT", result["note"])
        self.assertEqual(pg.new_plan(self.root, "KML", "Preserve source styling")["id"], "0003")

    def test_test_run_writes_only_results_not_test_data(self):
        pg.init(self.root)
        fixture = self.root / "testing data/in.tif"
        fixture.write_bytes(b"sample-fixture")
        previous = fixture.read_bytes()
        created = pg.new_test_run(self.root, "Spectral Indices")
        self.assertTrue((self.root / created["run"] / "TEST_RUN.md").is_file())
        self.assertIn("NOT RUN", (self.root / created["run"] / "TEST_RUN.md").read_text(encoding="utf-8"))
        self.assertEqual(fixture.read_bytes(), previous)
        self.assertEqual(Path(pg.new_test_run(self.root, "Another Run")["run"]).name[:4], "0002")

    def test_external_skill_is_candidate_only(self):
        pg.init(self.root)
        result = pg.register_skill(self.root, "Qt UI Review",
                                   "https://github.com/example/qt-skill",
                                   "Review Qt UI patterns", "123abc", "MIT")
        self.assertEqual(result["status"], "CANDIDATE_UNREVIEWED")
        self.assertFalse(result["executed"])
        registry = json.loads((self.root / "New Skill/SKILLS_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertEqual(registry["skills"][0]["security_review"], "NOT RUN")
        self.assertEqual(registry["skills"][0]["revision"], "123abc")
        with self.assertRaises(ValueError):
            pg.register_skill(self.root, "Qt UI Review",
                              "https://github.com/example/qt-skill", "duplicate", "", "")
        with self.assertRaises(ValueError):
            pg.register_skill(self.root, "Unsafe", "file:///etc/passwd", "bad", "", "")

    def test_governance_symlink_and_injected_metadata_are_rejected(self):
        outside = Path(self.temp.name) / "outside.md"
        outside.write_text("do not touch", encoding="utf-8")
        link = self.root / "AGENTS.md"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            return
        with self.assertRaises(ValueError):
            pg.init(self.root)
        self.assertEqual(outside.read_text(encoding="utf-8"), "do not touch")
        link.unlink()
        pg.init(self.root)
        with self.assertRaises(ValueError):
            pg.register_skill(self.root, "Injected", "https://example.org/skill\nunsafe",
                              "test", "", "")
        with self.assertRaises(ValueError):
            pg.register_folder(self.root, "plans", "purpose\nnew heading")

    def test_audit_is_read_only(self):
        before = sorted(x.name for x in self.root.iterdir())
        result = pg.audit(self.root)
        self.assertIn("AGENTS.md", result["missing_required"])
        self.assertEqual(sorted(x.name for x in self.root.iterdir()), before)


if __name__ == "__main__":
    unittest.main()
