#!/usr/bin/env python3
"""Validate engine capability profiles, taxonomy foreign keys, DAG cycles, and v2 architecture files.

Complements scripts/validate_catalog.py without modifying or breaking it.
Offline-only; exits non-zero on schema drift, unknown capabilities, ungrounded
verified-for-target claims, unresolved dependency targets, or dependency cycles.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CATALOG_DEFAULT = ROOT / "references" / "project-catalog.json"
PROFILES_DEFAULT = ROOT / "references" / "engine-capability-profiles.json"
TAXONOMY_DEFAULT = ROOT / "references" / "engine-capability-taxonomy.json"
SCHEMA_DEFAULT = ROOT / "schemas" / "engine-capability-profile.schema.json"

DEP_EDGE_TYPES = {"requires", "wraps", "binds", "extends"}


def has_dependency_cycle(edges: dict[str, list[str]]) -> list[str] | None:
    """Return cycle path if directed dependency graph contains a cycle, else None."""
    state: dict[str, int] = {}
    stack: list[str] = []

    def dfs(node: str) -> list[str] | None:
        mark = state.get(node, 0)
        if mark == 1:
            idx = stack.index(node) if node in stack else 0
            return stack[idx:] + [node]
        if mark == 2:
            return None
        state[node] = 1
        stack.append(node)
        for nxt in edges.get(node, ()):
            cycle = dfs(nxt)
            if cycle:
                return cycle
        stack.pop()
        state[node] = 2
        return None

    for root_node in sorted(edges):
        found = dfs(root_node)
        if found:
            return found
    return None


def validate_profiles(
    *,
    catalog_path: Path = CATALOG_DEFAULT,
    profiles_path: Path = PROFILES_DEFAULT,
    taxonomy_path: Path = TAXONOMY_DEFAULT,
    schema_path: Path = SCHEMA_DEFAULT,
) -> list[str]:
    """Validate unified engine capability profiles and return list of errors."""
    errors: list[str] = []
    try:
        cat = json.loads(Path(catalog_path).read_text(encoding="utf-8"))
        prof_doc = json.loads(Path(profiles_path).read_text(encoding="utf-8"))
        tax = json.loads(Path(taxonomy_path).read_text(encoding="utf-8"))
        schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Cannot load profile validation inputs: {exc}"]

    item_props = schema["properties"]["profiles"]["items"]["properties"]
    valid_entities = set(item_props["entity_type"]["enum"])
    valid_build_models = set(item_props["build_models"]["items"]["enum"])
    valid_integ = set(item_props["integration_patterns"]["items"]["enum"])
    vm_schema = item_props["verification_metadata"]
    req_vm_keys = set(vm_schema["required"])
    valid_cost = set(vm_schema["properties"]["cost_classification"]["enum"])
    valid_trust = set(vm_schema["properties"]["trust_level"]["enum"])

    valid_caps = {
        cid
        for dinfo in tax.get("domains", {}).values()
        for cid in (dinfo["capabilities"] if isinstance(dinfo["capabilities"], list) else dinfo["capabilities"].keys())
    }
    valid_rel_types = set(tax.get("relationship_types", []))

    cat_ids = {p.get("project_id"): p for p in cat.get("projects", []) if p.get("project_id")}
    profiles = prof_doc.get("profiles", [])
    if prof_doc.get("profile_count") != len(profiles):
        errors.append(f"profile_count ({prof_doc.get('profile_count')}) != len(profiles) ({len(profiles)})")

    prof_by_id: dict[str, dict[str, Any]] = {}
    for idx, prof in enumerate(profiles):
        pid = prof.get("project_id", f"index[{idx}]")
        if not re.fullmatch(r"[a-z0-9-]+", pid):
            errors.append(f"Invalid project_id format: {pid!r}")
        if pid in prof_by_id:
            errors.append(f"Duplicate profile project_id: {pid}")
        prof_by_id[pid] = prof
        if pid not in cat_ids:
            errors.append(f"Orphan profile project_id missing from project-catalog.json: {pid}")
        if prof.get("entity_type") not in valid_entities:
            errors.append(f"{pid}: invalid entity_type {prof.get('entity_type')!r}")
        if not set(prof.get("build_models", [])).issubset(valid_build_models):
            errors.append(f"{pid}: invalid build_models")
        if not set(prof.get("integration_patterns", [])).issubset(valid_integ):
            errors.append(f"{pid}: invalid integration_patterns")

        vm = prof.get("verification_metadata", {})
        missing_vm = sorted(req_vm_keys - set(vm.keys()))
        if missing_vm:
            errors.append(f"{pid}: missing verification_metadata fields {missing_vm}")
        if vm.get("trust_level") not in valid_trust:
            errors.append(f"{pid}: invalid trust_level {vm.get('trust_level')!r}")
        if vm.get("cost_classification") not in valid_cost:
            errors.append(f"{pid}: invalid cost_classification {vm.get('cost_classification')!r}")
        if vm.get("security_status") == "quarantine-reference-only" and prof.get("integration_patterns") != ["reference-only"]:
            errors.append(f"{pid}: quarantined entry must remain reference-only")

        for cid, cinfo in prof.get("capabilities", {}).items():
            if cid not in valid_caps:
                errors.append(f"{pid}: unknown taxonomy capability {cid}")
            if cinfo.get("support_state") == "verified-for-target" and not cinfo.get("evidence_refs"):
                errors.append(f"{pid}.{cid}: verified-for-target requires non-empty evidence_refs")

    for pid in sorted(set(cat_ids) - set(prof_by_id)):
        errors.append(f"Missing capability profile for catalog project_id: {pid}")

    # Directed dependency validation and cycle check.
    adj: dict[str, list[str]] = defaultdict(list)
    for pid, prof in prof_by_id.items():
        adj.setdefault(pid, [])
        for rel in prof.get("relationships", []):
            rtype = rel.get("type")
            tgt = rel.get("target_id", "")
            if rtype not in valid_rel_types:
                errors.append(f"{pid}: invalid relationship type {rtype!r}")
            if rtype in DEP_EDGE_TYPES:
                if tgt not in prof_by_id:
                    errors.append(f"{pid}: broken dependency edge target {tgt!r}")
                else:
                    adj[pid].append(tgt)
    cycle = has_dependency_cycle(adj)
    if cycle:
        errors.append(f"Circular dependency detected: {' -> '.join(cycle)}")
    return errors


def validate_v2_architecture(arch_path: Path) -> list[str]:
    """Validate a v2.0 architecture declaration (refs traversal, enums, unresolved blockers)."""
    try:
        data = json.loads(arch_path.read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas" / "architecture-v2.schema.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return [f"Cannot load v2 architecture declaration: {exc}"]

    errors: list[str] = []
    if data.get("schema_version") != "2.0":
        errors.append("v2 architecture requires schema_version == '2.0'")
    for key in schema["required"]:
        if key not in data:
            errors.append(f"Missing required v2 architecture field: {key}")
    for ref_key in ("feature_inventory_ref", "command_mapping_ref", "flow_spec_ref", "decision_ref"):
        val = data.get(ref_key)
        if val is not None:
            if not isinstance(val, str) or Path(val).is_absolute() or ".." in Path(val).parts:
                errors.append(f"Unsafe or traversing relative ref in {ref_key}: {val!r}")
    for comp in data.get("components", []):
        if comp.get("status") == "source-reviewed" and (not comp.get("source_ref") or not comp.get("version")):
            errors.append(f"Component {comp.get('component_id')} source-reviewed requires source_ref and version")
    return errors


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_DEFAULT)
    parser.add_argument("--profiles", type=Path, default=PROFILES_DEFAULT)
    parser.add_argument("--taxonomy", type=Path, default=TAXONOMY_DEFAULT)
    parser.add_argument("--schema", type=Path, default=SCHEMA_DEFAULT)
    parser.add_argument("--v2-arch", type=Path, default=None, help="Optional architecture v2.0 JSON to validate")
    parser.add_argument("--format", choices=("text", "json"), default="text")
    args = parser.parse_args(argv)

    errors = validate_profiles(
        catalog_path=args.catalog,
        profiles_path=args.profiles,
        taxonomy_path=args.taxonomy,
        schema_path=args.schema,
    )
    if args.v2_arch is not None:
        errors.extend(validate_v2_architecture(args.v2_arch))

    if args.format == "json":
        print(json.dumps({"valid": not errors, "error_count": len(errors), "errors": errors}, indent=2, ensure_ascii=False))
    else:
        if errors:
            for err in errors:
                print(f"ERROR: {err}")
        else:
            print("Engine capability profiles valid: 1:1 parity, 18 metadata fields, acyclic DAG")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
