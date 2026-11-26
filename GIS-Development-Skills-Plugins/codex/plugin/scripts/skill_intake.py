"""Review candidate snapshots as inert data inside the existing quarantine."""

from contextlib import contextmanager
import hashlib
from io import BytesIO
from pathlib import PurePosixPath
import re
from urllib.parse import urlsplit
from zipfile import BadZipFile, ZIP_DEFLATED, ZIP_STORED, ZipFile
import zlib

if __package__:
    from .project_structure import safe_path
    from .security_audit import PATTERNS
    from .security_guardian import inspect_archive
else:
    from project_structure import safe_path
    from security_audit import PATTERNS
    from security_guardian import inspect_archive


VERSION = "1.0"
MAX_SNAPSHOT_BYTES = 4 * 1024 * 1024
MAX_MEMBER_BYTES = 64 * 1024
MAX_FINDINGS = 64
EFFECTS = ("read", "write", "desktop-input", "network", "execute")
FULL_REVISION = re.compile(r"(?i)(?:[a-f0-9]{40}|[a-f0-9]{64})\Z")
MARKDOWN_NAME = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*\Z")
EXECUTABLE_SUFFIXES = {".bat", ".cmd", ".dll", ".exe", ".jar", ".js", ".mjs", ".msi", ".ps1",
                       ".py", ".pyc", ".sh", ".so", ".vbs", ".wasm"}
DEPENDENCY_FILES = {"package.json", "pyproject.toml", "requirements.txt", "uv.lock",
                    "package-lock.json", "pipfile", "cargo.toml"}
