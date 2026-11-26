"""Comprehensive Phase P09 verification suite for all 6 client adapters, marketplaces, hooks, and CI workflows."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest import mock

REPO_ROOT = Path(__file__).resolve().parents[2]
PLUGIN_SYS = REPO_ROOT / "plugin-system"
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


def _load_pipeline():
    import importlib

    return importlib.import_module("plugin_system.core.pipeline")


def _load_test_helper_modules():
    import importlib.util

    pkg_dir = PLUGIN_SYS
    if "plugin_system" not in sys.modules:
        spec = importlib.util.spec_from_file_location(
            "plugin_system",
            pkg_dir / "__init__.py",
            submodule_search_locations=[str(pkg_dir)],
        )
        mod = importlib.util.module_from_spec(spec)
        sys.modules["plugin_system"] = mod
        spec.loader.exec_module(mod)


_load_test_helper_modules()
pipeline_mod = _load_pipeline()
registry_mod = sys.modules["plugin_system.core.registry"]
models_mod = sys.modules["plugin_system.core.models"]


def _create_temp_canonical_workspace(dest: Path) -> Path:
    """Create an isolated canonical repo copy fast enough for deterministic P09 tests."""
    source_map = json.loads((PLUGIN_SYS / "config" / "source-map.json").read_text(encoding="utf-8"))
    for d in source_map["canonical_bundle_directories"]:
        src_d = REPO_ROOT / d
        if src_d.is_dir():
            shutil.copytree(
                src_d,
                dest / d,
                ignore=shutil.ignore_patterns("__pycache__", "*.pyc", "*.tmp", "node_modules"),
            )
    for f in source_map["canonical_bundle_files"]:
        src_f = REPO_ROOT / f
        if src_f.is_file():
            shutil.copy2(src_f, dest / f)
    (dest / "VERSION").write_text((REPO_ROOT / "VERSION").read_text(encoding="utf-8"), encoding="utf-8")
    shutil.copytree(
        PLUGIN_SYS,
        dest / "plugin-system",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    master_prompt_rel = Path("plans/active/0007_Master-Integration/MASTER_AGENT_PROMPT.md")
    if (REPO_ROOT / master_prompt_rel).is_file():
        (dest / master_prompt_rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO_ROOT / master_prompt_rel, dest / master_prompt_rel)
    return dest


class P09PlatformAdapterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls._tmp_holder = tempfile.TemporaryDirectory()
        cls.fixture_root = _create_temp_canonical_workspace(Path(cls._tmp_holder.name) / "repo")
        cls.build_result = pipeline_mod.run_pipeline(
            cls.fixture_root,
            mode="build-only",
            write_report=False,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        cls._tmp_holder.cleanup()

    def test_all_seven_platforms_built_and_e39_skill_parity(self):
        self.assertEqual(0, self.build_result["exit_code"])
        expected_ids = {"portable", "codex", "chatgpt", "claude-code", "claude-ai", "antigravity", "cursor"}
        self.assertEqual(expected_ids, set(self.build_result["platforms"].keys()))
        for pid in expected_ids:
            pinfo = self.build_result["platforms"][pid]
            self.assertEqual("BUILT", pinfo["state"], f"{pid} unexpected state: {pinfo}")
            bundle_dir = self.fixture_root / self._cfg(pid).bundle_dir
            self.assertTrue(
                (bundle_dir / "skills" / "geospatial-engine-selection" / "SKILL.md").is_file(),
                f"E39: geospatial-engine-selection missing in {pid}",
            )
            parity_file = self.fixture_root / self._cfg(pid).parity_report_path
            self.assertTrue(parity_file.is_file(), f"Missing parity report for {pid}")
            parity = json.loads(parity_file.read_text(encoding="utf-8"))
            self.assertTrue(parity["carried_components"])
            self.assertTrue(parity["adapted_components"])
            self.assertTrue(parity["excluded_components"])
            readme = self.fixture_root / self._cfg(pid).output_dir / "README.md"
            self.assertTrue(readme.is_file(), f"Missing bilingual README for {pid}")
            rtext = readme.read_text(encoding="utf-8")
            self.assertIn("## English", rtext)
            self.assertIn("العربية", rtext)

    @classmethod
    def _cfg(cls, pid: str):
        reg = registry_mod.load_platforms_registry(cls.fixture_root)
        return next(c for c in registry_mod.list_platform_configs(cls.fixture_root, reg) if c.id == pid)

    def test_pl_plat_codex_manifest_and_marketplace(self):
        cfg = self._cfg("codex")
        manifest = json.loads((self.fixture_root / cfg.manifest_path).read_text(encoding="utf-8"))
        self.assertEqual("codex", manifest["platform"])
        self.assertEqual("./skills", manifest["skills"])
        self.assertEqual("AGENTS.md", manifest["instructions"])
        mkt = self.fixture_root / ".agents" / "plugins" / "marketplace.json"
        self.assertTrue(mkt.is_file())
        mkt_data = json.loads(mkt.read_text(encoding="utf-8"))
        self.assertEqual(manifest["source_digest"], mkt_data["source_digest"])

    def test_pl_plat_chatgpt_strips_hooks_and_shares_openai_listing(self):
        cfg = self._cfg("chatgpt")
        manifest = json.loads((self.fixture_root / cfg.manifest_path).read_text(encoding="utf-8"))
        self.assertFalse(manifest["supports_hooks"])
        self.assertEqual([], manifest["lifecycle_hooks"])
        self.assertEqual("openai-directory", manifest["shared_listing_group"])
        self.assertTrue(manifest["duplicate_public_listing_blocked"])
        bundle_dir = self.fixture_root / cfg.bundle_dir
        self.assertFalse((bundle_dir / ".claude-plugin" / "hooks.json").exists())
        self.assertFalse((bundle_dir / "hooks.json").exists())

    def test_pl_plat_claude_code_manifest_marketplace_and_hooks(self):
        cfg = self._cfg("claude-code")
        bundle_dir = self.fixture_root / cfg.bundle_dir
        manifest = json.loads((self.fixture_root / cfg.manifest_path).read_text(encoding="utf-8"))
        self.assertEqual("claude-code", manifest["platform"])
        self.assertEqual(["user", "project", "local"], manifest["scopes"])
        self.assertTrue(manifest["supports_hooks"])
        self.assertTrue((bundle_dir / ".claude-plugin" / "hooks.json").is_file())
        hooks = json.loads((bundle_dir / ".claude-plugin" / "hooks.json").read_text(encoding="utf-8"))
        self.assertTrue(hooks["loop_safe"])
        mkt = self.fixture_root / ".claude-plugin" / "marketplace.json"
        self.assertTrue(mkt.is_file())
        mkt_data = json.loads(mkt.read_text(encoding="utf-8"))
        self.assertEqual(manifest["source_digest"], mkt_data["metadata"]["source_digest"])

    def test_pl_plat_claude_ai_shared_payload_and_portal_limits(self):
        cfg = self._cfg("claude-ai")
        manifest = json.loads((self.fixture_root / cfg.manifest_path).read_text(encoding="utf-8"))
        self.assertEqual("claude-code", manifest["shared_payload_with"])
        self.assertEqual("manual-org-portal", manifest["portal_refresh_mode"])
        bundle_dir = self.fixture_root / cfg.bundle_dir
        self.assertTrue((bundle_dir / ".claude-plugin" / "plugin.json").is_file())

    def test_pl_plat_antigravity_manifest_and_honest_absent_cli(self):
        cfg = self._cfg("antigravity")
        bundle_dir = self.fixture_root / cfg.bundle_dir
        manifest = json.loads((self.fixture_root / cfg.manifest_path).read_text(encoding="utf-8"))
        self.assertEqual("agy", manifest["cli_command"])
        self.assertTrue((bundle_dir / ".antigravity" / "plugin.json").is_file())
        ad = registry_mod.load_adapter(self.fixture_root, cfg)
        ctx = models_mod.AdapterContext(
            repo_root=self.fixture_root,
            version="0.3.5",
            source_commit="deadbeef",
            source_digest="0" * 64,
            bundle_digest="1" * 64,
            plugin_id="ahmadibrahim4geo.gis-development-skills",
            suite_name="GIS Development Skills",
            source_map={},
            sync_config={},
            owner_config={},
        )
        with mock.patch("shutil.which", return_value=None):
            det = ad.detect(ctx)
            self.assertFalse(det["installed"])
            self.assertEqual("NOT_INSTALLED", det["state"])
            val = ad.validate_platform_extras(ctx, bundle_dir, manifest)
            self.assertEqual("NOT_RUN", val["cli_validation"])

    def test_pl_plat_cursor_manifest_and_rules_mdc(self):
        cfg = self._cfg("cursor")
        bundle_dir = self.fixture_root / cfg.bundle_dir
        manifest = json.loads((self.fixture_root / cfg.manifest_path).read_text(encoding="utf-8"))
        self.assertEqual(".cursor/rules/gis-development-skills.mdc", manifest["rules"])
        mdc = bundle_dir / ".cursor" / "rules" / "gis-development-skills.mdc"
        self.assertTrue(mdc.is_file())
        self.assertIn("alwaysApply: true", mdc.read_text(encoding="utf-8"))
        self.assertTrue((self.fixture_root / ".cursor" / "rules" / "gis-development-skills.mdc").is_file())

    def test_pl_t16_hook_loop_prevention_idempotency(self):
        check = pipeline_mod.run_pipeline(self.fixture_root, mode="check-only", write_report=False)
        self.assertEqual(0, check["exit_code"])
        self.assertEqual("UP_TO_DATE", check["overall_state"])
        self.assertEqual(self.build_result["source_digest"], check["source_digest"])

    def test_pl_t18_ci_stale_package_and_marketplace_gate(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp) / "repo"
            shutil.copytree(self.fixture_root, copy_root, ignore=shutil.ignore_patterns("*.zip", "*.zip.sha256", ".plugin-*"))
            mkt = copy_root / ".agents" / "plugins" / "marketplace.json"
            data = json.loads(mkt.read_text(encoding="utf-8"))
            data["source_digest"] = "0" * 64
            mkt.write_text(json.dumps(data, indent=2), encoding="utf-8")
            with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
                check = pipeline_mod.run_pipeline(
                    copy_root,
                    mode="check-only",
                    selected_platforms=["codex"],
                    write_report=False,
                )
            self.assertEqual(2, check["exit_code"])
            self.assertEqual("OUTDATED", check["overall_state"])

    def test_pl_t13_t20_t21_t28_t29_sync_verify_and_release_guards(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp) / "repo"
            shutil.copytree(self.fixture_root, copy_root, ignore=shutil.ignore_patterns(".plugin-*"))
            owner_path = Path(tmp) / "owner-config.json"
            codex_sync_dir = Path(tmp) / "codex-installed"
            owner_path.write_text(
                json.dumps(
                    {
                        "allowLocalSync": True,
                        "allowRemoteUpdate": True,
                        "allowPublicPublish": False,
                        "targets": {
                            "codex": {"enabled": True, "localSyncDir": str(codex_sync_dir)},
                            "cursor": {"enabled": True, "authState": "AUTH_REQUIRED"},
                        },
                    }
                ),
                encoding="utf-8",
            )
            with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": ""}), mock.patch(
                "shutil.which", side_effect=lambda cmd: "/usr/bin/cursor" if cmd == "cursor" else None
            ):
                res = pipeline_mod.run_pipeline(
                    copy_root,
                    mode="full",
                    selected_platforms=["codex", "cursor", "chatgpt"],
                    owner_config_path=owner_path,
                    write_report=False,
                )
            self.assertEqual("SYNCED_VERIFIED", res["platforms"]["codex"]["sync"]["state"])
            self.assertEqual("AUTH_REQUIRED", res["platforms"]["cursor"]["sync"]["state"])
            self.assertEqual("MANUAL_ACTION_REQUIRED", res["platforms"]["chatgpt"]["sync"]["state"])

            # PL-T29: tampering installed manifest must flip verify to OUTDATED
            (codex_sync_dir / "bundle-manifest.json").write_text('{"content_sha256": "stale"}', encoding="utf-8")
            cfg = self._cfg("codex")
            ad = registry_mod.load_adapter(copy_root, cfg)
            ctx = models_mod.AdapterContext(
                repo_root=copy_root,
                version=res["version"],
                source_commit=res["source_commit"],
                source_digest=res["source_digest"],
                bundle_digest=res["bundle_digest"],
                plugin_id="ahmadibrahim4geo.gis-development-skills",
                suite_name="GIS Development Skills",
                source_map={},
                sync_config={},
                owner_config=json.loads(owner_path.read_text(encoding="utf-8")),
            )
            self.assertEqual("OUTDATED", ad.verify(ctx)["state"])

            # PL-T20 & PL-T28: bounded retry + listingAlias scoping
            attempts = []

            def flaky_dispatcher(pid, alias, attempt):
                attempts.append((pid, alias, attempt))
                if attempt < 2:
                    raise TimeoutError("transient timeout")
                return {"state": "PENDING_REVIEW", "notes": "Submitted under review"}

            ctx_remote = models_mod.AdapterContext(
                repo_root=copy_root,
                version=res["version"],
                source_commit=res["source_commit"],
                source_digest=res["source_digest"],
                bundle_digest=res["bundle_digest"],
                plugin_id="ahmadibrahim4geo.gis-development-skills",
                suite_name="GIS Development Skills",
                source_map={},
                sync_config={},
                owner_config={
                    "allowRemoteUpdate": True,
                    "targets": {
                        "codex": {
                            "listingAlias": "my-gis-alias",
                            "cliCommand": "codex",
                            "_test_remote_dispatcher": flaky_dispatcher,
                        }
                    },
                },
                publish_approved=True,
            )
            with mock.patch("shutil.which", return_value="/usr/bin/codex"):
                remote_out = ad.update_owner_remote(ctx_remote)
            self.assertEqual("PENDING_REVIEW", remote_out["state"])
            self.assertEqual("my-gis-alias", remote_out["listing_alias"])
            self.assertEqual(2, remote_out["attempts"])

            # PL-T21: prepare-release returns PREPARED_FOR_SUBMISSION cleanly
            prep = pipeline_mod.run_pipeline(copy_root, mode="prepare-release", write_report=False)
            self.assertEqual("PREPARED_FOR_SUBMISSION", prep["overall_state"])
            for pid in ("codex", "chatgpt", "claude-code", "claude-ai", "antigravity", "cursor"):
                self.assertEqual("PREPARED_FOR_SUBMISSION", prep["platforms"][pid]["release"]["state"])

    def test_pl_t22_and_t27_ci_boundary_and_dirty_tree_safety(self):
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp) / "repo"
            shutil.copytree(self.fixture_root, copy_root, ignore=shutil.ignore_patterns(".plugin-*"))
            dirty_note = copy_root / "uncommitted_owner_note.txt"
            dirty_note.write_text("keep-me", encoding="utf-8")
            with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true"}):
                ci_res = pipeline_mod.run_pipeline(
                    copy_root,
                    mode="full",
                    selected_platforms=["codex", "portable"],
                    write_report=False,
                )
            self.assertEqual(0, ci_res["exit_code"])
            self.assertEqual("NOT_APPLICABLE", ci_res["platforms"]["codex"]["sync"]["state"])
            self.assertEqual("keep-me", dirty_note.read_text(encoding="utf-8"))

    def test_ci_workflows_sha_pinned_and_safe_permissions(self):
        sha_uses = re.compile(r"uses:\s*[^@\s]+@([0-9a-f]{40})\b")
        for wf_name in ("plugin-validate.yml", "plugin-build.yml", "plugin-release.yml"):
            wf_path = REPO_ROOT / ".github" / "workflows" / wf_name
            self.assertTrue(wf_path.is_file(), f"Missing workflow: {wf_name}")
            text = wf_path.read_text(encoding="utf-8")
            self.assertNotIn("pull_request_target", text)
            self.assertIn("concurrency:", text)
            self.assertIn("contents: read", text)
            uses_lines = [line.strip() for line in text.splitlines() if line.strip().startswith(("uses:", "- uses:"))]
            self.assertTrue(uses_lines, f"No uses directives in {wf_name}")
            for uline in uses_lines:
                self.assertRegex(uline, sha_uses, f"Unpinned action in {wf_name}: {uline}")

    def test_req_pl_026_update_my_platforms_outside_git_powershell(self):
        # Verify external owner-config loading & CLI integration outside Git without mutating workspace.
        sync_mod = sys.modules["plugin_system.sync.sync_manager"]
        with tempfile.TemporaryDirectory() as tmp:
            ext_cfg = Path(tmp) / "outside-owner-config.json"
            ext_cfg.write_text(
                (PLUGIN_SYS / "config" / "owner-config.example.json").read_text(encoding="utf-8"),
                encoding="utf-8",
            )
            self.assertFalse(ext_cfg.is_relative_to(REPO_ROOT))
            loaded, source_label = sync_mod.load_owner_config({}, override_path=ext_cfg)
            self.assertFalse(loaded["allowRemoteUpdate"])
            self.assertEqual(f"external-file:{ext_cfg.name}", source_label)

            # Verify CLI honors external --owner-config strictly outside Git without leaking secrets.
            proc = subprocess.run(
                [
                    sys.executable,
                    "-B",
                    str(PLUGIN_SYS / "core" / "pipeline.py"),
                    "--repo-root",
                    str(self.fixture_root),
                    "--owner-config",
                    str(ext_cfg),
                    "--platform",
                    "portable",
                    "--status",
                    "--json",
                ],
                capture_output=True,
                text=True,
                timeout=30,
                check=False,
            )
            self.assertEqual(0, proc.returncode, proc.stderr)
            out_data = json.loads(proc.stdout)
            self.assertEqual(f"external-file:{ext_cfg.name}", out_data["owner_config_source"])

        ps1_text = (REPO_ROOT / "Update-My-Platforms.ps1").read_text(encoding="utf-8")
        bat_text = (REPO_ROOT / "Update-My-Platforms.bat").read_text(encoding="utf-8")
        self.assertIn("owner-config.json", ps1_text)
        self.assertIn("-NoProfile -File", bat_text)
        self.assertNotIn("ExecutionPolicy Bypass", ps1_text + bat_text)

        ps_bin = shutil.which("powershell")
        if ps_bin:
            parse_cmd = (
                "$err=$null; "
                f"[void][System.Management.Automation.Language.Parser]::ParseFile('{(REPO_ROOT / 'Update-My-Platforms.ps1')}',[ref]$null,[ref]$err); "
                "if($err -and $err.Count -gt 0){ exit 2 }; exit 0"
            )
            pcheck = subprocess.run([ps_bin, "-NoProfile", "-Command", parse_cmd], capture_output=True, text=True, timeout=20, check=False)
            self.assertEqual(0, pcheck.returncode, pcheck.stderr)


if __name__ == "__main__":
    unittest.main()
