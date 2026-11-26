"""Synchronization and stale-gate checks for tracked client marketplaces, rules, and bilingual platform READMEs."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from .models import AdapterContext, PlatformConfig


def _codex_marketplace_payload(context: AdapterContext, codex_cfg: PlatformConfig) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "marketplace": "openai-codex-local",
        "plugin_id": context.plugin_id,
        "name": "gis-development-skills",
        "display_name": context.suite_name,
        "version": context.version,
        "source_commit": context.source_commit,
        "source_digest": context.source_digest,
        "bundle_digest": context.bundle_digest,
        "plugins": [
            {
                "id": context.plugin_id,
                "name": "gis-development-skills",
                "title": context.suite_name,
                "version": context.version,
                "source_commit": context.source_commit,
                "source_digest": context.source_digest,
                "plugin_path": codex_cfg.bundle_dir,
                "manifest_path": codex_cfg.manifest_path,
                "shared_listing_group": str(codex_cfg.raw.get("shared_listing_group", "openai-directory")),
                "license": "MIT",
                "repository": "https://github.com/ahmadibrahim4geo/GIS-Development-Skills",
            }
        ],
    }


def _claude_marketplace_payload(context: AdapterContext, claude_cfg: PlatformConfig) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "name": "gis-development-skills-marketplace",
        "owner": {
            "name": "Ahmad Ibrahim",
            "url": "https://ahmadibrahim4geo.github.io/MIRSAD/",
        },
        "metadata": {
            "plugin_id": context.plugin_id,
            "version": context.version,
            "source_commit": context.source_commit,
            "source_digest": context.source_digest,
            "bundle_digest": context.bundle_digest,
        },
        "plugins": [
            {
                "name": "gis-development-skills",
                "plugin_id": context.plugin_id,
                "description": "Verifiable GIS Engineering, Spatial Architecture, Web/Mobile GIS, and Security Governance Suite.",
                "version": context.version,
                "source": f"./{claude_cfg.bundle_dir}",
                "manifest": claude_cfg.manifest_path,
                "supported_scopes": ["user", "project", "local"],
                "shared_payload_platforms": ["claude-code", "claude-ai"],
                "license": "MIT",
            }
        ],
    }


def _cursor_rules_text(context: AdapterContext) -> str:
    return "\n".join(
        [
            "---",
            "description: GIS Development Skills governance, engine selection, security guardian, and DoneProof rules",
            "alwaysApply: true",
            "---",
            "",
            f"# GIS Development Skills (`{context.version}` · `{context.source_digest[:12]}`)",
            "",
            f"<!-- source-digest: {context.source_digest} -->",
            f"<!-- version: {context.version} -->",
            "",
            "- Follow root `AGENTS.md` and `skills/gis-development/SKILL.md` for task routing and single specialist ownership.",
            "- Run `skills/gis-security-guardian/SKILL.md` checks before accepting third-party code, archives, or network links.",
            "- Prefer verified open-source geospatial stacks from `references/project-catalog.json` via `scripts/search_catalog.py` before reimplementing engines.",
            "- Never fabricate `T2-T4` native GIS/browser/device pass results when hosts or SDKs are absent; emit `NOT_RUN` honestly via `skills/completion-evidence/SKILL.md`.",
            "- Record meaningful work and test verification in `.agent-development-log/` via `scripts/development_journal.py`.",
            "",
        ]
    )


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def render_platform_readme(cfg: PlatformConfig, context: AdapterContext, metadata: dict[str, Any]) -> str:
    """Render deterministic bilingual English/Arabic install & verification documentation."""
    pid = cfg.id
    manifest_rel = Path(cfg.manifest_path).relative_to(Path(cfg.output_dir)).as_posix() if cfg.manifest_path else "plugin/plugin.json"
    archive_name = cfg.archive_name or f"gis-development-skills-{pid}.zip"
    cli_cmd = str(cfg.raw.get("cli_command", "") or "").strip()
    hooks_note_en = (
        "Includes opt-in, loop-safe lifecycle hook metadata (`supports_hooks: true`)."
        if metadata.get("supports_hooks")
        else "Lifecycle hooks are explicitly omitted/stripped (`supports_hooks: false`)."
    )
    hooks_note_ar = (
        "يدعم بيانات الخطافات الاختيارية الآمنة ضد التكرار (`supports_hooks: true`)."
        if metadata.get("supports_hooks")
        else "يتم استبعاد خطافات دورة الحياة غير المدعومة صراحةً (`supports_hooks: false`)."
    )
    portal_note_en = metadata.get("install_note_en", "Install from unpacked `plugin/` folder or verified ZIP artifact locally.")
    portal_note_ar = metadata.get("install_note_ar", "ثبّت الحزمة من المجلد `plugin/` أو من أرشيف `.zip` محليًا بعد التحقق من SHA-256.")

    lines = [
        f"# {cfg.display_name} (`{pid}`)",
        "",
        f"- **Plugin ID:** `{context.plugin_id}`",
        f"- **Version:** `{context.version}` (`{context.source_commit}`)",
        f"- **Phase Status:** `{cfg.phase_status}`",
        f"- **Manifest:** [{manifest_rel}]({manifest_rel})",
        f"- **Parity Report:** [parity-report.json](parity-report.json)",
        f"- **Local ZIP Artifact:** `artifacts/{archive_name}` (`artifacts/{archive_name}.sha256`)",
        f"- **Hooks Contract:** {hooks_note_en}",
        "",
        "## English — Installation, Verification & Uninstall",
        "",
        f"1. **Verify integrity locally:** `python -B ../../scripts/build_skill_bundle.py --check plugin`",
        f"2. **Platform installation:** {portal_note_en}",
    ]
    if cli_cmd:
        lines.append(f"3. **Client CLI check:** When `{cli_cmd}` is installed on `PATH`, run `{cli_cmd}` discovery/validation; otherwise status remains `NOT_INSTALLED` cleanly without auto-installing.")
    else:
        lines.append("3. **Submission boundary:** Remote/portal uploads remain `PREPARED_FOR_SUBMISSION` / `MANUAL_ACTION_REQUIRED` until manually uploaded or authorized.")
    lines.extend(
        [
            f"4. **Rollback / Uninstall:** Remove the synced copy or run `python -B ../../plugin-system/core/pipeline.py --rollback --platform {pid}`.",
            "",
            "## العربية — التثبيت والتحقق والإزالة",
            "",
            f"- **توافق المنصة:** {hooks_note_ar}",
            f"- **التثبيت والمزامنة:** {portal_note_ar}",
            f"- **التحقق دون اتصال:** نفّذ `python -B ../../scripts/build_skill_bundle.py --check plugin` ثم راجع تقرير التكافؤ [parity-report.json](parity-report.json).",
            f"- **الإزالة أو التراجع:** احذف النسخة المثبتة لدى العميل أو استرجع آخر نسخة سليمة عبر `--rollback --platform {pid}`.",
            "",
            "- [Canonical Repository Guide](../../README.md) · [Plugins Index](../index.json)",
            "",
        ]
    )
    return "\n".join(lines)


def sync_repo_client_catalogs(repo_root: Path, context: AdapterContext, configs: list[PlatformConfig]) -> list[str]:
    """Write repo-level client marketplace catalogs and Cursor rules for active P09 platforms."""
    by_id = {cfg.id: cfg for cfg in configs}
    updated: list[str] = []

    if "codex" in by_id and by_id["codex"].phase_status.startswith("ACTIVE_"):
        codex_path = repo_root / ".agents" / "plugins" / "marketplace.json"
        _write_json(codex_path, _codex_marketplace_payload(context, by_id["codex"]))
        updated.append(".agents/plugins/marketplace.json")

    if "claude-code" in by_id and by_id["claude-code"].phase_status.startswith("ACTIVE_"):
        claude_path = repo_root / ".claude-plugin" / "marketplace.json"
        _write_json(claude_path, _claude_marketplace_payload(context, by_id["claude-code"]))
        updated.append(".claude-plugin/marketplace.json")

    if "cursor" in by_id and by_id["cursor"].phase_status.startswith("ACTIVE_"):
        cursor_path = repo_root / ".cursor" / "rules" / "gis-development-skills.mdc"
        cursor_path.parent.mkdir(parents=True, exist_ok=True)
        cursor_path.write_text(_cursor_rules_text(context), encoding="utf-8", newline="\n")
        updated.append(".cursor/rules/gis-development-skills.mdc")

    return updated


def check_repo_client_catalogs(repo_root: Path, context: AdapterContext, configs: list[PlatformConfig]) -> list[str]:
    """Verify tracked marketplace manifests and Cursor rules match current canonical digest and version."""
    by_id = {cfg.id: cfg for cfg in configs}
    stale: list[str] = []

    if "codex" in by_id and by_id["codex"].phase_status.startswith("ACTIVE_"):
        codex_path = repo_root / ".agents" / "plugins" / "marketplace.json"
        if not codex_path.is_file():
            stale.append(".agents/plugins/marketplace.json (missing)")
        else:
            try:
                data = json.loads(codex_path.read_text(encoding="utf-8"))
                if data.get("source_digest") != context.source_digest or data.get("version") != context.version:
                    stale.append(".agents/plugins/marketplace.json (stale digest/version)")
            except (OSError, json.JSONDecodeError):
                stale.append(".agents/plugins/marketplace.json (invalid json)")

    if "claude-code" in by_id and by_id["claude-code"].phase_status.startswith("ACTIVE_"):
        claude_path = repo_root / ".claude-plugin" / "marketplace.json"
        if not claude_path.is_file():
            stale.append(".claude-plugin/marketplace.json (missing)")
        else:
            try:
                data = json.loads(claude_path.read_text(encoding="utf-8"))
                meta = data.get("metadata", {})
                if meta.get("source_digest") != context.source_digest or meta.get("version") != context.version:
                    stale.append(".claude-plugin/marketplace.json (stale digest/version)")
            except (OSError, json.JSONDecodeError):
                stale.append(".claude-plugin/marketplace.json (invalid json)")

    if "cursor" in by_id and by_id["cursor"].phase_status.startswith("ACTIVE_"):
        cursor_path = repo_root / ".cursor" / "rules" / "gis-development-skills.mdc"
        if not cursor_path.is_file():
            stale.append(".cursor/rules/gis-development-skills.mdc (missing)")
        else:
            text = cursor_path.read_text(encoding="utf-8")
            m = re.search(r"<!--\s*source-digest:\s*([0-9a-f]{64})\s*-->", text)
            if not m or m.group(1) != context.source_digest:
                stale.append(".cursor/rules/gis-development-skills.mdc (stale digest)")

    return stale
