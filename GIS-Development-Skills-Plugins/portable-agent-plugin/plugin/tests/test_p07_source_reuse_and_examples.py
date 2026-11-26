#!/usr/bin/env python3
"""P07 Source Reuse, Forking, Reference UI & Multi-Engine Integration Tests (T0/T1)."""

import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EXAMPLES = ROOT / "examples" / "engine-selection"
SCRIPTS = ROOT / "scripts"
REFS = ROOT / "references"


class P07SourceReuseAndExamplesTests(unittest.TestCase):
    """Validates P07 references, 8 runnable example packages, Qt .ui inspection, and E-rules."""

    def test_p07_references_and_qgis_skill_wiring(self):
        refs = (
            "source-fork-and-ui-reuse.md",
            "reference-ui-engine-mapping.md",
            "engine-integration-patterns.md",
        )
        for name in refs:
            fpath = REFS / name
            self.assertTrue(fpath.is_file(), f"Missing P07 reference: {name}")
            self.assertGreater(fpath.stat().st_size, 1500)

        qgis_skill = (ROOT / "skills" / "qgis-engine-integration" / "SKILL.md").read_text(encoding="utf-8")
        for token in (
            "source-fork-and-ui-reuse.md",
            "engine-integration-patterns.md",
            "inventory_ui_actions.py",
            "clean-room-reference-implementation",
            "geospatial-engine-selection",
        ):
            self.assertIn(token, qgis_skill)

        fork_doc = (REFS / "source-fork-and-ui-reuse.md").read_text(encoding="utf-8")
        for state in ("KEEP", "HIDE", "DISABLE", "REMOVE", "REPLACE", "DEFER"):
            self.assertIn(state, fork_doc)
        self.assertIn("GeoLibre", fork_doc)
        self.assertIn("RustGIS", fork_doc)

    def test_all_8_example_packages_run_through_recommend_stack(self):
        expected_dirs = (
            "qgis-fork",
            "arcgis-inspired-ui",
            "standalone-qgis-core",
            "virtual-globe",
            "city-engine",
            "remote-sensing",
            "crs-conversion",
            "mobile-web-gis",
        )
        req_schema = json.loads((ROOT / "schemas" / "engine-selection-request.schema.json").read_text(encoding="utf-8"))
        required_keys = set(req_schema["required"])

        for slug in expected_dirs:
            edir = EXAMPLES / slug
            self.assertTrue(edir.is_dir(), f"Missing example dir {slug}")
            req_path = edir / "request.json"
            exp_path = edir / "expected.json"
            self.assertTrue(req_path.is_file())
            self.assertTrue(exp_path.is_file())
            self.assertTrue((edir / "README.md").is_file())

            req_obj = json.loads(req_path.read_text(encoding="utf-8"))
            self.assertTrue(required_keys.issubset(req_obj.keys()), f"{slug} request missing required schema keys")

            proc = subprocess.run(
                [sys.executable, "-B", str(SCRIPTS / "recommend_stack.py"), "--request", str(req_path), "--format", "json"],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=20,
            )
            self.assertEqual(0, proc.returncode, f"recommend_stack failed on {slug}: {proc.stderr}")
            report = json.loads(proc.stdout)
            self.assertIn("recommended_stack", report)
            self.assertIn("recommended_build_models", report)
            self.assertGreaterEqual(len(report["recommended_stack"]), 1, f"{slug} produced empty recommended_stack")

    def test_e01_qgis_fork_qt_ui_inventory_and_protected_actions(self):
        ui_dir = EXAMPLES / "qgis-fork"
        proc = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPTS / "inventory_ui_actions.py"),
                "--root",
                str(ui_dir),
                "--ui-path",
                "minimal_qgis_subset.ui",
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        data = json.loads(proc.stdout)
        self.assertFalse(data["handlers_verified"])
        self.assertFalse(data["dynamic_actions_verified"])
        action_names = {a["action_id"] for a in data["actions"]}
        self.assertIn("mActionProjectSave", action_names)
        self.assertIn("mActionRemoveUnused3DPlugin", action_names)

        retention = json.loads((ui_dir / "feature_retention.json").read_text(encoding="utf-8"))
        save_entry = [r for r in retention["actions"] if r["action"] == "mActionProjectSave"][0]
        self.assertEqual("KEEP", save_entry["decision"])
        strip_entry = [r for r in retention["actions"] if r["action"] == "mActionRemoveUnused3DPlugin"][0]
        self.assertEqual("HIDE", strip_entry["decision"])

    def test_e02_e40_e26_arcgis_inspired_clean_room_guards(self):
        mapping = json.loads((EXAMPLES / "arcgis-inspired-ui" / "command_mapping.json").read_text(encoding="utf-8"))
        self.assertFalse(mapping["proprietary_assets_copied"])
        unbound = [c for c in mapping["commands"] if not c["handler_bound"]]
        self.assertEqual(1, len(unbound))
        self.assertEqual("DISABLED_UNAVAILABLE", unbound[0]["ui_state"])

        proc = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPTS / "recommend_stack.py"),
                "--request",
                str(EXAMPLES / "arcgis-inspired-ui" / "request.json"),
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        payload = proc.stdout.lower()
        self.assertIn("reference-inspired-ui", payload)
        self.assertNotIn("arcgis.desktop.dll", payload)

    def test_e08_lightweight_crs_selects_proj_without_heavy_bloat(self):
        proc = subprocess.run(
            [
                sys.executable,
                "-B",
                str(SCRIPTS / "recommend_stack.py"),
                "--request",
                str(EXAMPLES / "crs-conversion" / "request.json"),
                "--format",
                "json",
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, proc.returncode, proc.stderr)
        rec_ids = [r["project_id"] for r in json.loads(proc.stdout)["recommended_stack"]]
        self.assertIn("osgeo-proj", rec_ids)


if __name__ == "__main__":
    unittest.main()
