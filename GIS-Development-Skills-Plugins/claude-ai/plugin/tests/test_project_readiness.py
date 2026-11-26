"""Project-root preflight regressions with isolated files and declared inventory."""

import tempfile
import unittest
from pathlib import Path

from scripts.project_readiness import preflight


def local_tools(sdk="8.0.421", pack="8.0", editors=()):
    return {
        "native_inventory": {
            "dotnet": {"status": "OBSERVED", "sdk_versions": [sdk],
                       "reference_packs": {"dotnet": [pack], "wpf": [pack]}},
            "ui_tools": {"editors": [{"product": name, "status": "FILE_OBSERVED"} for name in editors]},
            "visual_studio": {"instances": []},
        }
    }


class ProjectReadinessTests(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.root = Path(folder.name)

    def inspect(self, inventory, **options):
        result = preflight(self.root, inspect_tools=lambda *_args, **_kw: inventory, **options)
        return result, {row["action"]: row for row in result["work"]}

    def make_wpf_project(self):
        source = self.root / "Window.csproj"
        text = ('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup>'
                '<TargetFramework>net8.0-windows</TargetFramework><UseWPF>true</UseWPF></PropertyGroup>'
                '<ItemGroup><PackageReference Include="Mapsui" Version="5.0.0"/></ItemGroup></Project>')
        source.write_text(text, encoding="utf-8")
        (self.root / "Window.sln").write_text("Microsoft Visual Studio Solution File", encoding="utf-8")
        return source, text

    def test_planned_root_reuses_sdk_and_does_not_require_an_editor(self):
        target = self.root / "future"
        plan = preflight(target, mode="new", target="wpf", target_version="8",
                         planned_packages=["Mapsui"], inspect_tools=lambda *_args, **_kw: local_tools())
        rows = {row["action"]: row for row in plan["work"]}
        self.assertFalse(target.exists())
        self.assertEqual(plan["dependencies"][0]["source"], "reviewed plan")
        self.assertEqual(rows["build"]["selected_candidate"], "dotnet-cli")
        self.assertEqual(rows["edit"]["status"], "OPTIONAL")
        self.assertEqual(plan["tasks_on_hold"], [])
        self.assertTrue(rows["build"]["options"][0]["official_url"].startswith("https://dotnet.microsoft.com/"))

    def test_visual_studio_solution_can_keep_existing_cli_and_rider_workflows(self):
        source, original = self.make_wpf_project()
        (self.root / ".vsconfig").write_text(
            '{"components":["Microsoft.VisualStudio.Workload.ManagedDesktop"]}', encoding="utf-8")
        result, work = self.inspect(local_tools(editors=["Rider"]), mode="existing",
                                    required_tools=["visual-studio"], prefer="rider", license_confirmed=["rider"])
        self.assertEqual(result["target"], "wpf")
        self.assertEqual(result["target_version"], "8.0")
        self.assertEqual(result["existing_solutions"], ["Window.sln"])
        self.assertEqual(result["dependencies"][0]["name"], "Mapsui")
        self.assertEqual(result["visual_studio_components"][0]["status"], "NOT CHECKED")
        self.assertEqual(work["required-tool:visual-studio"]["status"], "BLOCKED")
        self.assertEqual(work["edit"]["selected_candidate"], "rider")
        self.assertEqual(work["build"]["selected_candidate"], "dotnet-cli")
        self.assertEqual(result["tasks_on_hold"], ["required-tool:visual-studio"])
        self.assertEqual(result["existing_solution_paths"][1]["test"], "NOT RUN")
        self.assertTrue(result["continue_independent_work"])
        self.assertEqual(source.read_text(encoding="utf-8"), original)

    def test_hard_sdk_pin_blocks_only_its_dependent_action(self):
        self.make_wpf_project()
        (self.root / "global.json").write_text(
            '{"sdk":{"version":"8.0.100","rollForward":"disable"}}', encoding="utf-8")
        result, rows = self.inspect(local_tools(editors=["VS Code"]), mode="existing")
        self.assertEqual(result["tasks_on_hold"], ["build"])
        self.assertEqual(rows["inspect"]["status"], "CONTINUE")
        self.assertEqual(rows["edit"]["selected_candidate"], "vscode")
        self.assertIsNone(rows["build"]["selected_candidate"])

    def test_corrupt_sdk_config_pauses_build_and_preserves_editing(self):
        self.make_wpf_project()
        pin = self.root / "global.json"
        for text in ("{bad", '{"sdk":{"version":"eight"}}', '{"sdk":[]}'):
            with self.subTest(text=text):
                pin.write_text(text, encoding="utf-8")
                result, rows = self.inspect(local_tools(editors=["VS Code"]), mode="existing")
                self.assertEqual(result["tasks_on_hold"], ["build"])
                self.assertEqual(rows["build"]["status"], "VERIFY_REQUIRED")
                self.assertIn("global.json", rows["build"]["reason"])
                self.assertEqual(rows["edit"]["selected_candidate"], "vscode")
                self.assertEqual(pin.read_text(encoding="utf-8"), text)

    def test_missing_explicit_tool_only_pauses_the_bound_capability(self):
        self.make_wpf_project()
        for action in ("build", "visual-design"):
            with self.subTest(action=action):
                result, rows = self.inspect(local_tools(editors=["VS Code"]), mode="existing",
                                            requires_tool=[f"{action}=visual-studio"])
                self.assertEqual(result["tasks_on_hold"], [action])
                self.assertEqual(rows[action]["required_tools"][0]["id"], "visual-studio")
                self.assertEqual(rows[action]["status"], "BLOCKED")
                self.assertEqual(rows["edit"]["selected_candidate"], "vscode")
                if action == "visual-design":
                    self.assertEqual(rows["build"]["selected_candidate"], "dotnet-cli")
        _, rows = self.inspect(local_tools(), mode="existing", requires_tool=["build=dotnet-cli"])
        self.assertEqual(rows["build"]["selected_candidate"], "dotnet-cli")

    def test_linked_library_and_solution_path_keep_project_selection_scoped(self):
        app, original = self.make_wpf_project()
        (self.root / "Core").mkdir()
        library = '<Project Sdk="Microsoft.NET.Sdk"><TargetFramework>net8.0</TargetFramework></Project>'
        (self.root / "Core" / "Core.csproj").write_text(library, encoding="utf-8")
        app.write_text(original.replace("</Project>", r'<ItemGroup><ProjectReference Include="Core\Core.csproj" /></ItemGroup></Project>'),
                       encoding="utf-8")
        result, rows = self.inspect(local_tools(), mode="existing")
        self.assertEqual(result["target"], "wpf")
        self.assertEqual(result["target_version"], "8.0")
        self.assertEqual(rows["build"]["status"], "CANDIDATE")
        (self.root / "Independent.csproj").write_text(library, encoding="utf-8")
        result, rows = self.inspect(local_tools(), mode="existing")
        self.assertIsNone(result["target"])
        self.assertEqual(rows["build"]["status"], "VERIFY_REQUIRED")
        (self.root / "Window.slnx").write_text(
            '<Solution><Project Path="Window.csproj"/><Project Path="Core/Core.csproj"/></Solution>', encoding="utf-8")
        (self.root / "Window.sln").write_text(
            'Project("{TYPE}") = "Window", "Window.csproj", "{APP}"\nEndProject\n'
            'Project("{TYPE}") = "Core", "Core\\Core.csproj", "{CORE}"\nEndProject\n', encoding="utf-8")
        for entry in ("Window.csproj", "Window.sln", "Window.slnx"):
            with self.subTest(entry=entry):
                result, rows = self.inspect(local_tools(), mode="existing", project_file=entry)
                self.assertEqual(result["build_entry"], entry)
                self.assertEqual(result["primary_project"], "Window.csproj")
                self.assertEqual(rows["build"]["status"], "CANDIDATE")
        with self.assertRaises(ValueError):
            self.inspect(local_tools(), mode="existing", project_file="../other.csproj")

    def test_explicit_editor_file_is_observed_without_claiming_compatibility(self):
        executable = self.root / "Code.exe"
        executable.write_text("synthetic file", encoding="utf-8")
        self.make_wpf_project()
        result, rows = self.inspect(local_tools(), mode="existing", tool_paths=[f"vscode={executable}"])
        self.assertEqual(result["supplied_tool_paths"]["vscode"]["status"], "VERIFY_REQUIRED")
        candidate = next(row for row in rows["edit"]["options"] if row["id"] == "vscode")
        self.assertEqual(candidate["basis"], "USER_PATH_ONLY")
        self.assertIsNone(rows["edit"]["selected_candidate"])
        with self.assertRaises(ValueError):
            self.inspect(local_tools(), mode="existing", tool_paths=["vscode=Code.exe"])

    def test_legacy_and_conflicting_project_targets_stay_under_review(self):
        (self.root / "Legacy.csproj").write_text(
            "<Project><TargetFrameworkVersion>v4.8</TargetFrameworkVersion></Project>", encoding="utf-8")
        legacy, routes = self.inspect(local_tools(), mode="existing")
        self.assertEqual(routes["build"]["status"], "VERIFY_REQUIRED")
        self.assertEqual(legacy["existing_solution_paths"], [])
        self.make_wpf_project()
        conflicting, routes = self.inspect(local_tools(), mode="existing", target="qt-widgets")
        self.assertIn("wpf", conflicting["detected_targets"])
        self.assertEqual(routes["build"]["status"], "VERIFY_REQUIRED")

    def test_dependency_sources_are_bounded_and_urls_or_private_inputs_stay_out(self):
        (self.root / "package.json").write_text(
            '{"dependencies":{"leaflet":"1.9.4","sample":"https://token@private.invalid/package"}}', encoding="utf-8")
        (self.root / "requirements.txt").write_text(
            "numpy==1.26.4\n-r https://token@private.invalid/other.txt\n", encoding="utf-8")
        (self.root / "testing data").mkdir()
        (self.root / "testing data" / "requirements.txt").write_text("secret-lib==9\n", encoding="utf-8")
        result, _ = self.inspect(local_tools(), mode="existing", target="node")
        items = {row["name"]: row for row in result["dependencies"]}
        self.assertEqual(set(items), {"leaflet", "sample", "numpy"})
        self.assertIsNone(items["sample"]["declared_version"])
        self.assertNotIn("private.invalid", str(result))
        self.assertTrue(all(row["installation_status"] == "NOT CHECKED" for row in items.values()))

    def test_named_ide_path_only_stays_unverified(self):
        inv = local_tools()
        inv["tool_candidates"] = {"Visual Studio": {"status": "FOUND_ON_PATH_NOT_EXECUTED"}}
        result, rows = self.inspect(inv, mode="new", target="dotnet", target_version="8",
                                    required_tools=["visual-studio"])
        self.assertEqual(rows["required-tool:visual-studio"]["options"][0]["basis"], "PATH_ONLY")
        self.assertEqual(rows["required-tool:visual-studio"]["status"], "VERIFY_REQUIRED")
        self.assertEqual(rows["build"]["status"], "CANDIDATE")
        self.assertTrue(result["continue_independent_work"])
