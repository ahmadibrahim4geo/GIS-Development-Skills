"""Recommend observed toolchain candidates for an explicit project capability."""

import re


TARGETS = ("dotnet", "wpf", "winforms", "qt-widgets", "arcgis-pro-sdk")
CAPABILITIES = ("edit", "build", "preview", "visual-design")
TOOLS = {
    "visual-studio": ("Visual Studio", "CHECK_TERMS", "Community eligibility or the installed license"),
    "vscode": ("VS Code", "NO_COST", "The editor is free. Check extension terms separately."),
    "antigravity": ("Antigravity IDE", "CHECK_TERMS", "Check the installed product and any service or extension terms"),
    "rider": ("Rider", "CHECK_TERMS", "Free non-commercial license subject to JetBrains terms"),
    "qt-creator": ("Qt Creator", "OPEN_SOURCE_OPTION", "Check Qt edition, modules and distribution terms"),
    "qt-designer": ("Qt Designer", "OPEN_SOURCE_OPTION", "Check widget plugins and their licensing"),
    "qt-cmake": ("Qt SDK + CMake", "OPEN_SOURCE_OPTION", "Check Qt modules and compiler kit"),
    "dotnet-cli": (".NET SDK CLI", "NO_COST", "No .NET SDK license fee"),
}

VS_MINIMUM = {6: (17, 0), 7: (17, 4), 8: (17, 8), 9: (17, 12), 10: (18, 0)}
MANAGED_DESKTOP = "Microsoft.VisualStudio.Workload.ManagedDesktop"


def release(version):
    if isinstance(version, str) and re.fullmatch(r"\d+(?:\.\d+){0,3}", version):
        return tuple(int(part) for part in version.split("."))
    return ()


def options_for(target, action):
    if action == "edit":
        if target is None:
            return ["vscode", "antigravity"]
        preferred = ["qt-creator"] if target == "qt-widgets" else ["rider"]
        return ["vscode", *preferred, "visual-studio", "antigravity"]
    if action == "build":
        if target == "arcgis-pro-sdk":
            return ["visual-studio"]
        return ["qt-cmake"] if target == "qt-widgets" else ["dotnet-cli"]
    if target == "qt-widgets":
        return ["qt-designer", "qt-creator"]
    if target == "winforms":
        return ["visual-studio", "rider"]
    if target == "wpf":
        return ["visual-studio", "rider"] if action == "preview" else ["visual-studio"]
    return []


def observe(tool, inventory):
    """Use read-only inventory results. A PATH match is a weaker observation."""
    native = inventory.get("native_inventory", {})
    products = {
        "vscode": {"VS Code"}, "antigravity": {"Antigravity", "Antigravity IDE"},
        "rider": {"Rider"}, "qt-creator": {"Qt Creator"},
        "qt-designer": {"Qt Designer", "Qt Designer for QGIS"},
    }
    if tool == "visual-studio":
        instances = native.get("visual_studio", {}).get("instances", [])
        observed = [row for row in instances if row.get("complete") is True
                    and row.get("launchable_reported") is True]
        return observed, "INSTALLER_METADATA"
    if tool == "dotnet-cli":
        sdk = native.get("dotnet", {})
        versions = sdk.get("sdk_versions", []) if sdk.get("status") == "OBSERVED" else []
        return [{"version": version} for version in versions], "SDK_QUERY"
    if tool == "qt-cmake":
        return [row for row in native.get("qt_sdk_candidates", []) if row.get("version")], "SDK_QUERY"
    group = "designers" if tool == "qt-designer" else "editors"
    return [row for row in native.get("ui_tools", {}).get(group, [])
            if row.get("product") in products[tool] and row.get("status") == "FILE_OBSERVED"], "FILE_METADATA"


