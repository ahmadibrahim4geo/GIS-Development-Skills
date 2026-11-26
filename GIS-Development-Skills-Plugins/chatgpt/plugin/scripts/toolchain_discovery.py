#!/usr/bin/env python3
"""Discover build tools, with opt-in Windows installation and version queries.

The default audit does not launch executables. Installed-tool queries are
optional and do not establish licenses, IDE interaction or build/run results.
"""
import argparse
import json
import os
import shutil
import sys
from pathlib import Path

if __package__:
    from . import native_toolchain, toolchain_advice
else:
    import native_toolchain
    import toolchain_advice

TOOL_COMMANDS = {
    "Git": ("git",),
    "VS Code": ("code", "code.cmd"),
    "Antigravity IDE": ("antigravity", "antigravity.cmd"),
    "Rider": ("rider64", "rider", "rider.cmd"),
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


def audit(root, which=shutil.which, expose_paths=False, native=False, *, planned=False, extra_tools=()):
    root = root.resolve()
    if not root.is_dir() and not (planned and not root.exists() and root.parent.is_dir()):
        raise ValueError("Existing project directory required")
    stacks, matches = discover_stack(root)
    names = sorted({n for stack in stacks for n in STACK_TOOLS[stack]} | set(extra_tools))
    names += [n for n in ("VS Code", "Antigravity IDE", "Visual Studio", "Qt Creator", "Rider",
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
    result = {
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
    if native:
        installed = native_toolchain.probe(root, expose_paths)
        result["native_inventory"] = installed
        result["sdk_workload_verification"] = (
            "QUERY_RESULTS_RECORDED" if installed.get("status") != "WINDOWS_NATIVE_PROBE_UNAVAILABLE"
            else "NOT RUN")
        result["security"] = "Only fixed installed-tool queries and file metadata; no installer, IDE UI, project code or agent skill invoked."
    return result


def main(argv=None):
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--project", type=Path, required=True)
    cli.add_argument("--include-paths", action="store_true",
                     help="Show executable paths; may reveal local usernames and software locations")
    cli.add_argument("--native", action="store_true",
                     help="Query trusted Windows installs and SDK workloads without build or launch")
    cli.add_argument("--recommend", choices=toolchain_advice.TARGETS,
                     help="Recommend observed alternatives for an existing project target")
    cli.add_argument("--capability", choices=toolchain_advice.CAPABILITIES,
                     help="Requested capability, separate from the editor or project type")
    cli.add_argument("--target-version", help="Project's required major or major.minor runtime version")
    cli.add_argument("--prefer", choices=toolchain_advice.TOOLS, help="Prefer an applicable installed tool")
    cli.add_argument("--license-confirmed", choices=toolchain_advice.TOOLS, action="append", default=[],
                     help="Caller confirms the installed tool's terms cover this use")
    args = cli.parse_args(argv)
    if bool(args.recommend) != bool(args.capability):
        cli.error("--recommend and --capability are required together")
    if not args.recommend and (args.target_version or args.prefer or args.license_confirmed):
        cli.error("Version, preference and license declarations require --recommend")
    try:
        report = audit(args.project, expose_paths=args.include_paths, native=args.native or bool(args.recommend))
        if args.recommend:
            report["recommendation"] = toolchain_advice.recommend(
                report, args.recommend, args.capability, target_version=args.target_version,
                prefer=args.prefer, license_confirmed=args.license_confirmed,
            )
        print(json.dumps(report, indent=2, ensure_ascii=False))
        return 0
    except (OSError, ValueError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
