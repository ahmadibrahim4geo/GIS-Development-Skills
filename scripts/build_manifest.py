#!/usr/bin/env python3
"""Build/check derived inventory, and synchronize current README and HTML counters."""
import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "references/repository-manifest.json"


def derived(root=ROOT):
    root = Path(root)
    projects = json.loads((root / "references/project-catalog.json").read_text(encoding="utf-8"))["projects"]
    apis = json.loads((root / "references/free-geospatial-apis.json").read_text(encoding="utf-8"))["services"]
    changelog = (root / "CHANGELOG.md").read_text(encoding="utf-8")
    match = re.search(r"(?m)^## (\d+\.\d+\.\d+)\s", changelog)
    if not match:
        raise ValueError("No documentation revision heading in CHANGELOG")
    return {
        "schema_version": "1.0",
        "documentation_version": match.group(1),
        "skill_count": len(list((root / "skills").glob("*/SKILL.md"))),
        "reference_count": len(projects),
        "api_count": len(apis),
        "generated_from": ["skills/*/SKILL.md", "references/project-catalog.json",
                           "references/free-geospatial-apis.json"],
        "note": "Derived source inventory. Documentation version is baseline; unreleased changes remain in CHANGELOG."
    }


def synchronize_text(root, data, write=False):
    checks = []
    en = root / "README.md"
    ar = root / "README.ar.md"
    index = root / "index.html"
    replacements = [
        (en, r"(<strong>)(\d+)( installable GIS skills</strong>)", data["skill_count"]),
        (ar, r"(تشمل \*\*)(\d+)( مهارة قابلة للتثبيت\*\*)", data["skill_count"]),
        (index, r'(<div class="stat"><strong>)(\d+)(</strong><span data-i18n="statSkill">)', data["skill_count"]),
        (index, r'(<strong id="projectsCount">)(\d+)(</strong>)', data["reference_count"]),
        (index, r'(<strong id="apisCount">)(\d+)(</strong>)', data["api_count"]),
    ]
    changes = {}
    for path, pattern, number in replacements:
        value = changes.get(path, path.read_text(encoding="utf-8"))
        revised, count = re.subn(pattern, lambda match: match.group(1) + str(number) + match.group(3), value, count=1)
        if count != 1:
            checks.append("Expected exactly one live counter anchor in " + str(path))
        elif revised != value and not write:
            checks.append("Inventory count drift in " + str(path) + " (" + pattern + ")")
        changes[path] = revised
    if write:
        for path, value in changes.items():
            path.write_text(value, encoding="utf-8")
    return checks


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--check", action="store_true", help="fail when manifest or live counters drift")
    p.add_argument("--root", type=Path, default=ROOT)
    args = p.parse_args(argv)
    root = args.root
    data = derived(root)
    target = root / "references/repository-manifest.json"
    expected = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
    problems = synchronize_text(root, data, write=not args.check)
    if args.check:
        if not target.exists() or target.read_text(encoding="utf-8") != expected:
            problems.append("Derived manifest is stale")
    else:
        target.write_text(expected, encoding="utf-8")
    for item in problems:
        print("ERROR:", item)
    if problems:
        return 1
    print("Manifest valid: {} skills / {} references / {} APIs".format(
        data["skill_count"], data["reference_count"], data["api_count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
