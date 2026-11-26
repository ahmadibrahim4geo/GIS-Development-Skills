"""Read a target project's setup needs and reuse observed local toolchain candidates."""

import json
from pathlib import Path, PurePosixPath
import posixpath
import re
import xml.etree.ElementTree as ET

if __package__:
    from . import project_structure, toolchain_advice, toolchain_discovery
else:
    import project_structure
    import toolchain_advice
    import toolchain_discovery


RUNTIMES = {
    "python": ("Python", "https://www.python.org/downloads/"),
    "node": ("Node.js", "https://nodejs.org/en/download"),
    "qgis": ("QGIS", "https://qgis.org/download/"),
    "arcpy": ("ArcGIS Pro", "https://pro.arcgis.com/en/pro-app/latest/get-started/download-arcgis-pro.htm"),
}
TARGETS = (*toolchain_advice.TARGETS, *RUNTIMES)
OFFICIAL = {
    "dotnet-cli": "https://dotnet.microsoft.com/en-us/download/dotnet",
    "visual-studio": "https://visualstudio.microsoft.com/vs/older-downloads/",
    "vscode": "https://code.visualstudio.com/download",
    "rider": "https://www.jetbrains.com/rider/download/",
    "antigravity": "https://antigravity.google/",
    "qt-creator": "https://www.qt.io/development/tools",
    "qt-designer": "https://doc.qt.io/qt-6/qtdesigner-manual.html",
    "qt-cmake": "https://doc.qt.io/qt-6/cmake-manual.html",
}
KNOWN_MANIFESTS = {
    "global.json", ".vsconfig", "package.json", "pyproject.toml",
    "requirements.txt", "directory.packages.props", "packages.config", "cmakelists.txt",
}
PACKAGE_NAME = re.compile(r"(?:@[A-Za-z0-9_.-]+/)?[A-Za-z0-9][A-Za-z0-9_.-]{0,119}\Z")
PYTHON_REQUIREMENT = re.compile(r"^([A-Za-z0-9][A-Za-z0-9_.-]*)(?:\[[\w.,-]+\])?\s*([^;#]*)")
VERSION_TEXT = re.compile(r"[A-Za-z0-9.*^~<>=!, +()-]{1,96}\Z")
DOTNET_PROJECTS = {".csproj", ".vbproj", ".fsproj"}
DOTNET_TARGETS = {"dotnet", "wpf", "winforms", "arcgis-pro-sdk"}
TOOL_FILES = {
    "vscode": {"code"}, "antigravity": {"antigravity"}, "rider": {"rider", "rider64"},
    "visual-studio": {"devenv"}, "dotnet-cli": {"dotnet"}, "qt-creator": {"qtcreator"},
    "qt-designer": {"designer"}, "qt-cmake": {"cmake", "qmake", "qt-cmake"},
}


def package(ecosystem, name, version, source):
    if not isinstance(name, str) or not PACKAGE_NAME.fullmatch(name):
        return None
    value = version.strip() if isinstance(version, str) else ""
    return {"ecosystem": ecosystem, "name": name,
            "declared_version": value if VERSION_TEXT.fullmatch(value) else None,
            "source": source, "installation_status": "NOT CHECKED"}


def manifest_rows(path, source):
    """Read declarations only. Dynamic includes and nonliteral dependency values stay unresolved."""
    name = path.name.casefold()
    reference = path.as_posix()
    if name == "package.json":
        data = json.loads(source)
        if not isinstance(data, dict):
            raise ValueError("Expected a JSON object")
        for section in ("dependencies", "devDependencies", "peerDependencies"):
            deps = data.get(section, {})
            if isinstance(deps, dict):
                yield from (package("npm/" + section, key, version, reference) for key, version in deps.items())
    elif name in {"requirements.txt", "pyproject.toml"}:
        if name == "requirements.txt":
            requirements = source.splitlines()
        else:
            import tomllib
            requirements = tomllib.loads(source).get("project", {}).get("dependencies", [])
        if isinstance(requirements, list):
            for entry in requirements:
                match = PYTHON_REQUIREMENT.match(entry.strip()) if isinstance(entry, str) else None
                if match:
                    yield package("python", *match.groups(), reference)
    elif path.suffix.casefold() in DOTNET_PROJECTS or name in {"directory.packages.props", "packages.config"}:
        project = xml_project(source)
        if project is not None:
            for element in project.iter():
                tag = element.tag.split("}")[-1]
                if tag in {"PackageReference", "PackageVersion", "package"}:
                    key = element.get("Include") or element.get("Update") or element.get("id")
                    version = element.get("Version") or element.get("version")
                    if version is None:
                        version = next((child.text for child in element if child.tag.split("}")[-1] == "Version"), None)
                    yield package("nuget", key, version, reference)


