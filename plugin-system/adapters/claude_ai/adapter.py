"""Claude AI / Cowork compatible package sharing payload with Claude Code under explicit portal refresh limits."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from ..client_common import PackagedClientAdapter
from ...core.models import AdapterContext, ValidationFailedError


class ClaudeAiAdapter(PackagedClientAdapter):
    cli_command = None
    portal_only = True
    supports_hooks = False
    install_note_en = (
        "Upload `artifacts/gis-development-skills-claude-ai.zip` in Claude.ai / Cowork Team Settings. "
        "Shares canonical skill payload with `claude-code`; organization/portal catalog refreshes remain manual."
    )
    install_note_ar = (
        "ارفع أرشيف `artifacts/gis-development-skills-claude-ai.zip` في إعدادات Claude.ai / Cowork للمنظمة. "
        "تتشارك الحزمة المرجعية مع `claude-code` مع بقاء التحديث السحابي يدويًا عبر بوابة المنظمة."
    )

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "client": "claude-ai",
            "shared_payload_with": str(self.config.raw.get("shared_payload_with", "claude-code")),
            "portal_refresh_mode": "manual-org-portal",
            "portal_refresh_limits": "Claude AI / Cowork does not support unattended CLI overwrite of organization portal uploads.",
        }

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        claude_dir = staged_bundle / ".claude-plugin"
        claude_dir.mkdir(parents=True, exist_ok=True)
        compat = {
            "schema_version": "1.0",
            "plugin_id": context.plugin_id,
            "platform": "claude-ai",
            "shared_payload_with": "claude-code",
            "version": context.version,
            "source_digest": context.source_digest,
            "entrypoint": "SKILL.md",
        }
        (claude_dir / "plugin.json").write_text(json.dumps(compat, indent=2) + "\n", encoding="utf-8", newline="\n")
        adapted = [
            {
                "component": "plugin.json + .claude-plugin/plugin.json",
                "action": "Shared canonical skill payload with `claude-code` while declaring manual portal refresh limits.",
            }
        ]
        excluded = [
            {
                "item": "claude-code CLI interactive hooks (.claude-plugin/hooks.json)",
                "reason": "Claude AI / Cowork portal packages omit desktop CLI hook scripts and auto-sync daemons (REQ-PL-021).",
                "alternative": "claude-code local CLI package",
            }
        ]
        return adapted, excluded

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        if manifest_data.get("shared_payload_with") != "claude-code":
            raise ValidationFailedError("Claude AI manifest must declare shared_payload_with='claude-code'")
        if not (staged_bundle / ".claude-plugin" / "plugin.json").is_file():
            raise ValidationFailedError("Claude AI bundle missing shared .claude-plugin/plugin.json compatibility descriptor")
        return {"shared_payload_with": "claude-code", "portal_refresh_mode": manifest_data.get("portal_refresh_mode")}
