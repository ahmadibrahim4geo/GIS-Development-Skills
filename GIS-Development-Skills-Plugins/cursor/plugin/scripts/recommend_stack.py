#!/usr/bin/env python3
"""Generate 10-section multi-engine or lightweight GIS architecture recommendations.

Handles bilingual requests, lightweight utilities (PROJ-only), multi-engine 2D/3D/CAD
compositions, unresolved UI.js blockers, explicit commercial host add-ins, provider
fallback warnings, and strict developer-vs-enduser runtime separation without installs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import compare_engines, discover_engines  # noqa: E402


PROFILES_PATH = ROOT / "references" / "engine-capability-profiles.json"

ALL_21_SLOTS = (
    "intent_modes",
    "delivery_target",
    "existing_project",
    "preserve_invariants",
    "target_os",
    "target_arch",
    "preferred_languages",
    "ui_framework_preference",
    "required_capabilities",
    "optional_capabilities",
    "non_mercator_2d_required",
    "free_only",
    "offline_required",
    "allow_network_apis",
    "license_policy",
    "integration_preference",
    "deployment_model",
    "data_scales",
    "hardware_constraints",
    "reference_products",
    "weights_override",
)


def _infer_request_from_query(query: str, target_os: str = "windows", free_only: bool = True, offline: bool = False) -> dict[str, Any]:
    norm = discover_engines.normalize_bilingual_text(query)
    caps = discover_engines.extract_bilingual_capabilities(query)
    lower = query.casefold()

    ambiguous = []
    if re.search(r"\bui\.js\b|\bujs\b", lower):
        ambiguous.append("UI.js")

    non_mercator = any(k in norm for k in ("كل المساقط", "غير web mercator", "غير ميركاتور", "non mercator", "non-mercator", "polar", "projected map"))
    if non_mercator and "render.2d.projected" not in caps:
        caps.append("render.2d.projected")
        if "crs.transform" not in caps:
            caps.append("crs.transform")

    intent_modes = []
    if re.search(r"\barcgis\s+pro\b|\badd-in\b|\barcpy\b|داخل\s+arcgis|اضافه\s+كيو|qgis\s+plugin", lower):
        intent_modes.append("extend-host")
    if any(k in norm for k in ("نضف", "فورك", "اشتقاق", "source fork", "strip ui")):
        intent_modes.append("source-fork")
    if any(k in norm for k in ("زي arcgis", "مثل arcgis", "مثل google earth", "reference ui", "ribbon")):
        intent_modes.append("reference-inspired-ui")
    if any(k in norm for k in ("ادمج", "multi engine", "multi-engine", "cityengine", "globe")) and len(caps) >= 2:
        intent_modes.append("multi-engine-composition")
    if not intent_modes:
        intent_modes.append("embedded-engine")

    return {
        "schema_version": "1.0",
        "request_text": query,
        "intent_modes": intent_modes,
        "delivery_target": "arcgis-pro-addin" if ("arcgis" in lower and "extend-host" in intent_modes and not ("زي arcgis" in norm or "مثل arcgis" in norm or "بديل" in norm)) else "standalone-or-service",
        "existing_project": {"named_ambiguous_components": ambiguous},
        "target_os": [target_os],
        "required_capabilities": sorted(set(caps)),
        "non_mercator_2d_required": non_mercator,
        "free_only": free_only,
        "offline_required": offline,
        "license_policy": "commercial-host-explicit" if ("arcgis" in lower and "extend-host" in intent_modes and not free_only) else "free-first",
    }


def _inspect_existing_workspace(path_str: str | None) -> dict[str, Any]:
    if not path_str:
        return {"inspected": False, "observed_manifests": [], "note": "No existing project path supplied."}
    root = Path(path_str)
    if not root.is_dir():
        return {"inspected": False, "observed_manifests": [], "note": f"Supplied path not found: {path_str}"}
    manifests = []
    for pattern in ("package.json", "requirements.txt", "pyproject.toml", "CMakeLists.txt", "*.csproj"):
        manifests.extend(p.name for p in root.glob(pattern))
    return {"inspected": True, "observed_manifests": sorted(set(manifests)), "note": "Read-only manifest scan only."}


def recommend(
    request: dict[str, Any],
    *,
    profiles_data: dict[str, Any] | None = None,
    taxonomy_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Build a deterministic 10-section architectural stack recommendation."""
    prof_doc = profiles_data or json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    by_pid = {p["project_id"]: p for p in prof_doc["profiles"]}

    query = request.get("request_text", "")
    norm = discover_engines.normalize_bilingual_text(query)
    req_caps = sorted(set(request.get("required_capabilities") or discover_engines.extract_bilingual_capabilities(query, taxonomy_data)))
    lower = query.casefold()

    slots = {k: request.get(k) for k in ALL_21_SLOTS}
    slots["required_capabilities"] = req_caps

    # Guardrail 1: Ambiguous component name (e.g. UI.js).
    existing_raw = request.get("existing_project")
    existing_meta = existing_raw if isinstance(existing_raw, dict) else {}
    ambiguous = list(existing_meta.get("named_ambiguous_components") or [])
    if re.search(r"\bui\.js\b|\bujs\b", lower) and "UI.js" not in ambiguous:
        ambiguous.append("UI.js")

    existing_gate = _inspect_existing_workspace(existing_meta.get("root_path"))
    if ambiguous:
        return {
            "schema_version": "1.0",
            "status": "unresolved",
            "request_summary": query,
            "intent_slots": slots,
            "entity_role_split": {
                "ui_framework": {"name": ", ".join(ambiguous), "status": "unresolved"},
                "renderer": {"status": "deferred"},
                "gis_engine": {"status": "deferred"},
            },
            "existing_inventory_gate": existing_gate,
            "recommended_build_models": request.get("intent_modes") or ["unresolved"],
            "candidate_evaluations": [],
            "recommended_stack": [],
            "component_contracts": [],
            "developer_vs_enduser_setup": {
                "developer_toolchain": ["Verify exact package/repository identity and SPDX license before installing."],
                "end_user_runtime": [],
                "approval_required_downloads": False,
            },
            "fallback_and_compatibility_guardrails": [
                f"Ambiguous component name(s) {ambiguous} kept strictly unresolved; never infer Vue.js or generate adapters before repository inspection."
            ],
            "poc_benchmark_plan": {"required": True, "steps": ["Resolve component repo URL, version, and license."]},
            "adr_record": {"required": False, "reason": "Blocked pending unresolved identity resolution."},
            "gaps_and_limitations": [f"Unresolved component identity: {', '.join(ambiguous)}"],
            "evidence_boundaries": {"analysis_tier": "T0-T1", "native_runtime_verified": False, "heavy_installers_executed": False},
        }

    # Guardrail 2: Explicit commercial host extension (`ArcGIS Pro add-in` / `ArcPy`).
    intent_modes = list(request.get("intent_modes") or [])
    is_explicit_arcgis_host = (
        ("extend-host" in intent_modes or re.search(r"inside\s+arcgis|داخل\s+arcgis|\barcgis\s+pro\b|\barcpy\b", lower))
        and not any(k in norm for k in ("بديل", "زي arcgis", "مثل arcgis", "شبيه arcgis", "مجاني بديل", "alternative", "free", "open source", "open-source", "clone"))
    )

    if is_explicit_arcgis_host:
        arcgis_targets = [by_pid[pid] for pid in ("esri-arcgis-pro-sdk", "esri-arcpy") if pid in by_pid]
        return {
            "schema_version": "1.0",
            "status": "recommended",
            "request_summary": query,
            "intent_slots": slots,
            "entity_role_split": {
                "host": {"name": "ArcGIS Pro (Commercial Host)", "status": "commercial-host-explicit"},
                "extension": {"name": "ArcGIS Pro SDK (.NET C#) or ArcPy (.pyt)", "status": "documented"},
            },
            "existing_inventory_gate": existing_gate,
            "recommended_build_models": ["extend-host"],
            "candidate_evaluations": [{"project_id": p["project_id"], "gate_status": "host-explicit-commercial"} for p in arcgis_targets],
            "recommended_stack": [
                {"function": "host-extension", "project_id": "esri-arcgis-pro-sdk", "note": "Keep commercial host explicit; optionally mention QGIS PyQGIS as separate OSS analog."}
            ],
            "component_contracts": [{"interface": "ArcGIS Pro SDK / ArcPy .pyt", "boundary": "Host process add-in"}],
            "developer_vs_enduser_setup": {
                "developer_toolchain": ["Visual Studio / .NET SDK matching installed ArcGIS Pro version (verify locally first)."],
                "end_user_runtime": ["Licensed ArcGIS Pro workstation runtime required."],
                "approval_required_downloads": True,
            },
            "fallback_and_compatibility_guardrails": [
                "Explicit ArcGIS Pro host extension request honored; never rewrite silently into standalone app.",
                "Heavy host SDKs or Visual Studio components are never auto-installed without user approval.",
            ],
            "poc_benchmark_plan": {"required": False, "steps": ["Inspect installed ArcGIS Pro version via toolchain_discovery.py before coding."]},
            "adr_record": {"required": False, "reason": "Explicit commercial host extension requested."},
            "gaps_and_limitations": ["Native ArcGIS Pro execution NOT RUN offline."],
            "evidence_boundaries": {"analysis_tier": "T0-T1", "native_runtime_verified": False, "heavy_installers_executed": False},
        }

    # Special decomposition rules:
    # E08: Pure lightweight CRS utility -> prioritize tiny CRS library (`osgeo-proj` / `proj4js`) rather than desktop QGIS suite.
    lightweight_crs_only = (
        set(req_caps).issubset({"crs.transform", "crs.vertical", "geodesy.distance", "geodesy.area", "offline.no-key"})
        and bool(set(req_caps) & {"crs.transform", "crs.vertical"})
    )
    # E09: Arbitrary 2D projections separated from 3D Globe.
    separate_2d_crs_and_globe = bool(request.get("non_mercator_2d_required")) or (
        "render.2d.projected" in req_caps and "render.globe.ellipsoid" in req_caps
    )
    # E10: CityEngine procedural multi-engine decomposition.
    cityengine_decomposition = "cityengine" in lower or (
        bool(set(req_caps) & {"city.parcel.subdivide", "city.building.procedural"}) and bool(set(req_caps) & {"cad.brep", "simulation.traffic"})
    )

    if separate_2d_crs_and_globe:
        for extra in ("crs.transform", "render.2d.projected", "render.globe.ellipsoid"):
            if extra not in req_caps:
                req_caps.append(extra)
        req_caps = sorted(set(req_caps))
        slots["required_capabilities"] = req_caps

    # Per-function selection (best specialized engine per required capability).
    recommended_stack: list[dict[str, Any]] = []
    all_evaluations: list[dict[str, Any]] = []
    selected_pids: set[str] = set()
    gaps: list[str] = []

    for cap in req_caps or ["offline.no-key"]:
        disc = discover_engines.discover(
            capabilities=[cap],
            platform=(request.get("target_os") or [""])[0],
            profiles_data=prof_doc,
            taxonomy_data=taxonomy_data,
        )
        cands = [by_pid[item["project_id"]] for item in disc["candidates"] if item["project_id"] in by_pid]
        if lightweight_crs_only:
            # Prefer lightweight CRS bindings/engines over full desktop suites (`E08`).
            light_first = [c for c in cands if c["entity_type"] not in {"Application", "Fork"}]
            if light_first:
                cands = light_first

        sub_req = dict(request)
        sub_req["required_capabilities"] = [cap]
        comp = compare_engines.compare_candidates(cands, sub_req, weights=request.get("weights_override"))
        all_evaluations.extend(comp["evaluations"][:3])

        winner_pid = comp["winner"]
        if winner_pid:
            prof = by_pid[winner_pid]
            if winner_pid not in selected_pids:
                selected_pids.add(winner_pid)
                recommended_stack.append(
                    {
                        "function": cap,
                        "project_id": winner_pid,
                        "name": prof["name"],
                        "entity_type": prof["entity_type"],
                        "integration_patterns": prof["integration_patterns"],
                        "license_spdx_hint": prof["verification_metadata"]["license_spdx_hint"],
                    }
                )
        else:
            gaps.append(f"No eligible candidate passed all hard gates for '{cap}' under current license/free_only constraints.")

    heavy_downloads = any(
        by_pid[p["project_id"]]["entity_type"] in {"Application", "SDK", "Engine"}
        for p in recommended_stack
    ) or cityengine_decomposition

    contracts = [
        {"interface": "ICrsTransformer", "data_contract": "EPSG / WKT2 + axis order"},
        {"interface": "IDataProvider", "data_contract": "DatasetRef + FeatureIdentity + RasterRef"},
    ]
    if separate_2d_crs_and_globe:
        contracts.append({"interface": "IMapRenderer (2D != 3D Globe)", "data_contract": "Projected Viewport (OpenLayers/PROJ) + Ellipsoidal Globe (CesiumJS)"})

    guardrails = [
        "No silent algorithmic fallback across distinct providers (e.g., OTB vs SNAP vs GDAL): expose algorithm/unit differences explicitly (E37).",
        "Never mix PyPI binary GDAL wheels with OSGeo4W or Conda GDAL/PROJ DLLs in the same process (E17).",
    ]
    if cityengine_decomposition:
        gaps.append("No single OSS engine replicates proprietary Esri CityEngine CGA grammar natively; compose OCCT/Clipper2 + Three/Cesium + SUMO.")

    status = "recommended" if (recommended_stack and not gaps) else ("partial-with-gaps" if recommended_stack else "blocked-by-gate")

    return {
        "schema_version": "1.0",
        "status": status,
        "request_summary": query,
        "intent_slots": slots,
        "entity_role_split": {
            "ui_framework": request.get("ui_framework_preference") or "independent-shell",
            "separated_renderers": ["2D projected renderer", "3D ellipsoid globe"] if separate_2d_crs_and_globe else ["task-scoped renderer"],
            "geospatial_engines": [item["project_id"] for item in recommended_stack],
        },
        "existing_inventory_gate": existing_gate,
        "recommended_build_models": intent_modes or (["multi-engine-composition"] if len(recommended_stack) > 1 else ["embedded-engine"]),
        "candidate_evaluations": all_evaluations,
        "recommended_stack": recommended_stack,
        "component_contracts": contracts,
        "developer_vs_enduser_setup": {
            "developer_toolchain": [
                "Version-pinned language compiler/build tools (Python venv / CMake / Node LTS) and dev headers only on build workstation.",
            ],
            "end_user_runtime": [
                "Self-contained runtime bundle (PROJ_DATA / GDAL_DATA + dynamically linked LGPL shared libs) without dev compilers.",
            ],
            "approval_required_downloads": heavy_downloads,
        },
        "fallback_and_compatibility_guardrails": guardrails,
        "poc_benchmark_plan": {
            "required": True,
            "steps": [
                "Run golden UTM/polar projection & readback fixture before full build (E09).",
                "Capture cold/warm runtime + RSS memory before final tiebreak (V2 §32.1).",
            ],
        },
        "adr_record": {
            "required": bool(gaps),
            "template_ref": "templates/ARCHITECTURE_DECISION_RECORD.md",
            "reason": "Capability gap requires documented ADR if custom component is authored." if gaps else "Satisfied via existing open-source catalog reuse.",
        },
        "gaps_and_limitations": gaps,
        "evidence_boundaries": {
            "analysis_tier": "T0-T1",
            "native_runtime_verified": False,
            "heavy_installers_executed": False,
        },
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--request", type=Path, help="Structured engine-selection request JSON")
    parser.add_argument("--query", default="", help="Free-form EN/AR architectural prompt")
    parser.add_argument("--os", dest="target_os", default="windows")
    parser.add_argument("--free-only", dest="free_only", action="store_true", default=True)
    parser.add_argument("--allow-commercial", dest="free_only", action="store_false")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    if args.request:
        req = json.loads(args.request.read_text(encoding="utf-8"))
    elif args.query.strip():
        req = _infer_request_from_query(args.query, target_os=args.target_os, free_only=args.free_only, offline=args.offline)
    else:
        parser.exit(2, "Provide --request <json> or --query <text>\n")

    report = recommend(req)
    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"# Technology Stack Recommendation ({report['status']})")
        print(f"## 1. Request\n{report['request_summary']}")
        print(f"## 2. Build Modes\n{', '.join(report['recommended_build_models'])}")
        print("## 3. Recommended Engines")
        for s in report["recommended_stack"]:
            print(f"- **{s['function']}**: `{s['project_id']}` ({s['entity_type']} · {s['license_spdx_hint']})")
        print("## 4. Developer vs End-User Runtime")
        print(f"- Developer: {report['developer_vs_enduser_setup']['developer_toolchain']}")
        print(f"- End-User: {report['developer_vs_enduser_setup']['end_user_runtime']}")
        print("## 5. Gaps & Evidence Boundaries")
        print(f"- Native Runtime Verified: {report['evidence_boundaries']['native_runtime_verified']} (`NOT RUN`)")
        for g in report["gaps_and_limitations"]:
            print(f"- Gap: {g}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
