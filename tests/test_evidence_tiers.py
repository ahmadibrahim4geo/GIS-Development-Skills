"""Canonical T0-T4 registry and documentation-drift checks."""
import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "evidence_tiers", ROOT / "scripts" / "validate_evidence_tiers.py")
tiers = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tiers)


class EvidenceTierRegistryTests(unittest.TestCase):
    def test_registry_is_ordered_and_native_boundary_is_explicit(self):
        data, errors = tiers.load_registry()
        self.assertEqual([], errors)
        self.assertEqual(["T0", "T1", "T2", "T3", "T4"],
                         [item["id"] for item in data["tiers"]])
        self.assertFalse(data["tiers"][1]["native_runtime_required"])
        self.assertTrue(data["tiers"][2]["native_runtime_required"])
        self.assertTrue(data["tiers"][3]["output_readback_required"])
        self.assertTrue(data["tiers"][4]["clean_environment_required"])

    def test_offline_fixture_cannot_be_called_t2(self):
        errors = tiers.scan_text("This is a T2 synthetic fixture.", "bad.md")
        self.assertTrue(errors)
        errors = tiers.scan_text("Offline fixture-only evidence: T2.", "bad.md")
        self.assertTrue(errors)

    def test_canonical_native_t2_wording_is_allowed(self):
        text = ("T1 deterministic offline fixture. "
                "T2 observed load in QGIS 3.40. "
                "T3 processing output reopened and compared.")
        self.assertEqual([], tiers.scan_text(text, "good.md"))

    def test_malformed_registry_is_rejected(self):
        errors = tiers.validate_registry({"schema_version": "1.0", "tiers": []})
        self.assertTrue(errors)


if __name__ == "__main__":
    unittest.main()
