"""11-method platform adapter contract plus shared P09 scaffold base class."""

from __future__ import annotations

import json
import shutil
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from ..core.models import AdapterContext, ApprovalRequiredError, PlatformConfig
from ..core.parity import build_parity_report


class PluginAdapter(ABC):
    """Unified 11-method lifecycle contract implemented by every platform adapter."""

    def __init__(self, config: PlatformConfig):
        self.config = config

    @abstractmethod
    def detect(self, context: AdapterContext) -> dict[str, Any]:
        """Detect platform availability / CLI presence read-only."""

    @abstractmethod
    def capabilities(self) -> dict[str, Any]:
        """Declare supported packaging, hooks, local sync, verification, and release features."""

    @abstractmethod
    def build(self, context: AdapterContext, staging_dir: Path) -> dict[str, Any]:
        """Build unpacked platform payload inside clean staging_dir."""

    @abstractmethod
    def validate(self, context: AdapterContext, staged_dir: Path) -> dict[str, Any]:
        """Validate staged output schema, links, UTF-8, and security isolation."""

    @abstractmethod
    def package(self, context: AdapterContext, built_dir: Path, artifacts_dir: Path) -> dict[str, Any]:
        """Package deterministic archive (.zip + .sha256) into artifacts_dir."""

    @abstractmethod
    def status(self, context: AdapterContext) -> dict[str, Any]:
        """Return built vs source vs installed status honestly."""

    @abstractmethod
    def sync_local(self, context: AdapterContext) -> dict[str, Any]:
        """Perform authorized local sync if configured and installed."""

    @abstractmethod
    def prepare_release(self, context: AdapterContext) -> dict[str, Any]:
        """Prepare release artifacts locally without publishing externally."""

    @abstractmethod
    def update_owner_remote(self, context: AdapterContext) -> dict[str, Any]:
        """Execute owner-authorized remote update or raise ApprovalRequiredError."""

    @abstractmethod
    def verify(self, context: AdapterContext) -> dict[str, Any]:
        """Verify live local installation hash matches latest built package."""

    @abstractmethod
    def rollback(self, context: AdapterContext, version: str | None) -> dict[str, Any]:
        """Restore a prior known-good package snapshot for this platform."""


class P09StubAdapter(PluginAdapter):
    """Shared honest scaffold for the 6 client adapters scheduled for full completion in P09."""

    cli_command: str | None = None
    scaffold_notes: str = "Scheduled for full platform contract implementation in Phase P09."

    def detect(self, context: AdapterContext) -> dict[str, Any]:
        cmd = self.cli_command
        found = shutil.which(cmd) if cmd else None
        return {
            "platform": self.config.id,
            "installed": bool(found),
            "cli_command": cmd,
            "state": "NOT_RUN" if found else "NOT_INSTALLED",
        }

    def capabilities(self) -> dict[str, Any]:
        return {
            "unpacked": bool(self.config.raw.get("supports_unpacked", True)),
            "zip": bool(self.config.raw.get("supports_zip", True)),
            "hooks": bool(self.config.raw.get("supports_hooks", False)),
            "local_sync": bool(self.config.raw.get("supports_local_sync", False)),
            "verify": bool(self.config.raw.get("supports_verify", False)),
            "rollback": bool(self.config.raw.get("supports_rollback", True)),
            "phase_status": self.config.phase_status,
        }

    def build(self, context: AdapterContext, staging_dir: Path) -> dict[str, Any]:
        out = staging_dir / self.config.id
        out.mkdir(parents=True, exist_ok=True)
        readme = (
            f"# {self.config.display_name} — Plugin Scaffold ({self.config.phase_target})\n\n"
            f"- **Platform ID:** `{self.config.id}`\n"
            f"- **Plugin ID:** `{context.plugin_id}`\n"
            f"- **Phase Status:** `{self.config.phase_status}` (Full manifest & client validation scheduled in `{self.config.phase_target}`)\n"
            f"- **Target Manifest Path:** `{self.config.manifest_path}`\n"
            f"- **Canonical Version:** `{context.version}` (`{context.source_commit}`)\n\n"
            f"{self.scaffold_notes}\n\n"
            f"Use `../portable-agent-plugin/` for the active P02 self-contained bundle.\n"
        )
        (out / "README.md").write_text(readme, encoding="utf-8", newline="\n")
        parity = build_parity_report(
            self.config.id,
            self.config.display_name,
            phase_status=self.config.phase_status,
            version=context.version,
            source_commit=context.source_commit,
            source_digest=context.source_digest,
            carried=[],
            adapted=[],
            excluded=[
                {
                    "item": "full-platform-manifest",
                    "reason": f"Scheduled for live documentation verification and packaging in {self.config.phase_target}.",
                    "alternative": "portable-agent-plugin/plugin",
                }
            ],
            notes=self.scaffold_notes,
        )
        return {"staged_output_dir": str(out), "parity_report": parity}

    def validate(self, context: AdapterContext, staged_dir: Path) -> dict[str, Any]:
        readme = Path(staged_dir) / "README.md"
        if not readme.is_file():
            raise RuntimeError(f"Scaffold README missing for {self.config.id}")
        return {"status": "PASS", "phase_status": self.config.phase_status}

    def package(self, context: AdapterContext, built_dir: Path, artifacts_dir: Path) -> dict[str, Any]:
        return {"archive_name": None, "archive_sha256": None, "state": "NOT_RUN"}

    def status(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "platform": self.config.id,
            "state": "NOT_RUN",
            "phase_status": self.config.phase_status,
            "bundle_sha256": None,
            "archive_sha256": None,
            "notes": self.scaffold_notes,
        }

    def sync_local(self, context: AdapterContext) -> dict[str, Any]:
        det = self.detect(context)
        return {
            "platform": self.config.id,
            "state": det["state"],
            "installed_digest": None,
            "built_digest": None,
            "actions": [f"Client sync deferred until {self.config.phase_target} ({det['state']})."],
        }

    def prepare_release(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "platform": self.config.id,
            "state": "NOT_RUN",
            "notes": f"Release packaging scheduled in {self.config.phase_target}.",
        }

    def update_owner_remote(self, context: AdapterContext) -> dict[str, Any]:
        raise ApprovalRequiredError(
            f"Remote update for {self.config.id} not active until {self.config.phase_target} and explicit owner approval.",
            state="MANUAL_ACTION_REQUIRED",
        )

    def verify(self, context: AdapterContext) -> dict[str, Any]:
        det = self.detect(context)
        return {"platform": self.config.id, "state": det["state"], "installed_digest": None, "built_digest": None}

    def rollback(self, context: AdapterContext, version: str | None) -> dict[str, Any]:
        return {
            "platform": self.config.id,
            "state": "NOT_RUN",
            "notes": f"Rollback snapshots begin once full {self.config.id} packaging runs in {self.config.phase_target}.",
        }