SECRETS = {".env", "credentials.json", "secrets.json", "id_rsa", "id_ed25519"}
TEXT_SUFFIXES = {".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".lock"}
MS_DEVICE = re.compile(r"(?i)(?:CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(?:\.|$)")


def public_https(value):
    if not isinstance(value, str):
        return False
    try:
        parts = urlsplit(value)
        return bool(parts.scheme == "https" and parts.hostname and not (
            parts.username or parts.password or parts.query or parts.fragment
            or "\\" in value or "." not in parts.hostname
            or any(ord(char) < 33 or ord(char) == 127 for char in value)))
    except ValueError:
        return False


@contextmanager
def registry_lock(root):
    base = safe_path(root, "New Skill")
    base.mkdir(exist_ok=True)
    lock = safe_path(root, "New Skill/.intake.lock")
    lock.mkdir()
    try:
        yield
    finally:
        lock.rmdir()


def skill_header(text, file_path):
    lines = text.splitlines()
    if not lines or lines[0] != "---":
        return False
    try:
        close = lines.index("---", 1)
    except ValueError:
        return False
    names = [line.split(":", 1)[1].strip().strip('\'"') for line in lines[1:close] if line.startswith("name:")]
    descriptions = [line.split(":", 1)[1].strip() for line in lines[1:close] if line.startswith("description:")]
    return (len(names) == len(descriptions) == 1 and bool(MARKDOWN_NAME.fullmatch(names[0]))
            and 0 < len(descriptions[0]) <= 1024
            and (not file_path.parent.name or file_path.parent.name == names[0]))


def suspicious_member(name):
    parts = PurePosixPath(name).parts
    return any(part.endswith((" ", ".")) or MS_DEVICE.match(part) or
               re.search(r'[:*?"<>|\x00-\x1f]', part) for part in parts)


def inspect_members(blob):
    findings, skills, licenses, names = [], [], [], set()
    truncated = False

    def record(code, severity, member, line=0):
        nonlocal truncated
        if len(findings) >= MAX_FINDINGS:
            truncated = True
        else:
            findings.append({"code": code, "severity": severity, "member": member, "line": line})

    with ZipFile(BytesIO(blob)) as archive:
        for entry in archive.infolist():
            name = entry.orig_filename.rstrip("/")
            if name.casefold() in names or suspicious_member(name):
                record("ambiguous-windows-member", "high", "<archive>")
                continue
            names.add(name.casefold())
            path = PurePosixPath(name)
            parts = tuple(part.lower() for part in path.parts)
            basename = path.name.lower()
            if entry.is_dir():
                continue
            if entry.compress_type not in (ZIP_STORED, ZIP_DEFLATED):
                record("unsupported-compression", "high", name)
                continue
            if path.suffix.lower() in EXECUTABLE_SUFFIXES or "hooks" in parts or basename == "autorun.inf":
                record("executable-or-hook", "high", name)
                continue
            if basename in SECRETS or basename.startswith(".env."):
                record("private-file-name", "high", name)
                continue
            if basename in DEPENDENCY_FILES:
                record("dependency-manifest", "medium", name)
            if basename in {"agents.md", "claude.md", "gemini.md"}:
                record("additional-agent-entrypoint", "medium", name)
            if path.suffix.lower() not in TEXT_SUFFIXES and basename not in {"license", "copying", "notice"}:
                record("unreviewed-member-type", "medium", name)
                continue
            try:
                with archive.open(entry) as handle:
                    content = handle.read(MAX_MEMBER_BYTES + 1)
                if len(content) > MAX_MEMBER_BYTES or b"\x00" in content:
                    raise ValueError("unexpected binary or oversized member")
                text = content.decode("utf-8-sig")
            except (BadZipFile, ValueError, RuntimeError, NotImplementedError, EOFError, zlib.error):
                record("unreadable-member", "high", name)
                continue
            if basename == "skill.md":
                skills.append(name)
                if not skill_header(text, path):
                    record("invalid-skill-frontmatter", "high", name)
            if basename in {"license", "license.md", "license.txt", "copying"} and text.strip():
                licenses.append(name)
            for line_number, line in enumerate(text.splitlines(), 1):
                for code, severity, pattern in PATTERNS:
                    if pattern.search(line):
                        record(code, severity, name, line_number)
    if len(skills) != 1:
        record("expected-one-skill-entrypoint", "high", "<archive>")
    if not licenses:
        record("missing-license-document", "medium", "<archive>")
    if truncated:
        findings.append({"code": "finding-budget-exceeded", "severity": "high",
                         "member": "<archive>", "line": 0})
    return findings


def inspect_snapshot(snapshot, expected_sha256, candidate):
    if snapshot.suffix.lower() != ".zip" or not re.fullmatch(r"[0-9a-f]{64}", expected_sha256):
        raise ValueError("Supply a ZIP and its lowercase expected SHA-256")
    if not snapshot.is_file() or snapshot.stat().st_size > MAX_SNAPSHOT_BYTES:
        raise ValueError("Snapshot must be an existing ZIP no larger than 4 MiB")
    with snapshot.open("rb") as handle:
        blob = handle.read(MAX_SNAPSHOT_BYTES + 1)
    digest = hashlib.sha256(blob).hexdigest()
    if len(blob) > MAX_SNAPSHOT_BYTES or digest != expected_sha256:
        raise ValueError("Snapshot differs from its expected SHA-256 or exceeds the size limit")

    scan = inspect_archive(snapshot, max_files=64, max_bytes=2 * 1024 * 1024,
                           max_member_bytes=MAX_MEMBER_BYTES, payload=blob)
    findings = [{"code": code, "severity": "high", "member": "<archive>", "line": 0}
                for code in scan["issues"]]
    if not findings:
        findings.extend(inspect_members(blob))
    metadata_gaps = []
    revision = candidate.get("revision")
    if not isinstance(revision, str) or not FULL_REVISION.fullmatch(revision):
        metadata_gaps.append("immutable-revision-missing")
    if candidate.get("license") in (None, "", "UNVERIFIED") or not public_https(candidate.get("license_evidence") or ""):
        metadata_gaps.append("license-evidence-missing")
    if candidate.get("declared_effects") != ["read"] or candidate.get("dependencies"):
        metadata_gaps.append("effects-or-dependencies-need-review")
    rejected = any(item["severity"] == "high" or item["code"] == "agent-instruction-override" for item in findings)
    decision = "REJECTED_ISOLATED" if rejected else "REVIEW_REQUIRED" if findings or metadata_gaps else "READY_FOR_MANUAL_REVIEW"
    return {"id": candidate["id"], "scanner": "stdlib-quarantine", "scanner_version": VERSION,
            "scope": "ZIP metadata and bounded UTF-8 text inspection with the repository rules",
            "snapshot_sha256": digest, "source": candidate["source"], "revision": revision,
            "license_evidence": candidate.get("license_evidence"), "metadata_gaps": metadata_gaps,
            "findings": findings, "archive": scan, "status": decision, "active": False,
            "candidate_execution": "NOT RUN", "external_scanners": "NOT RUN"}
