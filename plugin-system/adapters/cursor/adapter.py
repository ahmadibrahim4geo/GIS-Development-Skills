"""Cursor adapter (`.cursor-plugin/plugin.json` + `.cursor/rules/gis-development-skills.mdc`)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ..client_common import PackagedClientAdapter
from ...core.catalogs import _cursor_rules_text
from ...core.models import AdapterContext, ValidationFailedError


class CursorAdapter(PackagedClientAdapter):
    cli_command = "cursor"
    supports_hooks = False
    detect_hints = (".cursor",)
    install_note_en = (
        "Import `GIS-Development-Skills-Plugins/cursor/plugin` via Cursor Plugins or copy repo `.cursor/rules/gis-development-skills.mdc` "
        "into your Cursor workspace rules directory (honors Cursor team/import controls)."
    )
    install_note_ar = (
        "استورد المجلد `GIS-Development-Skills-Plugins/cursor/plugin` في Cursor أو اعتمد ملف القواعد "
        "`.cursor/rules/gis-development-skills.mdc` مع الالتزام بضوابط استيراد الفريق."
    )

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "client": "cursor",
            "skills": "./skills",
            "rules": ".cursor/rules/gis-development-skills.mdc",
            "team_import_mode": "manual-team-marketplace-or-workspace-rules",
        }

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        rules_dir = staged_bundle / ".cursor" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)
        (rules_dir / "gis-development-skills.mdc").write_text(
            _cursor_rules_text(context),
            encoding="utf-8",
            newline="\n",
        )
        adapted = [
            {
                "component": ".cursor-plugin/plugin.json + .cursor/rules/gis-development-skills.mdc",
                "action": "Mapped Cursor plugin manifest and workspace `.mdc` governance rule file.",
            }
        ]
        excluded = [
            {
                "item": "Cursor Team Admin Marketplace auto-sync",
                "reason": "Team dashboard publishing requires organization admin import rather than unattended local CLI push (REQ-PL-023).",
                "alternative": "Verified workspace `.cursor/rules/gis-development-skills.mdc` + `artifacts/gis-development-skills-cursor.zip`",
            }
        ]
        return adapted, excluded

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        rule_file = staged_bundle / ".cursor" / "rules" / "gis-development-skills.mdc"
        if not rule_file.is_file():
            raise ValidationFailedError("Cursor bundle missing .cursor/rules/gis-development-skills.mdc")
        text = rule_file.read_text(encoding="utf-8")
        if "alwaysApply: true" not in text:
            raise ValidationFailedError("Cursor .mdc rule missing expected frontmatter 'alwaysApply: true'")
        return {"rules_file": ".cursor/rules/gis-development-skills.mdc"}