def technical_checks(tool, inventory, target, action, required, observations):
    if action == "edit":
        return []
    if tool == "dotnet-cli":
        if not required:
            return ["Confirm the target framework from the project."]
        if not any(release(row.get("version"))[:2] >= required for row in observations):
            return ["Verify a .NET SDK compatible with the requested target."]
        packs = inventory["native_inventory"]["dotnet"].get("reference_packs", {})
        if not any(release(version)[:len(required)] == required for version in packs.get(target, [])):
            return ["Verify the reference pack for the project's .NET target."]
        return []
    if tool == "qt-cmake":
        if required and not any(release(row.get("version"))[:len(required)] == required for row in observations):
            return ["Find the Qt SDK version that matches the project."]
        return ["Verify CMake or qmake and the compiler kit against the selected Qt SDK."]
    if tool == "visual-studio":
        if target == "arcgis-pro-sdk":
            return ["Verify the ArcGIS Pro SDK extension and host/IDE compatibility for the installed Pro release."]
        eligible = [row for row in observations if row.get("workloads", {}).get(MANAGED_DESKTOP) is True]
        checks = []
        if not eligible:
            checks.append("Verify the .NET Desktop Development workload and the selected designer.")
        minimum = VS_MINIMUM.get(required[0]) if required else None
        if not minimum or not any(release(row.get("version"))[:2] >= minimum for row in (eligible or observations)):
            checks.append("Verify that this Visual Studio release supports the project's target framework in the designer.")
        return checks
    if tool == "qt-designer" and required and any(
            release(row.get("version"))[:len(required)] == required for row in observations):
        return []
    if tool.startswith("qt-"):
        return ["Verify the designer's Qt version and required custom widgets against the project."]
    return ["Verify the Rider release supports the project's Windows designer or preview target."]


def recommend(inventory, target, action, *, target_version=None, prefer=None, license_confirmed=()):
    required = release(target_version)
    if (target not in TARGETS and not (target is None and action == "edit")) or action not in CAPABILITIES:
        raise ValueError("Choose a supported target and capability.")
    if target_version is not None and not 1 <= len(required) <= 2:
        raise ValueError("Target version must be a major or major.minor number.")
    if (prefer is not None and prefer not in TOOLS) or set(license_confirmed) - TOOLS.keys():
        raise ValueError("Unknown tool in the preference or license declarations.")
    candidates = []
    for tool in options_for(target, action):
        label, cost, terms = TOOLS[tool]
        observations, basis = observe(tool, inventory)
        on_path = inventory.get("tool_candidates", {}).get(label, {}).get("status") == "FOUND_ON_PATH_NOT_EXECUTED"
        checks = []
        if observations:
            checks = technical_checks(tool, inventory, target, action, required, observations)
        elif on_path:
            checks = ["Confirm the executable's identity and applicable capabilities."]
            basis = "PATH_ONLY"
        else:
            basis = "NOT_OBSERVED"
        if cost == "CHECK_TERMS" and tool not in license_confirmed and basis != "NOT_OBSERVED":
            checks.append("Confirm that the installed license covers this use.")
        status = "NOT_OBSERVED" if basis == "NOT_OBSERVED" else "VERIFY_REQUIRED" if checks else "CANDIDATE"
        candidates.append({"id": tool, "tool": label, "cost": cost, "terms": terms,
                           "basis": basis, "versions": [row["version"] for row in observations if row.get("version")],
                           "status": status, "checks": checks})
    ready = [row for row in candidates if row["status"] == "CANDIDATE"]
    selected = next((row for row in ready if row["id"] == prefer), ready[0] if ready else None)
    fallback = None
    if selected is None:
        fallback = "Keep the current project target and verify an applicable local tool."
        if target == "wpf" and action in ("visual-design", "preview"):
            fallback = "Verify a WPF designer for the project target, or confirm that XAML source editing meets the request."
    return {"target": target, "capability": action, "target_version": target_version,
            "preferred_tool": prefer,
            "selected_candidate": selected["id"] if selected else None,
            "options": candidates, "functional_test": "NOT RUN",
            "fallback": fallback}
