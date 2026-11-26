"""Portable Agent Plugin adapter wrapping scripts/build_skill_bundle.py cleanly."""

from __future__ import annotations

import importlib.util
import json
import shutil
from pathlib import Path
from typing import Any

from ..base import PluginAdapter
from ...core.builder import inspect_built_output
from ...core.hashing import sha256_file
from ...core.models import AdapterContext, ApprovalRequiredError, ValidationFailedError
from ...core.parity import build_parity_report
from ...sync.rollback import restore_snapshot, snapshot_known_good


def _load_bundle_module(repo_root: Path):
    script = Path(repo_root) / "scripts" / "build_skill_bundle.py"
    spec = importlib.util.spec_from_file_location("repo_build_skill_bundle", script)
    if spec is None or spec.loader is None:
        raise ValidationFailedError(f"Cannot load scripts/build_skill_bundle.py at {script}")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class PortableAdapter(PluginAdapter):
    """Production P02 adapter generating self-contained portable-agent-plugin payloads."""

    def detect(self, context: AdapterContext) -> dict[str, Any]:
        script = context.repo_root / "scripts" / "build_skill_bundle.py"
        return {
            "platform": self.config.id,
            "installed": script.is_file(),
            "state": "BUILT" if script.is_file() else "BUILD_FAILED",
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "unpacked": True,
            "zip": True,
            "hooks": False,
            "local_sync": True,
            "verify": True,
            "rollback": True,
            "phase_status": self.config.phase_status,
        }

    def build(self, context: AdapterContext, staging_dir: Path) -> dict[str, Any]:
        bundle_mod = _load_bundle_module(context.repo_root)
        base_out = staging_dir / "base-bundle"
        try:
            res = bundle_mod.build(base_out, root=context.repo_root)
        except bundle_mod.BundleError as exc:
            raise ValidationFailedError(f"Bundle build failed: {exc}") from exc

        staged_bundle = Path(res["bundle_directory"])
        base_manifest = json.loads((staged_bundle / "bundle-manifest.json").read_text(encoding="utf-8"))
        inv = base_manifest["inventory"]

        plugin_manifest = {
            "schema_version": "1.0",
            "plugin_id": context.plugin_id,
            "platform": self.config.id,
            "name": context.suite_name,
            "version": context.version,
            "source_commit": context.source_commit,
            "source_digest": context.source_digest,
            "bundle_digest": context.bundle_digest,
            "skill_count": inv["skill_count"],
            "license": "MIT",
            "repository": "https://github.com/ahmadibrahim4geo/GIS-Development-Skills",
            "author": {"name": "Ahmad Ibrahim", "url": "https://ahmadibrahim4geo.github.io/MIRSAD/"},
            "entrypoint": "SKILL.md",
            "content_sha256": context.bundle_digest,
        }
        (staged_bundle / "plugin.json").write_text(
            json.dumps(plugin_manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        # Re-index bundle-manifest.json once so plugin.json is checksummed cleanly without circular self-hash.
        final_manifest = bundle_mod.write_manifest(staged_bundle, context.source_commit)

        parity = build_parity_report(
            self.config.id,
            self.config.display_name,
            phase_status=self.config.phase_status,
            version=context.version,
            source_commit=context.source_commit,
            source_digest=context.source_digest,
            carried=[
                f"skills ({inv['skill_count']})",
                "references",
                "schemas",
                "scripts",
                "templates",
                "examples",
                "fixtures",
                "native_tests",
                "docs",
                "assets",
                "AGENTS.md",
                "LICENSE",
            ],
            adapted=[
                {
                    "component": "SKILL.md + plugin.json",
                    "action": "Generated suite entrypoint and portable plugin manifest wrapping build_skill_bundle.",
                }
            ],
            excluded=[
                {
                    "item": "plugin-system/, Update-All-Plugins.*, Update-My-Platforms.*, reports/, plans/, .agent-development-log/",
                    "reason": "Developer-only lifecycle infrastructure & secrets excluded from end-user payload (REQ-PL-026 / PL-T26).",
                    "alternative": "Source repository governance files",
                }
            ],
            notes=f"Deterministic portable bundle built cleanly ({final_manifest['file_count']} files).",
        )
        return {
            "staged_bundle_dir": str(staged_bundle),
            "parity_report": parity,
        }

    def validate(self, context: AdapterContext, staged_dir: Path) -> dict[str, Any]:
        bundle_mod = _load_bundle_module(context.repo_root)
        staged = Path(staged_dir)
        plugin_file = staged / "plugin.json"
        if not plugin_file.is_file():
            raise ValidationFailedError("Portable bundle missing plugin.json")
        p_data = json.loads(plugin_file.read_text(encoding="utf-8"))
        for field in ("schema_version", "plugin_id", "platform", "name", "version", "source_commit", "source_digest", "skill_count"):
            if field not in p_data:
                raise ValidationFailedError(f"Portable plugin.json missing required field: {field}")

        # Verify developer-only & secret files are strictly absent (PL-T26 / PL-T12).
        forbidden_roots = ("plugin-system", "reports", "plans", ".agent-development-log", ".git", ".plugin-local", ".plugin-secrets")
        forbidden_files = set(context.source_map.get("developer_only_files", []))
        for item in staged.rglob("*"):
            if not item.is_file():
                continue
            rel = item.relative_to(staged).as_posix()
            if rel in forbidden_files or any(rel == fr or rel.startswith(fr + "/") for fr in forbidden_roots):
                raise ValidationFailedError(f"Developer-only path leaked into end-user bundle: {rel}")

        try:
            audit = bundle_mod.audit_directory(staged)
        except bundle_mod.BundleError as exc:
            raise ValidationFailedError(f"Portable bundle audit failed: {exc}") from exc
        if audit.get("status") != "PASS":
            raise ValidationFailedError(f"Portable bundle audit did not pass: {audit}")
        return audit

    def package(self, context: AdapterContext, built_dir: Path, artifacts_dir: Path) -> dict[str, Any]:
        bundle_mod = _load_bundle_module(context.repo_root)
        artifacts = Path(artifacts_dir)
        artifacts.mkdir(parents=True, exist_ok=True)
        archive_name = self.config.archive_name or "gis-development-suite.zip"
        archive_path = artifacts / archive_name
        bundle_mod.write_deterministic_zip(Path(built_dir), archive_path)
        archive_hash = sha256_file(archive_path)
        (artifacts / f"{archive_name}.sha256").write_text(f"{archive_hash}  {archive_name}\n", encoding="ascii", newline="\n")
        # Extract-verify deterministic archive (Step 7 of 10-step update pipeline).
        try:
            bundle_mod.audit_path(archive_path)
        except bundle_mod.BundleError as exc:
            raise ValidationFailedError(f"Packaged ZIP verification failed: {exc}") from exc
        return {"archive_name": archive_name, "archive_sha256": archive_hash}

    def status(self, context: AdapterContext) -> dict[str, Any]:
        bundle_dir = context.repo_root / self.config.bundle_dir
        manifest_path = context.repo_root / self.config.manifest_path
        artifacts_dir = context.repo_root / self.config.artifacts_dir
        archive_name = self.config.archive_name or "gis-development-suite.zip"
        archive_path = artifacts_dir / archive_name

        state = inspect_built_output(bundle_dir, manifest_path, context.source_digest)
        bundle_sha = None
        if (bundle_dir / "bundle-manifest.json").is_file():
            try:
                bundle_sha = json.loads((bundle_dir / "bundle-manifest.json").read_text(encoding="utf-8")).get("content_sha256")
            except (OSError, json.JSONDecodeError):
                pass
        archive_sha = sha256_file(archive_path) if archive_path.is_file() else None
        if state == "UP_TO_DATE" and not archive_path.is_file() and not context.is_ci:
            state = "OUTDATED"
        return {
            "platform": self.config.id,
            "state": state,
            "phase_status": self.config.phase_status,
            "bundle_sha256": bundle_sha,
            "archive_sha256": archive_sha,
        }

    def sync_local(self, context: AdapterContext) -> dict[str, Any]:
        target_cfg = context.owner_config.get("targets", {}).get(self.config.id, {})
        local_dir_raw = str(target_cfg.get("localSyncDir", "")).strip()
        if not context.owner_config.get("allowLocalSync", False) or not target_cfg.get("enabled", False) or not local_dir_raw:
            return {
                "platform": self.config.id,
                "state": "NOT_INSTALLED",
                "installed_digest": None,
                "built_digest": self.status(context).get("bundle_sha256"),
                "actions": ["No external localSyncDir configured in owner-config.json; unpacked repo package kept clean."],
            }

        built_dir = context.repo_root / self.config.bundle_dir
        if not (built_dir / "bundle-manifest.json").is_file():
            return {
                "platform": self.config.id,
                "state": "BUILD_FAILED",
                "installed_digest": None,
                "built_digest": None,
                "actions": ["Cannot sync before portable bundle is built."],
            }

        built_sha = json.loads((built_dir / "bundle-manifest.json").read_text(encoding="utf-8")).get("content_sha256")
        dest_dir = Path(local_dir_raw).expanduser().resolve()
        retention = int(context.sync_config.get("retentionCount", 3))
        rollback_rel = context.sync_config.get("rollbackDirectoryRelativePath", ".plugin-local/rollback")
        if dest_dir.is_dir():
            snapshot_known_good(context.repo_root, f"{self.config.id}_sync", context.version, dest_dir, retention=retention, rollback_rel=rollback_rel)

        staging_copy = dest_dir.parent / f".{dest_dir.name}.sync-staging"
        if staging_copy.exists():
            shutil.rmtree(staging_copy)
        try:
            shutil.copytree(built_dir, staging_copy)
            if dest_dir.exists():
                shutil.rmtree(dest_dir)
            dest_dir.parent.mkdir(parents=True, exist_ok=True)
            staging_copy.rename(dest_dir)
            ver = self.verify(context)
            return {
                "platform": self.config.id,
                "state": ver["state"],
                "installed_digest": ver.get("installed_digest"),
                "built_digest": built_sha,
                "actions": [f"Synchronized portable bundle atomically to configured localSyncDir ({ver['state']})."],
            }
        except Exception as exc:  # noqa: BLE001 — isolated rollback on sync failure
            if staging_copy.exists():
                shutil.rmtree(staging_copy, ignore_errors=True)
            try:
                restore_snapshot(context.repo_root, f"{self.config.id}_sync", None, dest_dir, rollback_rel=rollback_rel)
            except Exception:
                pass
            return {
                "platform": self.config.id,
                "state": "SYNC_FAILED_ROLLED_BACK",
                "installed_digest": None,
                "built_digest": built_sha,
                "actions": [f"Portable local sync failed and rolled back cleanly: {exc}"],
            }

    def prepare_release(self, context: AdapterContext) -> dict[str, Any]:
        st = self.status(context)
        if not st.get("archive_sha256"):
            return {"platform": self.config.id, "state": "BUILD_FAILED", "notes": "Archive missing; build first."}
        return {
            "platform": self.config.id,
            "state": "PREPARED_FOR_SUBMISSION",
            "archive_sha256": st["archive_sha256"],
            "notes": "Portable ZIP + SHA-256 verified and staged locally; external upload remains manual/approval-gated.",
        }

    def update_owner_remote(self, context: AdapterContext) -> dict[str, Any]:
        raise ApprovalRequiredError(
            "Portable bundle does not auto-upload to remote hosts without explicit release workflow approval.",
            state="MANUAL_ACTION_REQUIRED",
        )

    def verify(self, context: AdapterContext) -> dict[str, Any]:
        built_dir = context.repo_root / self.config.bundle_dir
        built_sha = None
        if (built_dir / "bundle-manifest.json").is_file():
            built_sha = json.loads((built_dir / "bundle-manifest.json").read_text(encoding="utf-8")).get("content_sha256")
        target_cfg = context.owner_config.get("targets", {}).get(self.config.id, {})
        local_dir_raw = str(target_cfg.get("localSyncDir", "")).strip()
        if not local_dir_raw or not Path(local_dir_raw).expanduser().is_dir():
            return {"platform": self.config.id, "state": "NOT_INSTALLED", "installed_digest": None, "built_digest": built_sha}
        inst_manifest = Path(local_dir_raw).expanduser() / "bundle-manifest.json"
        if not inst_manifest.is_file():
            return {"platform": self.config.id, "state": "OUTDATED", "installed_digest": None, "built_digest": built_sha}
        inst_sha = json.loads(inst_manifest.read_text(encoding="utf-8")).get("content_sha256")
        return {
            "platform": self.config.id,
            "state": "SYNCED_VERIFIED" if inst_sha == built_sha and built_sha else "OUTDATED",
            "installed_digest": inst_sha,
            "built_digest": built_sha,
        }

    def rollback(self, context: AdapterContext, version: str | None) -> dict[str, Any]:
        bundle_dir = context.repo_root / self.config.bundle_dir
        rollback_rel = context.sync_config.get("rollbackDirectoryRelativePath", ".plugin-local/rollback")
        return restore_snapshot(context.repo_root, self.config.id, version, bundle_dir, rollback_rel=rollback_rel)
