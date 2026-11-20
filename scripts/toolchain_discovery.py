#!/usr/bin/env python3
"""Read-only build/IDE/toolchain candidate discovery for GIS projects.

No executable is launched. Presence on PATH is not evidence that SDK workloads,
licenses, extensions, GUI interaction, or build/run are actually available.
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

TOOL_COMMANDS = {
    "Git": ("git",),
    "VS Code": ("code", "code.cmd"),
    "Visual Studio": ("devenv", "devenv.exe"),
    "Visual Studio Installer Discovery": ("vswhere", "vswhere.exe"),
    "dotnet SDK CLI": ("dotnet", "dotnet.exe"),
    "MSBuild": ("msbuild", "msbuild.exe"),
    "CMake": ("cmake", "cmake.exe"),
    "Ninja": ("ninja", "ninja.exe"),
    "Qt Creator": ("qtcreator", "qtcreator.exe"),
    "Qt QMake": ("qmake", "qmake.exe", "qmake6"),
    "Python": ("python", "python3", "py"),
    "Pip": ("pip", "pip3"),
    "Node.js": ("node", "node.exe"),
    "npm": ("npm", "npm.cmd"),
    "Rust Cargo": ("cargo", "cargo.exe"),
    "Java": ("java", "java.exe"),
    "Android adb": ("adb", "adb.exe"),
}
STACK_TOOLS = {
    "python": ("Python", "Pip", "Git"),
    "dotnet": ("dotnet SDK CLI", "MSBuild", "Git"),
    "qt-cpp": ("CMake", "Ninja", "Qt QMake", "Git"),
    "javascript": ("Node.js", "npm", "Git"),
    "qgis-plugin": ("Python", "Git"),
    "arcgis-toolbox": ("Python", "Git"),
}


def discover_stack(root):
    """Source-file hints, not a runtime guarantee."""
    stacks = set()
    matches = {}
    checks = {
        "dotnet": ["*.sln", "*.slnx", "*.csproj", "*.vbproj"],
        "qt-cpp": ["CMakeLists.txt", "*.pro", "*.ui", "*.qml"],
        "python": ["pyproject.toml", "setup.py", "requirements.txt", "*.py"],
        "javascript": ["package.json", "vite.config.js", "vite.config.ts"],
        "arcgis-toolbox": ["*.pyt", "*.atbx"],
        "qgis-plugin": ["metadata.txt"],
    }
    for stack, patterns in checks.items():
        found = []
        for pattern in patterns:
            found.extend(p.name for p in root.glob(pattern) if p.is_file() and not p.is_symlink())
        if found:
            stacks.add(stack)
            matches[stack] = sorted(set(found))
    return sorted(stacks), matches


def audit(root, which=shutil.which, expose_paths=False):
    root = root.resolve()
    if not root.is_dir():
        raise ValueError("Existing project directory required")
    stacks, matches = discover_stack(root)
    names = sorted(set(n for stack in stacks for n in STACK_TOOLS[stack]))
    names += [n for n in ("VS Code", "Visual Studio", "Qt Creator",
                          "Visual Studio Installer Discovery") if n not in names]
    tools = {}
    for name in names:
        located = None
        for command in TOOL_COMMANDS[name]:
            located = which(command)
            if located:
                break
        state = "FOUND_ON_PATH_NOT_EXECUTED" if located else "NOT_FOUND_ON_PATH"
        item = {"status": state, "selected_command": command if located else None}
        if expose_paths and located:
            item["path"] = str(located)
        tools[name] = item
    missing = [name for name in sorted(set(n for s in stacks for n in STACK_TOOLS[s]))
               if tools[name]["status"] == "NOT_FOUND_ON_PATH"]
    return {
        "schema_version": "1.0",
        "platform": sys.platform,
        "project_type_hints": stacks,
        "matched_files": matches,
        "tool_candidates": tools,
        "missing_from_path": missing,
        "native_ide_gui_test": "NOT RUN",
        "sdk_workload_verification": "NOT RUN",
        "build_test": "NOT RUN",
        "security": "No programs run. No installer, network or agent skills invoked.",
        "note": "NOT_FOUND_ON_PATH does not prove a tool is not installed; inspect installed Windows apps and SDK registration separately when authorized.",
    }


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--project", type=Path, required=True)
    cli.add_argument("--include-paths", action="store_true",
                     help="Show executable paths; may reveal local usernames and software locations")
    args = cli.parse_args(argv)
    try:
        print(json.dumps(audit(args.project, expose_paths=args.include_paths),
                         indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
