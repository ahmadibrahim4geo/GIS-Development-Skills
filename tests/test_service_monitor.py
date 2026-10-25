import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("monitor", ROOT / "scripts/monitor_public_services.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


class ServiceMonitorTests(unittest.TestCase):
    def test_status_classification(self):
        self.assertEqual(mod.classify(200), "reachable")
        self.assertEqual(mod.classify(401), "auth_required")
        self.assertEqual(mod.classify(429), "rate_limited")
        self.assertEqual(mod.classify(410), "deprecated")
        self.assertEqual(mod.classify(405), "unknown")
        self.assertEqual(mod.classify(200, True), "policy_changed")

    def test_localhost_and_cloud_metadata_rejected(self):
        def local_resolver(host, port, type):
            return [(0, 0, 0, "", ("169.254.169.254", 443))]
        self.assertFalse(mod.valid_url("https://example.org/docs", {"example.org"}, local_resolver))
        self.assertFalse(mod.valid_url("http://example.org/docs", {"example.org"}, local_resolver))
        self.assertFalse(mod.valid_url("https://example.org:8080/docs", {"example.org"}, local_resolver))
        self.assertFalse(mod.valid_url("https://localhost/path", {"example.org"}, local_resolver))

    def test_offline_report_never_calls_service(self):
        catalog = json.loads((ROOT / "references/free-geospatial-apis.json").read_text(encoding="utf-8"))
        records = mod.inspect(catalog["services"], {"open-meteo.com"}, network=False)
        self.assertEqual(len(records), len(catalog["services"]))
        self.assertTrue(all(x["status"] == "unknown" for x in records))
        self.assertTrue(all("offline-only" in x["reason"] for x in records))
