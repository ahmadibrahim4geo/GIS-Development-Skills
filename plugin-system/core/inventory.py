"""Canonical inventory collection with strict allowlist, symlink, and traversal guards."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

from .models import SecretLeakError, ValidationFailedError


def is_sensitive_filename(rel_path: Path, source_map: dict[str, Any]) -> bool:
    name = rel_path.name.casefold()
    sensitive_names = {s.casefold() for s in source_map.get("sensitive_filenames", [])}
    sensitive_suffixes = {s.casefold() for s in source_map.get("sensitive_suffixes", [])}
    return (
        name == ".env"
        or name.startswith(".env.")
        and name != ".env.example"
        or name in sensitive_names
        or rel_path.suffix.casefold() in sensitive_suffixes
    )


def _assert_safe_relative(path: Path, root: Path) -> Path:
    if path.is_symlink():
        raise ValidationFailedError(f"Refusing symlink in canonical repository: {path}")
    resolved_root = root.resolve()
    try:
        resolved = path.resolve()
        rel = resolved.relative_to(resolved_root)
    except (OSError, ValueError) as exc:
        raise ValidationFailedError(f"Path escapes repository root: {path}") from exc
    if ".." in rel.parts:
        raise ValidationFailedError(f"Unsafe traversal segment in path: {rel.as_posix()}")
    return rel


def _is_excluded(rel_path: Path, source_map: dict[str, Any]) -> bool:
    excluded_dirs = set(source_map.get("excluded_directories", []))
    developer_files = set(source_map.get("developer_only_files", []))
    if any(part in excluded_dirs for part in rel_path.parts[:-1]):
        return True
    if rel_path.as_posix() in developer_files:
        return True
    if rel_path.suffix.casefold() in {".pyc", ".pyo", ".tmp"}:
        return True
    if rel_path.name.casefold() in {"thumbs.db", ".ds_store"}:
        return True
    return False


def collect_canonical_inventory(repo_root: Path, source_map: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Collect canonical bundle files plus governance/template digest inputs.

    Walks the filesystem directly rather than relying solely on `git diff`,
    so untracked additions, deletions, renames, and Arabic/spaced filenames are
    captured deterministically while rejecting symlinks and sensitive files.
    """
    root = Path(repo_root).resolve()
    bundle_files: dict[str, dict[str, Any]] = {}
    governance_files: dict[str, dict[str, Any]] = {}

    for name in source_map.get("canonical_bundle_files", []):
        candidate = root / name
        if candidate.is_symlink():
            raise ValidationFailedError(f"Refusing symlink root file: {name}")
        if not candidate.is_file():
            continue
        rel = _assert_safe_relative(candidate, root)
        if is_sensitive_filename(rel, source_map):
            raise SecretLeakError(f"Sensitive file forbidden in canonical bundle root: {rel.as_posix()}")
        bundle_files[rel.as_posix()] = {
            "path": rel.as_posix(),
            "abs_path": candidate,
            "size": candidate.stat().st_size,
            "scope": "bundle",
        }

    for dir_name in source_map.get("canonical_bundle_directories", []):
        base_dir = root / dir_name
        if base_dir.is_symlink():
            raise ValidationFailedError(f"Refusing symlink directory: {dir_name}")
        if not base_dir.is_dir():
            continue
        for current_root, dir_names, file_names in os.walk(base_dir, followlinks=False):
            current_path = Path(current_root)
            rel_dir = current_path.relative_to(root)
            excluded_dirs = set(source_map.get("excluded_directories", []))
            kept_dirs = []
            for d in sorted(dir_names):
                sub = current_path / d
                if sub.is_symlink():
                    # Check if an allowed bundle directory contains a symlink escaping root.
                    raise ValidationFailedError(f"Refusing symlink directory inside canonical tree: {(rel_dir / d).as_posix()}")
                if d not in excluded_dirs:
                    kept_dirs.append(d)
            dir_names[:] = kept_dirs

            for fname in sorted(file_names):
                fpath = current_path / fname
                rel = _assert_safe_relative(fpath, root)
                if _is_excluded(rel, source_map):
                    continue
                if is_sensitive_filename(rel, source_map):
                    raise SecretLeakError(f"Sensitive file forbidden inside bundle directory: {rel.as_posix()}")
                bundle_files[rel.as_posix()] = {
                    "path": rel.as_posix(),
                    "abs_path": fpath,
                    "size": fpath.stat().st_size,
                    "scope": "bundle",
                }

    for rel_str in source_map.get("additional_digest_inputs", []):
        candidate = root / rel_str
        if candidate.is_symlink():
            raise ValidationFailedError(f"Refusing symlink governance input: {rel_str}")
        if not candidate.is_file():
            continue
        rel = _assert_safe_relative(candidate, root)
        if is_sensitive_filename(rel, source_map):
            raise SecretLeakError(f"Sensitive file forbidden in digest inputs: {rel.as_posix()}")
        if rel.as_posix() not in bundle_files:
            governance_files[rel.as_posix()] = {
                "path": rel.as_posix(),
                "abs_path": candidate,
                "size": candidate.stat().st_size,
                "scope": "governance",
            }

    return {
        "bundle_files": sorted(bundle_files.values(), key=lambda x: x["path"].casefold()),
        "governance_files": sorted(governance_files.values(), key=lambda x: x["path"].casefold()),
    }
