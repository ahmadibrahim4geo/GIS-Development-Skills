"""Bounded fixture snapshots and independent readback for project test runs."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import tempfile

if __package__:
    from .project_structure import next_id, numbered, safe_path, walk_project
    from .verify_completion import read_json
else:
    from project_structure import next_id, numbered, safe_path, walk_project
    from verify_completion import read_json


MAX_FILE = 64 * 1024 * 1024
MAX_TOTAL = 256 * 1024 * 1024
MAX_INPUTS = 100
MAX_INVENTORY = 500
MAX_RECEIPT = 4 * 1024 * 1024
FORMATS = {
    ".asc": "ASCII grid", ".geojson": "GeoJSON", ".json": "JSON",
    ".tif": "TIFF", ".tiff": "TIFF", ".shp": "Shapefile", ".shx": "Shapefile index",
    ".dbf": "dBASE", ".prj": "CRS sidecar", ".cpg": "Encoding sidecar", ".gpkg": "GeoPackage",
    ".kml": "KML", ".kmz": "KMZ", ".csv": "CSV", ".nc": "NetCDF",
    ".hdf": "HDF", ".h5": "HDF5", ".las": "LAS", ".laz": "LAZ",
}
MTL_FIELDS = {"SPACECRAFT_ID", "SENSOR_ID", "COLLECTION_NUMBER", "PROCESSING_LEVEL",
              "DATA_TYPE", "DATE_ACQUIRED", "MAP_PROJECTION", "UTM_ZONE",
              "REFLECTIVE_LINES", "REFLECTIVE_SAMPLES", "GRID_CELL_SIZE_REFLECTIVE"}
ASCII_FIELDS = {"ncols", "nrows", "xllcorner", "yllcorner", "xllcenter", "yllcenter",
                "cellsize", "nodata_value"}


def format_hint(path):
    if path.name.upper().endswith("_MTL.TXT"):
        return "Landsat MTL"
    return FORMATS.get(path.suffix.casefold())


def metadata(path, hint):
    info = {}
    try:
        if hint == "ASCII grid":
            with path.open("rb") as handle:
                for _ in range(8):
                    cells = handle.readline(256).decode("ascii").split()
                    if len(cells) != 2 or cells[0].casefold() not in ASCII_FIELDS:
                        break
                    info[cells[0].casefold()] = cells[1]
        elif hint == "Landsat MTL" and path.stat().st_size <= 256 * 1024:
            with path.open("rb") as handle:
                text = handle.read(256 * 1024).decode("utf-8-sig")
            for line in text.splitlines():
                key, _, value = line.partition("=")
                if key.strip() in MTL_FIELDS and len(value) < 100:
                    info[key.strip()] = value.strip().strip('"')
        elif hint in {"GeoJSON", "JSON"}:
            data = read_json(path)
            if isinstance(data, dict) and data.get("type") in ("FeatureCollection", "Feature"):
                if isinstance(data.get("features"), list):
                    info["feature_count"] = len(data["features"])
                if isinstance(data.get("crs"), dict):
                    crs = data["crs"].get("properties")
                    if isinstance(crs, dict) and isinstance(crs.get("name"), str):
                        info["declared_crs"] = crs["name"][:160]
                if isinstance(data.get("stac_version"), str):
                    info["stac_version"] = data["stac_version"][:40]
    except (OSError, ValueError, RecursionError):
        return {"metadata_status": "UNAVAILABLE"}
    return info


def inventory(root):
    data_root = safe_path(root, "testing data")
    if not data_root.is_dir():
        raise ValueError("Run init first to create the user-owned testing data directory")
    entries, considered = [], 0
    for directory, _, names in walk_project(data_root, max_depth=8):
        for name in names:
            if considered >= MAX_INVENTORY:
                return {"files": entries, "truncated": True, "read_only": True}
            considered += 1
            path = directory / name
            hint = format_hint(path)
            item = path.lstat()
            if hint and stat.S_ISREG(item.st_mode):
                entries.append({"path": path.relative_to(data_root).as_posix(),
                                "format_hint": hint, "bytes": item.st_size,
                                "metadata": metadata(path, hint)})
    return {"files": entries, "truncated": False, "read_only": True}


def digest(path, copy=None):
    if not stat.S_ISREG(path.lstat().st_mode):
        raise ValueError("Evidence must be an ordinary file")
    total = 0
    checksum = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            total += len(block)
            if total > MAX_FILE:
                raise ValueError("Fixture or output exceeds the 64 MiB bound")
            checksum.update(block)
            if copy is not None:
                copy.write(block)
    return checksum.hexdigest(), total


def expectations(path):
    data = read_json(path)
    checks = data.get("checks") if isinstance(data, dict) else None
    if not isinstance(checks, list) or not 1 <= len(checks) <= MAX_INPUTS:
        raise ValueError("Expected evidence requires a nonempty checks list")
    for check in checks:
        if (not isinstance(check, dict) or set(check) != {"artifact", "comparison", "expected"}
                or check["comparison"] not in ("json", "sha256")
                or not isinstance(check["artifact"], str)):
            raise ValueError("Each expected check needs artifact, comparison and expected")
        if check["comparison"] == "sha256" and (
                not isinstance(check["expected"], str) or not re.fullmatch(r"[0-9a-f]{64}", check["expected"])):
            raise ValueError("Expected SHA-256 must be 64 lowercase hexadecimal digits")
    return checks


def snapshot(data_root, run, inputs, license_note):
    fixtures, seen, total = [], set(), 0
    for requested in inputs:
        source = safe_path(data_root, requested)
        relative = source.relative_to(data_root).as_posix()
        hint = format_hint(source)
        normalized = relative.casefold() if os.name == "nt" else relative
        if not hint or not source.is_file() or normalized in seen:
            raise ValueError("Choose distinct, existing supported data files under testing data/")
        seen.add(normalized)
        size = source.stat().st_size
        if size > MAX_FILE or size + total > MAX_TOTAL:
            raise ValueError("Fixture snapshot size exceeds the per-file or aggregate bound")
        target = safe_path(run / "inputs", relative)
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open("xb") as handle:
            checksum, count = digest(source, handle)
        total += count
        if total > MAX_TOTAL or (checksum, count) != digest(target) or (checksum, count) != digest(source):
            raise ValueError("Fixture snapshot differs from source or exceeds its size bound")
        fixtures.append({"path": relative, "bytes": count, "sha256": checksum,
                         "format_hint": hint, "metadata": metadata(target, hint),
                         "provenance_license": license_note or "UNDECLARED"})
    return fixtures


def json_write(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, allow_nan=False, indent=2) + "\n", encoding="utf-8")


def render(manifest, receipt=None):
    title = manifest["title"]
    lines = [f'# Test run {manifest["id"]}: {title}', "",
             f'Status: {receipt["status"] if receipt else "NOT RUN"}', "",
             "Original inputs: ../../testing data/ (read-only). Copies: inputs/. Outputs: outputs/.",
             f'Independent checks declared: {len(manifest["checks"])}.']
    if receipt:
        lines.extend(["", f'Runtime: {receipt["runtime"]}', f'Command: {receipt["command"]}',
                      f'GIS semantics: {receipt["semantics"]}',
                      f'Original inputs match snapshot: {receipt["originals_unchanged"]}',
                      "", "Expected values, actual values, output hashes and readback outcomes are in RESULT.json."])
    else:
        lines.extend(["", "Expected results: see RUN.json if supplied.",
                      "Actual result, runtime and independent readback: NOT RUN."])
    return "\n".join(lines) + "\n"


def create(root, title, stem, inputs, expected_file, license_note):
    if not title.strip() or len(title) > 160 or any(ord(char) < 32 for char in title):
        raise ValueError("Test name must be a concise single line")
    if len(inputs) > MAX_INPUTS or (inputs and not expected_file):
        raise ValueError("Choose up to 100 fixtures and declare independent output expectations")
    data_root = safe_path(root, "testing data")
    if not data_root.is_dir():
        raise ValueError("Run init first to create the user-owned testing data directory")
    checks = expectations(safe_path(root, expected_file)) if expected_file else []
    results = safe_path(root, "testing results")
    results.mkdir(exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".prepare-", dir=results) as temp:
        pending = Path(temp) / "run"
        (pending / "inputs").mkdir(parents=True)
        (pending / "outputs").mkdir()
        for check in checks:
            check["artifact"] = safe_path(pending / "outputs", check["artifact"]).relative_to(pending / "outputs").as_posix()
        fixtures = snapshot(data_root, pending, inputs, license_note)
        lock = safe_path(root, "testing results/.allocation.lock")
        lock.mkdir()
        try:
            sequence = next_id(root, ("testing results",))
            relative = f"testing results/{sequence}_{stem}"
            final = safe_path(root, relative)
            manifest = {"id": sequence, "title": title.strip(), "status": "NOT RUN",
                        "created": datetime.now(timezone.utc).isoformat(), "inputs": fixtures, "checks": checks}
            json_write(pending / "RUN.json", manifest)
            (pending / "TEST_RUN.md").write_text(render(manifest), encoding="utf-8")
            if final.exists():
                raise FileExistsError(final)
            pending.rename(final)
        finally:
            lock.rmdir()
    return {"id": sequence, "run": relative, "status": "NOT RUN", "input_folder": "testing data",
            "output_folder": relative, "fixture_copy_folder": relative + "/inputs",
            "artifact_folder": relative + "/outputs"}


def output_check(output_root, check):
    try:
        path = safe_path(output_root, check["artifact"])
        checksum, size = digest(path)
        actual = read_json(path) if check["comparison"] == "json" else checksum
        if check["comparison"] == "json" and digest(path) != (checksum, size):
            raise ValueError("Output changed while it was being read")
        same = json.dumps(actual, sort_keys=True) == json.dumps(check["expected"], sort_keys=True)
        if check["comparison"] == "json" and size > 16 * 1024:
            actual = {"readback": "See artifact; large JSON value omitted from receipt"}
        return {**check, "actual": actual, "sha256": checksum, "bytes": size, "status": "PASS" if same else "FAIL"}
    except (OSError, ValueError, RecursionError) as error:
        return {**check, "actual": None, "status": "FAIL", "readback_error": type(error).__name__}


def original_matches(data_root, fixture):
    try:
        return digest(safe_path(data_root, fixture["path"])) == (fixture["sha256"], fixture["bytes"])
    except (OSError, ValueError):
        return False


def record(root, run_id, command, runtime, semantics):
    if not re.fullmatch(r"\d{4}", run_id):
        raise ValueError("Run ID must be four digits")
    if any(not value.strip() or len(value) > 2000 or any(ord(char) < 32 for char in value)
           for value in (command, runtime, semantics)):
        raise ValueError("Command, runtime and GIS semantics must be short nonempty single lines")
    results = safe_path(root, "testing results")
    matches = [path for path in numbered(results) if path.name.startswith(run_id + "_")]
    if len(matches) != 1:
        raise ValueError("Exactly one run with this ID is required")
    run = matches[0]
    manifest = read_json(safe_path(run, "RUN.json"), max_bytes=MAX_RECEIPT)
    if manifest.get("id") != run_id or not manifest.get("checks"):
        raise ValueError("The run does not have predeclared independent checks")
    output_root = safe_path(run, "outputs")
    copy_root = safe_path(run, "inputs")
    data_root = safe_path(root, "testing data")
    lock = safe_path(run, ".record.lock")
    lock.mkdir()
    try:
        result_path = safe_path(run, "RESULT.json")
        if result_path.exists():
            receipt = read_json(result_path, max_bytes=MAX_RECEIPT)
            if receipt.get("id") != run_id or receipt.get("status") not in ("PASS", "FAIL"):
                raise ValueError("Recorded result does not match the test run")
        else:
            checks = [output_check(output_root, check) for check in manifest["checks"]]
            originals = all(original_matches(data_root, fixture) for fixture in manifest["inputs"])
            copies = all(original_matches(copy_root, fixture) for fixture in manifest["inputs"])
            receipt = {"id": run_id, "recorded": datetime.now(timezone.utc).isoformat(), "command": command,
                       "runtime": runtime, "semantics": semantics, "originals_unchanged": originals,
                       "fixture_copies_unchanged": copies,
                       "status": "PASS" if originals and copies and all(check["status"] == "PASS" for check in checks)
                       else "FAIL", "checks": checks}
        summary = safe_path(run, "TEST_RUN.md")
        current = summary.read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory(prefix=".record-", dir=run) as temp:
            if not result_path.exists():
                pending = Path(temp) / "RESULT.json"
                json_write(pending, receipt)
                os.replace(pending, result_path)
            if current == render(manifest):
                pending = Path(temp) / "TEST_RUN.md"
                pending.write_text(render(manifest, receipt), encoding="utf-8")
                os.replace(pending, summary)
    finally:
        lock.rmdir()
    return receipt
