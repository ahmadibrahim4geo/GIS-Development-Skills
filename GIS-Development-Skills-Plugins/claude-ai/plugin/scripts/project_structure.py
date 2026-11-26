"""Read-only source inspection for the project governance CLI."""

import ast
from collections import defaultdict
from graphlib import CycleError, TopologicalSorter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import stat


IGNORED_WALK = {".git", ".venv", "venv", "node_modules", "__pycache__",
                ".pytest_cache", ".mypy_cache", ".idea", ".vs", ".next",
                "bin", "obj", "build", "dist", "testing data", "testing results",
                ".agent-development-log"}
SOURCE_EXCLUSIONS = IGNORED_WALK | {"agent", "context", "plans", "reports", "new skill"}
MAX_FILE_BYTES = 256 * 1024
MAX_SOURCE_BYTES = 8 * 1024 * 1024
MAX_SOURCE_FILES = 1500
WALK_DEPTH = 10
TEXT_SUFFIXES = {".py", ".pyt", ".cs", ".csproj", ".vbproj", ".fsproj", ".sln", ".slnx", ".cpp", ".h", ".xaml",
                 ".qml", ".ui", ".pro", ".js", ".mjs", ".ts", ".html", ".md"}
TEXT_NAMES = {"cmakelists.txt", "metadata.txt", "package.json", "pyproject.toml", "requirements.txt",
              "global.json", ".vsconfig", "directory.packages.props", "packages.config"}
PROJECT_REFERENCE = re.compile(r'<ProjectReference\b[^>]*\bInclude\s*=\s*["\']([^"\']+)["\']', re.I)


def is_link(path):
    """Include Windows junctions and other reparse points in the link boundary."""
    try:
        info = path.lstat()
    except FileNotFoundError:
        return False
    return stat.S_ISLNK(info.st_mode) or bool(
        getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT)


def safe_path(root, relative):
    """Resolve a project-relative path without following links below the root."""
    if not isinstance(relative, str) or not relative.strip():
        raise ValueError("Nonempty relative path required")
    if any(ord(char) < 32 for char in relative) or "\\" in relative or ":" in relative:
        raise ValueError("Use a POSIX-style project-relative path")
    candidate = Path(relative)
    if candidate.anchor or not candidate.parts or ".." in candidate.parts:
        raise ValueError("Root, absolute and traversing paths are prohibited")
    if os.name == "nt" and any(part.endswith((" ", ".")) for part in candidate.parts):
        raise ValueError("Windows paths must not end in a space or period")
    root = root.resolve()
    full = root / candidate
    for part in candidate.parts:
        root = root / part
        if is_link(root):
            raise ValueError("Symlinked paths are not permitted")
    return full


def numbered(base):
    if is_link(base) or not base.is_dir():
        return []
    return sorted(path for path in base.iterdir()
                  if re.match(r"^\d{4}_", path.name) and not is_link(path) and path.is_dir())


def next_id(root, locations):
    used = [int(entry.name[:4]) for location in locations
            for entry in numbered(safe_path(root, location))]
    sequence = max(used, default=0) + 1
    if sequence > 9999:
        raise ValueError("Four-digit sequence is exhausted")
    return f"{sequence:04d}"


def walk_project(root, max_depth=WALK_DEPTH, excludes=IGNORED_WALK, onerror=None):
    for base, folders, files in os.walk(root, topdown=True, followlinks=False, onerror=onerror):
        directory = Path(base)
        depth = len(directory.relative_to(root).parts)
        folders[:] = sorted(name for name in folders if depth < max_depth
                            and name.casefold() not in excludes and not is_link(directory / name))
        yield directory, folders, sorted(name for name in files if not is_link(directory / name))


def source_excluded(path):
    return any(part.casefold() in SOURCE_EXCLUSIONS for part in PurePosixPath(path).parts)


