#!/usr/bin/env python3
"""Deterministic hard-gate screener and weighted 0-5 comparator for GIS engines.

Enforces security, platform, license, free-first, and capability gates BEFORE
weighted scoring so rejected or unverified candidates can never rank first.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PROFILES_PATH = ROOT / "references" / "engine-capability-profiles.json"

DEFAULT_WEIGHTS: dict[str, float] = {
    "functional_capability": 25.0,
    "geodetic_fidelity": 20.0,
    "runtime_performance": 15.0,
    "license_cost": 15.0,
    "integration_cleanliness": 10.0,
    "deployment_footprint": 10.0,
    "maintenance_hygiene": 5.0,
}

STATUS_RANK = {"eligible": 0, "needs-evidence": 1, "rejected": 2}
EMPIRICAL_METRICS = ("cold_start_ms", "peak_rss_mb", "throughput", "accuracy_delta")


def _license_family(spdx_hint: str) -> str:
    txt = (spdx_hint or "").casefold()
    if any(k in txt for k in ("agpl",)):
        return "network-copyleft"
    if any(k in txt for k in ("gpl-2", "gpl-3", "gpl")):
        return "lgpl" if "lgpl" in txt else "strong-copyleft"
    if any(k in txt for k in ("lgpl", "mpl", "epl")):
        return "weak-copyleft"
    if any(k in txt for k in ("mit", "bsd", "apache", "isc", "bsl", "cc0", "public domain", "zlib", "unlicense")):
        return "permissive"
    if any(k in txt for k in ("noncommercial", "polyform", "academic")):
        return "noncommercial"
    if any(k in txt for k in ("commercial", "proprietary", "esri", "mapbox")):
        return "commercial"
    return "unknown"


def _supports_platform(profile: dict[str, Any], target_os_list: list[str]) -> tuple[bool, bool]:
    """Return (supported_in_process, worker_isolation_possible)."""
    if not target_os_list or "any" in target_os_list or "cross-platform" in target_os_list:
        return True, False
    vm = profile.get("verification_metadata", {})
    supported = {x.casefold() for x in vm.get("supported_os", [])} | {x.casefold() for x in profile.get("platforms", [])}
    if "cross-platform" in supported:
        return True, False
    if all(os_name.casefold() in supported for os_name in target_os_list):
        return True, False
    build_models = set(profile.get("build_models", []))
    integ = set(profile.get("integration_patterns", []))
    if "worker-service" in build_models or "service-api" in integ:
        return False, True
    return False, False


def hard_gate(profile: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
    """Evaluate hard exclusion gates returning eligible, needs-evidence, or rejected."""
    vm = profile.get("verification_metadata", {})
    failed_gates: list[str] = []
    missing_evidence: list[str] = []
    warnings: list[str] = []
    isolation_required = False

    # 1. Security quarantine gate.
    if vm.get("security_status") == "quarantine-reference-only":
        failed_gates.append("security: quarantined external reference/agent skill cannot be selected as runtime engine")

    # 2. Cost & Free-First gate.
    free_only = bool(request.get("free_only", True))
    cost_class = vm.get("cost_classification", "unknown")
    lic_status = vm.get("license_status", "verify-upstream")
    spdx_hint = vm.get("license_spdx_hint", "unknown")
    lic_family = _license_family(spdx_hint)
    api_billing = (vm.get("api_key_or_billing") or "").casefold()
    host_dep = (vm.get("host_dependency") or "")

    if free_only:
        if cost_class in {"commercial", "trial"} or lic_status == "commercial-terms" or lic_family == "commercial":
            failed_gates.append(f"free-only-gate: cost={cost_class} / license_status={lic_status} requires commercial terms")
        elif cost_class in {"non-commercial", "academic-only"} or lic_family == "noncommercial":
            failed_gates.append(f"free-only-gate: restricted cost classification {cost_class}")
        elif host_dep.startswith("Required") and "open-source" not in host_dep.casefold():
            failed_gates.append(f"free-only-gate: proprietary host required ({host_dep})")
        elif any(tok in api_billing for tok in ("paid", "billing required", "credit card", "subscription")):
            failed_gates.append(f"free-only-gate: mandatory paid API or billing ({vm.get('api_key_or_billing')})")

    if cost_class == "unknown" or (lic_status == "verify-upstream" and lic_family == "unknown"):
        missing_evidence.append(f"license-and-cost-unverified (cost={cost_class}, spdx_hint={spdx_hint})")
    elif request.get("require_verified_license") and lic_status != "verified-upstream":
        missing_evidence.append(f"upstream-license-file-not-yet-verified ({lic_status})")
    elif lic_status == "verify-upstream":
        warnings.append("verify-upstream-license-before-release")

    # 3. License compatibility gate.
    license_policy = request.get("license_policy", "free-first")
    integ_pref = request.get("integration_preference", "any")
    if lic_family in {"strong-copyleft", "network-copyleft"}:
        if license_policy == "permissive-only" and integ_pref != "worker-ipc":
            failed_gates.append(f"license-policy: {spdx_hint} incompatible with permissive-only in-process linkage")
        elif license_policy == "oss-compatible":
            isolation_required = True
            warnings.append("copyleft-isolation-or-gpl-compliance-required")
    elif lic_family in {"lgpl", "weak-copyleft"} and license_policy == "permissive-only":
        warnings.append("weak-copyleft-requires-dynamic-shared-linking")

    # 4. Platform / OS gate.
    target_os = [x for x in (request.get("target_os") or []) if isinstance(x, str)]
    in_proc_ok, worker_ok = _supports_platform(profile, target_os)
    if not in_proc_ok:
        if worker_ok and integ_pref in {"worker-ipc", "service", "any"}:
            isolation_required = True
            warnings.append(f"platform-requires-worker-or-service-boundary for {target_os}")
        else:
            failed_gates.append(f"platform-unsupported: target_os={target_os} not in supported_os={vm.get('supported_os')}")

    # 5. Atomic capability satisfaction gate.
    prof_caps = profile.get("capabilities", {})
    for cid in request.get("required_capabilities") or []:
        if cid not in prof_caps:
            missing_evidence.append(f"missing-required-capability: {cid}")
            continue
        support_state = prof_caps[cid].get("support_state", "unknown")
        if support_state == "unsupported":
            failed_gates.append(f"capability-unsupported: {cid}")
        elif support_state == "unknown":
            missing_evidence.append(f"capability-unknown: {cid}")
        elif support_state in {"extension-required", "external-component-required"}:
            warnings.append(f"{cid}: {support_state}")

    # Offline requirement check.
    if request.get("offline_required") and "offline-no-key" not in prof_caps and "offline.no-key" not in prof_caps:
        if "service" in profile.get("entity_type", "").casefold() and "runtime.offline" not in prof_caps:
            warnings.append("verify-offline-packaging-for-service")

    if failed_gates:
        gate_status = "rejected"
    elif missing_evidence:
        gate_status = "needs-evidence"
    else:
        gate_status = "eligible"

    return {
        "gate_status": gate_status,
        "failed_gates": sorted(failed_gates),
        "missing_evidence": sorted(missing_evidence),
        "warnings": sorted(set(warnings)),
        "isolation_required": isolation_required,
    }


def evaluate_candidate(
    profile: dict[str, Any],
    request: dict[str, Any],
    *,
    weights: dict[str, float] | None = None,
    benchmarks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Screen a candidate through hard_gate and compute deterministic 0-5 weighted scores."""
    w = dict(DEFAULT_WEIGHTS)
    if weights:
        w.update({k: float(v) for k, v in weights.items() if k in w})
    total_w = sum(w.values()) or 100.0

    gate = hard_gate(profile, request)
    vm = profile.get("verification_metadata", {})
    prof_caps = profile.get("capabilities", {})
    req_caps = list(request.get("required_capabilities") or [])
    opt_caps = list(request.get("optional_capabilities") or [])

    # 1. Functional & capability score (0-5).
    if req_caps:
        matched_req = sum(
            1 for c in req_caps if c in prof_caps and prof_caps[c].get("support_state") not in {"unknown", "unsupported"}
        )
        matched_opt = sum(1 for c in opt_caps if c in prof_caps)
        func_raw = 4.0 * (matched_req / len(req_caps)) + (1.0 * (matched_opt / len(opt_caps)) if opt_caps else 1.0)
    else:
        func_raw = min(5.0, 2.0 + 0.3 * len(prof_caps))

    # 2. Geodetic fidelity (0-5).
    crs_hits = sum(1 for c in prof_caps if c.startswith(("crs.", "geodesy.", "geometry.")) or c == "io.vector.gpkg.roundtrip.zm")
    geod_raw = min(5.0, 2.0 + 0.75 * crs_hits)

    # 3. Runtime performance (neutral 3.0 if empirical benchmarks not supplied — never fake tiebreak speedup).
    cand_bench = (benchmarks or {}).get(profile["project_id"], {})
    missing_metrics = [m for m in EMPIRICAL_METRICS if m not in cand_bench]
    perf_raw = 3.0 if missing_metrics else float(cand_bench.get("perf_score_0_5", 3.5))

    # 4. License & cost score (0-5). Verified upstream license slightly outranks unverified preliminary hint.
    lic_family = _license_family(vm.get("license_spdx_hint", "unknown"))
    cost_class = vm.get("cost_classification", "unknown")
    is_lic_verified = vm.get("license_status") == "verified-upstream"
    if cost_class == "open-source" and lic_family == "permissive":
        lic_raw = 5.0 if is_lic_verified else 4.0
    elif cost_class == "open-source" and lic_family in {"lgpl", "weak-copyleft"}:
        lic_raw = 4.0 if is_lic_verified else 3.25
    elif cost_class == "open-source" and lic_family == "strong-copyleft":
        lic_raw = 3.0 if is_lic_verified else 2.5
    elif cost_class in {"source-available", "free-tier"}:
        lic_raw = 2.0
    elif cost_class == "unknown":
        lic_raw = 1.5
    else:
        lic_raw = 0.0

    # 5. Integration cleanliness (0-5).
    integ_patterns = set(profile.get("integration_patterns", [])) - {"reference-only"}
    integ_raw = min(5.0, 2.0 + 0.8 * len(integ_patterns) - (1.0 if gate["isolation_required"] else 0.0))

    # 6. Deployment footprint & offline readiness (0-5).
    deploy_raw = 3.0
    if "offline.no-key" in prof_caps:
        deploy_raw += 1.0
    if profile.get("entity_type") in {"Library", "Kernel", "Binding/Wrapper", "CLI"}:
        deploy_raw += 1.0
    elif profile.get("entity_type") in {"Application", "Fork"}:
        deploy_raw -= 0.5
    deploy_raw = max(0.0, min(5.0, deploy_raw))

    # 7. Maintenance hygiene & trust grade (0-5).
    trust_map = {"RUN-VERIFIED": 5.0, "V3": 4.5, "V2": 4.0, "V1": 2.5}
    maint_raw = trust_map.get(vm.get("trust_level", "V1"), 2.0)

    dimension_scores = {
        "functional_capability": round(func_raw, 2),
        "geodetic_fidelity": round(geod_raw, 2),
        "runtime_performance": round(perf_raw, 2),
        "license_cost": round(lic_raw, 2),
        "integration_cleanliness": round(integ_raw, 2),
        "deployment_footprint": round(deploy_raw, 2),
        "maintenance_hygiene": round(maint_raw, 2),
    }
    raw_weighted = sum((dimension_scores[k] / 5.0) * w[k] for k in w) * (100.0 / total_w)
    weighted_score = round(raw_weighted, 2)

    return {
        "project_id": profile["project_id"],
        "name": profile["name"],
        "entity_type": profile["entity_type"],
        "gate_status": gate["gate_status"],
        "failed_gates": gate["failed_gates"],
        "missing_evidence": gate["missing_evidence"],
        "warnings": gate["warnings"],
        "isolation_required": gate["isolation_required"],
        "weighted_score": weighted_score,
        "eligible_for_selection": gate["gate_status"] == "eligible",
        "dimension_scores_0_5": dimension_scores,
        "missing_metrics": missing_metrics,
        "poc_benchmark_required": bool(missing_metrics),
        "license_spdx_hint": vm.get("license_spdx_hint"),
        "cost_classification": cost_class,
    }


