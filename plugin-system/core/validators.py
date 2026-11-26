"""Offline canonical repository, license, UTF-8, and secret-leak validators."""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any

from .models import ConfigError, REDISTRIBUTION_ALLOWED_SPDX, SecretLeakError, ValidationFailedError

SEMVER_RE = re.compile(r"^[0-9]+\.[0-9]+\.[0-9]+(?:[-+][A-Za-z0-9.-]+)?$")

# High-confidence secret signatures; values are NEVER echoed in findings or logs.
SECRET_PATTERNS = (
    ("private-key-block", re.compile(r"-----BEGIN (?:RSA |EC |DSA |OPENSSH |PGP )?PRIVATE KEY-----")),
    ("github-pat-classic", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{20,}\b")),
    ("github-pat-fine", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{20,}\b")),
    ("aws-access-key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("openai-key", re.compile(r"\bsk-[A-Za-z0-9]{24,}\b")),
    ("google-api-key", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
)


def _load_script_module(repo_root: Path, script_name: str):
    scripts_dir = (Path(repo_root) / "scripts").resolve()
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))
    path = scripts_dir / f"{script_name}.py"
    spec = importlib.util.spec_from_file_location(f"repo_script_{script_name}", path)
    if spec is None or spec.loader is None:
        raise ConfigError(f"Unable to load helper script: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_semver_version(repo_root: Path) -> str:
    version_file = Path(repo_root) / "VERSION"
    if not version_file.is_file():
        raise ConfigError("Root VERSION file is missing.")
    value = version_file.read_text(encoding="utf-8").strip()
    if not SEMVER_RE.fullmatch(value):
        raise ConfigError(f"Root VERSION must be valid SemVer; found {value!r}")
    return value


def scan_files_for_secrets(files: list[dict[str, Any]], repo_root: Path) -> None:
    """Inspect candidate bundle/report files for raw secret patterns without echoing secret values."""
    for entry in files:
        path = Path(entry["abs_path"])
        try:
            raw = path.read_bytes()
        except OSError as exc:
            raise ValidationFailedError(f"Cannot read {entry['path']}: {exc}") from exc
        if b"\x00" in raw:
            continue
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValidationFailedError(f"File is not valid UTF-8: {entry['path']}") from exc
        for rule_id, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                # Security requirement (REQ-PL-037): report rule & file only, never the matched value.
                raise SecretLeakError(f"Secret leak detected ({rule_id}) in {entry['path']}; value redacted.")


def validate_license_redistribution(repo_root: Path, bundled_project_urls: set[str] | None = None) -> dict[str, Any]:
    """Validate license metadata integrity and enforce link-only policy for restricted sources."""
    catalog_path = Path(repo_root) / "references" / "project-catalog.json"
    if not catalog_path.is_file():
        raise ValidationFailedError("Missing references/project-catalog.json")
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    projects = data.get("projects", [])
    audit_license = _load_script_module(repo_root, "audit_license_catalog")
    problems = audit_license.scan(projects)
    if problems:
        raise ValidationFailedError("; ".join(problems))

    summary = audit_license.classify(projects)
    blocked: list[str] = []
    if bundled_project_urls:
        by_url = {p.get("url", "").casefold(): p for p in projects}
        for url in sorted(bundled_project_urls):
            rec = by_url.get(url.casefold())
            if rec is None:
                blocked.append(f"{url} (not registered in project-catalog.json)")
                continue
            spdx = str(rec.get("license", "")).strip().upper()
            if rec.get("license_verified") is not True or spdx not in REDISTRIBUTION_ALLOWED_SPDX:
                blocked.append(f"{rec.get('name', url)} (license={rec.get('license')}, verified={rec.get('license_verified')})")
    if blocked:
        raise ValidationFailedError(
            "Redistribution blocked for unlicensed/non-permissive third-party code (keep link-only): "
            + ", ".join(blocked)
        )
    return summary


def validate_canonical_repository(repo_root: Path) -> dict[str, Any]:
    """Run existing skill pack, security audit, and catalog validators cleanly."""
    root = Path(repo_root).resolve()
    skill_validator = _load_script_module(root, "validate_skill_pack")
    skill_errors = skill_validator.inspect_repository(root)
    if skill_errors:
        raise ValidationFailedError("Skill pack validation failed: " + "; ".join(skill_errors[:5]))

    security_mod = _load_script_module(root, "security_audit")
    sec_report = security_mod.audit(root)
    if sec_report.get("blocking_findings", 0) > 0:
        raise ValidationFailedError(f"Security Guardian blocked build ({sec_report['blocking_findings']} blocking findings)")

    license_summary = validate_license_redistribution(root)
    return {
        "skill_errors": 0,
        "security_status": sec_report.get("status", "pass"),
        "license_summary": license_summary,
    }