def source_profile(path, source, imports):
    name = path.name.casefold()
    suffix = path.suffix.casefold()
    families = set()
    if suffix in {".sln", ".slnx", ".csproj", ".vbproj", ".fsproj"}:
        families.add("dotnet")
    if suffix in {".csproj", ".vbproj"}:
        for family, flag in (("wpf", "UseWPF"), ("winforms", "UseWindowsForms")):
            if re.search(fr"<{flag}>\s*true\s*</{flag}>", source, re.I):
                families.add(family)
    if suffix in {".ui", ".qml", ".pro"} or (name == "cmakelists.txt" and re.search(
            r"\bfind_package\s*\(\s*Qt(?:[56])?\b", source, re.I)):
        families.add("qt")
    if imports & {"PySide2", "PySide6", "PyQt5", "PyQt6"}:
        families.add("qt")
    if suffix in {".py", ".pyt"} or name == "pyproject.toml":
        families.add("python")
    if suffix in {".pyt", ".tbx", ".atbx"} or "arcpy" in imports:
        families.add("arcgis")
    if suffix in {".qgs", ".qgz"} or "qgis" in imports:
        families.add("qgis")
    if name == "metadata.txt" and re.search(r"(?mi)^\[general\]\s*$", source) and re.search(
            r"(?mi)^qgisMinimumVersion\s*=", source):
        families.add("qgis-plugin")
    if suffix == ".html":
        families.add("web")
    if name == "package.json":
        families.add("javascript")
        try:
            package = json.loads(source)
        except (ValueError, RecursionError):
            package = None
        if isinstance(package, dict):
            for section in ("dependencies", "devDependencies", "peerDependencies"):
                dependencies = package.get(section)
                if isinstance(dependencies, dict) and dependencies.keys() & {"maplibre-gl", "mapbox-gl", "cesium", "leaflet", "ol"}:
                    families.update(("web", "web-gis"))
    if imports & {"ee", "sentinelhub", "landsatxplore", "s2cloudless", "eemont"}:
        families.add("remote-sensing")
    if name in {"requirements.txt", "pyproject.toml"} and re.search(
            r"(?im)(?:^|['\"])(?:earthengine-api|sentinelhub|landsatxplore|s2cloudless|eemont)(?=[\s'\"<=>~;\[]|$)", source):
        families.add("remote-sensing")
    return families


def python_bindings(path, tree, modules):
    parts = path.with_suffix("").parts[:-1]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            if node.level > len(parts) + 1:
                continue
            if node.level:
                base = parts[:len(parts) - node.level + 1]
                name = ".".join((*base, node.module)) if node.module else ".".join(base)
            else:
                name = node.module or ""
            names = [f"{name}.{alias.name}".lstrip(".") for alias in node.names]
            names.append(name)
        else:
            continue
        for name in names:
            known = modules.get(name, ())
            if len(known) == 1 and known[0] != path.as_posix():
                yield {"file": path.as_posix(), "line": node.lineno,
                       "target": known[0], "kind": "python-import"}


def _source_files(root, include_docs):
    """Return bounded source text, name-only markers and scanning limitations."""
    sources, markers = {}, []
    limits = {"bytes_read": 0, "files_considered": 0, "skipped_files": 0,
              "unreadable_directories": 0, "budget_reached": False, "walk_depth": WALK_DEPTH}

    def unreadable(_):
        limits["unreadable_directories"] += 1

    for directory, _, names in walk_project(root, excludes=SOURCE_EXCLUSIONS, onerror=unreadable):
        for name in names:
            file = directory / name
            path = PurePosixPath(file.relative_to(root).as_posix())
            suffix = path.suffix.casefold()
            if suffix == ".md" and not include_docs:
                continue
            is_text = suffix in TEXT_SUFFIXES or name.casefold() in TEXT_NAMES
            if not is_text and suffix not in {".sln", ".slnx", ".tbx", ".atbx", ".qgs", ".qgz"}:
                continue
            if limits["files_considered"] == MAX_SOURCE_FILES:
                limits["budget_reached"] = True
                return sources, markers, limits
            limits["files_considered"] += 1
            markers.append(path)
            if not is_text:
                continue
            try:
                info = file.lstat()
                if not stat.S_ISREG(info.st_mode) or info.st_size > MAX_FILE_BYTES or is_link(file):
                    limits["skipped_files"] += 1
                    continue
                remaining = MAX_SOURCE_BYTES - limits["bytes_read"]
                if info.st_size > remaining or remaining <= 0:
                    limits["budget_reached"] = True
                    return sources, markers, limits
                with file.open("rb") as handle:
                    data = handle.read(min(remaining, MAX_FILE_BYTES) + 1)
                limits["bytes_read"] += len(data)
                if len(data) > min(remaining, MAX_FILE_BYTES):
                    limits["skipped_files"] += 1
                    continue
                sources[path] = data.decode("utf-8-sig")
            except (OSError, UnicodeError):
                limits["skipped_files"] += 1
    return sources, markers, limits