def compare_candidates(
    profiles: list[dict[str, Any]],
    request: dict[str, Any],
    *,
    weights: dict[str, float] | None = None,
    benchmarks: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Compare all candidate profiles deterministically with hard gates strictly dominant."""
    evals = [evaluate_candidate(p, request, weights=weights, benchmarks=benchmarks) for p in profiles]
    evals.sort(key=lambda item: (STATUS_RANK[item["gate_status"]], -item["weighted_score"], item["project_id"]))

    eligible_top = next((e for e in evals if e["gate_status"] == "eligible"), None)
    close_tie = False
    if eligible_top is not None:
        eligible_others = [e for e in evals if e["gate_status"] == "eligible" and e["project_id"] != eligible_top["project_id"]]
        if eligible_others and abs(eligible_top["weighted_score"] - eligible_others[0]["weighted_score"]) <= 2.5 and eligible_top["poc_benchmark_required"]:
            close_tie = True

    return {
        "schema_version": "1.0",
        "weights": weights or DEFAULT_WEIGHTS,
        "free_only": bool(request.get("free_only", True)),
        "winner": eligible_top["project_id"] if eligible_top else None,
        "close_tie_requires_poc_benchmark": close_tie,
        "counts": {
            "total": len(evals),
            "eligible": sum(e["gate_status"] == "eligible" for e in evals),
            "needs_evidence": sum(e["gate_status"] == "needs-evidence" for e in evals),
            "rejected": sum(e["gate_status"] == "rejected" for e in evals),
        },
        "evaluations": evals,
        "note": "Hard gate dominates ranking: rejected/needs-evidence candidates can never outrank eligible winners.",
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, help="Path to engine-selection request JSON")
    parser.add_argument("--candidates", default="", help="Comma-separated project_id list (optional)")
    parser.add_argument("--profiles", type=Path, default=PROFILES_PATH)
    parser.add_argument("--free-only", dest="free_only", action="store_true", default=True)
    parser.add_argument("--allow-commercial", dest="free_only", action="store_false")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    request: dict[str, Any] = {"request_text": "CLI candidate comparison", "target_os": ["cross-platform"], "required_capabilities": [], "free_only": args.free_only}
    if args.request:
        request.update(json.loads(args.request.read_text(encoding="utf-8")))

    prof_doc = json.loads(args.profiles.read_text(encoding="utf-8"))
    by_pid = {p["project_id"]: p for p in prof_doc["profiles"]}
    if args.candidates.strip():
        pids = [c.strip() for c in args.candidates.split(",") if c.strip()]
        selected = [by_pid[p] for p in pids if p in by_pid]
    else:
        req_caps = set(request.get("required_capabilities") or [])
        selected = [
            p for p in prof_doc["profiles"]
            if (not req_caps or any(c in p.get("capabilities", {}) for c in req_caps))
        ][:25]

    report = compare_candidates(selected, request, weights=request.get("weights_override"))
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"# Engine Comparison (Winner: `{report['winner']}`)")
        for e in report["evaluations"]:
            print(f"- `{e['project_id']}`: **{e['gate_status']}** | score={e['weighted_score']} | missing_metrics={len(e['missing_metrics'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
