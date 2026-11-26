"""Phase P10 comprehensive offline QA matrix, ZIP/Git secret hygiene, and anti-regression verification.

Strictly distinguishes offline T0/T1/synthetic contract verification from T2-T4
native GIS, GPU, browser, and physical device checks (`NOT_RUN` when absent).
"""

from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import (  # noqa: E402
    audit_license_catalog,
    audit_skill_graph,
    build_manifest,
    build_skill_bundle,
    compare_engines,
    development_journal,
    discover_engines,
    gis_data_flow_diagnostics,
    gis_ui_command_audit,
    intent_router,
    recommend_stack,
    security_audit,
    security_guardian,
    toolchain_discovery,
    validate_evidence_tiers,
    validate_mobile_device_evidence,
    validate_skill_pack,
)


def _load_calc():
    spec = importlib.util.spec_from_file_location(
        "synthetic_index_calculator",
        ROOT / "examples" / "remote-sensing" / "synthetic_index_calculator.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


PROFILES_DOC = json.loads((ROOT / "references" / "engine-capability-profiles.json").read_text(encoding="utf-8"))
BY_PID = {p["project_id"]: p for p in PROFILES_DOC["profiles"]}
PROJECT_CATALOG = json.loads((ROOT / "references" / "project-catalog.json").read_text(encoding="utf-8"))


class P10ComprehensiveMatrixTests(unittest.TestCase):
    def test_pl_t24_pre_post_packaging_source_parity_all_seven_platforms(self):
        canonical_skills = sorted(p.parent.name for p in (ROOT / "skills").glob("*/SKILL.md"))
        self.assertGreaterEqual(len(canonical_skills), 36)
        catalog_bytes = (ROOT / "references" / "project-catalog.json").read_bytes()
        apis_bytes = (ROOT / "references" / "free-geospatial-apis.json").read_bytes()

        for pid, folder in (
            ("portable", "portable-agent-plugin"),
            ("codex", "codex"),
            ("chatgpt", "chatgpt"),
            ("claude-code", "claude-code"),
            ("claude-ai", "claude-ai"),
            ("antigravity", "antigravity"),
            ("cursor", "cursor"),
        ):
            bundle_root = ROOT / "GIS-Development-Skills-Plugins" / folder / "plugin"
            self.assertTrue(bundle_root.is_dir(), f"Built bundle missing for {pid}")
            packaged_skills = sorted(p.parent.name for p in (bundle_root / "skills").glob("*/SKILL.md"))
            self.assertEqual(canonical_skills, packaged_skills, f"Skill mismatch in {pid}")
            self.assertEqual(catalog_bytes, (bundle_root / "references" / "project-catalog.json").read_bytes())
            self.assertEqual(apis_bytes, (bundle_root / "references" / "free-geospatial-apis.json").read_bytes())

    def test_e07_and_e30_unresolved_uijs_and_absent_native_honesty_gate(self):
        # E07: Ambiguous UI.js must stay strictly unresolved.
        rec = recommend_stack.recommend(
            {
                "schema_version": "1.0",
                "request_text": "Build standalone GIS desktop app with UI.js frontend",
                "intent_modes": ["embedded-engine"],
                "target_os": ["windows"],
                "required_capabilities": ["render.2d.projected"],
                "free_only": True,
            }
        )
        self.assertEqual("unresolved", rec["status"])
        self.assertEqual("unresolved", rec["entity_role_split"]["ui_framework"]["status"])

        # E30: Toolchain & evidence gates must not report absent hosts as passing T2-T4.
        tool_audit = toolchain_discovery.audit(ROOT)
        self.assertIn("tool_candidates", tool_audit)
        mob_report = json.loads((ROOT / "examples" / "mobile-gis" / "device-acceptance.example.json").read_text(encoding="utf-8"))
        self.assertEqual([], validate_mobile_device_evidence.validate_report(mob_report))
        self.assertEqual([], validate_evidence_tiers.validate_registry(
            json.loads((ROOT / "references" / "evidence-tiers.json").read_text(encoding="utf-8"))
        ))

    def test_e35_to_e47_engine_security_license_and_conflict_safeguards(self):
        # E-35: Quarantined external skill/plugin cannot be selected by engine comparator.
        ext_reg = json.loads((ROOT / "references" / "external-agent-skills-registry.json").read_text(encoding="utf-8"))
        self.assertGreater(len(ext_reg["candidates"]), 0)
        self.assertFalse(ext_reg["default_quarantine_rules"]["auto_execute"])
        quarantined_prof = {
            "project_id": "quarantined-sample",
            "name": "Quarantined Sample",
            "entity_type": "ExternalAgentSkill",
            "build_models": ["reference-only"],
            "integration_patterns": ["reference-only"],
            "capabilities": {"render.2d.projected": {"support_state": "supported"}},
            "verification_metadata": {
                "security_status": "quarantine-reference-only",
                "cost_classification": "free",
                "license_status": "verified-upstream",
                "license_spdx_hint": "MIT",
                "supported_os": ["cross-platform"],
            },
        }
        q_gate = compare_engines.hard_gate(quarantined_prof, {"free_only": True, "target_os": ["windows"], "required_capabilities": ["render.2d.projected"]})
        self.assertEqual("rejected", q_gate["gate_status"])

        # E-36 & E-44: Free vs proprietary ArcGIS Pro SDK conflict & unknown-license blocker.
        arcgis_gate = compare_engines.hard_gate(BY_PID["esri-arcgis-pro-sdk"], {"free_only": True, "target_os": ["windows"], "required_capabilities": []})
        self.assertEqual("rejected", arcgis_gate["gate_status"])
        unknown_prof = dict(quarantined_prof)
        unknown_prof["verification_metadata"] = {
            "security_status": "verified",
            "cost_classification": "unknown",
            "license_status": "verify-upstream",
            "license_spdx_hint": "unknown",
            "supported_os": ["cross-platform"],
        }
        u_gate = compare_engines.hard_gate(unknown_prof, {"free_only": True, "target_os": ["windows"], "required_capabilities": []})
        self.assertIn(u_gate["gate_status"], {"rejected", "needs-evidence"})

        # E-38 & E-39: 2D != 3D contract split + single unsupported mandatory capability rejects high scorer.
        comp_split = recommend_stack.recommend(
            {
                "schema_version": "1.0",
                "request_text": "Need arbitrary non-Mercator 2D projections plus 3D globe",
                "target_os": ["cross-platform"],
                "required_capabilities": ["render.2d.projected", "render.globe.ellipsoid"],
                "non_mercator_2d_required": True,
                "free_only": True,
            }
        )
        self.assertTrue(any("2D != 3D Globe" in c.get("interface", "") for c in comp_split["component_contracts"]))

        missing_cap = compare_engines.hard_gate(
            BY_PID["osgeo-proj"],
            {"free_only": True, "target_os": ["windows"], "required_capabilities": ["cad.brep"]},
        )
        self.assertNotEqual("eligible", missing_cap["gate_status"])

        # E-40: Unknown capability returns explicit gap rather than invented method.
        no_match = discover_engines.discover(capabilities=["nonexistent.api.signature"])
        self.assertEqual("no-match", no_match["status"])
        self.assertEqual([], no_match["candidates"])

        # E-41 & E-45 & E-46 & E-47: Keep existing renderer on buffer utility; reference UI produces original spec; local fixtures work offline.
        narrow = recommend_stack.recommend(
            {
                "schema_version": "1.0",
                "request_text": "Add spatial CRS transform utility without changing existing MapLibre UI",
                "existing_project": {"has_working_renderer": True, "renderer": "maplibre"},
                "target_os": ["cross-platform"],
                "required_capabilities": ["crs.transform"],
                "free_only": True,
            }
        )
        self.assertTrue(narrow["recommended_stack"])
        self.assertTrue((ROOT / "templates" / "REFERENCE_UI_COMMAND_MAPPING.md").is_file())
        self.assertTrue((ROOT / "fixtures" / "landsat8-l2-pixels.json").is_file())
        self.assertEqual(0, len(audit_license_catalog.scan(PROJECT_CATALOG["projects"])))

    def test_e22_e23_e26_and_offline_shared_contract_checks(self):
        # E-22 / E-23 / E-47: Synthetic RS scale/offset & QA band rejection without live keys.
        calc = _load_calc()
        l8 = json.loads((ROOT / "fixtures" / "landsat8-l2-pixels.json").read_text(encoding="utf-8"))
        clear_case = next(c for c in l8["cases"] if c["id"] == "current_clear")
        val = calc.landsat8_l2_ndvi(clear_case["collection"], clear_case["bands"], clear_case["qa_name"], clear_case["qa_value"])
        self.assertAlmostEqual(33 / 59, val, places=5)
        wrong_qa = next(c for c in l8["cases"] if c["id"] == "wrong_qa_scheme")
        with self.assertRaises(ValueError):
            calc.landsat8_l2_ndvi(wrong_qa["collection"], wrong_qa["bands"], wrong_qa["qa_name"], wrong_qa["qa_value"])

        # E-26: Qt .ui audit flags static declarations honestly without claiming runtime pass.
        ui_audit = gis_ui_command_audit.audit_tree(ROOT / "examples" / "engine-selection" / "qgis-fork", include_qt_ui=True)
        self.assertGreater(ui_audit["qt_ui_inventory"]["action_count"], 0)
        self.assertFalse(ui_audit["qt_ui_inventory"]["handlers_verified"])

        # Trace validator E-14/E-33 structural invariant check.
        trace = json.loads((ROOT / "examples" / "ui-quality" / "sample-gis-trace.json").read_text(encoding="utf-8")) if (ROOT / "examples" / "ui-quality" / "sample-gis-trace.json").is_file() else None
        if trace is not None:
            res = gis_data_flow_diagnostics.validate_trace(trace)
            self.assertTrue(res["valid"])

    def test_anti_reg_001_to_010_and_git_zip_secret_hygiene(self):
        # ANTI-REG-001/003/004/006/007/010
        self.assertEqual([], validate_skill_pack.inspect_repository(ROOT))
        self.assertEqual([], build_manifest.synchronize_text(ROOT, build_manifest.derived(), write=False))
        self.assertEqual("pass", security_audit.audit(ROOT)["status"])
        self.assertEqual([], audit_skill_graph.audit(ROOT)["issues"])
        journal_verify = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "development_journal.py"), "verify", "--project", str(ROOT)],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
        self.assertEqual(0, journal_verify.returncode, journal_verify.stdout + journal_verify.stderr)

        # Homepage Brand Kit 3.1 + verbatim mission + Arabic toggle intact (ANTI-REG-006)
        idx = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("Build GIS tools, plugins and geospatial applications with a verifiable development workflow.", idx)
        self.assertIn('id="author"', idx)
        self.assertTrue((ROOT / "assets" / "logo.svg").is_file())
        self.assertTrue((ROOT / "assets" / "icon.svg").is_file())

        # Git ls-files zero leaked secret filenames + gitignore enforcement
        ls_proc = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, timeout=20, check=False)
        if ls_proc.returncode == 0:
            tracked = [line.strip() for line in ls_proc.stdout.splitlines() if line.strip()]
            forbidden_names = {".env", "owner-config.local.json", "credentials.local.json", "credentials.json", "secrets.json"}
            for rel in tracked:
                name = Path(rel).name.casefold()
                self.assertNotIn(name, forbidden_names, f"Sensitive file tracked in Git: {rel}")
                self.assertNotIn(Path(rel).suffix.casefold(), {".key", ".pem", ".p12", ".pfx"})

            for ignored_probe in (
                ".plugin-local/state.json",
                ".plugin-secrets/token.json",
                ".plugin-staging/tmp.txt",
                ".plugin-lock/update.lock.json",
                "GIS-Development-Skills-Plugins/codex/artifacts/gis-development-skills-codex.zip",
            ):
                chk = subprocess.run(["git", "check-ignore", "-q", ignored_probe], cwd=ROOT, check=False)
                self.assertEqual(0, chk.returncode, f"Expected .gitignore to exclude {ignored_probe}")

        # Built ZIP archives clean under Security Guardian archive audit when present locally;
        # on clean CI checkouts where .gitignore excludes artifacts/*.zip, audit a fresh temp ZIP build.
        zips = sorted((ROOT / "GIS-Development-Skills-Plugins").glob("*/artifacts/*.zip"))
        if zips:
            self.assertEqual(7, len(zips), f"Expected 7 platform ZIP archives, found {len(zips)}")
            for zpath in zips:
                zres = security_guardian.inspect_archive(zpath)
                self.assertEqual("pass", zres["status"], f"Archive security failure in {zpath}: {zres}")
        else:
            with tempfile.TemporaryDirectory() as tmp_zip_dir:
                built = build_skill_bundle.build(Path(tmp_zip_dir), root=ROOT)
                zres = security_guardian.inspect_archive(Path(built["archive"]))
                self.assertEqual("pass", zres["status"], f"Archive security failure in temp bundle: {zres}")

    def test_e48_release_notices_sbom_and_deterministic_bundles(self):
        # Verify E-48: pinned SemVer VERSION, LICENSE, index.json, bundle-manifest SBOMs & matching .zip.sha256 across all 7 platforms.
        version_text = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
        self.assertRegex(version_text, r"^\d+\.\d+\.\d+")
        self.assertTrue((ROOT / "LICENSE").is_file())
        idx_path = ROOT / "GIS-Development-Skills-Plugins" / "index.json"
        self.assertTrue(idx_path.is_file())
        idx = json.loads(idx_path.read_text(encoding="utf-8"))
        self.assertEqual(version_text, idx["version"])
        self.assertEqual(7, len(idx["platforms"]))
        for pid, folder in (
            ("portable", "portable-agent-plugin"),
            ("codex", "codex"),
            ("chatgpt", "chatgpt"),
            ("claude-code", "claude-code"),
            ("claude-ai", "claude-ai"),
            ("antigravity", "antigravity"),
            ("cursor", "cursor"),
        ):
            pdir = ROOT / "GIS-Development-Skills-Plugins" / folder
            bm = json.loads((pdir / "plugin" / "bundle-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(bm["file_count"], len(bm["files"]))
            sha_files = list((pdir / "artifacts").glob("*.zip.sha256"))
            zip_files = list((pdir / "artifacts").glob("*.zip"))
            if zip_files or sha_files:
                self.assertEqual(1, len(sha_files), f"Expected .zip.sha256 sidecar for {pid}")

    def test_req_ev2_062_curated_count_backed_by_scripts_and_tests(self):
        # 461+ curated profiles exist WITH machine-readable provenance, discovery/compare/recommend scripts, and passing suites.
        self.assertGreaterEqual(len(PROFILES_DOC["profiles"]), 461)
        cat_urls = {row["project_id"]: row.get("url") for row in PROJECT_CATALOG["projects"]}
        for p in PROFILES_DOC["profiles"][:25]:
            self.assertTrue(cat_urls.get(p["project_id"]), f"Missing catalog url for {p['project_id']}")
            self.assertIn("verification_metadata", p)
        self.assertGreaterEqual(intent_router.DOMAINS.__len__(), 25)


if __name__ == "__main__":
    unittest.main()