def inspect_sources(root, *, include_docs=False):
    sources, markers, limits = _source_files(root, include_docs)
    profiles, modules, digests = defaultdict(list), defaultdict(list), defaultdict(list)
    trees, references, findings = {}, [], []
    for path, source in sources.items():
        if path.suffix.casefold() == ".py":
            parts = path.with_suffix("").parts
            key = ".".join(parts[:-1] if path.stem == "__init__" else parts)
            modules[key].append(path.as_posix())
        if path.suffix.casefold() in {".py", ".pyt"}:
            try:
                trees[path] = ast.parse(source)
            except (SyntaxError, ValueError, RecursionError):
                findings.append({"kind": "python-unparsed", "file": path.as_posix()})
        if path.suffix.casefold() in {".py", ".pyt", ".cs", ".cpp", ".js", ".ts"} and source.strip():
            digest = hashlib.sha256(source.encode("utf-8").replace(b"\r\n", b"\n")).hexdigest()
            digests[digest].append(path.as_posix())
        if path.suffix.casefold() in {".csproj", ".vbproj", ".fsproj"}:
            # Keep line positions for source references and ignore commented XML.
            source = re.sub(r"<!--.*?-->", lambda match: re.sub(r"[^\n]", " ", match[0]), source, flags=re.S)
            sources[path] = source
            for match in PROJECT_REFERENCE.finditer(source):
                raw = match[1].replace("\\", "/")
                target = posixpath.normpath(f"{path.parent}/{raw}")
                if (not raw or raw.startswith("/") or re.search(r"[\x00-\x1f:*?%$@;]", raw)
                        or target.startswith("../") or source_excluded(target)):
                    continue
                reference = {"kind": "dotnet-project-reference", "file": path.as_posix(),
                             "line": source.count("\n", 0, match.start()) + 1, "target": target}
                references.append(reference)
                parent_paths = [root / part for part in PurePosixPath(target).parents]
                target_file = root / target
                linked = any(is_link(part) for part in reversed(parent_paths)) or is_link(target_file)
                if not linked and not target_file.is_file():
                    findings.append({**reference, "kind": "missing-project-reference"})

    for path in markers:
        tree = trees.get(path)
        imported = set()
        if tree:
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    imported.update(alias.name.split(".")[0] for alias in node.names)
                elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
                    imported.add(node.module.split(".")[0])
            references.extend(python_bindings(path, tree, modules))
        for kind in sorted(source_profile(path, sources.get(path, ""), imported)):
            profiles[kind].append(path.as_posix())

    findings.extend({"kind": "identical-source", "files": files}
                    for files in digests.values() if len(files) > 1)
    dependencies = defaultdict(set)
    for ref in references:
        dependencies[ref["file"]].add(ref["target"])
    try:
        TopologicalSorter({file: sorted(targets) for file, targets in dependencies.items()}).prepare()
    except CycleError as exc:
        findings.append({"kind": "local-dependency-cycle", "files": exc.args[1]})
    references = list({(ref["file"], ref["line"], ref["target"], ref["kind"]): ref
                       for ref in references}.values())
    return dict(sorted(profiles.items())), findings, references, sources, limits


def move_references(source, target, references, sources):
    comparison = source.casefold() if os.name == "nt" else source

    def affected(path):
        candidate = path.casefold() if os.name == "nt" else path
        return candidate == comparison or candidate.startswith(comparison + "/")

    def future(path):
        return target + path[len(source):] if affected(path) else path

    result = [{**ref, "file_after": future(ref["file"]), "target_after": future(ref["target"])}
              for ref in references if affected(ref["file"]) or affected(ref["target"])]
    if len(result) > 200:
        return result[:200], True
    seen = {(ref["file"], ref["line"]) for ref in result}
    # Also surface quoted paths and full path mentions, including docs/resources
    # outside the explicitly parsed import and project-reference syntax.
    pattern = re.compile(r"(?<![\w./-])" + re.escape(source) + r"(?=[/\s\"'\x60),;\]]|$)",
                         re.I if os.name == "nt" else 0)
    for path, content in sources.items():
        for line_number, line in enumerate(content.splitlines(), 1):
            key = (path.as_posix(), line_number)
            if key not in seen and pattern.search(line.replace("\\", "/")):
                if len(result) == 200:
                    return result, True
                result.append({"kind": "path-mention", "file": key[0], "line": line_number,
                               "target": source, "file_after": future(key[0]), "target_after": target})
    return result, False
