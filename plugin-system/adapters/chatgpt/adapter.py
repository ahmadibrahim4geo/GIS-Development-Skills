"""ChatGPT portable plugin ZIP adapter sharing OpenAI listing group while stripping lifecycle hooks."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..client_common import PackagedClientAdapter
from ...core.models import AdapterContext, ValidationFailedError


class ChatGptAdapter(PackagedClientAdapter):
    cli_command = None
    portal_only = True
    supports_hooks = False
    install_note_en = (
        "Upload the verified `artifacts/gis-development-skills-chatgpt.zip` archive via ChatGPT Plugin/Custom GPT developer import. "
        "Shares OpenAI directory listing group (`openai-directory`) without duplicate public listing."
    )
    install_note_ar = (
        "ارفع أرشيف `artifacts/gis-development-skills-chatgpt.zip` التحقّقي يدويًا في بوابة ChatGPT دون إنشاء إدراج عام مكرر مع Codex، "
        "مع إزالة جميع خطافات التشغيل المحلية."
    )

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "client": "chatgpt",
            "shared_listing_group": str(self.config.raw.get("shared_listing_group", "openai-directory")),
            "duplicate_public_listing_blocked": True,
            "lifecycle_hooks": [],
            "stripped_components": ["lifecycle-hooks", "local-app-cli-wrappers"],
        }

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        adapted = [
            {
                "component": "plugin.json (OpenAI shared directory identity)",
                "action": "Configured ChatGPT portable package linked to shared `openai-directory` group with zero duplicate public listing.",
            }
        ]
        excluded = [
            {
                "item": "lifecycle-hooks (.claude-plugin/hooks.json, .cursor/rules/, local pre-commit/app hooks)",
                "reason": "ChatGPT hosted runtime does not execute desktop agent lifecycle hooks or local CLI wrappers (REQ-PL-019).",
                "alternative": "Canonical SKILL.md & Python validators inside bundle or local Codex adapter",
            }
        ]
        return adapted, excluded

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        if manifest_data.get("supports_hooks") is not False or manifest_data.get("lifecycle_hooks") != []:
            raise ValidationFailedError("ChatGPT bundle must explicitly set supports_hooks=false and lifecycle_hooks=[]")
        if (staged_bundle / ".claude-plugin" / "hooks.json").exists() or (staged_bundle / "hooks.json").exists():
            raise ValidationFailedError("ChatGPT bundle leaked unsupported lifecycle hooks file")
        return {
            "shared_listing_group": manifest_data.get("shared_listing_group"),
            "hooks_stripped": True,
        }
