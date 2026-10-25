"""Offline regression guard: independently documented KML/KMZ upstream licenses.

This verifies that our local review keeps precise upstream evidence links.
It does NOT perform online license checking or legal compatibility analysis.
"""
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "references" / "kml-kmz-repository-review.md"

# Repository, primary license label, and official upstream license-file URL.
SOURCES = {
    "google/libkml": ("BSD-3-Clause", "https://github.com/google/libkml/blob/master/LICENSE"),
    "OSGeo/gdal": ("MIT-style core", "https://github.com/OSGeo/gdal/blob/master/LICENSE.TXT"),
    "cleder/fastkml": ("LGPL-2.1", "https://github.com/cleder/fastkml/blob/develop/LICENSE"),
    "tylere/pykml": ("BSD-3-Clause", "https://github.com/tylere/pykml/blob/master/LICENSE.txt"),
    "CesiumGS/cesium": ("Apache-2.0", "https://github.com/CesiumGS/cesium/blob/main/LICENSE.md"),
    "mapbox/togeojson": ("BSD-2-Clause", "https://github.com/mapbox/togeojson/blob/master/LICENSE"),
    "qgis/QGIS": ("GPL-2.0 family", "https://github.com/qgis/QGIS/blob/master/COPYING"),
}


class KmlUpstreamLicenseReviewTests(unittest.TestCase):
    def test_each_reviewed_dependency_has_upstream_license_evidence(self):
        table = REVIEW.read_text(encoding="utf-8")
        for repo, (license_label, evidence_url) in SOURCES.items():
            with self.subTest(repository=repo):
                rows = [
                    line for line in table.splitlines()
                    if line.startswith("| [") and "](https://github.com/" + repo + ") |" in line
                ]
                self.assertEqual(len(rows), 1, "one review row is required per source")
                self.assertIn(license_label, rows[0])
                self.assertIn(evidence_url, rows[0])

    def test_license_scope_and_host_acceptance_not_overstated(self):
        review = REVIEW.read_text(encoding="utf-8")
        self.assertIn("not redistribution", review.lower())
        self.assertIn("cannot override upstream licenses", review.lower())
        self.assertIn("not permanent clearance", review.lower())
        self.assertIn("not scene-fidelity equivalence", review.lower())
        self.assertIn("actual round-trip", review.lower())


if __name__ == "__main__":
    unittest.main()
