"""Per-platform parity report generation and root index.json synchronization."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def build_parity_report(
    platform_id: str,
    display_name: str,
    *,
    phase_status: str,
    version: str,
    source_commit: str,
    source_digest: str,
    carried: list[str],
    adapted: list[dict[str, str]],
    excluded: list[dict[str, str]],
    notes: str = "",
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "platform": platform_id,
        "display_name": display_name,
        "phase_status": phase_status,
        "version": version,
        "source_commit": source_commit,
        "source_digest": source_digest,
        "carried_components": carried,
        "adapted_components": adapted,
        "excluded_components": excluded,
        "notes": notes,
    }


def write_parity_files(report: dict[str, Any], json_path: Path) -> None:
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def write_root_plugins_index(
    output_root: Path,
    *,
    plugin_id: str,
    version: str,
    source_commit: str,
    source_digest: str,
    bundle_digest: str,
    platforms_summary: dict[str, Any],
) -> Path:
    output_root.mkdir(parents=True, exist_ok=True)
    index_path = output_root / "index.json"
    payload = {
        "schema_version": "1.0",
        "plugin_id": plugin_id,
        "version": version,
        "source_commit": source_commit,
        "source_digest": source_digest,
        "bundle_digest": bundle_digest,
        "platforms": platforms_summary,
    }
    index_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")
    return index_path
