"""Offline tests: toolchain discovery does not invoke any program."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import native_toolchain, toolchain_advice, toolchain_discovery as td


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

    def test_installed_probe_is_explicit(self):
        with patch.object(native_toolchain, "probe", return_value={"dotnet": {"status": "OBSERVED"}}) as probe:
            self.assertNotIn("native_inventory", td.audit(self.root, which=lambda _: None))
            probe.assert_not_called()
            report = td.audit(self.root, which=lambda _: None, native=True)
            self.assertEqual(report["sdk_workload_verification"], "QUERY_RESULTS_RECORDED")
            self.assertEqual(report["build_test"], "NOT RUN")
            self.assertEqual(report["native_ide_gui_test"], "NOT RUN")
            probe.assert_called_once()

    def test_windows_uses_known_installs_and_removes_default_paths(self):
        programs = self.root / "Program Files"
        programs86 = self.root / "Program Files (x86)"
        project = self.root / "project"
        paths = [
            programs / "dotnet/dotnet.exe",
            programs / "nodejs/node.exe",
            programs86 / "Microsoft Visual Studio/Installer/vswhere.exe",
            programs / "QGIS 4.2.3/bin/qgis-bin.exe",
            programs / "ArcGIS/Pro/bin/Python/envs/arcgispro-py3/conda-meta/python-3.13.7-build.json",
            project / ".venv/pyvenv.cfg",
            project / "dotnet.exe",
        ]
        for path in paths:
            path.parent.mkdir(exist_ok=True, parents=True)
            path.touch()
        calls = []
        visual_studio = {"instanceId": "local", "displayName": "Visual Studio Community",
                         "installationVersion": "17.14.1", "isComplete": True,
                         "isLaunchable": True, "installationPath": "C:/private/VS"}

        def invoke(executable, arguments):
            calls.append((executable, arguments))
            if executable.name == "vswhere.exe":
                return json.dumps([visual_studio] if "-requires" not in arguments or
                                  arguments[-1].endswith(".ManagedDesktop") else [])
            if executable.name == "node.exe":
                return "v24.1.0"
            return {
                ("--list-sdks",): "10.0.300 [C:/private/dotnet]",
                ("--list-runtimes",): "Microsoft.WindowsDesktop.App 10.0.8 [C:/private/dotnet]",
                ("workload", "list"): "Installed Workload Id  Manifest Version  Installation Source\n"
                                     "android  36.1.2/10.0.100  SDK\n",
            }[arguments]

        result = native_toolchain.native_windows(
            project, program_files=programs, program_files_x86=programs86, drive=self.root,
            invoke=invoke, version_reader=lambda _: "4.2.3.0")
        self.assertEqual(result["dotnet"]["sdk_versions"], ["10.0.300"])
        self.assertEqual(result["dotnet"]["workloads_status"], "OBSERVED")
        self.assertEqual(result["dotnet"]["workloads"][0]["id"], "android")
        self.assertTrue(result["visual_studio"]["instances"][0]["workloads"][
            "Microsoft.VisualStudio.Workload.ManagedDesktop"])
        self.assertEqual(result["installer_file_versions"][0]["status"], "VERSION_RESOURCE_READ")
        self.assertEqual(result["arcgis_conda_python"][0]["version"], "3.13.7")
        self.assertEqual(result["project_virtualenvs"], [".venv"])
        self.assertNotIn("private", json.dumps(result))
        self.assertTrue(all(path in paths[:3] for path, _ in calls))

    def test_failed_probes_do_not_imply_no_installed_workloads(self):
        runtime = native_toolchain.clr_inventory(Path("dotnet.exe"), lambda path, args: None)
        self.assertEqual(runtime["status"], "QUERY_FAILED")
        self.assertEqual(runtime["workloads_status"], "QUERY_UNAVAILABLE")
        studio = native_toolchain.visual_studio_inventory(Path("vswhere.exe"), lambda path, args: "", False)
        self.assertEqual(studio["status"], "QUERY_FAILED")

    def test_user_editor_and_visual_designer_are_distinct_metadata(self):
        user_programs = self.root / "UserPrograms"
        programs = self.root / "Program Files"
        qgis = programs / "QGIS"
        for executable in (
            user_programs / "Microsoft VS Code/Code.exe",
            user_programs / "Antigravity IDE/Antigravity IDE.exe",
            programs / "JetBrains/JetBrains Rider 2026/bin/rider64.exe",
            programs / "Qt Creator/bin/qtcreator.exe",
            qgis / "apps/qt6/bin/designer.exe",
        ):
            executable.parent.mkdir(parents=True)
            executable.touch()
        result = native_toolchain.local_ui_tools(programs, user_programs, (), (qgis,), lambda _: "1.0", False)
        self.assertEqual({row["product"] for row in result["editors"]},
                         {"VS Code", "Antigravity IDE", "Qt Creator", "Rider"})
        self.assertEqual([row["product"] for row in result["designers"]], ["Qt Designer for QGIS"])
        for entry in result["editors"] + result["designers"]:
            self.assertEqual(entry["functional_test"], "NOT RUN")
            self.assertNotIn("path", entry)

    def test_sdk_inventory_distinguishes_runtime_from_target_reference_packs(self):
        runtime = self.root / "dotnet"
        pack = runtime / "packs/Microsoft.WindowsDesktop.App.Ref/8.0.28/ref/net8.0"
        pack.mkdir(parents=True)
        (pack / "PresentationFramework.dll").touch()
        self.assertEqual(native_toolchain.reference_packs(runtime),
                         {"wpf": ["8.0"], "winforms": [], "dotnet": []})

    def test_recommendation_prefers_free_eligible_editor_and_respects_preference(self):
        editors = [{"product": tool, "status": "FILE_OBSERVED", "version": "1.2"}
                   for tool in ("VS Code", "Rider")]
        input_data = {"native_inventory": {"ui_tools": {"editors": editors}}}
        default = toolchain_advice.recommend(input_data, "winforms", "edit", prefer="rider")
        self.assertEqual(default["selected_candidate"], "vscode")
        self.assertEqual(default["options"][1]["status"], "VERIFY_REQUIRED")
        self.assertEqual(default["functional_test"], "NOT RUN")
        preferred = toolchain_advice.recommend(
            input_data, "winforms", "edit", prefer="rider", license_confirmed=["rider"],
        )
        self.assertEqual(preferred["selected_candidate"], "rider")

    def test_recommendation_keeps_a_compatible_older_dotnet_build(self):
        inventory = {"native_inventory": {"dotnet": {
            "status": "OBSERVED", "sdk_versions": ["8.0.421"],
            "reference_packs": {"wpf": ["8.0"]},
        }}}
        compatible = toolchain_advice.recommend(inventory, "wpf", "build", target_version="8.0")
        self.assertEqual(compatible["selected_candidate"], "dotnet-cli")
        incompatible = toolchain_advice.recommend(inventory, "wpf", "build", target_version="10.0")
        self.assertIsNone(incompatible["selected_candidate"])
        self.assertEqual(incompatible["options"][0]["status"], "VERIFY_REQUIRED")

    def test_qt_designer_cannot_replace_wpf_design_or_arcgis_sdk(self):
        driver = {"product": "Qt Designer for QGIS", "version": "6.11.1", "status": "FILE_OBSERVED"}
        visual_studio = {"complete": True, "launchable_reported": True, "version": "17.14.37710.0",
                         "workloads": {toolchain_advice.MANAGED_DESKTOP: True}}
        inventory = {"native_inventory": {
            "ui_tools": {"designers": [driver], "editors": [{"product": "Rider", "status": "FILE_OBSERVED"}]},
            "visual_studio": {"instances": [visual_studio]},
        }}
        qt = toolchain_advice.recommend(inventory, "qt-widgets", "visual-design", target_version="6")
        self.assertEqual(qt["selected_candidate"], "qt-designer")
        wpf = toolchain_advice.recommend(inventory, "wpf", "visual-design", target_version="10",
                                         license_confirmed=["visual-studio"])
        self.assertIsNone(wpf["selected_candidate"])
        self.assertEqual([item["id"] for item in wpf["options"]], ["visual-studio"])
        preview = toolchain_advice.recommend(inventory, "wpf", "preview", target_version="8")
        self.assertIn("rider", [item["id"] for item in preview["options"]])
        arcgis = toolchain_advice.recommend(inventory, "arcgis-pro-sdk", "build", prefer="rider")
        self.assertIsNone(arcgis["selected_candidate"])
        self.assertEqual([item["id"] for item in arcgis["options"]], ["visual-studio"])

    def test_path_hit_alone_does_not_pass_as_a_confirmed_editor(self):
        inventory = {"tool_candidates": {"VS Code": {"status": "FOUND_ON_PATH_NOT_EXECUTED"}}}
        plan = toolchain_advice.recommend(inventory, "dotnet", "edit")
        self.assertIsNone(plan["selected_candidate"])
        self.assertEqual(plan["options"][0]["basis"], "PATH_ONLY")
        self.assertEqual(plan["options"][0]["status"], "VERIFY_REQUIRED")


if __name__ == "__main__":
    unittest.main()
