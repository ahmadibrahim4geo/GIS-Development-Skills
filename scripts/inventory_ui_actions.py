#!/usr/bin/env python3
"""Safe read-only static inventory for Qt Designer .ui XML action declarations.

Blocks symlinks outside root, path traversal, XML files > 5 MiB, and <!DOCTYPE /
<!ENTITY declarations. Extracts QAction entries, shortcuts, tooltips, icons, and
menu/toolbar placements with handlers_verified=False and dynamic_actions_verified=False.
"""

from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any


MAX_UI_FILE_BYTES = 5 * 1024 * 1024


def _read_property_map(element: ET.Element) -> dict[str, str]:
    props: dict[str, str] = {}
    for prop in element.findall("property"):
        name = prop.get("name", "")
        if not name:
            continue
        if name == "iconset":
            normaloff = prop.find(".//normaloff")
            if normaloff is not None and (normaloff.text or "").strip():
                props["icon"] = normaloff.text.strip()
            else:
                iconset = prop.find("iconset")
                if iconset is not None and iconset.get("resource"):
                    props["icon"] = iconset.get("resource", "")
        else:
            string_el = prop.find("string")
            bool_el = prop.find("bool")
            if string_el is not None and string_el.text is not None:
                props[name] = string_el.text
            elif bool_el is not None and bool_el.text is not None:
                props[name] = bool_el.text
    return props


def _collect_placements(widget: ET.Element, parent_trail: list[str], out: dict[str, list[str]]) -> None:
    cls = widget.get("class", "QWidget")
    name = widget.get("name", "")
    node_label = f"{cls}:{name}" if name else cls
    trail = parent_trail + [node_label]

    for child in list(widget):
        if child.tag == "addaction":
            act_name = child.get("name", "")
            if act_name and act_name != "separator":
                out.setdefault(act_name, []).append(" > ".join(trail))
        elif child.tag == "widget":
            _collect_placements(child, trail, out)


def inspect_qt_ui(ui_path: Path, *, root: Path | None = None) -> dict[str, Any]:
    """Parse one Qt .ui file safely and extract static action declarations."""
    path = Path(ui_path)
    base = Path(root).resolve() if root is not None else path.resolve().parent

    if path.is_symlink():
        raise ValueError(f"Refusing symlink .ui input: {path}")
    resolved = path.resolve()
    if not resolved.is_relative_to(base):
        raise ValueError(f"Path traversal escapes allowed root: {ui_path}")
    if not resolved.is_file():
        raise ValueError(f"Missing .ui file: {ui_path}")
    size = resolved.stat().st_size
    if size > MAX_UI_FILE_BYTES:
        raise ValueError(f".ui file exceeds {MAX_UI_FILE_BYTES} byte limit ({size} bytes): {resolved.name}")

    text = resolved.read_text(encoding="utf-8-sig")
    upper_head = text.upper()
    if "<!DOCTYPE" in upper_head or "<!ENTITY" in upper_head:
        raise ValueError("Refusing XML with DTD or ENTITY declaration (XXE guard)")

    xml_root = ET.fromstring(text)
    placements: dict[str, list[str]] = {}
    top_widget = xml_root.find("widget")
    if top_widget is not None:
        _collect_placements(top_widget, [], placements)

    declared_actions: list[dict[str, Any]] = []
    for action in sorted(xml_root.findall(".//action"), key=lambda el: el.get("name", "")):
        act_name = action.get("name", "")
        if not act_name:
            continue
        props = _read_property_map(action)
        declared_actions.append(
            {
                "action_id": act_name,
                "text": props.get("text", ""),
                "tooltip": props.get("toolTip", ""),
                "shortcut": props.get("shortcut", ""),
                "icon": props.get("icon", ""),
                "checkable": props.get("checkable", "false").lower() == "true",
                "placements": placements.get(act_name, []),
                "handler_state": "unresolved",
                "runtime_status": "NOT RUN",
            }
        )

    connections = []
    for conn in xml_root.findall(".//connections/connection"):
        connections.append(
            {
                "sender": (conn.findtext("sender") or "").strip(),
                "signal": (conn.findtext("signal") or "").strip(),
                "receiver": (conn.findtext("receiver") or "").strip(),
                "slot": (conn.findtext("slot") or "").strip(),
            }
        )

    return {
        "source_file": resolved.relative_to(base).as_posix(),
        "action_count": len(declared_actions),
        "actions": declared_actions,
        "declared_connections": connections,
        "handlers_verified": False,
        "dynamic_actions_verified": False,
        "native_ui_tested": False,
    }


def inventory_tree(scan_root: Path) -> dict[str, Any]:
    """Scan all .ui files safely under scan_root."""
    base = Path(scan_root).resolve()
    if not base.is_dir():
        raise ValueError(f"Root directory does not exist: {scan_root}")

    files = []
    errors = []
    for path in sorted(base.rglob("*.ui"), key=lambda p: p.as_posix()):
        try:
            files.append(inspect_qt_ui(path, root=base))
        except (ValueError, OSError, UnicodeError, ET.ParseError) as exc:
            errors.append({"source_file": str(path), "error": str(exc)})

    total_actions = sum(f["action_count"] for f in files)
    return {
        "schema_version": "1.0",
        "kind": "static_qt_ui_inventory",
        "files_scanned": len(files),
        "action_count": total_actions,
        "handlers_verified": False,
        "dynamic_actions_verified": False,
        "native_ui_tested": False,
        "files": files,
        "errors": errors,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Root directory containing .ui files")
    parser.add_argument("--ui-path", type=Path, default=None, help="Specific single .ui file relative to --root or inside --root")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    try:
        if args.ui_path is not None:
            candidate = args.ui_path if args.ui_path.is_absolute() else (args.root / args.ui_path)
            report: dict[str, Any] = inspect_qt_ui(candidate, root=args.root)
            has_errors = False
        else:
            report = inventory_tree(args.root)
            has_errors = bool(report["errors"])
    except (ValueError, OSError, UnicodeError, ET.ParseError) as exc:
        if args.format == "json":
            print(json.dumps({"errors": [{"error": str(exc)}], "handlers_verified": False, "dynamic_actions_verified": False}, indent=2))
        else:
            print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"# Qt UI Action Inventory (`handlers_verified={report['handlers_verified']}`)")
        if "files" in report:
            print(f"- Files: {report['files_scanned']} | Actions: {report['action_count']} | Errors: {len(report['errors'])}")
        else:
            print(f"- File: `{report['source_file']}` | Actions: {report['action_count']}")
    return 1 if has_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
