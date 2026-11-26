"""Secret-isolated local synchronization engine with per-platform rollback."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

from ..core.models import AdapterContext, ConfigError


def resolve_owner_config_path(sync_config: dict[str, Any], override_path: Path | None = None) -> Path:
    if override_path is not None:
        return Path(override_path).expanduser().resolve()
    env_var = sync_config.get("ownerConfigEnvVar", "GIS_SKILLS_OWNER_CONFIG")
    env_val = os.environ.get(env_var, "").strip()
    if env_val:
        return Path(env_val).expanduser().resolve()
    if os.name == "nt":
        local_app_data = os.environ.get("LOCALAPPDATA", "").strip()
        if local_app_data:
            return Path(local_app_data) / "GIS-Development-Skills" / "PluginSync" / "owner-config.json"
        raw = sync_config.get("ownerConfigDefaultWindowsPath", "%LOCALAPPDATA%\\GIS-Development-Skills\\PluginSync\\owner-config.json")
        return Path(os.path.expandvars(raw)).expanduser()
    raw = sync_config.get("ownerConfigDefaultUnixPath", "~/.config/gis-development-skills/owner-config.json")
    return Path(raw).expanduser()


def load_owner_config(sync_config: dict[str, Any], override_path: Path | None = None) -> tuple[dict[str, Any], str]:
    """Load private owner config strictly outside Git without ever exposing secret values."""
    cfg_path = resolve_owner_config_path(sync_config, override_path=override_path)
    if not cfg_path.is_file():
        return (
            {
                "allowLocalSync": bool(sync_config.get("autoSyncLocal", True)),
                "allowRemoteUpdate": False,
                "allowPublicPublish": False,
                "targets": {},
            },
            "default-no-owner-file",
        )
    try:
        data = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Invalid owner-config.json outside repo: {exc}") from exc
    return data, f"external-file:{cfg_path.name}"


def sync_platforms_transactionally(adapters: list[Any], context: AdapterContext) -> dict[str, Any]:
    """Sync eligible adapters independently; failure on one rolls back only that platform."""
    results: dict[str, Any] = {}
    partial_failure = False

    if context.is_ci:
        for adapter in adapters:
            results[adapter.config.id] = {
                "platform": adapter.config.id,
                "state": "NOT_APPLICABLE",
                "installed_digest": None,
                "built_digest": None,
                "actions": ["Skipped local host synchronization inside CI runtime."],
            }
        return {"partial_failure": False, "platforms": results}

    for adapter in adapters:
        pid = adapter.config.id
        try:
            sync_res = adapter.sync_local(context)
            results[pid] = sync_res
            if sync_res.get("state") == "SYNC_FAILED_ROLLED_BACK":
                partial_failure = True
        except Exception as exc:  # noqa: BLE001 — isolated per-platform rollback barrier
            results[pid] = {
                "platform": pid,
                "state": "SYNC_FAILED_ROLLED_BACK",
                "installed_digest": None,
                "built_digest": None,
                "actions": [f"Sync error isolated and rolled back: {exc}"],
            }
            partial_failure = True

    return {"partial_failure": partial_failure, "platforms": results}
