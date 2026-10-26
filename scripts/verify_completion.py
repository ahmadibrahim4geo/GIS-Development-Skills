#!/usr/bin/env python3
"""DoneProof report-consistency checker. Does not execute or authenticate evidence."""
import argparse
import json
from pathlib import Path

STATES = {"verified", "partial", "failed", "blocked", "not_run"}
KINDS = {"command_output", "artifact_readback", "provider_receipt", "native_interaction", "manual_review"}


def nonempty(x):
    return isinstance(x, str) and bool(x.strip())


def validate(data):
    errors = []
    if not isinstance(data, dict):
        return ["Report must be an object"]
    if data.get("schema_version") != "1.0":
        errors.append("Invalid schema_version")
    for key in ("task_id", "revision"):
        if not nonempty(data.get(key)):
            errors.append(key + " must be nonempty")
    overall = data.get("overall_status")
    if not isinstance(overall, str) or overall not in STATES:
        errors.append("Invalid overall_status")
    items = data.get("criteria")
    if not isinstance(items, list) or not items:
        return errors + ["criteria must be a nonempty list"]
    ids, statuses = set(), []
    for i, item in enumerate(items):
        prefix = "criteria[{}]".format(i)
        if not isinstance(item, dict):
            errors.append(prefix + " must be an object")
            continue
        key = item.get("id")
        if not nonempty(key) or key in ids:
            errors.append(prefix + ": missing or duplicate id")
        else:
            ids.add(key)
        if not nonempty(item.get("statement")):
            errors.append(prefix + ": missing statement")
        status = item.get("status")
        if not isinstance(status, str) or status not in STATES:
            errors.append(prefix + ": invalid status")
            continue
        statuses.append(status)
        observations = item.get("evidence")
        if not isinstance(observations, list):
            errors.append(prefix + ": evidence must be a list")
            continue
        if status in {"partial", "blocked", "not_run"} and not nonempty(item.get("reason")):
            errors.append(prefix + ": missing incomplete reason")
        if status == "not_run" and observations:
            errors.append(prefix + ": not_run cannot have evidence")
        passed = failed = 0
        for j, obs in enumerate(observations):
            name = "{}.evidence[{}]".format(prefix, j)
            if not isinstance(obs, dict):
                errors.append(name + ": must be an object")
                continue
            if not isinstance(obs.get("type"), str) or obs.get("type") not in KINDS:
                errors.append(name + ": unsupported type")
            for field in ("reference", "observed"):
                if not nonempty(obs.get(field)):
                    errors.append(name + ": missing " + field)
            if not nonempty(obs.get("revision")) or obs.get("revision") != data.get("revision"):
                errors.append(name + ": stale evidence revision")
            if obs.get("result") == "pass":
                passed += 1
            elif obs.get("result") == "fail":
                failed += 1
            else:
                errors.append(name + ": invalid result")
        if status == "verified" and (passed < 1 or failed > 0):
            errors.append(prefix + ": unsupported verified claim")
        if status == "failed" and failed < 1:
            errors.append(prefix + ": failed claim lacks failure observation")
    if overall == "verified" and (len(statuses) != len(items) or any(s != "verified" for s in statuses)):
        errors.append("Overall verified requires every criterion verified")
    if overall == "not_run" and any(s != "not_run" for s in statuses):
        errors.append("Overall not_run requires all criteria not_run")
    if overall == "failed" and "failed" not in statuses:
        errors.append("Overall failed requires a failed criterion")
    return errors


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("report", type=Path)
    p.add_argument("--require-verified", action="store_true")
    args = p.parse_args(argv)
    try:
        data = json.loads(args.report.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("ERROR:", exc)
        return 1
    errors = validate(data)
    if args.require_verified and data.get("overall_status") != "verified":
        errors.append("Release gate: overall_status is not verified")
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1
    print("DoneProof report structure valid; status={}; observations NOT independently checked".format(
        data["overall_status"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
