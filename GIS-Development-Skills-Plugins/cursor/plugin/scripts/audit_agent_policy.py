#!/usr/bin/env python3
"""Deterministic audit for AAREF root constitution, rule registry, and ownership links.

Performs static schema, anchor, ownership, and conflict checks only. It does
NOT parse free-form semantic intent, run live LLMs, or grant host permissions.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
VALID_STRENGTHS = {"MUST", "SHOULD", "MAY"}
REQUIRED_RULE_FIELDS = (
    "rule_id",
    "canonical_source",
    "agents_anchor",
    "scope",
    "trigger",
    "strength",
    "owner",
    "enforcement",
    "evidence",
    "test_ids",
    "legacy_mapping",
)
HEADER_RX = re.compile(r"^#{1,6}\s+(.+?)\s*$")
MD_LINK_RX = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def github_slug(heading: str) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", heading)
    text = re.sub(r"<[^>]+>", "", text).strip().lower().replace(" ", "-")
    return "".join(char for char in text if char in "-_" or unicodedata.category(char)[0] in "LMN")


def extract_anchors(markdown_text: str) -> set[str]:
    anchors = set()
    in_fence = False
    for line in markdown_text.splitlines():
        if line.strip().startswith("```") or line.strip().startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADER_RX.match(line)
        if m:
            anchors.add("#" + github_slug(m.group(1)))
    return anchors


def audit_policy(root: Path = ROOT) -> dict:
    errors: list[str] = []
    warnings: list[str] = []

    agents_path = root / "AGENTS.md"
    registry_path = root / "references" / "agent-reasoning" / "rule-registry.json"
    levels_path = root / "references" / "agent-reasoning" / "reasoning-levels.json"
    skills_dir = root / "skills"

    if not agents_path.is_file():
        return {"status": "FAIL", "errors": ["Missing root AGENTS.md"], "warnings": []}

    agents_text = agents_path.read_text(encoding="utf-8")
    if "](plans/" in agents_text:
        errors.append("AGENTS.md must not use Markdown links pointing to plans/ (excluded from self-contained ZIP)")

    agents_anchors = extract_anchors(agents_text)
    known_skills = {p.parent.name for p in skills_dir.glob("*/SKILL.md")} if skills_dir.is_dir() else set()
    if not known_skills:
        errors.append("No discoverable skills/*/SKILL.md found")

    if not registry_path.is_file():
        errors.append("Missing references/agent-reasoning/rule-registry.json")
        rule_count = 0
    else:
        reg = json.loads(registry_path.read_text(encoding="utf-8"))
        rules = reg.get("rules")
        if not isinstance(rules, list) or not rules:
            errors.append("rule-registry.json rules must be a nonempty array")
            rule_count = 0
        else:
            rule_count = len(rules)
            seen_ids: set[str] = set()
            for idx, rule in enumerate(rules):
                pref = f"rules[{idx}]"
                if not isinstance(rule, dict):
                    errors.append(f"{pref} must be an object")
                    continue
                for field in REQUIRED_RULE_FIELDS:
                    if field not in rule:
                        errors.append(f"{pref} missing field '{field}'")
                rid = rule.get("rule_id")
                if not isinstance(rid, str) or not rid.strip():
                    errors.append(f"{pref}.rule_id must be nonempty")
                elif rid in seen_ids:
                    errors.append(f"Duplicate rule_id: {rid}")
                else:
                    seen_ids.add(rid)

                if rule.get("strength") not in VALID_STRENGTHS:
                    errors.append(f"{rid or pref}: invalid strength '{rule.get('strength')}'")

                owner = rule.get("owner")
                if owner not in known_skills:
                    errors.append(f"{rid or pref}: unknown owner skill '{owner}'")

                anchor = rule.get("agents_anchor", "")
                if not isinstance(anchor, str) or anchor not in agents_anchors:
                    errors.append(f"{rid or pref}: AGENTS.md missing heading anchor '{anchor}'")

                src = rule.get("canonical_source", "")
                if not isinstance(src, str) or not src.strip():
                    errors.append(f"{rid or pref}: missing canonical_source")
                else:
                    src_file_rel, _, frag = src.partition("#")
                    src_file = root / src_file_rel
                    if not src_file.is_file():
                        errors.append(f"{rid or pref}: canonical_source file does not exist: {src_file_rel}")
                    elif frag and src_file.suffix.lower() == ".md":
                        src_anchors = extract_anchors(src_file.read_text(encoding="utf-8"))
                        if "#" + frag not in src_anchors:
                            errors.append(f"{rid or pref}: missing anchor #{frag} in {src_file_rel}")

                for list_field in ("enforcement", "evidence", "test_ids", "legacy_mapping"):
                    val = rule.get(list_field)
                    if not isinstance(val, list) or not val:
                        errors.append(f"{rid or pref}.{list_field} must be a non-empty list")
                for tid in rule.get("test_ids", []):
                    if isinstance(tid, str) and tid.endswith(".py"):
                        if not ((root / "tests" / tid).is_file() or (root / "scripts" / tid).is_file() or (root / "plugin-system" / "tests" / tid).is_file()):
                            errors.append(f"{rid or pref}: test_ids target missing: {tid}")

    if not levels_path.is_file():
        errors.append("Missing references/agent-reasoning/reasoning-levels.json")
    else:
        levels_data = json.loads(levels_path.read_text(encoding="utf-8"))
        for lv in ("L0", "L1", "L2", "L3", "L4", "L5"):
            if lv not in levels_data.get("reasoning_levels", {}):
                errors.append(f"reasoning-levels.json missing level {lv}")
        for imp in ("I0", "I1", "I2", "I3", "I4"):
            if imp not in levels_data.get("impact_classes", {}):
                errors.append(f"reasoning-levels.json missing impact class {imp}")
        for rm in ("INDEPENDENT_AGENT", "HUMAN_REVIEW", "SELF_REVIEW", "NOT_RUN"):
            if rm not in levels_data.get("review_modes", []):
                errors.append(f"reasoning-levels.json missing review_mode {rm}")
        methods = levels_data.get("cognitive_methods", [])
        if len(methods) != 18 or len(set(methods)) != 18:
            errors.append("reasoning-levels.json must enumerate 18 unique cognitive_methods")
        dims = levels_data.get("classification_dimensions", [])
        if len(dims) != 10 or len(set(dims)) != 10:
            errors.append("reasoning-levels.json must enumerate 10 unique classification_dimensions")

    # Verify all local Markdown links AND fragments inside AGENTS.md and references/agent-reasoning/*.md
    anchor_cache: dict[Path, set[str]] = {agents_path: agents_anchors}
    md_docs = [agents_path]
    ar_dir = root / "references" / "agent-reasoning"
    if ar_dir.is_dir():
        md_docs.extend(sorted(ar_dir.glob("*.md")))
    for md_doc in md_docs:
        doc_text = md_doc.read_text(encoding="utf-8")
        if "](plans/" in doc_text:
            errors.append(f"{md_doc.relative_to(root).as_posix()}: forbidden plans/ link")
        for target in MD_LINK_RX.findall(doc_text):
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            rel_path, _, frag = target.partition("#")
            dest = md_doc if not rel_path else (md_doc.parent / rel_path).resolve()
            if rel_path.startswith(("plans/", "reports/", "dist/", ".agent-development-log/")):
                errors.append(f"{md_doc.relative_to(root).as_posix()} links non-bundled path: {target}")
            elif not dest.exists():
                errors.append(f"{md_doc.relative_to(root).as_posix()} broken link target: {target}")
            elif frag and dest.suffix.lower() == ".md":
                if dest not in anchor_cache:
                    anchor_cache[dest] = extract_anchors(dest.read_text(encoding="utf-8"))
                if "#" + frag not in anchor_cache[dest]:
                    errors.append(f"{md_doc.relative_to(root).as_posix()} missing fragment #{frag} in {target}")

    if (root / "references" / "repository-manifest.json").is_file() and (root / "scripts" / "audit_skill_graph.py").is_file():
        import importlib.util
        gspec = importlib.util.spec_from_file_location("_audit_skill_graph", root / "scripts" / "audit_skill_graph.py")
        gmod = importlib.util.module_from_spec(gspec)
        gspec.loader.exec_module(gmod)
        graph_res = gmod.audit(root)
        for issue in graph_res.get("issues", []):
            errors.append("skill_graph: " + issue)

    return {
        "status": "PASS" if not errors else "FAIL",
        "rule_count": rule_count,
        "skill_count": len(known_skills),
        "errors": errors,
        "warnings": warnings,
        "note": "Static policy structure/link audit only; does not prove live model reasoning or host enforcement.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)
    report = audit_policy(args.root.resolve())
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"Policy audit {report['status']}: rules={report['rule_count']}, skills={report['skill_count']}")
        for err in report["errors"]:
            print("ERROR:", err)
        for warn in report["warnings"]:
            print("WARN:", warn)
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
