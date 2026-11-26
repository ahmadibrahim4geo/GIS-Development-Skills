#!/usr/bin/env python3
"""Check and run the two local web guidance providers with scoped commands."""

import argparse
import base64
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

if __package__:
    from .project_structure import is_link, safe_path
else:
    from project_structure import is_link, safe_path


VERSION = "1.0.1"
SKILL_VERSION = "2026_11_10-47b4c80e"
ARCHIVE_NAME = f"modern-web-guidance-{VERSION}.tgz"
ARCHIVE_BYTES = 8_878_299
ARCHIVE_SHA512 = "5ztUh5F1p2PewnSkA6EhsGUXqomaZY9qe6iWJCU4JbIQxHTky7s5lMJcPE4EbD1uhbQZIhl0HROH0+s6fIiGzg=="
MODERN_ENTRY = Path("package/skills/modern-web-guidance/modern-web.mjs")
UI_FILES = (
    "SKILL.md", "scripts/search.py", "scripts/core.py", "scripts/design_system.py",
    "scripts/reasoning_contract.py", "data/catalog-summary.json", "data/products.csv",
    "data/ux-guidelines.csv", "data/ui-reasoning.csv", "data/styles.csv",
    "data/colors.csv", "data/typography.csv", "data/landing.csv", "data/charts.csv",
    "references/quick-reference.md", "references/pro-rules.md",
)
GUIDE_IDS = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*(?:,[a-z0-9]+(?:-[a-z0-9]+)*)*\Z")


class GuidanceError(ValueError):
    """A required provider or result could not be verified."""


def verified_archive(path):
    # Hash the bytes subsequently opened by tarfile rather than reopening the path.
    with path.open("rb") as archive:
        content = archive.read(ARCHIVE_BYTES + 1)
    digest = base64.b64encode(hashlib.sha512(content).digest()).decode("ascii")
    if len(content) != ARCHIVE_BYTES or digest != ARCHIVE_SHA512:
        raise GuidanceError(f"{ARCHIVE_NAME} does not match the reviewed npm artifact.")
    return content


def uiux_directory(project, explicit):
    if explicit is not None:
        return explicit.absolute()
    roots = (
        project / ".agents/skills", project / ".claude/skills",
        Path.home() / ".agents/skills", Path.home() / ".codex/skills",
        Path.home() / ".claude/skills",
    )
    return next((root / "ui-ux-pro-max" for root in roots
                 if (root / "ui-ux-pro-max/SKILL.md").is_file()), None)


def prerequisites(project, package, uiux):
    problems = []
    content = None
    if not package.is_file():
        problems.append(f"Modern Web Guidance archive: {package}")
    else:
        try:
            content = verified_archive(package)
        except (GuidanceError, OSError) as exc:
            problems.append(str(exc))
    uiux = uiux_directory(project, uiux)
    if uiux is None:
        problems.append("UI/UX Pro Max skill directory (or supply --ui-ux-dir).")
    elif any(part.casefold() == "new skill" for part in uiux.parts):
        problems.append("UI/UX Pro Max must use an approved installation outside the candidate quarantine.")
    else:
        if any(is_link(path) for path in (*uiux.parents, uiux)):
            problems.append("UI/UX Pro Max requires an inspectable directory without links.")
        else:
            for relative in UI_FILES:
                path = safe_path(uiux, relative)
                if not path.is_file() or path.stat().st_size == 0:
                    problems.append(f"UI/UX Pro Max file: {relative}")
    node = shutil.which("node")
    if node is None:
        problems.append("Node.js 22 or newer.")
    if problems:
        raise GuidanceError("\n".join(problems))
    version = run([node, "--version"], project).strip()
    match = re.fullmatch(r"v(\d+)\.\d+\.\d+(?:[-+].*)?", version)
    if not match or int(match[1]) < 22:
        raise GuidanceError(f"Modern Web Guidance requires Node.js 22 or newer. Found {version}.")
    return content, uiux, node, version


