#!/usr/bin/env python3
"""Validate declared UI/engine flows offline. Never imports or executes a GIS host.

This checks graph/schema consistency, not source truth, runtime behavior or consent.
"""
import argparse
import json
from collections import defaultdict
from pathlib import Path

CHANGE_TYPES = {"ui-reorganization", "ui-shell-migration", "engine-integration", "engine-replacement"}
KINDS = {"request", "result", "error", "state", "persist", "readback", "progress", "cancel"}
EDGE_FIELDS = {"id", "from", "to", "kind", "contract", "execution", "thread_owner",
               "evidence_basis", "source_ref", "command_id"}
MAP_FIELDS = {"command_id", "before", "after", "handler", "shortcut", "enabled_state",
              "checked_state", "disposition", "reason"}


def text(value):
    return isinstance(value, str) and bool(value.strip()) and "\x00" not in value


def reachable(edges, start, end, kinds, required_kind=None):
    adjacency = defaultdict(set)
    for edge in edges:
        if edge["kind"] in kinds:
            adjacency[edge["from"]].add((edge["to"], edge["kind"]))
    seen, todo = set(), [(start, False)]
    while todo:
        node, used_required = todo.pop()
        if node == end and (required_kind is None or used_required):
            return True
        state = (node, used_required)
        if state not in seen:
            seen.add(state)
            todo.extend((target, used_required or kind == required_kind) for target, kind in adjacency[node]
                        if (target, used_required or kind == required_kind) not in seen)
    return False


