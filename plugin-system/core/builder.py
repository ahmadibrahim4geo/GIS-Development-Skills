"""Clean-staging atomic swap builder & integrity verifier integrating build_skill_bundle.py."""

from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
from typing import Any

from .hashing import fingerprint_records, sha256_file
from .models import AdapterContext, LifecycleError, ValidationFailedError


def _atomic_replace_directory(staged_dir: Path, target_dir: Path) -> None:
    """Replace target_dir from staged_dir cleanly without leaving stale deletions."""
    target_dir = target_dir.resolve()
    target_dir.parent.mkdir(parents=True, exist_ok=True)
    backup_dir = target_dir.parent / f".{target_dir.name}.swap-backup"
    if backup_dir.exists():
        shutil.rmtree(backup_dir)
    had_existing = target_dir.exists()
    if had_existing:
        target_dir.rename(backup_dir)
    try:
        shutil.copytree(staged_dir, target_dir)
    except Exception:
        if target_dir.exists():
            shutil.rmtree(target_dir)
        if had_existing and backup_dir.exists():
            backup_dir.rename(target_dir)
        raise
    if backup_dir.exists():
        shutil.rmtree(backup_dir, ignore_errors=True)


def inspect_built_output(cfg_bundle_dir: Path, cfg_manifest_path: Path, expected_source_digest: str) -> str:
    """Check whether an unpacked output exists, matches source digest, and has untampered manifest."""
    if not cfg_bundle_dir.is_dir() or not cfg_manifest_path.is_file():
        return "OUTDATED"
    try:
        manifest = json.loads(cfg_manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return "VALIDATION_FAILED"
    if manifest.get("source_digest") != expected_source_digest:
        return "OUTDATED"
    bundle_manifest = cfg_bundle_dir / "bundle-manifest.json"
    if bundle_manifest.is_file():
        try:
            bm = json.loads(bundle_manifest.read_text(encoding="utf-8"))
            files = bm.get("files", [])
            actual_files = {
                p.relative_to(cfg_bundle_dir).as_posix(): p
                for p in cfg_bundle_dir.rglob("*")
                if p.is_file() and p.name != "bundle-manifest.json"
            }
            expected_map = {item["path"]: item for item in files}
            if set(actual_files) != set(expected_map):
                return "VALIDATION_FAILED"
            for rel, fpath in actual_files.items():
                if fpath.stat().st_size != expected_map[rel].get("size") or sha256_file(fpath) != expected_map[rel].get("sha256"):
                    return "VALIDATION_FAILED"
            if bm.get("content_sha256") != fingerprint_records(files):
                return "VALIDATION_FAILED"
        except (OSError, json.JSONDecodeError, KeyError, TypeError):
            return "VALIDATION_FAILED"
    return "UP_TO_DATE"


def build_platform_transactionally(adapter, context: AdapterContext, *, check_only: bool = False) -> dict[str, Any]:
    """Execute clean staging build -> validate -> package -> atomic swap for one adapter."""
    cfg = adapter.config
    status_info = adapter.status(context)
    if not (cfg.phase_status.startswith("ACTIVE_") or cfg.raw.get("build_in_p02", False)):
        # P09 adapters write only lightweight honest scaffold files if absent; never fake client builds.
        out_dir = context.repo_root / cfg.output_dir
        staged_root = context.repo_root / ".plugin-staging"
        staged_root.mkdir(parents=True, exist_ok=True)
        if not check_only:
            with tempfile.TemporaryDirectory(prefix=f"stage-{cfg.id}-", dir=staged_root) as tmp:
                tmp_path = Path(tmp)
                build_res = adapter.build(context, tmp_path)
                adapter.validate(context, Path(build_res["staged_output_dir"]))
                _atomic_replace_directory(Path(build_res["staged_output_dir"]), out_dir)
                parity = build_res.get("parity_report")
                if parity and cfg.parity_report_path:
                    from .parity import write_parity_files

                    write_parity_files(parity, context.repo_root / cfg.parity_report_path)
        return {
            "platform": cfg.id,
            "state": "NOT_RUN",
            "phase_status": cfg.phase_status,
            "bundle_sha256": None,
            "archive_sha256": None,
            "notes": f"Scaffold ready; full {cfg.display_name} adapter scheduled in {cfg.phase_target}.",
        }

    current_state = status_info.get("state", "OUTDATED")
    if current_state == "UP_TO_DATE" and not context.force:
        return {
            "platform": cfg.id,
            "state": "UP_TO_DATE",
            "phase_status": cfg.phase_status,
            "bundle_sha256": status_info.get("bundle_sha256"),
            "archive_sha256": status_info.get("archive_sha256"),
            "notes": "Source digest and built manifest match; skipped rebuild.",
        }

    if check_only:
        return {
            "platform": cfg.id,
            "state": current_state,
            "phase_status": cfg.phase_status,
            "bundle_sha256": status_info.get("bundle_sha256"),
            "archive_sha256": status_info.get("archive_sha256"),
            "notes": f"CheckOnly detected {current_state}; rebuild required.",
        }

    staging_parent = context.repo_root / ".plugin-staging"
    staging_parent.mkdir(parents=True, exist_ok=True)
    bundle_target = context.repo_root / cfg.bundle_dir
    artifacts_target = context.repo_root / cfg.artifacts_dir if cfg.artifacts_dir else None

    with tempfile.TemporaryDirectory(prefix=f"build-{cfg.id}-", dir=staging_parent) as tmp:
        stage_dir = Path(tmp)
        build_res = adapter.build(context, stage_dir)
        staged_bundle = Path(build_res["staged_bundle_dir"])
        val_res = adapter.validate(context, staged_bundle)
        staged_artifacts = stage_dir / "artifacts"
        staged_artifacts.mkdir(parents=True, exist_ok=True)
        pkg_res = adapter.package(context, staged_bundle, staged_artifacts)

        # Atomic directory swap eliminates stale/deleted/renamed files cleanly.
        _atomic_replace_directory(staged_bundle, bundle_target)
        if artifacts_target is not None:
            _atomic_replace_directory(staged_artifacts, artifacts_target)
        parity = build_res.get("parity_report")
        if parity and cfg.parity_report_path:
            from .parity import write_parity_files

            write_parity_files(parity, context.repo_root / cfg.parity_report_path)

    return {
        "platform": cfg.id,
        "state": "BUILT",
        "phase_status": cfg.phase_status,
        "bundle_sha256": val_res.get("content_sha256"),
        "archive_sha256": pkg_res.get("archive_sha256"),
        "archive_path": str((artifacts_target / pkg_res["archive_name"]).relative_to(context.repo_root).as_posix())
        if artifacts_target and pkg_res.get("archive_name")
        else None,
        "file_count": val_res.get("file_count"),
        "notes": "Cleanly staged, validated, packaged, and atomically updated.",
    }
