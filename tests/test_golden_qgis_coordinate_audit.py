"""Acceptance tests for the first golden open-source GIS workflow."""

import importlib.util
import json
import py_compile
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
EXAMPLE = ROOT / "examples" / "golden-qgis-coordinate-audit"
SPEC = importlib.util.spec_from_file_location("golden_audit_core", EXAMPLE / "audit_core.py")
CORE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CORE)


class GoldenCoordinateAuditTests(unittest.TestCase):
    def test_homepage_exposes_bilingual_golden_workflow_without_native_overclaim(self):
        homepage = (ROOT / "index.html").read_text(encoding="utf-8")
        section = homepage.split('id="golden-workflow"', 1)[1].split("</section>", 1)[0]
        self.assertIn('id="goldenWorkflowCommand"', section)
        self.assertIn("copyUsage('golden',this)", section)
        self.assertIn("T1 · VERIFIED", section)
        self.assertIn("T2–T4 · NOT RUN", section)
        self.assertIn('data-lang="en"', section)
        self.assertIn('data-lang="ar"', section)
        self.assertIn("golden-qgis-coordinate-audit/README.md", section)

    def test_fixture_matches_committed_expected_artifacts(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "output"
            summary = CORE.run_audit(EXAMPLE / "fixtures" / "points.geojson", output)
            self.assertEqual(2, summary["accepted_feature_count"])
            self.assertEqual(3, summary["rejected_feature_count"])
            for name in ("audited_points.geojson", "summary.json"):
                self.assertEqual(
                    (EXAMPLE / "expected" / name).read_bytes(),
                    (output / name).read_bytes(),
                    name,
                )

    def test_cli_returns_machine_readable_summary(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "cli-output"
            result = subprocess.run(
                [
                    sys.executable,
                    str(EXAMPLE / "coordinate_audit.py"),
                    str(EXAMPLE / "fixtures" / "points.geojson"),
                    str(output),
                ],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertEqual("T1", json.loads(result.stdout)["evidence_tier"])

    def test_missing_crs_is_rejected_before_output_creation(self):
        document = {"type": "FeatureCollection", "features": []}
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "missing-crs.geojson"
            output = Path(temporary) / "output"
            source.write_text(json.dumps(document), encoding="utf-8")
            with self.assertRaisesRegex(CORE.AuditError, "EPSG:4326"):
                CORE.run_audit(source, output)
            self.assertFalse(output.exists())

    def test_malformed_geometry_is_reported_not_copied(self):
        document = {
            "type": "FeatureCollection",
            "crs": {"type": "name", "properties": {"name": "EPSG:4326"}},
            "features": [
                {
                    "type": "Feature",
                    "id": "bad",
                    "geometry": {"type": "Polygon", "coordinates": []},
                    "properties": {},
                }
            ],
        }
        artifact, summary = CORE.audit_document(document, "bad.geojson", "0" * 64)
        self.assertEqual([], artifact["features"])
        self.assertEqual("geometry-not-point", summary["rejected"][0]["reason"])

    def test_existing_output_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "existing"
            output.mkdir()
            marker = output / "keep.txt"
            marker.write_text("user data", encoding="utf-8")
            with self.assertRaisesRegex(CORE.AuditError, "must not already exist"):
                CORE.run_audit(EXAMPLE / "fixtures" / "points.geojson", output)
            self.assertEqual("user data", marker.read_text(encoding="utf-8"))

    def test_feature_limit_prevents_unbounded_batch(self):
        original = CORE.MAX_FEATURES
        CORE.MAX_FEATURES = 1
        try:
            document = json.loads((EXAMPLE / "fixtures" / "points.geojson").read_text("utf-8"))
            with self.assertRaisesRegex(CORE.AuditError, "safe limit"):
                CORE.audit_document(document, "points.geojson", "0" * 64)
        finally:
            CORE.MAX_FEATURES = original

    def test_duplicate_json_keys_are_rejected(self):
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "duplicate.geojson"
            output = Path(temporary) / "output"
            source.write_text('{"type":"FeatureCollection","type":"FeatureCollection"}', encoding="utf-8")
            with self.assertRaisesRegex(CORE.AuditError, "Duplicate JSON key"):
                CORE.run_audit(source, output)
            self.assertFalse(output.exists())

    def test_qgis_adapter_is_syntax_valid_and_native_status_is_honest(self):
        py_compile.compile(
            str(EXAMPLE / "qgis_processing" / "coordinate_audit_algorithm.py"),
            doraise=True,
        )
        py_compile.compile(str(EXAMPLE / "native_qgis_smoke.py"), doraise=True)
        evidence = json.loads((EXAMPLE / "evidence" / "offline-t1.json").read_text("utf-8"))
        self.assertEqual("verified", evidence["status"])
        self.assertEqual({"T2": "NOT RUN", "T3": "NOT RUN", "T4": "NOT RUN"}, evidence["native_qgis"])

    def test_benchmark_reports_correctness_and_rate(self):
        result = subprocess.run(
            [sys.executable, str(EXAMPLE / "benchmark_coordinate_audit.py"), "--features", "2000"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(0, result.returncode, result.stderr)
        report = json.loads(result.stdout)
        self.assertEqual("pass", report["correctness_check"])
        self.assertEqual(2000, report["feature_count"])
        self.assertGreater(report["features_per_second"], 0)


if __name__ == "__main__":
    unittest.main()
