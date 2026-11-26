#!/usr/bin/env python3
"""Build an installed WPF template and read back its native automation receipt."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import xml.etree.ElementTree as ET


FIXTURE = Path(__file__).resolve().parent / "wpf-toolchain"
EXPECTED = {"Crs": "EPSG:4326", "Rows": 2, "Columns": 2, "NoData": -9999, "ValidCells": 3}


def external_invoke(dotnet, assembly, driver, local_input, readback, work, environment):
    with (work / "launch.log").open("xb") as log:
        app = subprocess.Popen([str(dotnet), str(assembly), "--external-uia",
                                str(local_input), str(readback)], cwd=work, env=environment,
                               stdin=subprocess.DEVNULL, stdout=log, stderr=subprocess.STDOUT,
                               creationflags=subprocess.CREATE_NO_WINDOW)
        try:
            client = subprocess.run(
                [str(dotnet), str(driver), str(app.pid)], cwd=work, env=environment,
                stdin=subprocess.DEVNULL, capture_output=True, timeout=20,
                creationflags=subprocess.CREATE_NO_WINDOW, check=False,
            )
            (work / "uia-client.log").write_bytes(client.stdout + client.stderr)
            if client.returncode:
                raise RuntimeError("External Windows UI Automation client failed. See uia-client.log.")
            if app.wait(timeout=10):
                raise RuntimeError("The WPF application did not validate the externally invoked action.")
            observed = json.loads(client.stdout.decode("ascii").strip())
            if observed != {"WindowAutomationId": "RasterReadbackWindow",
                            "ButtonAutomationId": "ReadRaster", "Pattern": "Invoke", "SeparateProcess": True}:
                raise RuntimeError("Unexpected external UI Automation receipt.")
            return observed
        finally:
            if app.poll() is None:
                app.terminate()
                app.wait(timeout=5)


def run(dotnet, work, fixture, *, external_uia=False):
    if os.name != "nt":
        raise ValueError("WPF acceptance requires Windows")
    dotnet = dotnet.resolve(strict=True)
    if dotnet.name.lower() != "dotnet.exe":
        raise ValueError("Select an installed dotnet.exe SDK CLI")
    fixture = fixture.resolve(strict=True)
    with fixture.open("rb") as handle:
        data = handle.read(65537)
    if len(data) > 65536:
        raise ValueError("Raster readback JSON exceeds 64 KiB")
    content = json.loads(data)
    if not isinstance(content, dict) or not isinstance(content.get("raster"), dict):
        raise ValueError("Expected a bounded GIS raster readback JSON")
    work = work.absolute()
    work.mkdir()
    project = work / "ToolchainSmoke"
    nuget = work / "NuGet.Config"
    nuget.write_text("<configuration><packageSources><clear /></packageSources>"
                     "<auditSources><clear /></auditSources></configuration>\n", encoding="utf-8")
    environment = dict(os.environ, DOTNET_CLI_HOME=str(work / "dotnet-home"),
                       DOTNET_CLI_TELEMETRY_OPTOUT="1", DOTNET_NOLOGO="1",
                       DOTNET_CLI_WORKLOAD_UPDATE_NOTIFY_DISABLE="true",
                       DOTNET_GENERATE_ASPNET_CERTIFICATE="false",
                       DOTNET_ADD_GLOBAL_TOOLS_TO_PATH="0",
                       DOTNET_CLI_DO_NOT_USE_MSBUILD_SERVER="1",
                       NUGET_PACKAGES=str(work / "nuget-packages"), MSBUILDDISABLENODEREUSE="1")
    steps = {}

    def execute(stage, arguments, timeout=90):
        with (work / (stage + ".log")).open("xb") as log:
            result = subprocess.run([str(dotnet), *map(str, arguments)], cwd=work,
                                    env=environment, stdin=subprocess.DEVNULL, stdout=log,
                                    stderr=subprocess.STDOUT, timeout=timeout,
                                    creationflags=subprocess.CREATE_NO_WINDOW, check=False)
        steps[stage] = result.returncode
        if result.returncode:
            raise RuntimeError(f"{stage} exited {result.returncode}. See {stage}.log.")

    execute("sdk", ["--version"])
    execute("template", ["new", "wpf", "--name", "ToolchainSmoke", "--no-update-check",
                          "--no-restore", "--output", project])
    for name in ("MainWindow.xaml", "MainWindow.xaml.cs"):
        shutil.copyfile(FIXTURE / name, project / name)
    local_input = work / "raster-input.json"
    local_input.write_bytes(data)
    project_file = project / "ToolchainSmoke.csproj"
    configuration = ET.parse(project_file)
    framework = configuration.findtext(".//TargetFramework")
    if not framework or configuration.findtext(".//UseWPF") != "true":
        raise RuntimeError("The installed template did not produce a WPF project")
    execute("restore", ["restore", project_file, "--configfile", nuget, "--disable-build-servers"])
    execute("build", ["build", project_file, "--no-restore", "--disable-build-servers"])
    assembly = project / "bin" / "Debug" / framework / "ToolchainSmoke.dll"
    readback = work / "application-receipt.json"
    client = None
    if external_uia:
        driver_dir = work / "ExternalUia"
        driver_dir.mkdir()
        driver_project = driver_dir / "ExternalUia.csproj"
        project_xml = ET.Element("Project", {"Sdk": "Microsoft.NET.Sdk"})
        properties = ET.SubElement(project_xml, "PropertyGroup")
        ET.SubElement(properties, "TargetFramework").text = framework
        ET.SubElement(properties, "UseWPF").text = "true"
        ET.SubElement(properties, "OutputType").text = "Exe"
        ET.ElementTree(project_xml).write(driver_project, encoding="utf-8")
        shutil.copyfile(FIXTURE / "InvokeWindow.cs", driver_dir / "InvokeWindow.cs")
        execute("uia-restore", ["restore", driver_project, "--configfile", nuget, "--disable-build-servers"])
        execute("uia-build", ["build", driver_project, "--no-restore", "--disable-build-servers"])
        driver = driver_dir / "bin" / "Debug" / framework / "ExternalUia.dll"
        client = external_invoke(dotnet, assembly, driver, local_input, readback, work, environment)
        steps["launch"] = 0
    else:
        execute("launch", [assembly, "--smoke", local_input, readback], timeout=30)
    receipt = json.loads(readback.read_text(encoding="utf-8"))
    if (receipt["NativeWindowLoaded"] is not True or receipt["AutomationPattern"] != "Invoke"
            or receipt["Clicks"] != 1 or receipt["Raster"] != EXPECTED
            or receipt["Label"] != "EPSG:4326 | 2 x 2 | 3 valid cells"):
        raise RuntimeError("Native window, action or raster receipt did not match expectations")
    if local_input.read_bytes() != data or fixture.read_bytes() != data:
        raise RuntimeError("Input raster evidence changed")
    result = {"status": "PASS", "sdk": (work / "sdk.log").read_text(encoding="utf-8-sig").strip(),
              "framework": framework, "stages": steps, "window_readback": receipt,
              "assembly_sha256": hashlib.sha256(assembly.read_bytes()).hexdigest(),
              "input_sha256": hashlib.sha256(data).hexdigest()}
    if client is not None:
        result["external_uia"] = client
    with (work / "WPF_ACCEPTANCE.json").open("x", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dotnet", type=Path, required=True)
    parser.add_argument("--work", type=Path, required=True, help="New scratch directory")
    parser.add_argument("--raster-readback", type=Path, required=True)
    parser.add_argument("--external-uia", action="store_true", help="Use Windows UI Automation from a separate process")
    args = parser.parse_args()
    try:
        report = run(args.dotnet, args.work, args.raster_readback, external_uia=args.external_uia)
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as error:
        parser.exit(1, str(error) + "\n")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