def xml_project(source):
    if re.search(r"<!\s*(?:DOCTYPE|ENTITY)\b", source, re.I):
        raise ValueError("Unexpected XML declarations")
    return ET.fromstring(source) if source.strip() else None


def dotnet_metadata(sources):
    targets, frameworks, projects, sdk_styles = set(), set(), [], []
    for path, source in sources.items():
        if path.suffix.casefold() not in DOTNET_PROJECTS:
            continue
        projects.append(path.as_posix())
        try:
            document = xml_project(source)
        except (ET.ParseError, ValueError):
            document = None
        sdk_styles.append(document is not None and bool(document.get("Sdk") or any(
            child.tag.split("}")[-1] == "Sdk" for child in document)))
        if document is None:
            continue
        target = "dotnet"
        values = {}
        for node in document.iter():
            tag = node.tag.split("}")[-1]
            if tag in {"TargetFramework", "TargetFrameworks", "TargetFrameworkVersion", "UseWPF", "UseWindowsForms"}:
                values.setdefault(tag, []).append((node.text or "").strip())
            if tag in {"Reference", "PackageReference"} and re.match(r"ArcGIS\.Desktop\.", node.get("Include", ""), re.I):
                target = "arcgis-pro-sdk"
        if target != "arcgis-pro-sdk":
            ui_targets = {key for key, field in (("wpf", "UseWPF"), ("winforms", "UseWindowsForms"))
                          if any(value.casefold() == "true" for value in values.get(field, []))}
            targets.update(ui_targets or {target})
        else:
            targets.add(target)
        for field in ("TargetFramework", "TargetFrameworks", "TargetFrameworkVersion"):
            for value in values.get(field, []):
                frameworks.update(token for raw in value.split(";") if (token := raw.strip())
                                  and re.fullmatch(r"[A-Za-z0-9.-]{1,64}", token))
    return targets, sorted(frameworks), projects, bool(sdk_styles) and all(sdk_styles)


def dotnet_scope(root, sources, references, entry):
    projects = {path for path in sources if path.suffix.casefold() in DOTNET_PROJECTS}
    # Index scanned paths, rather than following paths written in project files.
    case_key = str.casefold if root.drive else str
    lookup = {case_key(path.as_posix()): path for path in projects}
    dependency_map = {path: set() for path in projects}
    for reference in references:
        if reference["kind"] == "dotnet-project-reference":
            owner = lookup.get(case_key(reference["file"]))
            dependency = lookup.get(case_key(reference["target"]))
            if owner is not None and dependency is not None:
                dependency_map[owner].add(dependency)

    if entry is not None:
        path = project_structure.safe_path(root, entry)
        scope = PurePosixPath(path.relative_to(root).as_posix())
        if scope in projects:
            return scope, scope, False
        if scope not in sources or scope.suffix.casefold() not in {".sln", ".slnx"}:
            raise ValueError("Choose a readable project or solution from the scanned project root.")
        source = sources[scope]
        if scope.suffix.casefold() == ".slnx":
            try:
                solution = xml_project(source)
            except (ET.ParseError, ValueError) as exc:
                raise ValueError("The selected solution manifest needs manual review.") from exc
            members = [node.get("Path", "") for node in solution.iter()
                       if node.tag.split("}")[-1] == "Project"] if solution is not None else []
        else:
            members = re.findall(r'^Project\([^\n]+?\)\s*=\s*"[^"]*",\s*"([^"]+)"', source, re.M)
        members = [name.replace("\\", "/") for name in members
                   if PurePosixPath(name.replace("\\", "/")).suffix.casefold() in DOTNET_PROJECTS]
        selected = [lookup.get(case_key(posixpath.normpath(f"{scope.parent}/{name}")))
                    if not name.startswith("/") and not re.search(r"[\x00-\x1f:*?%$@;]", name) else None
                    for name in members]
        if not selected or None in selected:
            return scope, None, True
        projects = set(selected)
    else:
        scope = None

    referenced = set().union(*(dependency_map[path] for path in projects))
    roots = projects - referenced
    primary = next(iter(roots)) if len(roots) == 1 else None
    return scope or primary, primary, bool(projects) and primary is None


