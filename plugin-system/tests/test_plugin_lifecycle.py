"""Tests for P02 Plugin Lifecycle Engine (PL-T02..T12, T14..T17, T19, T25, T26, PL-PLAT-PORTABLE)."""

from __future__ import annotations

import importlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _load_plugin_system():
    pkg_dir = ROOT / "plugin-system"
    if "plugin_system" not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            "plugin_system",
            pkg_dir / "__init__.py",
            submodule_search_locations=[str(pkg_dir)],
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["plugin_system"] = mod
        spec.loader.exec_module(mod)
    return importlib.import_module("plugin_system.core.pipeline")


pipeline = _load_plugin_system()
lock_mod = importlib.import_module("plugin_system.core.lock")
models_mod = importlib.import_module("plugin_system.core.models")
validators_mod = importlib.import_module("plugin_system.core.validators")
rollback_mod = importlib.import_module("plugin_system.sync.rollback")
registry_mod = importlib.import_module("plugin_system.core.registry")


def _create_mini_repo(base_dir: Path, *, arabic_folder: bool = False) -> Path:
    """Create a self-contained canonical fixture repository under base_dir."""
    repo = base_dir / ("مجلد GIS عربي" if arabic_folder else "mini-gis-repo")
    repo.mkdir(parents=True, exist_ok=True)

    (repo / "VERSION").write_text("0.3.5\n", encoding="utf-8")
    (repo / "LICENSE").write_text("MIT License\n", encoding="utf-8")
    (repo / "AGENTS.md").write_text("# Start here\n\nPolicy text.\n", encoding="utf-8")
    (repo / "CLAUDE.md").write_text("@AGENTS.md\n", encoding="utf-8")
    (repo / "CHANGELOG.md").write_text("## 0.3.5\n\nBaseline.\n", encoding="utf-8")
    (repo / "PUBLISHING.md").write_text("## Approved GitHub delivery\n\nManual approval required.\n", encoding="utf-8")
    (repo / "README.md").write_text("# Mini Repo\n\nClean README.\n", encoding="utf-8")
    (repo / "README.ar.md").write_text("# مستودع تجريبي\n\nنص عربي سليم.\n", encoding="utf-8")
    (repo / "SECURITY.md").write_text("# Security\n", encoding="utf-8")
    (repo / ".gitignore").write_text("/.plugin-secrets/\n**/owner-config.local.json\n", encoding="utf-8")

    # Docs and templates required by build_skill_bundle.REQUIRED_PATHS
    (repo / "docs").mkdir()
    (repo / "docs" / "HOW_TO_USE.md").write_text("# How to use\n", encoding="utf-8")
    (repo / "docs" / "HOW_TO_USE.ar.md").write_text("# كيفية الاستخدام\n", encoding="utf-8")
    (repo / "templates").mkdir()
    (repo / "templates" / "GIS_ACCEPTANCE_REPORT.md").write_text("# Acceptance\n", encoding="utf-8")

    # Required skills matching bundle_skill_bundle REQUIRED_PATHS
    required_skills = (
        "gis-development",
        "prompt-intent-orchestrator",
        "gis-security-guardian",
        "completion-evidence",
        "agent-development-journal",
    )
    for sk in required_skills:
        sdir = repo / "skills" / sk
        sdir.mkdir(parents=True)
        (sdir / "SKILL.md").write_text(
            f"---\nname: {sk}\ndescription: Test skill {sk} for lifecycle verification.\n---\n\n# {sk}\n\nReady.\n",
            encoding="utf-8",
        )

    # References required by build_skill_bundle and validators
    refs = repo / "references"
    (refs / "security").mkdir(parents=True)
    (refs / "repository-manifest.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "documentation_version": "0.3.5",
                "skill_count": len(required_skills),
                "skill_ids": sorted(required_skills),
                "reference_count": 2,
                "api_count": 0,
                "data_repository_count": 0,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (refs / "project-catalog.json").write_text(
        json.dumps(
            {
                "schema_version": "1.0",
                "projects": [
                    {
                        "name": "VerifiedMITProject",
                        "url": "https://github.com/example-org/verified-mit-project",
                        "category": "geoprocessing",
                        "license": "MIT",
                        "license_verified": True,
                        "license_scope": "Repository LICENSE",
                        "license_checked_on": "2026-11-25",
                        "license_evidence_url": "https://github.com/example-org/verified-mit-project/blob/main/LICENSE",
                        "license_caveat": "None",
                    },
                    {
                        "name": "RestrictedProprietaryRepo",
                        "url": "https://github.com/example-org/restricted-prop-repo",
                        "category": "geoprocessing",
                        "license": "Proprietary",
                        "license_verified": False,
                    },
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (refs / "security" / "security-tools.json").write_text(
        json.dumps(
            {
                "tools": [
                    {
                        "id": "mock-scanner",
                        "url": "https://github.com/example-org/mock-scanner",
                        "automatically_executed": False,
                        "bundled": False,
                    }
                ]
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    (refs / "free-geospatial-apis.json").write_text('{"services": []}\n', encoding="utf-8")
    (refs / "geospatial-data-repositories.json").write_text('{"repositories": []}\n', encoding="utf-8")
    (refs / "project-governance-workflow.md").write_text("## Skill readiness before use\n\nCheck scope.\n", encoding="utf-8")
    (refs / "portable-execution-guidance.md").write_text("## Work within existing ownership\n\nWork cleanly.\n", encoding="utf-8")
    (refs / "repository-wide-skill-orchestration.md").write_text("# Orchestration\n", encoding="utf-8")
    (refs / "ui-engine-architecture-contract.md").write_text("# UI Contract\n", encoding="utf-8")

    # Developer-only files excluded from end-user bundle (PL-T26)
    (repo / "Update-All-Plugins.ps1").write_text("# dev script\n", encoding="utf-8")
    (repo / "Update-My-Platforms.ps1").write_text("# dev owner script\n", encoding="utf-8")
    (repo / "plans" / "active" / "0007_Master-Integration").mkdir(parents=True)
    (repo / "plans" / "active" / "0007_Master-Integration" / "MASTER_AGENT_PROMPT.md").write_text(
        "# Master Agent Prompt\n\nBaseline prompt.\n", encoding="utf-8"
    )

    shutil.copytree(ROOT / "scripts", repo / "scripts", ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    shutil.copytree(
        ROOT / "plugin-system",
        repo / "plugin-system",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "tests"),
    )
    return repo


class PluginLifecycleP02Tests(unittest.TestCase):
    def test_deterministic_zip_repeatability_and_noop_PL_T06_T25_T26_portable(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_mini_repo(Path(tmp), arabic_folder=True)  # Covers PL-T10 Arabic path + spaces!
            res1 = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            self.assertEqual("BUILT", res1["overall_state"])
            zip1 = res1["platforms"]["portable"]["archive_sha256"]
            self.assertTrue(zip1)

            # PL-T06: Immediate check-only & build-only without edits must return UP_TO_DATE
            res_chk = pipeline.run_pipeline(repo, mode="check-only", selected_platforms=["portable"], write_report=False)
            self.assertEqual("UP_TO_DATE", res_chk["overall_state"])
            res_noop = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"], write_report=False)
            self.assertEqual("UP_TO_DATE", res_noop["overall_state"])

            # PL-T25: Forced clean rebuild yields IDENTICAL ZIP bytes & SHA-256
            res2 = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"], force=True)
            zip2 = res2["platforms"]["portable"]["archive_sha256"]
            self.assertEqual(zip1, zip2)

            # PL-PLAT-PORTABLE & PL-T26: Inspect ZIP for plugin.json, UTF-8 Arabic paths, and zero dev-only scripts
            archive_file = repo / res2["platforms"]["portable"]["archive_path"]
            with zipfile.ZipFile(archive_file, "r") as zf:
                names = set(zf.namelist())
                self.assertIn("gis-development-suite/plugin.json", names)
                self.assertIn("gis-development-suite/bundle-manifest.json", names)
                for n in names:
                    self.assertNotIn("Update-All-Plugins", n)
                    self.assertNotIn("Update-My-Platforms", n)
                    self.assertNotIn("plugin-system/", n)
                    self.assertNotIn("MASTER_AGENT_PROMPT.md", n)
                    self.assertNotIn("owner-config", n)

    def test_digest_invalidation_deletion_and_untracked_files_PL_T02_T03_T04_T05(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_mini_repo(Path(tmp))
            res1 = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            digest1 = res1["source_digest"]

            # PL-T02 + PL-T05: New untracked allowed file triggers digest change and enters bundle
            (repo / "docs" / "NEW_GUIDE.md").write_text("# New Guide\n", encoding="utf-8")
            chk1 = pipeline.run_pipeline(repo, mode="check-only", selected_platforms=["portable"], write_report=False)
            self.assertEqual("OUTDATED", chk1["platforms"]["portable"]["state"])
            self.assertNotEqual(digest1, chk1["source_digest"])
            res2 = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            self.assertTrue((repo / "GIS-Development-Skills-Plugins/portable-agent-plugin/plugin/docs/NEW_GUIDE.md").is_file())

            # PL-T04: Deleting file removes stale output via atomic clean swap
            (repo / "docs" / "NEW_GUIDE.md").unlink()
            res3 = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            self.assertEqual("BUILT", res3["overall_state"])
            self.assertFalse((repo / "GIS-Development-Skills-Plugins/portable-agent-plugin/plugin/docs/NEW_GUIDE.md").exists())

            # PL-T03: Editing MASTER_AGENT_PROMPT.md invalidates source digest without bundling it
            prompt_file = repo / "plans/active/0007_Master-Integration/MASTER_AGENT_PROMPT.md"
            prompt_file.write_text(prompt_file.read_text(encoding="utf-8") + "\nUpdated rule.\n", encoding="utf-8")
            chk2 = pipeline.run_pipeline(repo, mode="check-only", selected_platforms=["portable"], write_report=False)
            self.assertNotEqual(res3["source_digest"], chk2["source_digest"])
            self.assertEqual("OUTDATED", chk2["platforms"]["portable"]["state"])

    def test_corrupt_output_detection_and_rebuild_PL_T07(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_mini_repo(Path(tmp))
            res1 = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            self.assertEqual("BUILT", res1["overall_state"])

            # Corrupt output file without touching canonical repo source
            target_file = repo / "GIS-Development-Skills-Plugins/portable-agent-plugin/plugin/AGENTS.md"
            target_file.write_text("# CORRUPTED TAMPERING\n", encoding="utf-8")

            chk = pipeline.run_pipeline(repo, mode="check-only", selected_platforms=["portable"], write_report=False)
            self.assertEqual("VALIDATION_FAILED", chk["platforms"]["portable"]["state"])

            rebuilt = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            self.assertEqual("BUILT", rebuilt["overall_state"])
            self.assertIn("Policy text.", target_file.read_text(encoding="utf-8"))

    def test_invalid_yaml_or_broken_link_preserves_last_good_PL_T08(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_mini_repo(Path(tmp))
            pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            good_manifest = (repo / "GIS-Development-Skills-Plugins/portable-agent-plugin/plugin/plugin.json").read_text(encoding="utf-8")

            # Inject broken link into a canonical skill
            bad_skill = repo / "skills/gis-development/SKILL.md"
            bad_skill.write_text(bad_skill.read_text(encoding="utf-8") + "\n[Dead](../../references/nonexistent.md)\n", encoding="utf-8")

            with self.assertRaises(models_mod.ValidationFailedError) as ctx:
                pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"], write_report=False)
            self.assertEqual(models_mod.EXIT_BUILD_OR_VALIDATION_FAILED, ctx.exception.exit_code)
            # Last known-good output untouched!
            self.assertEqual(
                good_manifest,
                (repo / "GIS-Development-Skills-Plugins/portable-agent-plugin/plugin/plugin.json").read_text(encoding="utf-8"),
            )

    def test_license_redistribution_gate_PL_T09(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_mini_repo(Path(tmp))
            ok = validators_mod.validate_license_redistribution(
                repo, {"https://github.com/example-org/verified-mit-project"}
            )
            self.assertEqual(1, ok["verified_source_licenses"])

            with self.assertRaises(models_mod.ValidationFailedError):
                validators_mod.validate_license_redistribution(
                    repo, {"https://github.com/example-org/restricted-prop-repo"}
                )

    def test_path_traversal_and_secret_redaction_PL_T05_T11_T12(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo = _create_mini_repo(Path(tmp))

            # PL-T12: Dummy secret in ignored private dir must stay excluded from build & logs
            secret_token = "ghp_" + "Z9X8C7V6B5N4M3L2K1J0"
            (repo / ".plugin-secrets").mkdir()
            (repo / ".plugin-secrets" / "owner-config.local.json").write_text(
                json.dumps({"dummy": secret_token}), encoding="utf-8"
            )
            res = pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            self.assertEqual("BUILT", res["overall_state"])
            rep_text = (repo / res["report_json"]).read_text(encoding="utf-8")
            self.assertNotIn(secret_token, rep_text)

            # PL-T05 + T12: Sensitive file inside canonical skills dir fails immediately without printing token
            (repo / "skills/gis-development/.env").write_text(f"TOKEN={secret_token}\n", encoding="utf-8")
            with self.assertRaises(models_mod.SecretLeakError) as sec_ctx:
                pipeline.run_pipeline(repo, mode="check-only", selected_platforms=["portable"], write_report=False)
            self.assertNotIn(secret_token, str(sec_ctx.exception))
            (repo / "skills/gis-development/.env").unlink()

            # Secret token accidentally typed into a tracked markdown file fails with value redacted
            (repo / "docs/LEAK.md").write_text(f"Accidentally pasted {secret_token}\n", encoding="utf-8")
            with self.assertRaises(models_mod.SecretLeakError) as leak_ctx:
                pipeline.run_pipeline(repo, mode="check-only", selected_platforms=["portable"], write_report=False)
            self.assertIn("redacted", str(leak_ctx.exception))
            self.assertNotIn(secret_token, str(leak_ctx.exception))
            (repo / "docs/LEAK.md").unlink()

            # PL-T11: Explicit traversal guard in inventory helper
            inv_mod = importlib.import_module("plugin_system.core.inventory")
            with self.assertRaises(models_mod.ValidationFailedError):
                inv_mod._assert_safe_relative(Path(tmp), repo)

    def test_lock_contention_and_stale_recovery_PL_T15(self):
        with tempfile.TemporaryDirectory() as tmp:
            lock_file = Path(tmp) / ".plugin-lock" / "update.lock.json"
            with lock_mod.ProjectLock(lock_file, timeout_seconds=0.3, stale_seconds=60):
                with self.assertRaises(models_mod.LockTimeoutError) as ctx:
                    with lock_mod.ProjectLock(lock_file, timeout_seconds=0.25, stale_seconds=60):
                        pass
                self.assertEqual(models_mod.EXIT_LOCK_OR_CONFIG_ERROR, ctx.exception.exit_code)

            # Simulate stale lock written 10 minutes ago
            lock_file.parent.mkdir(parents=True, exist_ok=True)
            lock_file.write_text(json.dumps({"pid": 999999, "acquired_at_epoch": time.time() - 900}), encoding="utf-8")
            with lock_mod.ProjectLock(lock_file, timeout_seconds=0.5, stale_seconds=60):
                self.assertTrue(lock_file.is_file())
            self.assertFalse(lock_file.exists())

    def test_pluggable_mock_adapter_and_rollback_and_publish_gate_PL_T14_T17_T19(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = _create_mini_repo(base)

            # Snapshot & rollback test
            pipeline.run_pipeline(repo, mode="build-only", selected_platforms=["portable"])
            bundle_dir = repo / "GIS-Development-Skills-Plugins/portable-agent-plugin/plugin"
            snap_dir = rollback_mod.snapshot_known_good(repo, "portable", "0.3.4", bundle_dir)
            self.assertIsNotNone(snap_dir)
            marker = bundle_dir / "SKILL.md"
            marker.write_text("MUTATED_VER_035", encoding="utf-8")
            rb = pipeline.run_pipeline(repo, mode="rollback", selected_platforms=["portable"], rollback_version="0.3.4", write_report=False)
            self.assertEqual("ROLLED_BACK", rb["overall_state"])
            self.assertNotIn("MUTATED_VER_035", marker.read_text(encoding="utf-8"))

            # PL-T19: Publish blocked without approval -> EXIT 4
            with self.assertRaises(models_mod.ApprovalRequiredError) as pub_ctx:
                pipeline.run_pipeline(repo, mode="publish", selected_platforms=["portable"], write_report=False)
            self.assertEqual(models_mod.EXIT_APPROVAL_OR_MANUAL_REQUIRED, pub_ctx.exception.exit_code)

            # PL-T17: Register a custom mock adapter strictly in platforms.json without touching engine core!
            mock_mod = repo / "custom_mock_adapter.py"
            mock_mod.write_text(
                """from pathlib import Path
class ExperimentalMockAdapter:
    def __init__(self, config): self.config = config
    def detect(self, context): return {"platform": self.config.id, "installed": True, "state": "BUILT"}
    def capabilities(self): return {"unpacked": True, "zip": False}
    def build(self, context, staging_dir):
        d = Path(staging_dir) / "mock-plugin"
        d.mkdir(parents=True, exist_ok=True)
        (d / "mock.manifest.json").write_text('{"source_digest":"' + context.source_digest + '","ok":true}', encoding="utf-8")
        return {"staged_bundle_dir": str(d)}
    def validate(self, context, staged_dir): return {"status": "PASS", "content_sha256": "m"*64, "file_count": 1}
    def package(self, context, built_dir, artifacts_dir): return {"archive_name": None, "archive_sha256": None}
    def status(self, context): return {"platform": self.config.id, "state": "OUTDATED", "phase_status": "ACTIVE_P02"}
    def sync_local(self, context): return {"platform": self.config.id, "state": "NOT_INSTALLED"}
    def prepare_release(self, context): return {"platform": self.config.id, "state": "NOT_RUN"}
    def update_owner_remote(self, context): return {"platform": self.config.id, "state": "NOT_RUN"}
    def verify(self, context): return {"platform": self.config.id, "state": "NOT_INSTALLED"}
    def rollback(self, context, version): return {"platform": self.config.id, "state": "NOT_RUN"}
""",
                encoding="utf-8",
            )
            custom_platforms = repo / "custom-platforms.json"
            custom_platforms.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "plugin_id": "test.extensible",
                        "platforms": [
                            {
                                "id": "mock-ide",
                                "display_name": "Experimental Mock IDE",
                                "enabled": True,
                                "phase_target": "P02",
                                "phase_status": "ACTIVE_P02",
                                "adapter": "custom_mock_adapter.py:ExperimentalMockAdapter",
                                "output_dir": "GIS-Development-Skills-Plugins/mock-ide",
                                "bundle_dir": "GIS-Development-Skills-Plugins/mock-ide/plugin",
                                "manifest_path": "GIS-Development-Skills-Plugins/mock-ide/plugin/mock.manifest.json",
                                "artifacts_dir": "GIS-Development-Skills-Plugins/mock-ide/artifacts",
                                "build_in_p02": True,
                            }
                        ],
                    },
                    indent=2,
                ),
                encoding="utf-8",
            )
            ext_res = pipeline.run_pipeline(
                repo,
                mode="build-only",
                platforms_config_path=custom_platforms,
                write_report=False,
            )
            self.assertEqual("BUILT", ext_res["platforms"]["mock-ide"]["state"])
            self.assertTrue((repo / "GIS-Development-Skills-Plugins/mock-ide/plugin/mock.manifest.json").is_file())

    def test_local_sync_verify_and_isolated_partial_rollback_PL_T14_T29(self):
        with tempfile.TemporaryDirectory() as tmp:
            base = Path(tmp)
            repo = _create_mini_repo(base)
            sync_dest = base / "local-portable-client"
            owner_cfg = base / "outside-git-owner-config.json"
            owner_cfg.write_text(
                json.dumps(
                    {
                        "allowLocalSync": True,
                        "allowRemoteUpdate": False,
                        "allowPublicPublish": False,
                        "targets": {"portable": {"enabled": True, "localSyncDir": str(sync_dest)}},
                    }
                ),
                encoding="utf-8",
            )

            full_res = pipeline.run_pipeline(
                repo,
                mode="full",
                selected_platforms=["portable"],
                owner_config_path=owner_cfg,
                write_report=False,
            )
            self.assertEqual("SYNCED_VERIFIED", full_res["platforms"]["portable"]["sync"]["state"])

            # Verify live hash match -> tamper installed copy -> OUTDATED (PL-T29)
            cfg = [c for c in registry_mod.list_platform_configs(repo, registry_mod.load_platforms_registry(repo)) if c.id == "portable"][0]
            adapter = registry_mod.load_adapter(repo, cfg)
            ctx_res = pipeline.run_pipeline(repo, mode="status", selected_platforms=["portable"], owner_config_path=owner_cfg, write_report=False)
            self.assertEqual("UP_TO_DATE", ctx_res["platforms"]["portable"]["state"])

            inst_manifest = sync_dest / "bundle-manifest.json"
            bm = json.loads(inst_manifest.read_text(encoding="utf-8"))
            bm["content_sha256"] = "0" * 64
            inst_manifest.write_text(json.dumps(bm), encoding="utf-8")

            # Use adapter.verify via CLI sync_manager partial rollback barrier (PL-T14)
            sync_mgr = importlib.import_module("plugin_system.sync.sync_manager")
            ad_ctx = models_mod.AdapterContext(
                repo_root=repo,
                version="0.3.5",
                source_commit="abc1234",
                source_digest="a" * 64,
                bundle_digest="b" * 64,
                plugin_id="p",
                suite_name="s",
                source_map={},
                sync_config={},
                owner_config=json.loads(owner_cfg.read_text(encoding="utf-8")),
            )
            self.assertEqual("OUTDATED", adapter.verify(ad_ctx)["state"])

            class FailingAdapter:
                config = type("Cfg", (), {"id": "broken-client"})()
                def sync_local(self, context): raise RuntimeError("simulated client write error")

            partial = sync_mgr.sync_platforms_transactionally([adapter, FailingAdapter()], ad_ctx)
            self.assertTrue(partial["partial_failure"])
            self.assertEqual("SYNCED_VERIFIED", partial["platforms"]["portable"]["state"])
            self.assertEqual("SYNC_FAILED_ROLLED_BACK", partial["platforms"]["broken-client"]["state"])

    def test_cli_subprocess_exit_codes_and_negative_controls(self):
        # Unknown platform triggers EXIT 5; unapproved --publish triggers EXIT 4
        proc_bad_plat = subprocess.run(
            [sys.executable, "-B", str(ROOT / "plugin-system" / "core" / "pipeline.py"), "--status", "--platform", "nonexistent-plat", "--no-report"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(5, proc_bad_plat.returncode)

        proc_pub = subprocess.run(
            [sys.executable, "-B", str(ROOT / "plugin-system" / "core" / "pipeline.py"), "--publish", "--platform", "portable", "--no-report"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            timeout=20,
        )
        self.assertEqual(4, proc_pub.returncode)


if __name__ == "__main__":
    unittest.main()
