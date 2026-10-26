"""Ensure native mobile GIS outcomes are never falsely declared PASS in CI."""
import copy
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("mobile_device_evidence", ROOT / "scripts/validate_mobile_device_evidence.py")
import sys
validator = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validator
spec.loader.exec_module(validator)


class MobileEvidenceTests(unittest.TestCase):
    def make_report(self, **fields):
        case = {
            "case_id": "MOB-02",
            "platform": "android",
            "mode": "emulator",
            "status": "PASS",
            "device": "Android emulator test fixture",
            "os_version": "SDK 35",
            "app_build_sha": "abcdef123",
            "observed": "verified edit readback in actual mobile runtime",
            "evidence": ["artifacts/android-edit-log.txt"],
        }
        case.update(fields)
        return {"schema_version": "1.0", "cases": [case]}

    def test_complete_emulator_evidence_shape(self):
        self.assertEqual([], validator.validate_report(self.make_report()))

    def test_no_fake_native_pass_from_ci_fixture(self):
        problems = validator.validate_report(self.make_report(mode="ci-fixture"))
        self.assertTrue(any("fixture cannot PASS" in e for e in problems))

    def test_gnss_hardware_requires_physical_device(self):
        errors = validator.validate_report(self.make_report(case_id="MOB-03"))
        self.assertTrue(any("physical device" in e for e in errors))

    def test_missing_evidence_cannot_pass(self):
        errors = validator.validate_report(self.make_report(evidence=[]))
        self.assertTrue(any("requires evidence" in e for e in errors))

    def test_not_run_requires_reason(self):
        errors = validator.validate_report(self.make_report(status="NOT_RUN", reason=""))
        self.assertTrue(any("requires honest reason" in e for e in errors))

    def test_duplicate_cases_rejected(self):
        report = self.make_report()
        report["cases"].append(copy.deepcopy(report["cases"][0]))
        self.assertTrue(any("duplicate" in e for e in validator.validate_report(report)))

    def test_malformed_types_are_validation_errors_not_exceptions(self):
        report = self.make_report(platform=[], mode={}, status=12, case_id=[])
        problems = validator.validate_report(report)
        self.assertGreaterEqual(len(problems), 3)

    def test_example_reports_non_execution_truthfully(self):
        import json
        report = json.loads((ROOT / "examples/mobile-gis/device-acceptance.example.json").read_text(encoding="utf-8"))
        self.assertEqual([], validator.validate_report(report))
        self.assertTrue(all(x["status"] == "NOT_RUN" for x in report["cases"]))


if __name__ == "__main__":
    unittest.main()
