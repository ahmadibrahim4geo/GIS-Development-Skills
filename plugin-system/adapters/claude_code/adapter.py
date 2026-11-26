"""Claude Code adapter (`.claude-plugin/plugin.json`, `marketplace.json`, loop-safe opt-in hooks)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path
from typing import Any

from ..client_common import PackagedClientAdapter
from ...core.catalogs import _claude_marketplace_payload
from ...core.models import AdapterContext, ValidationFailedError


class ClaudeCodeAdapter(PackagedClientAdapter):
    cli_command = "claude"
    supports_hooks = True
    detect_hints = (".claude",)
    install_note_en = (
        "Add `.claude-plugin/marketplace.json` or install `GIS-Development-Skills-Plugins/claude-code/plugin` via "
        "Claude Code (`user`, `project`, or `local` scope) while keeping bundled references intact."
    )
    install_note_ar = (
        "ثبّت من فهرس `.claude-plugin/marketplace.json` أو من المجلد `GIS-Development-Skills-Plugins/claude-code/plugin` "
        "عبر Claude Code ضمن نطاق `user` أو `project` أو `local`."
    )

    def platform_manifest_extras(self, context: AdapterContext) -> dict[str, Any]:
        return {
            "client": "claude-code",
            "instructions": "CLAUDE.md",
            "skills": "./skills",
            "scopes": ["user", "project", "local"],
            "marketplace": ".claude-plugin/marketplace.json",
            "hooks": ".claude-plugin/hooks.json",
        }

    def apply_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        base_manifest: dict[str, Any],
    ) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
        claude_dir = staged_bundle / ".claude-plugin"
        claude_dir.mkdir(parents=True, exist_ok=True)
        mkt_payload = _claude_marketplace_payload(context, self.config)
        (claude_dir / "marketplace.json").write_text(
            json.dumps(mkt_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        hooks_payload = {
            "schema_version": "1.0",
            "opt_in": True,
            "loop_safe": True,
            "hooks": {
                "SessionStart": [
                    {
                        "command": "python -B scripts/validate_skill_pack.py",
                        "readonly": True,
                        "enabled_by_default": False,
                    }
                ]
            },
        }
        (claude_dir / "hooks.json").write_text(
            json.dumps(hooks_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        adapted = [
            {
                "component": ".claude-plugin/{plugin.json, marketplace.json, hooks.json}",
                "action": "Packaged Claude Code scopes (`user`/`project`/`local`), marketplace catalog, and loop-safe read-only hook descriptor.",
            }
        ]
        return adapted, []

    def validate_platform_extras(
        self,
        context: AdapterContext,
        staged_bundle: Path,
        manifest_data: dict[str, Any],
    ) -> dict[str, Any]:
        for rel in (".claude-plugin/marketplace.json", ".claude-plugin/hooks.json", "CLAUDE.md"):
            if not (staged_bundle / rel).is_file():
                raise ValidationFailedError(f"Claude Code bundle missing required file: {rel}")
        hooks_data = json.loads((staged_bundle / ".claude-plugin" / "hooks.json").read_text(encoding="utf-8"))
        if not hooks_data.get("loop_safe"):
            raise ValidationFailedError("Claude Code hooks.json must explicitly declare loop_safe=true")
        cli_bin = shutil.which("claude")
        cli_check = "NOT_RUN"
        if cli_bin:
            res = self.run_readonly_cli_check([cli_bin, "--help"])
            cli_check = "PASS" if res.get("executed") and res.get("returncode") == 0 else "FAILED"
        return {"scopes": manifest_data.get("scopes"), "cli_help_check": cli_check}
