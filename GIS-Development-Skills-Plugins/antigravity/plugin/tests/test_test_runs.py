"""Offline tests for fixture isolation and observed test-run receipts."""

import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from scripts import project_governance as governance
from scripts import test_runs


class TestRunEvidenceTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        governance.init(self.root)
        self.source = self.root / "testing data/map.asc"
        self.source.write_bytes(b"ncols 2\nnrows 2\ncellsize 30\nNODATA_value -9999\n1 2\n3 4\n")
        self.expect = self.root / "expected.json"
        self.expect.write_text(json.dumps({"checks": [
            {"artifact": "map.json", "comparison": "json", "expected": {"nodata": -9999}},
            {"artifact": "grid.asc", "comparison": "sha256",
             "expected": hashlib.sha256(self.source.read_bytes()).hexdigest()}
        ]}), encoding="utf-8")

    def prepare(self):
        entry = governance.new_test_run(self.root, "Raster", inputs=["map.asc"],
                                        expect="expected.json", license_note="synthetic")
        return entry["id"], self.root / entry["run"]

    def test_inventory_and_snapshot_leave_inputs_untouched(self):
        before = self.source.read_bytes()
        inventory = test_runs.inventory(self.root)
        self.assertEqual(inventory["files"][0]["metadata"]["nodata_value"], "-9999")
        first_id, first = self.prepare()
        second_id, _ = self.prepare()
        self.assertEqual((first_id, second_id), ("0001", "0002"))
        self.assertEqual((first / "inputs/map.asc").read_bytes(), before)
        self.assertEqual(self.source.read_bytes(), before)
        self.assertIn("Status: NOT RUN", (first / "TEST_RUN.md").read_text(encoding="utf-8"))

    def test_readback_checks_declared_json_hash_and_source_integrity(self):
        run_id, run = self.prepare()
        (run / "outputs/map.json").write_text('{"nodata": -9999}', encoding="utf-8")
        (run / "outputs/grid.asc").write_bytes(self.source.read_bytes())
        receipt = test_runs.record(self.root, run_id, "local fixture test", "Python", "30 m grid")
        self.assertEqual(receipt["status"], "PASS")
        self.assertTrue(receipt["originals_unchanged"])
        self.assertTrue(receipt["fixture_copies_unchanged"])
        self.assertEqual(receipt["checks"][0]["actual"], {"nodata": -9999})
        self.assertIn("Status: PASS", (run / "TEST_RUN.md").read_text(encoding="utf-8"))
        self.assertEqual(test_runs.record(self.root, run_id, "local fixture test", "Python", "30 m grid"), receipt)

    def test_wrong_or_missing_artifacts_and_changed_input_fail(self):
        run_id, run = self.prepare()
        (run / "outputs/map.json").write_text('{"nodata": false}', encoding="utf-8")
        self.source.write_bytes(b"changed outside the tool")
        receipt = test_runs.record(self.root, run_id, "local fixture test", "Python", "30 m grid")
        self.assertEqual(receipt["status"], "FAIL")
        self.assertFalse(receipt["originals_unchanged"])
        self.assertEqual([item["status"] for item in receipt["checks"]], ["FAIL", "FAIL"])
        self.assertEqual(self.source.read_bytes(), b"changed outside the tool")

    def test_outside_copy_or_readback_is_rejected_before_allocation(self):
        with self.assertRaises(ValueError):
            governance.new_test_run(self.root, "Escape", inputs=["../expected.json"], expect="expected.json")
        self.expect.write_text(
            '{"checks":[{"artifact":"../RUN.json","comparison":"json","expected":{}}]}',
            encoding="utf-8")
        with self.assertRaises(ValueError):
            governance.new_test_run(self.root, "Escape", inputs=["map.asc"], expect="expected.json")
        self.assertEqual(governance.numbered(self.root / "testing results"), [])


if __name__ == "__main__":
    unittest.main()