def validate_flow(flow):
    if not isinstance(flow, dict):
        return ["Flow must be an object"]
    errors = []
    required = {"schema_version", "change_type", "nodes", "edges", "command_mappings", "persistence_required"}
    if required - set(flow) or set(flow) - (required | {"purpose", "async_policy", "source_commands"}):
        errors.append("Flow has missing or unknown fields")
    if flow.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    change = flow.get("change_type")
    if not isinstance(change, str) or change not in CHANGE_TYPES:
        errors.append("change_type is invalid")
    if type(flow.get("persistence_required")) is not bool:
        errors.append("persistence_required must be boolean")
    if "purpose" in flow and not text(flow["purpose"]):
        errors.append("purpose must be nonempty text")
    nodes = flow.get("nodes")
    if not isinstance(nodes, list) or not 1 <= len(nodes) <= 256:
        return errors + ["nodes must contain 1-256 declarations"]
    ids = set()
    for node in nodes:
        if (not isinstance(node, dict) or set(node) != {"id", "role"}
                or not text(node.get("id")) or not text(node.get("role"))):
            errors.append("Every node needs only a nonempty id and role")
        elif node["id"] in ids:
            errors.append("Duplicate node: " + node["id"])
        else:
            ids.add(node["id"])
    mappings = flow.get("command_mappings")
    if not isinstance(mappings, list) or len(mappings) > 2000:
        return errors + ["command_mappings must be an array of at most 2000 entries"]
    commands, excluded = set(), set()
    for mapping in mappings:
        if not isinstance(mapping, dict) or set(mapping) != MAP_FIELDS:
            errors.append("Command mapping has missing or unknown fields")
            continue
        ident = mapping["command_id"]
        if not text(ident):
            errors.append("Command mapping needs a command_id")
        elif ident in commands:
            errors.append("Duplicate command mapping: " + ident)
        else:
            commands.add(ident)
        for key in ("before", "handler", "shortcut", "enabled_state", "checked_state"):
            if not text(mapping[key]):
                errors.append("Command mapping needs explicit " + key + " behavior")
        if mapping["disposition"] == "preserved":
            if not text(mapping["after"]):
                errors.append("Preserved command needs a target surface")
        elif mapping["disposition"] == "excluded":
            if text(ident):
                excluded.add(ident)
            if not text(mapping["reason"]) or mapping["after"] is not None:
                errors.append("Excluded command needs a reason and null target")
        else:
            errors.append("Command disposition must be preserved or excluded")
        if mapping["reason"] is not None and not text(mapping["reason"]):
            errors.append("Command reason must be text or null")
    source_commands = flow.get("source_commands")
    if change in ("ui-reorganization", "ui-shell-migration"):
        if not isinstance(source_commands, list) or not source_commands or any(not text(v) for v in source_commands):
            errors.append("UI migration needs source_commands from the declared in-scope inventory")
        elif len(set(source_commands)) != len(source_commands) or set(source_commands) != commands:
            errors.append("Each in-scope source command needs exactly one before/after mapping or explicit exclusion")
    elif source_commands is not None and (not isinstance(source_commands, list) or any(not text(v) for v in source_commands)):
        errors.append("source_commands must be a string array")
    edges = flow.get("edges")
    if not isinstance(edges, list) or not 1 <= len(edges) <= 2000:
        return errors + ["edges must contain 1-2000 declarations"]
    edge_ids, valid_edges = set(), []
    for edge in edges:
        if not isinstance(edge, dict) or set(edge) != EDGE_FIELDS:
            errors.append("Edge has missing or unknown fields")
            continue
        invalid = False
        for key in ("id", "from", "to", "contract", "thread_owner"):
            if not text(edge[key]):
                errors.append("Edge needs explicit " + key)
                invalid = True
        if invalid:
            continue
        if edge["id"] in edge_ids:
            errors.append("Duplicate edge: " + edge["id"])
        edge_ids.add(edge["id"])
        if edge["from"] not in ids or edge["to"] not in ids or edge["from"] == edge["to"]:
            errors.append("Edge endpoints must be distinct declared nodes: " + edge["id"])
            invalid = True
        if not isinstance(edge["kind"], str) or edge["kind"] not in KINDS:
            errors.append("Invalid edge kind: " + edge["id"])
            invalid = True
        if edge["execution"] not in ("sync", "async"):
            errors.append("Edge execution must be sync or async")
        basis = edge["evidence_basis"]
        if basis not in ("proposed", "source-reviewed", "runtime-observed"):
            errors.append("Invalid edge evidence_basis")
        if edge["source_ref"] is not None and not text(edge["source_ref"]):
            errors.append("Edge source_ref must be text or null")
        if basis in ("source-reviewed", "runtime-observed") and not text(edge["source_ref"]):
            errors.append("Reviewed/observed edge needs source evidence: " + edge["id"])
        command = edge["command_id"]
        if command is not None and (not text(command) or command not in commands):
            errors.append("Edge command_id must reference a declared command mapping")
            invalid = True
        elif command in excluded:
            errors.append("Excluded command cannot have active flow edges")
        if not invalid:
            valid_edges.append(edge)
    if any(edge["execution"] == "async" for edge in valid_edges):
        policy = flow.get("async_policy")
        if (not isinstance(policy, dict) or set(policy) != {"progress", "cancellation", "error", "recovery"}
                or any(not text(v) for v in policy.values())):
            errors.append("Async flow needs explicit progress, cancellation, error and recovery policies")
    elif "async_policy" in flow:
        policy = flow["async_policy"]
        if not isinstance(policy, dict) or set(policy) != {"progress", "cancellation", "error", "recovery"} or any(not text(v) for v in policy.values()):
            errors.append("async_policy has missing, empty or unknown fields")
    groups = {edge["command_id"] for edge in valid_edges if edge["kind"] == "request"}
    if not groups:
        errors.append("An architectural command/data flow needs at least one request edge")
    if change in ("ui-reorganization", "ui-shell-migration"):
        for command in commands - excluded:
            if command not in groups:
                errors.append("Preserved command needs a correlated request flow: " + command)
    for command in groups:
        group = [edge for edge in valid_edges if edge["command_id"] == command]
        requests = [edge for edge in group if edge["kind"] == "request"]
        starts = {e["from"] for e in requests} - {e["to"] for e in requests}
        ends = {e["to"] for e in requests} - {e["from"] for e in requests}
        if not starts or not ends:
            errors.append("Request flow needs a declared entry and terminal operation")
        for edge in requests:
            if not any(reachable(requests, start, edge["from"], {"request"})
                       and reachable(requests, edge["to"], end, {"request"})
                       for start in starts for end in ends):
                errors.append("Request edge is disconnected from an entry/operation path: " + edge["id"])
        for start in starts:
            for end in ends:
                if not reachable(requests, start, end, {"request"}):
                    continue
                for kind in ("result", "error"):
                    # Qt signals/commands may return via visible state instead
                    # of replaying every intermediate function in reverse.
                    if not reachable(group, end, start, {kind, "state"}, required_kind=kind):
                        errors.append("Missing " + kind + " return path for " + str(command))
                if not any(reachable(group, end, edge["to"], {"result", "state"}, required_kind="state")
                           for edge in group if edge["kind"] == "state"):
                    errors.append("Request flow needs a connected UI/map state update")
    if flow.get("persistence_required"):
        if not any(e["kind"] == "persist" for e in valid_edges) or not any(e["kind"] == "readback" for e in valid_edges):
            errors.append("Persistence needs save/export and independent readback edges")
        for edge in (e for e in valid_edges if e["kind"] == "persist"):
            readers = [e for e in valid_edges if e["kind"] == "readback"]
            if not any(reachable(valid_edges, edge["to"], reader["to"], {"readback", "result"}, required_kind="readback")
                       for reader in readers):
                errors.append("Readback must be connected to the persisted artifact")
    return errors


def unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key: " + key)
        result[key] = value
    return result


def reject_constant(value):
    raise ValueError("Non-finite JSON value: " + value)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("flow", type=Path)
    args = parser.parse_args(argv)
    try:
        if not args.flow.is_file() or args.flow.stat().st_size > 262144:
            raise ValueError("Missing or oversized flow JSON")
        flow = json.loads(args.flow.read_text(encoding="utf-8"), object_pairs_hook=unique_pairs,
                          parse_constant=reject_constant)
        errors = validate_flow(flow)
    except (OSError, ValueError) as exc:
        errors = [str(exc)]
    for error in errors:
        print("ERROR:", error)
    if not errors:
        print("Flow declaration consistent; source truth, runtime behavior and host permissions NOT verified")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
