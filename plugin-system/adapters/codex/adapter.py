"""OpenAI Codex (CLI / Desktop) plugin adapter (`.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..client_common import PackagedClientAdapter
from ...core.models import AdapterContext, ValidationFailedError


class CodexAdapter(PackagedClientAdapter):
    cli_command = "codex"
    supports_hooks = False
    detect_hints = (".codex",)
    install_note_en = (
        "Register `.agents/plugins/marketplace.json` in your Codex workspace or add "
        "`GIS-Development-Skills-Plugins/codex/plugin` directly for local Codex CLI / Desktop discovery."
    )
    install_note_ar = (
        "سجّل فهرس `.agents/plugins/marketplace.json` في مساحة عمل Codex أو أشر مباشرة إلى المجلد "
        "`GIS-Development-Skills-Plugins/codex/plugin` مع الحفاظ على سياسة `AGENTS.md`."
    )

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "client": "openai-codex",
            "skills": "./skills",
            "instructions": "AGENTS.md",
            "marketplace_entry": ".agents/plugins/marketplace.json",
            "shared_listing_group": str(self.config.raw.get("shared_listing_group", "openai-directory")),
        }

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        adapted = [
            {
                "component": ".codex-plugin/plugin.json + .agents/plugins/marketplace.json",
                "action": "Mapped Codex plugin manifest (`skills` + `AGENTS.md`) and OpenAI marketplace catalog entry.",
            }
        ]
        return adapted, []

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        if manifest_data.get("skills") != "./skills" or manifest_data.get("instructions") != "AGENTS.md":
            raise ValidationFailedError("Codex manifest must declare skills='./skills' and instructions='AGENTS.md'")
        if not (staged_bundle / manifest_data["instructions"]).is_file():
            raise ValidationFailedError("Codex bundle missing referenced AGENTS.md instructions")
        return {"client": "openai-codex", "marketplace_entry": manifest_data.get("marketplace_entry")}
