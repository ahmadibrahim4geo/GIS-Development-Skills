"""Bounded Windows discovery of installed build and GIS runtimes."""

import ctypes
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tempfile


VS_COMPONENTS = (
    "Microsoft.VisualStudio.Workload.ManagedDesktop",
    "Microsoft.VisualStudio.Workload.ManagedDesktopBuildTools",
    "Microsoft.VisualStudio.Workload.NativeDesktop",
    "Microsoft.VisualStudio.Workload.VCTools",
)


def reference_packs(dotnet_root):
    """Observe version-specific .NET reference assemblies without loading them."""
    desktop = "Microsoft.WindowsDesktop.App.Ref"
    return {
        target: sorted({path.parent.name.removeprefix("net") for path in
                        sorted((dotnet_root / "packs" / pack).glob("*/ref/net*/" + assembly))[:32]
                        if trusted_file(path, dotnet_root)})
        for target, pack, assembly in (
            ("wpf", desktop, "PresentationFramework.dll"),
            ("winforms", desktop, "System.Windows.Forms.dll"),
            ("dotnet", "Microsoft.NETCore.App.Ref", "System.Runtime.dll"),
        )
    }


def file_version(path):
    from ctypes import wintypes

    api = ctypes.WinDLL(str(Path(os.environ["SystemRoot"]) / "System32/version.dll"))
    api.GetFileVersionInfoSizeW.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(wintypes.DWORD)]
    api.GetFileVersionInfoSizeW.restype = wintypes.DWORD
    api.GetFileVersionInfoW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p]
    api.GetFileVersionInfoW.restype = wintypes.BOOL
    api.VerQueryValueW.argtypes = [ctypes.c_void_p, wintypes.LPCWSTR,
                                   ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.UINT)]
    api.VerQueryValueW.restype = wintypes.BOOL
    size = api.GetFileVersionInfoSizeW(str(path), None)
    if not 0 < size <= 1024 * 1024:
        return None
    buffer = ctypes.create_string_buffer(size)
    address, length = ctypes.c_void_p(), wintypes.UINT()
    if not (api.GetFileVersionInfoW(str(path), 0, size, buffer)
            and api.VerQueryValueW(buffer, "\\", ctypes.byref(address), ctypes.byref(length))
            and address.value and length.value >= 13 * 4):
        return None
    fixed = ctypes.cast(address, ctypes.POINTER(wintypes.DWORD * 13)).contents
    if fixed[0] != 0xFEEF04BD:
        return None
    upper, lower = (fixed[4], fixed[5]) if fixed[4] or fixed[5] else (fixed[2], fixed[3])
    return ".".join(map(str, (upper >> 16, upper & 65535, lower >> 16, lower & 65535)))


def query(executable, arguments, scratch):
    environment = dict(os.environ, DOTNET_CLI_HOME=str(scratch / "dotnet-home"),
                       DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1",
                       DOTNET_CLI_UI_LANGUAGE="en-US",
                       DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE="true",
                       DOTNET_GENERATE_ASPNET_CERTIFICATE="false",
                       DOTNET_ADD_GLOBAL_TOOLS_TO_PATH="0")
    try:
        result = subprocess.run([str(executable), *arguments], cwd=scratch, env=environment,
                                stdin=subprocess.DEVNULL, capture_output=True, timeout=12,
                                creationflags=subprocess.CREATE_NO_WINDOW, check=False)
    except (OSError, subprocess.TimeoutExpired):
        return None
    if result.returncode or len(result.stdout) > 1024 * 1024:
        return None
    return result.stdout.decode("utf-8-sig", "replace").strip()


def trusted_file(path, root):
    """Do not launch PATH or project replacements for installed tools."""
    try:
        return path.resolve(strict=True).is_relative_to(root.resolve(strict=True)) and path.is_file()
    except (OSError, RuntimeError):
        return False


