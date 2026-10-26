"""Upstream license evidence validation and coverage reporting, no network access."""
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def mod(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    obj=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj

class LicenseAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.audit=mod("license_audit","scripts/audit_license_catalog.py")
        cls.validator=mod("catalog_license_validator","scripts/validate_catalog.py")
        cls.catalog=json.loads((ROOT/"references/project-catalog.json").read_text(encoding="utf-8"))

    def test_evidence_coverage_is_explicit(self):
        summary=self.audit.classify(self.catalog["projects"])
        self.assertEqual(len(self.catalog["projects"]),summary["total"])
        self.assertGreaterEqual(summary["verified_source_licenses"],8)
        self.assertEqual(summary["verified_source_licenses"]+summary["unverified_source_licenses"],summary["total"])
        self.assertEqual([],self.audit.scan(self.catalog["projects"]))
        self.assertEqual([],self.validator.validate_catalog())

    def test_missing_license_evidence_is_an_error(self):
        source=next(x for x in self.catalog["projects"] if x.get("license_verified"))
        fake=dict(source)
        fake.pop("license_evidence_url",None)
        self.assertTrue(any("license_evidence_url" in x for x in self.audit.scan([fake])))

    def test_paid_vendor_is_separate_from_repo_code(self):
        source=next(x for x in self.catalog["projects"] if x["url"]=="https://github.com/Esri/arcgis-python-api")
        self.assertTrue(source["license_verified"])
        self.assertIn("ArcGIS platform",source["license_caveat"])
        self.assertIn("free-first", (ROOT/"references/free-first-policy.md").read_text(encoding="utf-8").lower())

    def test_bilingual_site_displays_license_coverage_from_json(self):
        page=(ROOT/"explorer.html").read_text(encoding="utf-8")
        for s in ('id="licenseAuditProgress"','renderLicenseAudit()','entry.license_verified===true','licenseAuditLabel:"تم التحقق'):
            self.assertIn(s,page)
        guide=(ROOT/"references/upstream-license-audit.md").read_text(encoding="utf-8")
        self.assertIn("130 remain unverified",guide)
