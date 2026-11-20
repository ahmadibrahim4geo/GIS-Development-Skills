"""Offline tests: toolchain discovery does not invoke any program."""
import tempfile
import unittest
from pathlib import Path

from scripts import toolchain_discovery as td


class ToolchainDiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)

    def test_dotnet_stack_and_unverified_tools(self):
        (self.root / "ZEARTH.sln").write_text("", encoding="utf-8")
        found = {"git": "/bin/git", "dotnet": "/bin/dotnet", "code": "/bin/code"}
        calls = []
        def fake_which(name):
            calls.append(name)
            return found.get(name)
        result = td.audit(self.root, which=fake_which)
        self.assertIn("dotnet", result["project_type_hints"])
        self.assertIn("ZEARTH.sln", result["matched_files"]["dotnet"])
        self.assertEqual(result["tool_candidates"]["dotnet SDK CLI"]["status"], "FOUND_ON_PATH_NOT_EXECUTED")
        self.assertIn("MSBuild", result["missing_from_path"])
        self.assertEqual(result["native_ide_gui_test"], "NOT RUN")
        self.assertEqual(result["build_test"], "NOT RUN")
        self.assertNotIn("path", result["tool_candidates"]["Git"])
        self.assertIn("git", calls)

    def test_fixture_files_are_not_executed_or_scanned(self):
        (self.root / "project.pyt").write_text("raise RuntimeError('never run')\n", encoding="utf-8")
        folder = self.root / "testing data"
        folder.mkdir()
        (folder / "malicious.py").write_text("raise RuntimeError('never run')", encoding="utf-8")
        result = td.audit(self.root, which=lambda _: None)
        self.assertIn("arcgis-toolbox", result["project_type_hints"])
        self.assertNotIn("python", result["project_type_hints"])
        self.assertNotIn("malicious.py", str(result))

    def test_paths_are_opt_in(self):
        (self.root / "package.json").write_text("{}", encoding="utf-8")
        default = td.audit(self.root, which=lambda c: "/home/private/" + c)
        opt_in = td.audit(self.root, which=lambda c: "/home/private/" + c,
                          expose_paths=True)
        self.assertNotIn("/home/private/", str(default))
        self.assertIn("/home/private/", str(opt_in))
        self.assertIn("javascript", opt_in["project_type_hints"])

    def test_nonexistent_root_is_rejected(self):
        with self.assertRaises(ValueError):
            td.audit(self.root / "no-project")


if __name__ == "__main__":
    unittest.main()