def clr_inventory(executable, invoke):
    sdks = invoke(executable, ("--list-sdks",))
    runtimes = invoke(executable, ("--list-runtimes",))
    workloads = invoke(executable, ("workload", "list"))
    sdk_rows = re.findall(r"(?m)^([0-9][\w.+-]+)\s+\[", sdks or "")
    runtime_rows = [{"name": name, "version": version} for name, version in
                    re.findall(r"(?m)^(\S+) ([0-9][\w.+-]+)\s+\[", runtimes or "")]
    workload_rows = None
    if workloads is not None and "Installed Workload Id" in workloads:
        workload_rows = [{"id": name, "manifest": version} for name, version in
                         re.findall(r"(?m)^([a-z][\w.-]+)\s+([0-9][\w./+-]+)\s+", workloads)]
    return {"status": "OBSERVED" if sdks is not None and runtimes is not None else "QUERY_FAILED",
            "sdk_versions": sdk_rows, "runtimes": runtime_rows,
            "workloads_status": "OBSERVED" if workload_rows is not None else "QUERY_UNAVAILABLE",
            "workloads": workload_rows or []}


def instances(executable, invoke, *arguments):
    reply = invoke(executable, ("-products", "*", "-format", "json", "-utf8", *arguments))
    try:
        records = json.loads(reply) if reply is not None else None
    except ValueError:
        return None
    if not isinstance(records, list) or any(
            not isinstance(entry, dict) or not isinstance(entry.get("instanceId"), str) for entry in records):
        return None
    return records


def visual_studio_inventory(executable, invoke, expose_paths):
    found = instances(executable, invoke)
    if found is None:
        return {"status": "QUERY_FAILED", "instances": []}
    components = {}
    if found:
        for name in VS_COMPONENTS:
            replies = instances(executable, invoke, "-requires", name)
            components[name] = None if replies is None else {item["instanceId"] for item in replies}
    items = []
    for source in found:
        item = {"product": source.get("displayName"), "version": source.get("installationVersion"),
                "complete": source.get("isComplete"), "launchable_reported": source.get("isLaunchable"),
                "workloads": {name: (None if matched is None else source["instanceId"] in matched)
                              for name, matched in components.items()}}
        if expose_paths:
            item["path"] = source.get("installationPath")
        items.append(item)
    return {"status": "OBSERVED", "instances": items}


def local_ui_tools(program_files, user_programs, qt_homes, qgis_homes, version_reader, expose_paths):
    """Read metadata for editors and visual designers separately. Never launch them."""
    editors = [
        ("VS Code", root, root / "Microsoft VS Code/Code.exe")
        for root in (program_files, user_programs) if root is not None
    ]
    if user_programs is not None:
        editors.extend([
            ("Antigravity", user_programs, user_programs / "antigravity/Antigravity.exe"),
            ("Antigravity IDE", user_programs, user_programs / "Antigravity IDE/Antigravity IDE.exe"),
        ])
    for root in (program_files, user_programs):
        if root is not None:
            editors.append(("Qt Creator", root, root / "Qt Creator/bin/qtcreator.exe"))
            for pattern in ("JetBrains/JetBrains Rider*/bin/rider64.exe",
                            "JetBrains Rider*/bin/rider64.exe", "Rider/bin/rider64.exe"):
                editors.extend(("Rider", root, path) for path in sorted(root.glob(pattern))[:12])
    if user_programs is not None:
        toolbox = user_programs.parent / "JetBrains/Toolbox/apps"
        for pattern in ("Rider/bin/rider64.exe", "Rider/*/*/bin/rider64.exe"):
            editors.extend(("Rider", toolbox, path) for path in sorted(toolbox.glob(pattern))[:12])
    designers = [
        ("Qt Designer for QGIS", program_files, qgis / "apps/qt6/bin/designer.exe")
        for qgis in qgis_homes
    ]
    for qt in qt_homes:
        editors.append(("Qt Creator", qt, qt / "Tools/QtCreator/bin/qtcreator.exe"))
        designers.extend(("Qt Designer", qt, executable)
                         for executable in sorted(qt.glob("*/*/bin/designer.exe"))[:24])
    found = {"editors": [], "designers": []}
    for category, candidates in (("editors", editors), ("designers", designers)):
        for product, root, executable in candidates:
            if trusted_file(executable, root):
                record = {"product": product, "version": version_reader(executable) if executable.suffix == ".exe" else None,
                          "status": "FILE_OBSERVED", "functional_test": "NOT RUN"}
                if expose_paths:
                    record["path"] = str(executable)
                found[category].append(record)
    return found