def run(command, project):
    env = os.environ.copy()
    for key in ("NODE_OPTIONS", "NODE_PATH"):
        env.pop(key, None)
    env.update(DISABLE_TELEMETRY="1", ENABLE_FILE_LOGGING="false")
    # The upstream CLI streams long guides when stdout is a file. This keeps the
    # full output available without relying on an unmanaged temporary guide path.
    with tempfile.TemporaryFile() as output:
        result = subprocess.run(command, cwd=project, env=env, stdout=output,
                                stderr=subprocess.PIPE, timeout=30, check=False)
        output.seek(0)
        text = output.read().decode("utf-8")
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip() or text.strip()
        raise GuidanceError(detail or f"Provider returned exit code {result.returncode}.")
    return text


def modern(node, entry, operation, value, project):
    return run([node, str(entry), operation, value, "--skill-version", SKILL_VERSION], project)


def design(uiux, operation, query, project):
    options = ["--design-system"] if operation == "design" else ["--domain", "ux"]
    return run([sys.executable, "-I", "-B", str(uiux / "scripts/search.py"),
                query, *options, "--json"], project)


def verify_providers(node, entry, uiux, project, version):
    matches = json.loads(modern(node, entry, "search", "confirmation modal dialog", project))
    if not isinstance(matches, list) or not matches or not isinstance(matches[0], dict):
        raise GuidanceError("Modern Web Guidance search did not return a usable guide ID.")
    guide_id = matches[0].get("id")
    if not isinstance(guide_id, str) or not GUIDE_IDS.fullmatch(guide_id):
        raise GuidanceError("Modern Web Guidance search did not return a usable guide ID.")
    guide = modern(node, entry, "retrieve", guide_id, project)
    if not guide.lstrip().startswith(f"--- Guide for {guide_id} ---\n#"):
        raise GuidanceError("Modern Web Guidance could not retrieve the matched guide.")
    ux = json.loads(design(uiux, "ux", "keyboard focus dialog accessibility", project))
    system = json.loads(design(uiux, "design", "responsive accessible landing page", project))
    if not (isinstance(ux, dict) and ux.get("results") and
            isinstance(system, dict) and system.get("design_system")):
        raise GuidanceError("UI/UX Pro Max did not return both UX results and a design system.")
    return json.dumps({
        "status": "READY", "modern_web_guidance": VERSION, "node": version,
        "guide_id": guide_id, "ui_ux_pro_max": str(uiux),
        "python": sys.version.split()[0], "ux_results": len(ux["results"]),
        "design_system": True,
    }, ensure_ascii=False, indent=2)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--package", type=Path,
                        default=Path("testing results/web-guidance") / ARCHIVE_NAME)
    parser.add_argument("--ui-ux-dir", type=Path, help="Host-reviewed UI/UX Pro Max directory")
    parser.add_argument("operation", choices=("check", "search", "retrieve", "design", "ux"))
    parser.add_argument("value", nargs="?")
    args = parser.parse_args(argv)
    value = args.value
    if args.operation == "check":
        if value is not None:
            parser.error("check takes no value")
    elif not value or not value.strip() or len(value) > 200 or value.lstrip().startswith("-"):
        parser.error("supply a short query or a guide ID")
    if args.operation == "retrieve" and not GUIDE_IDS.fullmatch(value):
        parser.error("guide IDs use lowercase letters, digits and hyphens, separated by commas")

    project = Path.cwd()
    try:
        content, uiux, node, version = prerequisites(project, args.package, args.ui_ux_dir)
        if args.operation in ("design", "ux"):
            result = design(uiux, args.operation, value, project)
        else:
            with tempfile.TemporaryDirectory(prefix="gis-web-guidance-") as staging:
                # Only the reviewed npm bytes are extracted. The data filter
                # also rejects unsafe tar paths and special files.
                with tarfile.open(fileobj=io.BytesIO(content), mode="r:gz") as archive:
                    archive.extractall(staging, filter="data")
                entry = Path(staging) / MODERN_ENTRY
                if args.operation == "check":
                    result = verify_providers(node, entry, uiux, project, version)
                else:
                    result = modern(node, entry, args.operation, value, project)
        sys.stdout.buffer.write((result.rstrip() + "\n").encode("utf-8"))
    except (OSError, ValueError, tarfile.TarError, subprocess.TimeoutExpired) as exc:
        print(f"Web guidance not ready: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
