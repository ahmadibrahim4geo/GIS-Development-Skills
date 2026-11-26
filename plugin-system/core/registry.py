"""Config-driven dynamic adapter loader (zero engine if/else hardcoding)."""

from __future__ import annotations

import importlib
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

from .models import ConfigError, PlatformConfig


def load_platforms_registry(repo_root: Path, registry_path: Path | None = None) -> dict[str, Any]:
    path = Path(registry_path) if registry_path else Path(repo_root) / "plugin-system" / "config" / "platforms.json"
    if not path.is_file():
        raise ConfigError(f"Missing platform registry: {path}")
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"Invalid platform registry JSON: {exc}") from exc
    if not isinstance(data.get("platforms"), list) or not data["platforms"]:
        raise ConfigError("Platform registry must declare at least one platform.")
    return data


def list_platform_configs(repo_root: Path, registry_data: dict[str, Any]) -> list[PlatformConfig]:
    configs: list[PlatformConfig] = []
    seen: set[str] = set()
    for raw in registry_data["platforms"]:
        pid = raw.get("id")
        if not isinstance(pid, str) or not pid or pid in seen:
            raise ConfigError(f"Invalid or duplicate platform id in platforms.json: {pid!r}")
        seen.add(pid)
        configs.append(
            PlatformConfig(
                id=pid,
                display_name=str(raw.get("display_name", pid)),
                enabled=bool(raw.get("enabled", True)),
                phase_target=str(raw.get("phase_target", "P09")),
                phase_status=str(raw.get("phase_status", "P09_STUB")),
                adapter=str(raw["adapter"]),
                output_dir=str(raw["output_dir"]),
                bundle_dir=str(raw.get("bundle_dir", "")),
                manifest_path=str(raw.get("manifest_path", "")),
                artifacts_dir=str(raw.get("artifacts_dir", "")),
                parity_report_path=str(raw.get("parity_report_path", "")),
                archive_name=str(raw.get("archive_name", "")),
                raw=dict(raw),
            )
        )
    return configs


def load_adapter(repo_root: Path, platform_cfg: PlatformConfig):
    """Dynamically resolve and instantiate `module_path.py:ClassName` from platforms.json."""
    spec_str = platform_cfg.adapter
    if ":" not in spec_str:
        raise ConfigError(f"Platform {platform_cfg.id} adapter spec must be 'rel/path.py:ClassName', got {spec_str!r}")
    rel_module, class_name = spec_str.split(":", 1)
    module_path = (Path(repo_root) / rel_module).resolve()
    if not module_path.is_file():
        raise ConfigError(f"Adapter module not found for {platform_cfg.id}: {rel_module}")
    if not module_path.is_relative_to(Path(repo_root).resolve()):
        raise ConfigError(f"Adapter module escapes repository root: {rel_module}")

    rel_posix = module_path.relative_to(Path(repo_root).resolve()).as_posix()
    if rel_posix.startswith("plugin-system/") and rel_posix.endswith(".py") and "plugin_system" in sys.modules:
        dotted = "plugin_system." + rel_posix[len("plugin-system/"):-3].replace("/", ".")
        module = importlib.import_module(dotted)
    else:
        mod_name = f"plugin_adapter_{platform_cfg.id.replace('-', '_')}_{abs(hash(str(module_path)))}"
        spec = importlib.util.spec_from_file_location(mod_name, module_path)
        if spec is None or spec.loader is None:
            raise ConfigError(f"Cannot load adapter module {rel_module}")
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
    adapter_cls = getattr(module, class_name, None)
    if adapter_cls is None:
        raise ConfigError(f"Adapter class {class_name!r} missing in {rel_module}")
    instance = adapter_cls(platform_cfg)
    required_methods = (
        "detect",
        "capabilities",
        "build",
        "validate",
        "package",
        "status",
        "sync_local",
        "prepare_release",
        "update_owner_remote",
        "verify",
        "rollback",
    )
    missing = [m for m in required_methods if not callable(getattr(instance, m, None))]
    if missing:
        raise ConfigError(f"Adapter {platform_cfg.id} missing contract methods: {missing}")
    return instance
