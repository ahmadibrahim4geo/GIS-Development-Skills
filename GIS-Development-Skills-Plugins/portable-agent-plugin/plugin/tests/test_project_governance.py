"""Offline regression tests for GIS project governance.

Tests use disposable projects only. No external downloads, skill execution, GIS
runtime, or changes to real user data.
"""
import json
from contextlib import redirect_stderr, redirect_stdout
import io
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

    def test_profiles_use_project_and_source_evidence(self):
        def write(relative, content):
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")

        write("desktop/Map.csproj", "<Project><UseWPF>true</UseWPF></Project>")
        write("qt/CMakeLists.txt", "find_package(Qt6 REQUIRED COMPONENTS Widgets)")
        write("qgis_addon/metadata.txt", "[general]\nqgisMinimumVersion=3.40\n")
        write("qgis_addon/__init__.py", "from qgis.core import QgsProject\n")
        write("Tool.pyt", "import arcpy\nraise RuntimeError('never execute this code')")
        write("web/package.json", '{"dependencies":{"maplibre-gl":"^5"}}')
        write("remote/job.py", "import sentinelhub")
        write("testing data/Private.qgz", "protected user input")
        write("New Skill/candidates/hidden.py", "from PySide6 import QtGui")
        write("deps/node_modules/map/package.json", '{"dependencies":{"cesium":"^1"}}')
        result = pg.audit(self.root)
        profiles = result["architecture_profiles"]
        self.assertEqual(profiles["wpf"], ["desktop/Map.csproj"])
        self.assertEqual(profiles["qt"], ["qt/CMakeLists.txt"])
        self.assertEqual(profiles["qgis-plugin"], ["qgis_addon/metadata.txt"])
        self.assertEqual(profiles["qgis"], ["qgis_addon/__init__.py"])
        self.assertEqual(profiles["arcgis"], ["Tool.pyt"])
        self.assertEqual(profiles["web-gis"], ["web/package.json"])
        self.assertEqual(profiles["remote-sensing"], ["remote/job.py"])
        self.assertNotIn("Private.qgz", str(profiles))
        self.assertNotIn("hidden.py", str(profiles))
        self.assertNotIn("node_modules", str(profiles))
        self.assertEqual(result["runtime_verification"], "NOT RUN")

    def test_linter_finds_local_cycles_duplicate_code_and_missing_project_references(self):
        (self.root / "main.py").write_text("import helper", encoding="utf-8")
        for name in ("helper.py", "duplicate.py"):
            (self.root / name).write_text("import main\n", encoding="utf-8")
        (self.root / "Map.csproj").write_text(
            '<Project><ProjectReference Include="Common/Missing.csproj"/></Project>',
            encoding="utf-8")
        findings = pg.audit(self.root)["source_findings"]
        cycle = next(finding for finding in findings if finding["kind"] == "local-dependency-cycle")
        self.assertEqual(set(cycle["files"]), {"main.py", "helper.py"})
        duplicate = next(finding for finding in findings if finding["kind"] == "identical-source")
        self.assertEqual(set(duplicate["files"]), {"helper.py", "duplicate.py"})
        missing = next(finding for finding in findings if finding["kind"] == "missing-project-reference")
        self.assertEqual(missing["target"], "Common/Missing.csproj")

    def test_audit_check_reports_document_and_registration_drift(self):
        pg.init(self.root)
        self.assertEqual(pg.audit(self.root)["disposition"], "KEEP")
        self.assertEqual(pg.audit(self.root)["structure_drift"]["documentation"], "CURRENT")
        folder = self.root / "assets"
        folder.mkdir()
        result = pg.audit(self.root)
        self.assertEqual(result["disposition"], "EXTEND")
        self.assertEqual(result["structure_drift"]["documentation"], "DRIFTED")
        self.assertEqual(result["undocumented_directories"], ["assets"])
        pg.register_folder(self.root, "assets", "Map assets owned by the project")
        self.assertEqual(pg.audit(self.root)["structure_drift"]["documentation"], "CURRENT")
        with redirect_stdout(io.StringIO()):
            self.assertEqual(pg.main(["--project", str(self.root), "audit", "--check"]), 0)
        folder.rmdir()
        self.assertEqual(pg.audit(self.root)["structure_drift"]["stale_folder_registrations"], ["assets"])
        with redirect_stdout(io.StringIO()):
            self.assertEqual(pg.main(["--project", str(self.root), "audit", "--check"]), 1)
            self.assertEqual(pg.main(["--project", str(self.root), "audit"]), 0)

    def test_move_preview_reports_impacted_references_and_keeps_bytes(self):
        helper = self.root / "helper.py"
        helper.write_text("def project():\n    return 4326\n", encoding="utf-8")
        (self.root / "main.py").write_text("from helper import project\n", encoding="utf-8")
        (self.root / "README.md").write_text("[Module](helper.py)\n", encoding="utf-8")
        before = {path.name: path.read_bytes() for path in self.root.iterdir()}
        with redirect_stdout(io.StringIO()) as stdout:
            self.assertEqual(pg.main(["--project", str(self.root), "plan-move",
                                      "--from", "helper.py", "--to", "coords.py"]), 0)
        result = json.loads(stdout.getvalue())
        self.assertEqual(result["disposition"], "REFACTOR")
        self.assertFalse(result["applied"])
        self.assertEqual(result["rollback"], {"from": "coords.py", "to": "helper.py",
                                              "restore_reference_edits": True})
        self.assertEqual({ref["file"]: ref["kind"] for ref in result["references_to_review"]},
                         {"main.py": "python-import", "README.md": "path-mention"})
        self.assertTrue(all(ref["target_after"] == "coords.py" for ref in result["references_to_review"]))
        self.assertEqual({path.name: path.read_bytes() for path in self.root.iterdir()}, before)

    def test_move_preview_rejects_protected_paths_and_collisions(self):
        pg.init(self.root)
        (self.root / "assets").mkdir()
        (self.root / "testing data/private.py").write_text("raise RuntimeError('protected')",
                                                           encoding="utf-8")
        cases = (("main.py", "../outside.py"), ("main.py", "/Windows/outside.py"),
                 ("main.py", "AGENTS.md"), ("main.py", "testing data/new.py"),
                 ("testing data/private.py", "copy.py"), (".", "inside"),
                 ("assets", "assets/moved"), ("main.py", "absent/moved.py"))
        for source, destination in cases:
            with self.subTest(source=source, destination=destination):
                with redirect_stderr(io.StringIO()) as stderr:
                    self.assertEqual(pg.main(["--project", str(self.root), "plan-move",
                                              "--from", source, "--to", destination]), 2)
                self.assertEqual(json.loads(stderr.getvalue())["action"], "plan-move")
        self.assertTrue((self.root / "main.py").is_file())
        self.assertFalse((self.root / "testing data/new.py").exists())


if __name__ == "__main__":
    unittest.main()