def native_windows(project, *, program_files, program_files_x86, drive, invoke,
                   version_reader=file_version, expose_paths=False, user_programs=None):
    dotnet = program_files / "dotnet/dotnet.exe"
    vswhere = program_files_x86 / "Microsoft Visual Studio/Installer/vswhere.exe"
    node = program_files / "nodejs/node.exe"
    result = {
        "platform": platform.system(), "release": platform.release(), "machine": platform.machine(),
        "python": {"version": platform.python_version(), "virtualenv": sys.prefix != sys.base_prefix,
                   "conda_prefix_metadata": (Path(sys.prefix) / "conda-meta").is_dir()},
        "dotnet": clr_inventory(dotnet, invoke) if trusted_file(dotnet, program_files) else {"status": "NOT_FOUND"},
        "visual_studio": visual_studio_inventory(vswhere, invoke, expose_paths)
        if trusted_file(vswhere, program_files_x86) else {"status": "NOT_FOUND"},
    }
    if expose_paths:
        result["python"]["executable"] = sys.executable
    if result["dotnet"]["status"] == "OBSERVED":
        result["dotnet"]["reference_packs"] = reference_packs(dotnet.parent)
    node_version = invoke(node, ("--version",)) if trusted_file(node, program_files) else None
    result["node"] = {"version": node_version if node_version and re.fullmatch(r"v[0-9][\w.+-]+", node_version)
                      else None}
    qgis_homes = sorted(program_files.glob("QGIS*"))[:16]
    qt_homes = (drive / "Qt", program_files / "Qt")
    result["ui_tools"] = local_ui_tools(program_files, user_programs, qt_homes, qgis_homes,
                                        version_reader, expose_paths)
    native_files = [("ArcGIS Pro", program_files / "ArcGIS/Pro/bin/ArcGISPro.exe", program_files)]
    for installation in qgis_homes:
        native_files.extend([
            ("QGIS", installation / "bin/qgis-bin.exe", program_files),
            ("Qt runtime bundled with QGIS", installation / "apps/qt6/bin/Qt6Core.dll", program_files),
            ("Python bundled with QGIS", installation / "bin/python.exe", program_files),
        ])
    result["installer_file_versions"] = []
    for product, executable, root in native_files:
        if trusted_file(executable, root):
            version = version_reader(executable)
            item = {"product": product, "version": version,
                    "status": "VERSION_RESOURCE_READ" if version else "FILE_ONLY"}
            if expose_paths:
                item["path"] = str(executable)
            result["installer_file_versions"].append(item)
    result["qt_sdk_candidates"] = []
    for qt in qt_homes:
        for qmake in sorted(qt.glob("*/*/bin/qmake.exe"))[:24]:
            if not trusted_file(qmake, qt):
                continue
            version = invoke(qmake, ("-query", "QT_VERSION"))
            item = {"version": version if version and re.fullmatch(r"[0-9][\w.+-]+", version) else None}
            if expose_paths:
                item["path"] = str(qmake)
            result["qt_sdk_candidates"].append(item)
    conda = program_files / "ArcGIS/Pro/bin/Python/envs"
    result["arcgis_conda_python"] = []
    for record in sorted(conda.glob("*/conda-meta/python-*.json"))[:32]:
        version = re.fullmatch(r"python-(\d+(?:\.\d+){1,3})-.+\.json", record.name)
        if version and trusted_file(record, program_files):
            result["arcgis_conda_python"].append({"environment": record.parents[1].name, "version": version[1]})
    result["project_virtualenvs"] = [name for name in (".venv", "venv")
                                    if trusted_file(project / name / "pyvenv.cfg", project)]
    result["license_or_host_execution"] = "NOT RUN"
    return result


def probe(project, expose_paths=False):
    if os.name != "nt":
        return {"status": "WINDOWS_NATIVE_PROBE_UNAVAILABLE"}
    drive = Path(os.environ.get("SystemDrive", "C:") + "/")
    program_files = Path(os.environ.get("ProgramW6432", os.environ.get("ProgramFiles", str(drive / "Program Files"))))
    program_files_x86 = Path(os.environ.get("ProgramFiles(x86)", str(drive / "Program Files (x86)")))
    user_profile = os.environ.get("USERPROFILE")
    user_programs = Path(user_profile) / "AppData/Local/Programs" if user_profile else None
    with tempfile.TemporaryDirectory(prefix="gis-native-probe-") as directory:
        return native_windows(project, program_files=program_files, program_files_x86=program_files_x86,
                              drive=drive, invoke=lambda exe, args: query(exe, args, Path(directory)),
                              expose_paths=expose_paths, user_programs=user_programs)
