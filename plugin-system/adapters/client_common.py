"""Shared packaged-client adapter inheriting deterministic portable bundling without logic duplication."""

from __future__ import annotations

import json
import shutil
import subprocess
import time
from pathlib import Path
from typing import Any

from .portable.adapter import PortableAdapter, _load_bundle_module
from ..core.builder import inspect_built_output
from ..core.catalogs import render_platform_readme
from ..core.hashing import sha256_file
from ..core.models import AdapterContext, ApprovalRequiredError, ValidationFailedError
from ..core.parity import build_parity_report


class PackagedClientAdapter(PortableAdapter):
    """Parameterizable adapter for real desktop/cloud AI coding client packages."""

    cli_command: str | None = None
    portal_only: bool = False
    supports_hooks: bool = True
    detect_hints: tuple[str, ...] = ()
    install_note_en: str = "Install from the unpacked plugin/ folder or verified ZIP archive locally."
    install_note_ar: str = "ثبّت الإضافة من مجلد `plugin/` المفكوك أو من أرشيف `.zip` محليًا بعد التحقق."

    def manifest_relpath(self) -> str:
        if self.config.manifest_path and self.config.bundle_dir:
            return Path(self.config.manifest_path).relative_to(Path(self.config.bundle_dir)).as_posix()
        return "plugin.json"

    def _effective_supports_hooks(self) -> bool:
        if "supports_hooks" in self.config.raw:
            return bool(self.config.raw["supports_hooks"])
        return bool(self.supports_hooks)

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {}

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        """Write client-specific files inside staged_bundle before final manifest hashing.

        Returns `(adapted_components, excluded_components)`.
        """
        return [], []

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        return {"cli_validation": "NOT_RUN" if self.cli_command else "NOT_APPLICABLE"}

    def detect(self, context: AdapterContext) -> dict[str, Any]:
        target_cfg = context.owner_config.get("targets", {}).get(self.config.id, {})
        local_sync_dir = str(target_cfg.get("localSyncDir", "")).strip()
        cmd = str(target_cfg.get("cliCommand") or self.config.raw.get("cli_command") or self.cli_command or "").strip() or None

        if self.portal_only and not local_sync_dir:
            return {
                "platform": self.config.id,
                "installed": False,
                "cli_command": None,
                "cli_path": None,
                "portal_only": True,
                "state": "MANUAL_ACTION_REQUIRED",
            }

        cli_path = shutil.which(cmd) if cmd else None
        if not cli_path and not local_sync_dir:
            return {
                "platform": self.config.id,
                "installed": False,
                "cli_command": cmd,
                "cli_path": None,
                "portal_only": self.portal_only,
                "state": "NOT_INSTALLED",
            }

        auth_state = target_cfg.get("authState")
        if auth_state == "AUTH_REQUIRED":
            return {
                "platform": self.config.id,
                "installed": True,
                "cli_command": cmd,
                "cli_path": cli_path,
                "portal_only": self.portal_only,
                "state": "AUTH_REQUIRED",
            }

        return {
            "platform": self.config.id,
            "installed": True,
            "cli_command": cmd,
            "cli_path": cli_path,
            "portal_only": self.portal_only,
            "state": "NOT_RUN" if cli_path else "UP_TO_DATE",
        }

    def capabilities(self) -> dict[str, Any]:
        caps = super().capabilities()
        caps.update(
            {
                "hooks": self._effective_supports_hooks(),
                "portal_only": self.portal_only,
                "cli_command": self.cli_command,
                "phase_status": self.config.phase_status,
            }
        )
        return caps

    def build(self, context: AdapterContext, staging_dir: Path) -> dict[str, Any]:
        bundle_mod = _load_bundle_module(context.repo_root)
        staged_bundle = Path(staging_dir) / "plugin"
        staged_bundle.mkdir(parents=True, exist_ok=True)
        total_bytes = 0
        for relative, source in bundle_mod.iter_source_files(context.repo_root):
            destination = staged_bundle / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            data = source.read_bytes()
            total_bytes += len(data)
            if total_bytes > bundle_mod.MAX_BUNDLE_BYTES:
                raise ValidationFailedError(f"{self.config.id} bundle exceeds {bundle_mod.MAX_BUNDLE_BYTES} byte limit")
            destination.write_bytes(data)
        (staged_bundle / "SKILL.md").write_text(bundle_mod.root_skill_text(), encoding="utf-8", newline="\n")
        inv = bundle_mod.inventory(staged_bundle)
        supports_hooks = self._effective_supports_hooks()

        if not supports_hooks:
            for hook_rel in (".claude-plugin/hooks.json", "hooks.json", ".cursor/rules/gis-development-skills.mdc"):
                hook_target = staged_bundle / hook_rel
                if hook_target.is_file():
                    hook_target.unlink()

        manifest_rel = self.manifest_relpath()
        manifest_dest = staged_bundle / manifest_rel
        manifest_dest.parent.mkdir(parents=True, exist_ok=True)

        base_manifest = {"inventory": inv}
        adapted, excluded = self.apply_platform_extras(context, staged_bundle, base_manifest)

        plugin_manifest: dict[str, Any] = {
            "schema_version": "1.0",
            "plugin_id": context.plugin_id,
            "platform": self.config.id,
            "name": context.suite_name,
            "description": "The Heart of Geospatial Innovation — By Ahmed Ibrahim",
            "icon": "assets/icon.svg",
            "version": context.version,
            "source_commit": context.source_commit,
            "source_digest": context.source_digest,
            "bundle_digest": context.bundle_digest,
            "skill_count": inv["skill_count"],
            "license": "MIT",
            "repository": "https://github.com/ahmadibrahim4geo/GIS-Development-Skills",
            "author": {"name": "Ahmad Ibrahim", "url": "https://ahmadibrahim4geo.github.io/MIRSAD/"},
            "entrypoint": "SKILL.md",
            "supports_hooks": supports_hooks,
            "content_sha256": context.bundle_digest,
        }
        plugin_manifest.update(self.platform_manifest_extras(context))
        manifest_dest.write_text(
            json.dumps(plugin_manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )

        final_manifest = bundle_mod.write_manifest(staged_bundle, context.source_commit)

        # Keep bilingual platform README next to parity-report.json outside plugin/ payload.
        if self.config.output_dir:
            out_root = context.repo_root / self.config.output_dir
            out_root.mkdir(parents=True, exist_ok=True)
            readme_text = render_platform_readme(
                self.config,
                context,
                {
                    "supports_hooks": supports_hooks,
                    "install_note_en": self.install_note_en,
                    "install_note_ar": self.install_note_ar,
                },
            )
            (out_root / "README.md").write_text(readme_text, encoding="utf-8", newline="\n")

        excluded_rows = list(excluded) + [
            {
                "item": "plugin-system/, Update-All-Plugins.*, Update-My-Platforms.*, reports/, plans/, .agent-development-log/",
                "reason": "Developer-only lifecycle infrastructure & secrets excluded from end-user payload (REQ-PL-026 / PL-T26).",
                "alternative": "Canonical repository governance surface",
            }
        ]
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
                    "component": f"SKILL.md + {manifest_rel}",
                    "action": f"Generated {self.config.display_name} manifest and self-contained canonical bundle.",
                },
                *adapted,
            ],
            excluded=excluded_rows,
            notes=f"{self.config.display_name} package built cleanly ({final_manifest['file_count']} files).",
        )
        return {
            "staged_bundle_dir": str(staged_bundle),
            "parity_report": parity,
        }

    def validate(self, context: AdapterContext, staged_dir: Path) -> dict[str, Any]:
        bundle_mod = _load_bundle_module(context.repo_root)
        staged = Path(staged_dir)
        manifest_rel = self.manifest_relpath()
        plugin_file = staged / manifest_rel
        if not plugin_file.is_file():
            raise ValidationFailedError(f"{self.config.id} bundle missing {manifest_rel}")
        p_data = json.loads(plugin_file.read_text(encoding="utf-8"))
        for field in (
            "schema_version",
            "plugin_id",
            "platform",
            "name",
            "version",
            "source_commit",
            "source_digest",
            "skill_count",
            "content_sha256",
        ):
            if field not in p_data:
                raise ValidationFailedError(f"{self.config.id} manifest missing required field: {field}")
        if p_data.get("platform") != self.config.id:
            raise ValidationFailedError(f"{self.config.id} manifest platform mismatch: {p_data.get('platform')!r}")

        forbidden_roots = ("plugin-system", "reports", "plans", ".agent-development-log", ".git", ".plugin-local", ".plugin-secrets")
        forbidden_files = set(context.source_map.get("developer_only_files", []))
        for item in staged.rglob("*"):
            if not item.is_file():
                continue
            rel = item.relative_to(staged).as_posix()
            if rel in forbidden_files or any(rel == fr or rel.startswith(fr + "/") for fr in forbidden_roots):
                raise ValidationFailedError(f"Developer-only path leaked into {self.config.id} bundle: {rel}")

        extra_audit = self.validate_platform_extras(context, staged, p_data)

        try:
            audit = bundle_mod.audit_directory(staged)
        except bundle_mod.BundleError as exc:
            raise ValidationFailedError(f"{self.config.id} bundle audit failed: {exc}") from exc
        if audit.get("status") != "PASS":
            raise ValidationFailedError(f"{self.config.id} bundle audit did not pass: {audit}")
        audit["platform_checks"] = extra_audit
        return audit

    def status(self, context: AdapterContext) -> dict[str, Any]:
        result = super().status(context)
        result["detection"] = self.detect(context)
        return result

    def sync_local(self, context: AdapterContext) -> dict[str, Any]:
        det = self.detect(context)
        target_cfg = context.owner_config.get("targets", {}).get(self.config.id, {})
        local_dir_raw = str(target_cfg.get("localSyncDir", "")).strip()

        if det["state"] == "NOT_INSTALLED" and not local_dir_raw:
            return {
                "platform": self.config.id,
                "state": "NOT_INSTALLED",
                "installed_digest": None,
                "built_digest": self.status(context).get("bundle_sha256"),
                "actions": [
                    f"{self.config.display_name} CLI/client not installed and no external localSyncDir configured; skipped cleanly."
                ],
            }
        if det["state"] == "AUTH_REQUIRED" and not local_dir_raw:
            return {
                "platform": self.config.id,
                "state": "AUTH_REQUIRED",
                "installed_digest": None,
                "built_digest": self.status(context).get("bundle_sha256"),
                "actions": [f"{self.config.display_name} client requires manual sign-in via official CLI session."],
            }
        if self.portal_only and not local_dir_raw:
            return {
                "platform": self.config.id,
                "state": "MANUAL_ACTION_REQUIRED",
                "installed_digest": None,
                "built_digest": self.status(context).get("bundle_sha256"),
                "actions": [
                    f"{self.config.display_name} requires manual/organization portal upload or refresh; package staged cleanly."
                ],
            }
        return super().sync_local(context)

    def verify(self, context: AdapterContext) -> dict[str, Any]:
        res = super().verify(context)
        target_cfg = context.owner_config.get("targets", {}).get(self.config.id, {})
        if res.get("state") == "SYNCED_VERIFIED" and target_cfg.get("requiresReload", False):
            res["state"] = "RELOAD_REQUIRED"
        return res

    def prepare_release(self, context: AdapterContext) -> dict[str, Any]:
        st = self.status(context)
        if not st.get("archive_sha256"):
            return {"platform": self.config.id, "state": "BUILD_FAILED", "notes": "Archive missing; build first."}
        return {
            "platform": self.config.id,
            "state": "PREPARED_FOR_SUBMISSION",
            "archive_sha256": st["archive_sha256"],
            "portal_only": self.portal_only,
            "notes": f"{self.config.display_name} ZIP + SHA-256 validated and staged for submission; no external upload executed.",
        }

    def update_owner_remote(self, context: AdapterContext) -> dict[str, Any]:
        allow_remote = bool(context.owner_config.get("allowRemoteUpdate", False))
        allow_public = bool(context.owner_config.get("allowPublicPublish", False))
        if not context.publish_approved or not (allow_remote or allow_public):
            raise ApprovalRequiredError(
                f"{self.config.display_name} remote/store publish blocked without explicit approval & external owner-config consent.",
                state="MANUAL_ACTION_REQUIRED",
            )
        if self.portal_only:
            return {
                "platform": self.config.id,
                "state": "MANUAL_ACTION_REQUIRED",
                "notes": f"{self.config.display_name} has no automated store push CLI; upload staged archive manually via portal.",
            }
        target_cfg = context.owner_config.get("targets", {}).get(self.config.id, {})
        listing_alias = str(target_cfg.get("listingAlias", "")).strip()
        det = self.detect(context)
        if det["state"] == "NOT_INSTALLED":
            return {
                "platform": self.config.id,
                "state": "NOT_INSTALLED",
                "notes": f"{self.config.display_name} CLI is not installed; remote update cannot proceed.",
            }
        if det["state"] == "AUTH_REQUIRED":
            return {
                "platform": self.config.id,
                "state": "AUTH_REQUIRED",
                "notes": f"{self.config.display_name} official CLI authentication required before remote update.",
            }

        # Support deterministic bounded retry hook ONLY when injected explicitly in tests/owner hooks (max 3 attempts).
        dispatcher = target_cfg.get("_test_remote_dispatcher")
        if callable(dispatcher):
            max_retries = min(3, max(1, int(target_cfg.get("maxRetries", 3))))
            last_error: str | None = None
            for attempt in range(1, max_retries + 1):
                try:
                    resp = dispatcher(self.config.id, listing_alias, attempt)
                    return {
                        "platform": self.config.id,
                        "state": str(resp.get("state", "PENDING_REVIEW")),
                        "listing_alias": listing_alias,
                        "attempts": attempt,
                        "notes": str(resp.get("notes", "Idempotent remote dispatcher completed cleanly.")),
                    }
                except TimeoutError as exc:
                    last_error = str(exc)
            return {
                "platform": self.config.id,
                "state": "NETWORK_UNAVAILABLE",
                "attempts": max_retries,
                "notes": f"Bounded retries ({max_retries}) exhausted cleanly: {last_error}",
            }

        return {
            "platform": self.config.id,
            "state": "PREPARED_FOR_SUBMISSION",
            "listing_alias": listing_alias or None,
            "notes": f"{self.config.display_name} artifact staged; invoke official client submission workflow manually.",
        }

    @staticmethod
    def run_readonly_cli_check(cmd: list[str], *, timeout: int = 15) -> dict[str, Any]:
        """Run a non-interactive, read-only local client validation command cleanly without shell=True."""
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, check=False, shell=False)
            return {
                "executed": True,
                "returncode": proc.returncode,
                "stdout": proc.stdout.strip()[:400],
                "stderr": proc.stderr.strip()[:400],
            }
        except (OSError, subprocess.SubprocessError) as exc:
            return {"executed": False, "error": str(exc)}
