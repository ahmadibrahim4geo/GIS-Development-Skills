#!/usr/bin/env python3
"""Python T0/T1 verification suite for Phase P06 Mobile GIS Expansion (M01-M10, MOB-01..20, GIS-015)."""

import copy
import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REFERENCES = ROOT / "references"
MOBILE_EXAMPLES = ROOT / "examples" / "mobile-gis"
SHARED_FIXTURES = ROOT / "tests" / "shared-gis-fixtures"
MOBILE_TEST_FILE = ROOT / "tests" / "mobile-gis" / "test_mobile_contracts.py"


class MobileGISExpansionP06Tests(unittest.TestCase):
    """Verifies P06 Mobile references, 20 6-folder templates, shared contracts, and evidence gate."""

    def test_mobile_references_guides_and_skill_wiring(self):
        expected_refs = (
            "mobile-gis-architecture.md",
            "mobile-gis-platform-selection.md",
            "mobile-gis-stack-decision.md",
            "mobile-gis-device-gnss-rtk.md",
            "web-mobile-testing-release-guide.md",
            "web-mobile-offline-sync-contract.md",
            "mobile-gis-offline-sync.md",
            "mobile-gis-authentication.md",
            "mobile-gis-device-test-matrix.md",
        )
        skill_text = (ROOT / "skills" / "gis-mobile-application-development" / "SKILL.md").read_text(encoding="utf-8")
        for ref in expected_refs:
            fpath = REFERENCES / ref
            self.assertTrue(fpath.is_file(), f"Missing P06 reference: {ref}")
            self.assertGreater(fpath.stat().st_size, 1000, f"Reference {ref} suspiciously sparse")
            self.assertIn(ref, skill_text, f"Mobile SKILL.md must link {ref}")

        for token in (
            "geospatial-engine-selection",
            "M01–M10",
            "maplibre-flutter-maplibre",
            "maplibre_gl",
            "macOS + Xcode",
            "MOBILE_GIS_GUIDE.md",
            "WEB_MOBILE_GUIDE.ar.md",
            "tile.openstreetmap.org",
            "NOT RUN",
        ):
            self.assertIn(token, skill_text)

        self.assertTrue((ROOT / "docs" / "MOBILE_GIS_GUIDE.md").is_file())
        self.assertTrue((ROOT / "docs" / "WEB_MOBILE_GUIDE.ar.md").is_file())

    def test_all_20_mobile_templates_have_six_subfolders_and_honest_verdicts(self):
        self.assertTrue((MOBILE_EXAMPLES / "README.md").is_file())
        self.assertTrue((MOBILE_EXAMPLES / "shared" / "mobile_field_core.py").is_file())

        for num in range(1, 21):
            tid = f"MOB-{num:02d}"
            tdir = MOBILE_EXAMPLES / "templates" / tid
            self.assertTrue(tdir.is_dir(), f"Missing mobile template {tid}")
            for sub in ("fixtures", "spec", "tests", "evidence", "docs", "safety"):
                self.assertTrue((tdir / sub).is_dir(), f"{tid} missing required subfolder '{sub}'")
            spec = json.loads((tdir / "spec" / "template-spec.json").read_text(encoding="utf-8"))
            self.assertEqual(spec["template_id"], tid)
            ev = json.loads((tdir / "evidence" / "STATUS.json").read_text(encoding="utf-8"))
            self.assertEqual(ev["t3_android_emulator_or_device"], "NOT_RUN")
            self.assertEqual(ev["t3_ios_simulator_or_device"], "NOT_RUN")
            self.assertEqual(ev["t4_signed_release"], "NOT_RUN")

        self.assertTrue((MOBILE_EXAMPLES / "templates" / "MOB-01" / "MainActivity.kt").is_file())
        self.assertTrue((MOBILE_EXAMPLES / "templates" / "MOB-02" / "FieldCollectorView.swift").is_file())
        self.assertTrue((MOBILE_EXAMPLES / "templates" / "MOB-03" / "pubspec.yaml").is_file())
        self.assertTrue((MOBILE_EXAMPLES / "templates" / "MOB-08" / "run_gnss_logger_contract.py").is_file())

    def test_mobile_contract_suite_and_mob08_runner(self):
        sub_tests = subprocess.run(
            [sys.executable, "-B", str(MOBILE_TEST_FILE)],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(0, sub_tests.returncode, f"mobile contracts failed:\n{sub_tests.stdout}\n{sub_tests.stderr}")

        mob08 = subprocess.run(
            [sys.executable, "-B", str(MOBILE_EXAMPLES / "templates" / "MOB-08" / "run_gnss_logger_contract.py")],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, mob08.returncode, f"MOB-08 runner failed:\n{mob08.stdout}\n{mob08.stderr}")
        self.assertIn("GNSS MOB-08 T1 OK: orthometric_egm2008 27.5", mob08.stdout)

    def test_mobile_device_evidence_validator_rejects_fake_ios_or_fixture_passes(self):
        ev_chk = subprocess.run(
            [
                sys.executable,
                "-B",
                str(ROOT / "scripts" / "validate_mobile_device_evidence.py"),
                str(MOBILE_EXAMPLES / "device-acceptance.example.json"),
            ],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, ev_chk.returncode, ev_chk.stderr)

        sys.path.insert(0, str(ROOT / "scripts"))
        import validate_mobile_device_evidence as vme  # noqa: E402

        fake_ios_emu = {
            "schema_version": "1.0",
            "cases": [
                {
                    "case_id": "MOB-02",
                    "platform": "ios",
                    "mode": "emulator",
                    "status": "PASS",
                    "device": "Windows CI",
                    "os_version": "18",
                    "app_build_sha": "abc123",
                    "observed": "claimed pass",
                    "evidence": ["log.txt"],
                }
            ],
        }
        self.assertTrue(any("iOS emulator label invalid" in err for err in vme.validate_report(copy.deepcopy(fake_ios_emu))))

    def test_shared_contracts_retain_p05_and_add_p06_15_fields(self):
        contracts = json.loads((SHARED_FIXTURES / "expected-shared-contracts.json").read_text(encoding="utf-8"))
        self.assertEqual(4, contracts["gis_001_expected"]["feature_count"])
        self.assertIn("gis_015_vertical_datum_z_utc", contracts)
        self.assertEqual(15, len(contracts["mobile_sync_15_fields"]))
        self.assertEqual(contracts["mobile_sync_15_fields"][0], "project_id")
        self.assertEqual(contracts["mobile_sync_15_fields"][-1], "sync_state")


if __name__ == "__main__":
    unittest.main()
