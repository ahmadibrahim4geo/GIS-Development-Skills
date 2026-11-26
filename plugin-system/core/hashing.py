"""Deterministic SHA-256 content and path digest computation."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fingerprint_records(records: list[dict[str, Any]]) -> str:
    """Compute a timestamp-free digest across sorted file records."""
    normalized = [
        {"path": rec["path"], "size": int(rec["size"]), "sha256": rec["sha256"]}
        for rec in sorted(records, key=lambda item: item["path"])
    ]
    payload = json.dumps(normalized, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return sha256_bytes(payload.encode("utf-8"))


def compute_digests(inventory_data: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    """Return both end-user bundle digest and full source+governance digest."""
    bundle_entries = []
    for item in inventory_data["bundle_files"]:
        bundle_entries.append(
            {
                "path": item["path"],
                "size": item["size"],
                "sha256": sha256_file(item["abs_path"]),
            }
        )
    governance_entries = []
    for item in inventory_data["governance_files"]:
        governance_entries.append(
            {
                "path": item["path"],
                "size": item["size"],
                "sha256": sha256_file(item["abs_path"]),
            }
        )
    all_entries = bundle_entries + governance_entries
    return {
        "bundle_digest": fingerprint_records(bundle_entries),
        "source_digest": fingerprint_records(all_entries),
        "bundle_file_count": len(bundle_entries),
        "governance_file_count": len(governance_entries),
        "bundle_entries": bundle_entries,
        "governance_entries": governance_entries,
    }


def resolve_git_commit(repo_root: Path) -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo_root,
            capture_output=True,
            text=True,
            timeout=10,
            check=False,
        )
        sha = proc.stdout.strip()
        if proc.returncode == 0 and re.fullmatch(r"[0-9a-fA-F]{40}", sha):
            return sha
    except (OSError, subprocess.SubprocessError):
        pass
    return "unknown"