def tool_path_findings(tool_paths):
    """Check explicit local file names and file types without launching them."""
    findings = {}
    for declaration in tool_paths:
        tool, _, value = declaration.partition("=")
        if tool not in TOOL_FILES or not value or tool in findings:
            raise ValueError("Supply one TOOL=LOCAL_PATH per known tool.")
        path = Path(value)
        if (not path.is_absolute() or path.drive.startswith("\\") or ".." in path.parts
                or any(":" in part for part in path.parts[1:])):
            raise ValueError("Use a fully qualified local tool path without traversal.")
        filename = path.name.casefold()
        command = Path(filename).stem if filename.endswith((".exe", ".cmd")) else filename
        valid_name = command in TOOL_FILES[tool]
        try:
            linked = any(project_structure.is_link(part) for part in (*reversed(path.parents), path))
            observed = valid_name and not linked and path.is_file()
        except OSError:
            observed = False
        findings[tool] = {"file": path.name, "status": "VERIFY_REQUIRED" if observed else "NOT_OBSERVED",
                          "reason": "Verify product identity and capability before use." if observed else
                          "No matching regular local tool file was verified."}
    return findings


def tool_requirements(items):
    requirements = {}
    for item in items:
        action, _, tool = item.partition("=")
        if action not in toolchain_advice.CAPABILITIES or tool not in OFFICIAL:
            raise ValueError("Use ACTION=TOOL with a supported capability and tool.")
        requirements.setdefault(action, set()).add(tool)
    return requirements


def required_tool_row(tool, inventory, paths):
    observed, basis = toolchain_advice.observe(tool, inventory)
    label = toolchain_advice.TOOLS[tool][0]
    if not observed:
        path_candidate = inventory.get("tool_candidates", {}).get(label, {})
        if paths.get(tool, {}).get("status") == "VERIFY_REQUIRED":
            basis = "USER_PATH_ONLY"
        elif path_candidate.get("status") == "FOUND_ON_PATH_NOT_EXECUTED":
            basis = "PATH_ONLY"
        else:
            basis = "NOT_OBSERVED"
    return {"id": tool, "official_url": OFFICIAL[tool], "basis": basis}


def environment_need(target, inventory):
    tool, url = RUNTIMES[target]
    native = inventory.get("native_inventory", {})
    if target in {"qgis", "arcpy"}:
        observed = any(row.get("product") == tool for row in native.get("installer_file_versions", []))
    else:
        observed = (inventory.get("tool_candidates", {}).get(tool, {}).get("status") == "FOUND_ON_PATH_NOT_EXECUTED"
                    or (target == "node" and bool(native.get("node", {}).get("version"))))
    return {"id": tool, "official_url": url,
            "status": "VERIFY_REQUIRED" if observed else "NOT_OBSERVED",
            "checks": ["Verify the project's runtime, version, environment and imports."]}


