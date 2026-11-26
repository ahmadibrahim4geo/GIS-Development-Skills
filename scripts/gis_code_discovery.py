#!/usr/bin/env python3
"""GIS Code Discovery & Reuse Engine.
Searches, analyzes, and evaluates GIS code snippets, SDK examples, and recipes.
Deterministic, offline-first, no external network dependencies.
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "references" / "gis-code-sources.json"
RECIPES_PATH = ROOT / "references" / "gis-code-recipes.json"

PLATFORM_PATTERNS = {
    "arcgis-pro-sdk": [
        r"\barcgis\s+pro\s+sdk\b", r"\barcgis\.desktop\b", r"\bqueuedtask\b"
    ],
    "arcpy": [
        r"\barcpy\b", r"\bspatial\s+analyst\b"
    ],
    "pyqgis": [
        r"\bpyqgis\b", r"\bqgis\b", r"\bqgsprocessing\w*\b"
    ],
    "gdal-rasterio": [
        r"\bgdal\b", r"\brasterio\b", r"\bdem\b", r"\belevation\b",
        r"\bsample\s+raster\b", r"\bgeotiff\b", r"\bnodata\b", r"\bارتفاع\b"
    ],
    "web-gis": [
        r"\bweb\s*gis\b", r"\bmaplibre\b", r"\bleaflet\b", r"\bopenlayers\b",
        r"\bvector\s+tiles\b", r"\bpmtiles\b", r"\bخريطة\s+تفاعلية\b"
    ],
    "kml-kmz": [
        r"\bkml\b", r"\bkmz\b", r"\bplacemark\b", r"\bstyle\b", r"\baabbggrr\b"
    ],
    "spatial-modeling": [
        r"\bspatial\s+prediction\b", r"\bspatial\s+machine\s+learning\b",
        r"\bscikit-map\b", r"\bensemble\b", r"\bتنبؤ\s+مكاني\b", r"\bتعلم\s+آلي\s+مكاني\b"
    ]
}

PLATFORM_ALIASES = {
    "qgis": "pyqgis", "gdal": "gdal-rasterio", "rasterio": "gdal-rasterio",
    "raster-analysis": "gdal-rasterio",
}
HOST_PLATFORMS = {"arcgis-pro-sdk", "arcpy", "pyqgis"}
NONFUNCTIONAL_TERMS = {
    "create", "convert", "use", "for", "with", "the", "and", "into", "from",
    "my", "app", "gis", "interface", "current", "build", "tool", "tools",
    "code", "find", "qgis", "pyqgis", "arcgis", "pro", "sdk", "arcpy",
    "gdal", "rasterio", "maplibre", "kml", "kmz", "python", "javascript",
}


def load_registry(path):
    path = Path(path)
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def detect_platforms(query_text):
    """Return lexical hints only; generic UI controls do not identify a GIS host."""
    text = query_text.lower()
    matches = []
    for platform, patterns in PLATFORM_PATTERNS.items():
        if any(re.search(pat, text, re.I) for pat in patterns):
            matches.append(platform)
    return matches or ["generic-gis"]


def selected_platforms(query_text, target_platform=None):
    """Constrain candidates; a caller-supplied target wins over lexical hints.

    This offline selector cannot authenticate a host or resolve an unknown engine.
    Conflicting host hints require an explicit target rather than mixed recipes.
    """
    if target_platform:
        target = PLATFORM_ALIASES.get(target_platform.lower(), target_platform.lower())
        return ([target], "declared") if target in PLATFORM_PATTERNS else ([], "unknown-target")
    detected = [p for p in detect_platforms(query_text) if p != "generic-gis"]
    hosts = [p for p in detected if p in HOST_PLATFORMS]
    if len(hosts) > 1:
        return [], "ambiguous-host"
    selected = hosts or detected
    return selected, "query-hint" if selected else "unresolved"


def candidate_platforms(item):
    """Read applicability from catalog identity/environment fields, never code."""
    domains = [item.get("domain", ""), *item.get("gis_domains", [])]
    platforms = {
        PLATFORM_ALIASES.get(domain.lower(), domain.lower()) for domain in domains
        if PLATFORM_ALIASES.get(domain.lower(), domain.lower()) in PLATFORM_PATTERNS
    }
    identity = " ".join([
        item.get("title", ""), item.get("source_name", ""),
        item.get("target_environment", ""), *item.get("frameworks", []),
    ])
    platforms.update(p for p in detect_platforms(identity) if p != "generic-gis")
    return platforms


def functional_terms(text):
    return {t for t in re.findall(r"[^\W_]+", text.lower())
            if len(t) > 2 and t not in NONFUNCTIONAL_TERMS}


def arcgis_pro_version(inventory):
    """Use the observed executable release from native toolchain discovery."""
    for item in inventory.get("native_inventory", {}).get("installer_file_versions", []):
        version = item.get("version")
        if (item.get("product") == "ArcGIS Pro" and item.get("status") == "VERSION_RESOURCE_READ"
                and isinstance(version, str) and re.fullmatch(r"\d+(?:\.\d+){1,3}", version)):
            return version
    return None


def evaluate_candidate(item, query_text, target_platform=None, *, observed_pro=None, check_release=False):
    """Score candidate recipe or source across 4 dimensions: fit, platform, license, spatial."""
    score = 0
    issues = []
    item_title = item.get("title") or item.get("source_name", "")
    item_domain = item.get("domain") or item.get("source_type", "")
    item_lic = item.get("license", "unknown").lower()

    # 1. Functional fit must be independent of host names and license boilerplate.
    tokens = functional_terms(query_text)
    description = " ".join([
        item_title, item_domain, *item.get("inputs", []), *item.get("outputs", []),
        *item.get("gis_domains", []), *item.get("code_categories", []),
        *item.get("recommended_use_cases", []),
    ])
    matched_tokens = tokens & functional_terms(description)
    token_ratio = len(matched_tokens) / max(1, len(tokens))
    score += int(token_ratio * 40)

    # 2. Applicability is a gate, not a ranking bonus that other scores can beat.
    selected, resolution = selected_platforms(query_text, target_platform)
    compatible = bool(set(selected) & candidate_platforms(item))
    if compatible:
        score += 30
    else:
        issues.append(f"Platform mismatch: expected {target_platform or ', '.join(selected) or 'resolved target'}")
    if not selected:
        issues.append(f"Target platform unresolved ({resolution}); inspect the requested engine/host")
    if not matched_tokens:
        issues.append("No functional match beyond platform or generic UI terms")

    # 3. License Permissibility
    if any(p in item_lic for p in ["mit", "apache", "bsd", "cc0"]):
        score += 20
    elif "gpl" in item_lic:
        score += 15
        issues.append("Copyleft license (GPL): review distribution/compatibility obligations; process isolation is not an automatic exemption")
    elif "unknown" in item_lic or "unverified" in item_lic:
        issues.append("Unverified license: direct copy prohibited, study conceptual logic only")
    else:
        score += 10

    # 4. Spatial Fidelity
    if "spatial_constraints" in item:
        score += 10
    else:
        issues.append("No explicit spatial constraints declared")

    candidate_release = None
    if compatible and check_release and selected == ["arcgis-pro-sdk"]:
        release = ".".join(observed_pro.split(".")[:2]) if observed_pro else None
        candidate_release = next(
            (record for record in item.get("reviewed_revisions", []) if record["host_release"] == release),
            None,
        )
        if candidate_release is None:
            issues.append(
                f"Find a source revision matching the installed ArcGIS Pro {observed_pro} and verify the SDK."
                if observed_pro else "Observe the installed ArcGIS Pro release before selecting SDK code."
            )
    release_checked = check_release and selected == ["arcgis-pro-sdk"]
    applicable = compatible and bool(matched_tokens) and (not release_checked or candidate_release is not None)
    return {
        "score": min(100, score) if applicable else 0,
        "issues": issues,
        "applicable": applicable,
        "functional_match": bool(matched_tokens),
        "platform_resolution": resolution,
        "is_safe_to_adapt": applicable and "Unverified license" not in " ".join(issues),
        "reviewed_revision": candidate_release,
    }


def search_knowledge_base(query, platform=None, sources_data=None, recipes_data=None, *, native_inventory=None):
    if sources_data is None:
        sources_data = load_registry(SOURCES_PATH)
    if recipes_data is None:
        recipes_data = load_registry(RECIPES_PATH)

    sources = sources_data.get("sources", [])
    recipes = recipes_data.get("recipes", [])
    detected = detect_platforms(query)
    selected, resolution = selected_platforms(query, platform)
    observed_pro = arcgis_pro_version(native_inventory) if native_inventory is not None else None
    release_context = {"observed_pro": observed_pro, "check_release": native_inventory is not None}

    ranked_recipes = []
    research_recipes = []
    for r in recipes:
        eval_res = evaluate_candidate(r, query, target_platform=platform, **release_context)
        if not eval_res["applicable"]:
            if eval_res["functional_match"]:
                research_recipes.append({
                    "id": r.get("recipe_id"), "title": r.get("title"),
                    "domain": r.get("domain"), "use": "reference-only",
                    "issues": eval_res["issues"], "is_safe_to_adapt": False,
                })
            continue
        ranked_recipes.append({
            "type": "recipe",
            "id": r.get("recipe_id"),
            "title": r.get("title"),
            "domain": r.get("domain"),
            "language": r.get("language"),
            "state": r.get("state"),
            "license": r.get("license"),
            "code_snippet": r.get("code_snippet"),
            "score": eval_res["score"],
            "issues": eval_res["issues"],
            "is_safe_to_adapt": eval_res["is_safe_to_adapt"]
        })

    ranked_sources = []
    research_sources = []
    for s in sources:
        eval_res = evaluate_candidate(s, query, target_platform=platform, **release_context)
        source = {
            "type": "source",
            "id": s.get("source_id"),
            "name": s.get("source_name"),
            "url": s.get("source_url"),
            "languages": s.get("programming_languages"),
            "license": s.get("license"),
            "score": eval_res["score"],
            "issues": eval_res["issues"],
            "limitations": s.get("limitations")
        }
        if eval_res["applicable"]:
            if eval_res["reviewed_revision"] is not None:
                revision = eval_res["reviewed_revision"]
                source.update(url=revision["url"], reviewed_revision=revision,
                              runtime_status="NOT RUN")
            ranked_sources.append(source)
        elif eval_res["functional_match"]:
            research_sources.append({**source, "use": "reference-only", "is_safe_to_adapt": False})

    ranked_recipes.sort(key=lambda x: x["score"], reverse=True)
    ranked_sources.sort(key=lambda x: x["score"], reverse=True)

    results = {
        "query": query,
        "detected_platforms": detected,
        "selected_platforms": selected,
        "platform_resolution": resolution,
        "matching_recipes": ranked_recipes[:5],
        "matching_sources": ranked_sources[:5],
        "research_recipes": research_recipes[:5],
        "research_sources": research_sources[:5],
        "status": "candidates" if ranked_recipes or ranked_sources else "unresolved",
    }
    if native_inventory is not None and selected == ["arcgis-pro-sdk"]:
        results["observed_arcgis_pro_version"] = observed_pro
    return results


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", type=str, required=True, help="Natural language GIS code query")
    parser.add_argument("--platform", type=str, default=None, help="Reviewed target platform (arcgis-pro-sdk, arcpy, pyqgis/qgis, gdal, web-gis); unknown targets remain unresolved")
    parser.add_argument("--native-inventory", type=Path,
                        help="Use an observed toolchain_discovery.py --native receipt for Pro SDK reference matching")
    parser.add_argument("--include-engines", action="store_true",
                        help="Include offline engine capability matches from scripts/discover_engines.py")
    parser.add_argument("--format", choices=["text", "json"], default="text", help="Output format")
    args = parser.parse_args(argv)

    try:
        inventory = load_registry(args.native_inventory) if args.native_inventory is not None else None
        results = search_knowledge_base(args.query, platform=args.platform, native_inventory=inventory)
        if args.include_engines:
            if str(ROOT) not in sys.path:
                sys.path.insert(0, str(ROOT))
            from scripts import discover_engines  # noqa: E402
            results["engine_candidates"] = discover_engines.discover(
                query=args.query, platform=args.platform or ""
            )["candidates"][:10]
    except (AttributeError, KeyError, OSError, TypeError, ValueError) as error:
        parser.exit(2, f"Unable to read discovery inputs: {error}\n")

    if args.format == "json":
        print(json.dumps(results, indent=2, ensure_ascii=False))
    else:
        print(f"\n{'='*70}")
        print(f"GIS Code Discovery: '{args.query}'")
        print(f"Detected Platforms: {', '.join(results['detected_platforms'])}")
        print(f"Target resolution: {results['platform_resolution']}; status: {results['status']}")
        print(f"{'='*70}\n")
        print("Matching Code Recipes:")
        for r in results["matching_recipes"]:
            print(f"  [{r['score']}%] {r['title']} ({r['language']}, State: {r['state']}, License: {r['license']})")
            if r["issues"]:
                print(f"       Note: {'; '.join(r['issues'])}")
        print("\nMatching Authoritative Sources:")
        for s in results["matching_sources"]:
            print(f"  [{s['score']}%] {s['name']} ({s['url']})")
        print("\nResearch references only (not implementation matches):")
        for r in results["research_recipes"]:
            print(f"  {r['title']}: {'; '.join(r['issues'])}")
        for s in results["research_sources"]:
            print(f"  {s['name']} ({s['url']}): {'; '.join(s['issues'])}")
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
