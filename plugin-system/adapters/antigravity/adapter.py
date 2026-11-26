"""Google Antigravity plugin adapter (`plugin.json` + `.antigravity/plugin.json` + optional `agy` validation)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from ..client_common import PackagedClientAdapter
from ...core.models import AdapterContext, ValidationFailedError


class AntigravityAdapter(PackagedClientAdapter):
    cli_command = "agy"
    supports_hooks = False
    detect_hints = (".antigravity", ".gemini/antigravity")
    install_note_en = (
        "Load `GIS-Development-Skills-Plugins/antigravity/plugin` via Antigravity Plugins or extract "
        "`artifacts/gis-development-skills-antigravity.zip`. Validate with `agy plugin validate` when `agy` CLI is installed."
    )
    install_note_ar = (
        "حمّل المجلد `GIS-Development-Skills-Plugins/antigravity/plugin` في Antigravity أو فك ضغط "
        "`artifacts/gis-development-skills-antigravity.zip`، وتحقق منه عبر `agy plugin validate` عند توفر أداة `agy`."
    )

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "client": "antigravity",
            "cli_command": "agy",
            "validate_command": "agy plugin validate",
            "skills_dir": "skills",
            "rules_file": "AGENTS.md",
        }

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        agy_dir = staged_bundle / ".antigravity"
        agy_dir.mkdir(parents=True, exist_ok=True)
        meta = {
            "schema_version": "1.0",
            "plugin_id": context.plugin_id,
            "name": "gis-development-skills",
            "description": "The Heart of Geospatial Innovation — By Ahmed Ibrahim",
            "icon": "../assets/icon.svg",
            "version": context.version,
            "source_digest": context.source_digest,
            "skills": "../skills",
            "entrypoint": "../SKILL.md",
            "rules": "../AGENTS.md",
        }
        (agy_dir / "plugin.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8", newline="\n")
        adapted = [
            {
                "component": "plugin.json + .antigravity/plugin.json",
                "action": "Packaged Antigravity plugin manifest, workspace rules (`AGENTS.md`), and `agy plugin validate` metadata.",
            }
        ]
        return adapted, []

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        if not (staged_bundle / ".antigravity" / "plugin.json").is_file():
            raise ValidationFailedError("Antigravity bundle missing .antigravity/plugin.json")
        cli_bin = shutil.which("agy")
        if not cli_bin:
            return {"cli_validation": "NOT_RUN", "reason": "agy CLI binary not installed on host PATH"}
        res = self.run_readonly_cli_check([cli_bin, "plugin", "validate", str(staged_bundle)])
        if not res.get("executed") or res.get("returncode") != 0:
            return {"cli_validation": "FAILED", "details": res}
        return {"cli_validation": "PASSED", "details": res}
