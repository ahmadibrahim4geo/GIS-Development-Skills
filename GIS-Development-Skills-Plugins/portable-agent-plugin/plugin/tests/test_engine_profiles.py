#!/usr/bin/env python3
"""Tests for scripts/validate_engine_profiles.py and scripts/engine_repo_metadata.py."""

import http.server
import json
import subprocess
import sys
import tempfile
import threading
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import engine_repo_metadata as repo_meta  # noqa: E402
from scripts import validate_engine_profiles as vep  # noqa: E402


class _MockGitHubHandler(http.server.BaseHTTPRequestHandler):
    routes: dict[str, tuple[int, dict[str, str], bytes]] = {}

    def do_GET(self):  # noqa: N802
        status, headers, body = self.routes.get(
            self.path,
            (404, {"Content-Type": "application/json"}, b'{"message": "Not Found"}'),
        )
        self.send_response(status)
        for k, v in headers.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, format, *args):  # noqa: A002
        return


class EngineProfilesAndMetadataTests(unittest.TestCase):
    """Covers validate_engine_profiles.py (E17, E21, E24) and mocked HTTP metadata (E18, E32, E-43)."""

    def test_validate_engine_profiles_cli_and_cycle_rejection_E24(self):
        errors = vep.validate_profiles()
        self.assertEqual([], errors, f"Profile validation errors: {errors}")

        res = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "validate_engine_profiles.py"), "--format", "json"],
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(0, res.returncode, res.stderr)
        self.assertTrue(json.loads(res.stdout)["valid"])

        # Negative test: circular dependency must fail.
        cat_orig = json.loads((ROOT / "references" / "project-catalog.json").read_text(encoding="utf-8"))
        prof_orig = json.loads((ROOT / "references" / "engine-capability-profiles.json").read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            tmp_dir = Path(tmp)
            p_by_id = {p["project_id"]: p for p in prof_orig["profiles"]}
            p_by_id["osgeo-proj"]["relationships"].append(
                {"type": "requires", "target_id": "osgeo-gdal", "notes": "synthetic cycle"}
            )
            cat_file = tmp_dir / "cat.json"
            prof_file = tmp_dir / "prof.json"
            cat_file.write_text(json.dumps(cat_orig), encoding="utf-8")
            prof_file.write_text(json.dumps(prof_orig), encoding="utf-8")
            cyc_errors = vep.validate_profiles(catalog_path=cat_file, profiles_path=prof_file)
            self.assertTrue(any("Circular dependency" in e for e in cyc_errors), cyc_errors)

    def test_v2_architecture_traversal_and_unverified_component_checks_E24(self):
        with tempfile.TemporaryDirectory() as tmp:
            bad = Path(tmp) / "arch.json"
            bad.write_text(
                json.dumps(
                    {
                        "schema_version": "2.0",
                        "intent": ["multi-engine-composition"],
                        "source_host": "custom",
                        "target_host": "windows",
                        "ui": {"framework": "Qt", "reference_reuse_mode": "independent-design", "status": "source-reviewed"},
                        "components": [
                            {
                                "component_id": "c1",
                                "project_id": "osgeo-gdal",
                                "role": "geospatial-engine",
                                "version": None,
                                "source_ref": None,
                                "integration_mode": "in-process",
                                "capabilities": ["io.vector.read"],
                                "status": "source-reviewed",
                            }
                        ],
                        "capability_requirements": ["io.vector.read"],
                        "preserved_invariants": ["CRS fidelity"],
                        "license_policy": "free-first",
                        "flow_spec_ref": "../outside/evil.json",
                    }
                ),
                encoding="utf-8",
            )
            issues = vep.validate_v2_architecture(bad)
            self.assertTrue(any("traversal" in e.lower() or "unsafe" in e.lower() for e in issues), issues)
            self.assertTrue(any("source_ref and version" in e for e in issues), issues)

    def test_repo_metadata_mocked_http_edge_cases_E18_E32(self):
        with self.assertRaises(ValueError):
            repo_meta.normalize_repo_slug("https://evil.example.com/a/b")
        with self.assertRaises(ValueError):
            repo_meta.fetch_repo_metadata("osgeo/gdal", _api_base="https://evil.example.com")

        _MockGitHubHandler.routes = {
            "/repos/osgeo/gdal": (
                200,
                {"Content-Type": "application/json"},
                json.dumps(
                    {
                        "full_name": "OSGeo/gdal",
                        "html_url": "https://github.com/OSGeo/gdal",
                        "default_branch": "master",
                        "archived": False,
                        "pushed_at": "2026-11-20T00:00:00Z",
                        "stargazers_count": 5000,
                        "language": "C++",
                        "topics": ["gis", "gdal"],
                        "license": {"spdx_id": "MIT"},
                    }
                ).encode("utf-8"),
            ),
            "/repos/old/archived-gis": (
                200,
                {"Content-Type": "application/json"},
                json.dumps(
                    {
                        "full_name": "old/archived-gis",
                        "default_branch": "main",
                        "archived": True,
                        "license": {"spdx_id": "MIT"},
                    }
                ).encode("utf-8"),
            ),
            "/repos/missing/repo": (404, {"Content-Type": "application/json"}, b'{"message":"Not Found"}'),
            "/repos/rate/limited": (
                429,
                {"Content-Type": "application/json", "Retry-After": "60"},
                b'{"message":"API rate limit"}',
            ),
            "/repos/redirect/me": (302, {"Location": "https://evil.example.com/payload"}, b""),
            "/repos/bad/json": (200, {"Content-Type": "application/json"}, b"{not valid json"),
            "/repos/huge/payload": (200, {"Content-Type": "application/json"}, b"{" + b"a" * (repo_meta.MAX_RESPONSE_BYTES + 10)),
        }

        server = http.server.HTTPServer(("127.0.0.1", 0), _MockGitHubHandler)
        port = server.server_address[1]
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{port}"
        try:
            with tempfile.TemporaryDirectory() as cache_tmp:
                cdir = Path(cache_tmp)
                ok = repo_meta.fetch_repo_metadata("osgeo/gdal", cache_dir=cdir, _api_base=base)
                self.assertEqual(ok["state"], "metadata-only")
                self.assertFalse(ok["license_verified"])
                self.assertEqual(ok["integration_recommendation"], "reference-only")
                self.assertFalse(ok["cache_hit"])

                ok_cached = repo_meta.fetch_repo_metadata("osgeo/gdal", cache_dir=cdir, _api_base="http://127.0.0.1:1")
                self.assertTrue(ok_cached["cache_hit"])
                self.assertEqual(ok_cached["repo"], "OSGeo/gdal")

                arch = repo_meta.fetch_repo_metadata("old/archived-gis", _api_base=base)
                self.assertTrue(arch["archived"])
                self.assertEqual(arch["integration_recommendation"], "archived-review-required")

                not_found = repo_meta.fetch_repo_metadata("missing/repo", _api_base=base)
                self.assertEqual(not_found["state"], "unresolved")
                self.assertEqual(not_found["reason"], "not-found")

                limited = repo_meta.fetch_repo_metadata("rate/limited", _api_base=base)
                self.assertEqual(limited["state"], "unresolved")
                self.assertTrue(limited["rate_limited"])
                self.assertEqual(limited["retry_after"], "60")

                redir = repo_meta.fetch_repo_metadata("redirect/me", _api_base=base)
                self.assertEqual(redir["state"], "unresolved")
                self.assertEqual(redir["reason"], "redirect-blocked")

                bad = repo_meta.fetch_repo_metadata("bad/json", _api_base=base)
                self.assertEqual(bad["state"], "unresolved")
                self.assertEqual(bad["reason"], "invalid-json")

                huge = repo_meta.fetch_repo_metadata("huge/payload", _api_base=base)
                self.assertEqual(huge["state"], "unresolved")
                self.assertEqual(huge["reason"], "response-exceeds-1mb-limit")
        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
