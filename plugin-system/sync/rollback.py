"""Per-platform N-version snapshot retention and isolated transactional rollback."""

from __future__ import annotations

import json
import shutil
import time
from pathlib import Path
from typing import Any

from ..core.models import ConfigError


def snapshot_known_good(
    repo_root: Path,
    platform_id: str,
    version: str,
    bundle_dir: Path,
    *,
    retention: int = 3,
    rollback_rel: str = ".plugin-local/rollback",
) -> Path | None:
    """Save an atomic known-good snapshot for `platform_id` keeping at most `retention` versions."""
    if not bundle_dir.is_dir():
        return None
    snap_base = (Path(repo_root) / rollback_rel / platform_id).resolve()
    snap_base.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    snap_dir = snap_base / f"{version}__{stamp}"
    suffix = 0
    while snap_dir.exists():
        suffix += 1
        snap_dir = snap_base / f"{version}__{stamp}_{suffix}"
    shutil.copytree(bundle_dir, snap_dir)
    meta = {"version": version, "platform": platform_id, "created_utc": stamp}
    (snap_dir / ".snapshot-meta.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

    # Prune oldest snapshots beyond retention
    snapshots = sorted([p for p in snap_base.iterdir() if p.is_dir()], key=lambda p: p.stat().st_mtime, reverse=True)
    for old in snapshots[retention:]:
        shutil.rmtree(old, ignore_errors=True)
    return snap_dir


def list_snapshots(repo_root: Path, platform_id: str, rollback_rel: str = ".plugin-local/rollback") -> list[dict[str, Any]]:
    snap_base = Path(repo_root) / rollback_rel / platform_id
    if not snap_base.is_dir():
        return []
    items = []
    for p in sorted([d for d in snap_base.iterdir() if d.is_dir()], key=lambda d: d.stat().st_mtime, reverse=True):
        meta_file = p / ".snapshot-meta.json"
        version = p.name.split("__", 1)[0]
        if meta_file.is_file():
            try:
                version = json.loads(meta_file.read_text(encoding="utf-8")).get("version", version)
            except (OSError, json.JSONDecodeError):
                pass
        items.append({"version": version, "path": p})
    return items


def restore_snapshot(
    repo_root: Path,
    platform_id: str,
    target_version: str | None,
    destination_dir: Path,
    *,
    rollback_rel: str = ".plugin-local/rollback",
) -> dict[str, Any]:
    """Restore the matching (or latest) known-good snapshot into `destination_dir`."""
    snaps = list_snapshots(repo_root, platform_id, rollback_rel=rollback_rel)
    if not snaps:
        raise ConfigError(f"No rollback snapshots available for platform {platform_id!r}.")
    chosen = None
    if target_version:
        for item in snaps:
            if item["version"] == target_version:
                chosen = item
                break
        if chosen is None:
            raise ConfigError(f"Rollback snapshot for {platform_id!r} version {target_version!r} not found.")
    else:
        chosen = snaps[0]

    tmp_restore = destination_dir.parent / f".{destination_dir.name}.rollback-tmp"
    if tmp_restore.exists():
        shutil.rmtree(tmp_restore)
    shutil.copytree(chosen["path"], tmp_restore)
    (tmp_restore / ".snapshot-meta.json").unlink(missing_ok=True)
    if destination_dir.exists():
        shutil.rmtree(destination_dir)
    destination_dir.parent.mkdir(parents=True, exist_ok=True)
    tmp_restore.rename(destination_dir)
    return {
        "platform": platform_id,
        "state": "ROLLED_BACK",
        "restored_version": chosen["version"],
        "restored_from": str(chosen["path"]),
    }