def preflight(root, *, mode, target=None, actions=(), target_version=None, prefer=None,
              license_confirmed=(), required_tools=(), planned_packages=(), inspect_tools=None,
              project_file=None, requires_tool=(), tool_paths=()):
    root = root.resolve()
    if mode not in {"new", "existing"} or target not in {None, *TARGETS}:
        raise ValueError("Choose a supported mode and project target")
    if (root.exists() or mode == "existing") and not root.is_dir():
        raise ValueError("Existing project mode requires an actual project directory")
    if mode == "new" and target is None:
        raise ValueError("A new project needs the reviewed target from the plan")
    if not root.is_dir() and not root.parent.is_dir():
        raise ValueError("Choose a planned directory under an existing parent")
    if set(required_tools) - OFFICIAL.keys() or set(actions) - set(toolchain_advice.CAPABILITIES):
        raise ValueError("Unknown required tool or capability")
    if project_file is not None and mode != "existing":
        raise ValueError("Project entry selection requires an existing project.")
    requirements = tool_requirements(requires_tool)
    explicit_paths = tool_path_findings(tool_paths)
    scan = project_structure.inspect_sources(root) if mode == "existing" else ({}, [], [], {}, {})
    profiles, _, references, sources, limits = scan
    detected, frameworks, project_files, sdk_style = dotnet_metadata(sources)
    entry, primary, ambiguous_entry = dotnet_scope(root, sources, references, project_file)
    candidates = detected.copy()
    if primary is not None:
        primary_targets, frameworks, _, sdk_style = dotnet_metadata({primary: sources[primary]})
        candidates = primary_targets
    if "qt" in profiles and any(path.suffix.casefold() == ".ui" or re.search(
        r"\bQt[56]?\b[^)]{0,200}\bWidgets\b", source, re.I)
        for path, source in sources.items() if path.suffix.casefold() == ".ui" or path.name.casefold() == "cmakelists.txt"):
        detected.add("qt-widgets")
    for profile, runtime in (("python", "python"), ("javascript", "node"), ("qgis", "qgis"),
                             ("qgis-plugin", "qgis"), ("arcgis", "arcpy")):
        if profile in profiles:
            detected.add(runtime)
    if detected & {"arcpy", "qgis"}:
        detected.discard("python")
    if project_file is None:
        candidates.update(detected - DOTNET_TARGETS)
    selected = target or (next(iter(candidates)) if len(candidates) == 1 and not ambiguous_entry else None)
    target_review = bool(target and candidates and target not in candidates)
    if ambiguous_entry and (selected in DOTNET_TARGETS or project_file is not None):
        target_review = True
    infer = re.fullmatch(r"net(\d+\.\d+)(?:-windows[\d.]*)?", frameworks[0], re.I) if len(frameworks) == 1 else None
    effective_version = target_version or (infer[1] if infer and selected in {"dotnet", "wpf", "winforms"} else None)
    if target_version and not re.fullmatch(r"\d+(?:\.\d+)?", target_version):
        raise ValueError("Use a literal target major or major.minor version")
    if target_version and infer and selected in {"dotnet", "wpf", "winforms"}:
        requested_release = toolchain_advice.release(target_version)
        target_review |= toolchain_advice.release(infer[1])[:len(requested_release)] != requested_release

    dependencies, manifests, warnings, studio_components = [], [], [], []
    dependency_count = 0
    for path, source in sources.items():
        if path.name.casefold() in KNOWN_MANIFESTS or path.as_posix() in project_files:
            manifests.append(path.as_posix())
            try:
                if path.name.casefold() == ".vsconfig":
                    components = json.loads(source).get("components", [])
                    if isinstance(components, list):
                        studio_components.extend({"id": item, "source": path.as_posix(), "status": "NOT CHECKED"}
                                                 for item in components[:100] if isinstance(item, str)
                                                 and re.fullmatch(r"[A-Za-z0-9.-]{1,150}", item))
                for row in manifest_rows(path, source):
                    if row is not None:
                        dependency_count += 1
                        if len(dependencies) < 200:
                            dependencies.append(row)
            except (ValueError, TypeError, AttributeError, RecursionError, ET.ParseError, ImportError):
                warnings.append({"file": path.as_posix(), "reason": "Manifest requires manual review"})
    for name in planned_packages:
        record = package("plan", name, None, "reviewed plan")
        if record is None:
            raise ValueError("Use literal dependency names from the reviewed plan")
        dependency_count += 1
        if len(dependencies) < 200:
            dependencies.append(record)

    sdk, sdk_unreadable = {}, False
    # Check the root and any applicable configurations between it and the entry.
    sdk_dirs = set(entry.parents) if entry is not None else {PurePosixPath(".")}
    for sdk_path in sorted((path for path in sources if path.name.casefold() == "global.json"
                            and path.parent in sdk_dirs), key=lambda path: len(path.parts)):
        try:
            sdk_settings = json.loads(sources[sdk_path]).get("sdk", {})
            version = sdk_settings.get("version")
            if version is not None:
                if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", version):
                    raise ValueError("Expected a full SDK version")
                sdk = {"source": sdk_path.as_posix(), "requested_sdk": version,
                       "roll_forward_disabled": sdk_settings.get("rollForward") == "disable"}
        except (ValueError, AttributeError, RecursionError):
            sdk_unreadable = True
            warnings.append({"file": sdk_path.as_posix(), "reason": "SDK selection needs manual review"})
    if mode == "existing":
        for directory in sdk_dirs:
            path = directory / "global.json"
            if not any(probed.parent == directory and probed.name.casefold() == "global.json" for probed in sources):
                candidate = root / path
                if candidate.exists() or project_structure.is_link(candidate):
                    sdk_unreadable = True
                    warnings.append({"file": path.as_posix(), "reason": "SDK configuration was outside the readable scan"})

    if inspect_tools is None:
        inspect_tools = toolchain_discovery.audit
    inventory = inspect_tools(root, native=True, planned=mode == "new", extra_tools=("Python", "Node.js"))
    work = [{"action": "inspect", "status": "CONTINUE", "required": False, "options": []}]
    requested = tuple(dict.fromkeys([*(actions or ("build",)), *requirements]))
    if "edit" not in requested:
        requested += ("edit",)
    for action in requested:
        editing = action == "edit"
        optional = editing and action not in requirements
        advice = None
        if selected in toolchain_advice.TARGETS or editing:
            advice_target = selected if selected in toolchain_advice.TARGETS else None
            advice = toolchain_advice.recommend(inventory, advice_target, action,
                                                target_version=effective_version, prefer=prefer,
                                                license_confirmed=license_confirmed)
            options = [{**row, "official_url": OFFICIAL[row["id"]]} for row in advice["options"]]
        elif selected in RUNTIMES and not optional:
            options = [environment_need(selected, inventory)] if action == "build" else []
        else:
            options = []
        for row in options:
            if row.get("basis") == "NOT_OBSERVED" and explicit_paths.get(row["id"], {}).get("status") == "VERIFY_REQUIRED":
                row.update(basis="USER_PATH_ONLY", status="VERIFY_REQUIRED",
                           checks=["Verify the supplied executable's product identity and applicable capabilities."])
        reason = None
        if editing:
            status = "REUSE_EDITOR" if advice and advice["selected_candidate"] else "OPTIONAL"
        elif not selected or target_review:
            status, reason = "VERIFY_REQUIRED", "Confirm the target in the reviewed plan against the project manifests."
        elif advice and advice["selected_candidate"]:
            status = "CANDIDATE"
        else:
            status = "VERIFY_REQUIRED" if not options or any(row["status"] != "NOT_OBSERVED" for row in options) else "BLOCKED"
        if action == "build" and selected in {"dotnet", "wpf", "winforms"} and mode == "existing" and not sdk_style:
            status, reason = "VERIFY_REQUIRED", "Check the project's MSBuild format and any legacy toolset or targeting packs."
        if action == "build" and sdk_unreadable and selected in DOTNET_TARGETS:
            status, reason = "VERIFY_REQUIRED", "Review the unreadable global.json SDK configuration before building."
        elif action == "build" and sdk and selected in DOTNET_TARGETS:
            observed = inventory.get("native_inventory", {}).get("dotnet", {})
            if sdk["requested_sdk"] not in observed.get("sdk_versions", []):
                status = "BLOCKED" if sdk["roll_forward_disabled"] and observed.get("status") == "OBSERVED" else "VERIFY_REQUIRED"
                reason = "The requested global.json SDK was not observed. Check its SDK selection rules."
        dependencies_for_action = [required_tool_row(tool, inventory, explicit_paths)
                                   for tool in sorted(requirements.get(action, ()))]
        missing = [tool["id"] for tool in dependencies_for_action if tool["basis"] == "NOT_OBSERVED"]
        available = {row["id"] for row in options if row["status"] == "CANDIDATE"}
        pending = [tool["id"] for tool in dependencies_for_action if tool["id"] not in available]
        if missing:
            status, reason = "BLOCKED", "Required tool unavailable: " + ", ".join(missing)
        elif pending and status != "BLOCKED":
            status, reason = "VERIFY_REQUIRED", "Check capability and license for required tool: " + ", ".join(pending)
        chosen = advice["selected_candidate"] if advice and status in {"REUSE_EDITOR", "CANDIDATE"} else None
        if dependencies_for_action and chosen not in requirements[action]:
            chosen = next((tool["id"] for tool in dependencies_for_action if tool["id"] in available), None) if chosen else None
        work.append({"action": action, "status": status, "required": not optional, "reason": reason,
                     "selected_candidate": chosen, "options": options, "required_tools": dependencies_for_action})
    for tool in dict.fromkeys(required_tools):
        observed = required_tool_row(tool, inventory, explicit_paths)
        basis = observed["basis"]
        work.append({"action": "required-tool:" + tool, "status": "VERIFY_REQUIRED" if basis != "NOT_OBSERVED" else "BLOCKED",
                     "required": True, "options": [observed],
                     "reason": "Check this specifically requested tool before using its dependent task."})

    solutions = [path for path in profiles.get("dotnet", []) if path.casefold().endswith((".sln", ".slnx"))]
    reuse = []
    if sdk_style and selected in {"dotnet", "wpf", "winforms"} and not target_review:
        build_status = next((row["status"] for row in work if row["action"] == "build"), "NOT CHECKED")
        reuse.append({"tool": "dotnet-cli", "purpose": "Build the existing compatible solution or project",
                      "source": "https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-build",
                      "availability": build_status, "test": "NOT RUN"})
        editors = next(row["options"] for row in work if row["action"] == "edit")
        rider = next((row for row in editors if row["id"] == "rider" and row["basis"] != "NOT_OBSERVED"), None)
        if rider and any(path.casefold().endswith(".sln") for path in solutions):
            reuse.append({"tool": "rider", "purpose": "Consider opening the existing .sln, then validate add-ins and build",
                          "source": "https://www.jetbrains.com/help/rider/Open_projects_and_solutions.html",
                          "test": "NOT RUN", "license_status": rider["status"]})
    paused = [row["action"] for row in work if row["required"] and row["status"] in {"BLOCKED", "VERIFY_REQUIRED"}]
    return {
        "root": str(root), "mode": mode, "root_exists": root.is_dir(), "target": selected,
        "detected_targets": sorted(detected), "target_version": effective_version,
        "build_entry": entry.as_posix() if entry else None,
        "primary_project": primary.as_posix() if primary else None,
        "project_files": sorted(project_files), "existing_solutions": sorted(solutions), "frameworks": frameworks,
        "sdk_config": sdk or None, "manifest_files": sorted(manifests),
        "dependencies": dependencies, "dependency_count": dependency_count,
        "visual_studio_components": studio_components[:100],
        "scan_limits": limits, "manifest_findings": warnings, "supplied_tool_paths": explicit_paths,
        "work": work, "tasks_on_hold": paused, "continue_independent_work": True,
        "existing_solution_paths": reuse, "installs_or_downloads": "NOT RUN",
        "next_action": "If a required tool remains unavailable, offer the compatible path or ask for an installation decision.",
    }
