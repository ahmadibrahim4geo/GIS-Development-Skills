#!/usr/bin/env python3
"""Offline-first bilingual discovery over unified GIS engine capability profiles.

Reuses scripts/search_catalog.py over references/project-catalog.json and joins
exact 1:1 records in references/engine-capability-profiles.json and
references/engine-capability-taxonomy.json without network calls or installs.
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

from scripts import gis_code_discovery, search_catalog  # noqa: E402


CATALOG_PATH = ROOT / "references" / "project-catalog.json"
PROFILES_PATH = ROOT / "references" / "engine-capability-profiles.json"
TAXONOMY_PATH = ROOT / "references" / "engine-capability-taxonomy.json"

# Maps normalized Arabic & English query terms deterministically to identical atomic capabilities.
BILINGUAL_CAPABILITY_MAP: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("crs.transform", ("تحويل احداثيات", "إحداثيات", "احداثيات", "مسقط", "مساقط", "اسقاط", "projection", "reprojection", "coordinate", "crs", "datum", "epsg", "proj")),
    ("crs.vertical", ("ارتفاعات راسية", "مرجع راسي", "geoid", "vertical datum", "vertical")),
    ("render.globe.ellipsoid", ("كره ارضيه", "كرة ارضية", "جلوب", "ثلاثي الابعاد", "ثلاثية الابعاد", "globe", "3d globe", "ellipsoid", "cesium", "ecef")),
    ("render.3d.terrain", ("تضاريس ثلاثيه", "تضاريس ثلاثية", "3d terrain", "quantized mesh", "terrain")),
    ("render.3d.tiles", ("بلاطات ثلاثيه", "3d tiles", "i3s", "citygml")),
    ("render.2d.projected", ("خريطه ثنائيه", "رسم خرائط", "2d map", "projected map", "openlayers")),
    ("render.2d.vector_tiles", ("بلاطات متجهه", "vector tiles", "mvt", "pmtiles", "mbtiles", "maplibre")),
    ("render.symbology", ("ترميز", "رموز الخريطه", "خرائط تفاعليه", "symbology", "styling", "web map", "leaflet")),
    ("io.vector.read", ("فيكتور", "متجهات", "قراءه فيكتور", "vector", "shapefile", "geojson")),
    ("io.vector.gpkg.read", ("جيوباكدج", "geopackage", "gpkg")),
    ("io.raster.window", ("راستر", "مرئيات", "صور فضائيه", "raster", "geotiff", "rasterio")),
    ("io.cog", ("كوج", "cog", "cloud optimized geotiff")),
    ("raster.reproject", ("اعاده اسقاط الراستر", "raster reproject", "gdalwarp")),
    ("rs.indices", ("مؤشرات طيفيه", "ندفي", "اقمار صناعيه", "ndvi", "ndwi", "spectral", "satellite", "sentinel", "landsat")),
    ("rs.sar", ("رادار", "سار", "sar", "sentinel-1", "calibration", "backscatter")),
    ("eo.sar.calibration", ("معايره سار", "sar calibration", "snap", "otb")),
    ("vector.buffer", ("بفر", "نطاق حول", "buffer")),
    ("vector.overlay", ("تقاطع", "دمج متجهات", "overlay", "intersection", "clip", "clipper")),
    ("vector.spatial_join", ("ربط مكاني", "spatial join")),
    ("vector.snap", ("التقاط", "سناب", "snapping", "snap")),
    ("cad.brep", ("كاد", "تصميم هندسي", "نواه هندسيه", "cad", "brep", "step", "occt", "freecad")),
    ("bim.ifc", ("بيم", "مباني ثلاثيه", "ifc", "bim", "ifcopenshell")),
    ("city.parcel.subdivide", ("تقسيم اراضي", "تصميم مدن", "تخطيط عمراني", "parcel", "cityengine", "urbansim", "procedural")),
    ("city.building.procedural", ("توليد مباني", "مباني بارامتريه", "cityjson", "3dcitydb", "procedural building")),
    ("city.road_geometry", ("هندسه طرق", "مقاطع شوارع", "road geometry", "streetmix", "corridor")),
    ("terrain.slope", ("انحدار", "ميول", "تضاريس", "slope", "aspect", "dem")),
    ("hydrology.watershed", ("سيول", "هيدرولوجيا", "احواض تصريف", "watershed", "flow accumulation", "hydrology")),
    ("io.pointcloud.laz", ("ليدار", "سحب نقطيه", "lidar", "point cloud", "las", "laz", "pdal")),
    ("db.spatial_sql", ("قاعده بيانات مكانيه", "بوست جيس", "دك دي بي", "spatial sql", "postgis", "duckdb", "spatialite")),
    ("service.tiles", ("خادم بلاطات", "tile server", "martin", "tegola")),
    ("service.stac", ("كتالوج ستاك", "ستاك", "stac")),
    ("routing.multimodal", ("توجيه", "شبكه طرق", "اقصر مسار", "routing", "isochrone", "valhalla", "osrm", "graphhopper")),
    ("simulation.traffic", ("محاكاه مرور", "حركه مرور", "traffic", "sumo", "matsim")),
    ("simulation.solar", ("محاكاه شمس", "ظلال", "solar", "ladybug")),
    ("ui.ribbon.command-registry", ("ريبون", "شريط ادوات", "واجهه", "ribbon", "command registry", "saribbon")),
    ("ui.rtl", ("عربي", "دعم العربيه", "rtl", "arabic")),
    ("offline.no-key", ("اوفلاين", "بدون نت", "بدون مفتاح", "مفتوح المصدر", "مجاني", "offline", "no-key", "local-first")),
    ("packaging.portable", ("حزمه محموله", "تشغيل محمول", "portable", "pyinstaller")),
)


def normalize_bilingual_text(text: str) -> str:
    """Normalize Arabic letters/diacritics and English case for consistent parity matching."""
    cleaned = text.casefold()
    cleaned = re.sub(r"[\u064b-\u065f\u0670\u0640]", "", cleaned)
    cleaned = re.sub(r"[أإآ]", "ا", cleaned)
    cleaned = cleaned.replace("ة", "ه").replace("ى", "ي")
    cleaned = re.sub(r"[^\w\u0600-\u06ff.+/-]+", " ", cleaned)
    return " ".join(cleaned.split())


def extract_bilingual_capabilities(query: str, taxonomy: dict[str, Any] | None = None) -> list[str]:
    """Resolve English or Arabic phrases deterministically into atomic capability IDs."""
    if not query.strip():
        return []
    norm = f" {normalize_bilingual_text(query)} "
    matched: set[str] = set()
    for cap_id, phrases in BILINGUAL_CAPABILITY_MAP:
        for phrase in phrases:
            pnorm = normalize_bilingual_text(phrase)
            if pnorm and ((f" {pnorm} " in norm) or (len(pnorm) >= 4 and pnorm in norm)):
                matched.add(cap_id)
                break
    if taxonomy:
        known_caps = {
            cid
            for dinfo in taxonomy.get("domains", {}).values()
            for cid in (dinfo["capabilities"] if isinstance(dinfo["capabilities"], list) else dinfo["capabilities"].keys())
        }
        matched &= known_caps
    return sorted(matched)


def _match_list_filter(values: list[str], expected: str) -> bool:
    needle = expected.casefold().strip()
    return any(needle == v.casefold() or needle in v.casefold() for v in values)


def discover(
    *,
    query: str = "",
    capabilities: list[str] | None = None,
    platform: str = "",
    language: str = "",
    license_filter: str = "",
    role: str = "",
    cost_class: str = "",
    include_quarantined: bool = False,
    include_code_hints: bool = False,
    catalog_data: dict[str, Any] | None = None,
    profiles_data: dict[str, Any] | None = None,
    taxonomy_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Discover compatible engines offline deterministically across unified profiles."""
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    catalog = catalog_data or json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    profiles_doc = profiles_data or json.loads(PROFILES_PATH.read_text(encoding="utf-8"))
    taxonomy = taxonomy_data or json.loads(TAXONOMY_PATH.read_text(encoding="utf-8"))

    by_pid_cat = {p["project_id"]: p for p in catalog["projects"]}
    explicit_caps = sorted({c.strip() for c in (capabilities or []) if c.strip()})
    inferred_caps = extract_bilingual_capabilities(query, taxonomy)
    target_caps = sorted(set(explicit_caps) | set(inferred_caps))

    # Reuse scripts/search_catalog.py strictly as baseline text filter when no atomic cap inferred.
    catalog_text_hits = {
        item["project_id"]
        for item in search_catalog.search(catalog["projects"], query=query, platform="", category="")
    } if query.strip() else set()

    quarantined_excluded = 0
    matches: list[dict[str, Any]] = []
    for prof in profiles_doc["profiles"]:
        pid = prof["project_id"]
        cat = by_pid_cat.get(pid, {})
        vm = prof["verification_metadata"]

        if not include_quarantined and vm.get("security_status") == "quarantine-reference-only":
            quarantined_excluded += 1
            continue

        if platform and not (
            _match_list_filter(prof.get("platforms", []), platform)
            or _match_list_filter(vm.get("supported_os", []), platform)
            or (platform.casefold() in {"windows", "linux", "macos"} and "cross-platform" in vm.get("supported_os", []))
        ):
            continue
        if language and not _match_list_filter(prof.get("languages", []), language):
            continue
        if role and prof.get("primary_role", "").casefold() != role.casefold() and not _match_list_filter(prof.get("secondary_roles", []), role):
            continue
        if cost_class and vm.get("cost_classification", "").casefold() != cost_class.casefold():
            continue
        if license_filter and license_filter.casefold() not in (vm.get("license_spdx_hint", "") + " " + vm.get("cost_classification", "")).casefold():
            continue

        prof_caps = prof.get("capabilities", {})
        if explicit_caps and not all(c in prof_caps for c in explicit_caps):
            continue

        cap_hits = sorted(c for c in target_caps if c in prof_caps)
        text_hit = pid in catalog_text_hits

        if explicit_caps:
            relevance = len(cap_hits) + (1 if text_hit else 0)
        elif target_caps:
            if not cap_hits and not text_hit:
                continue
            relevance = len(cap_hits) * 10 + (1 if text_hit else 0)
        elif query.strip():
            if not text_hit:
                continue
            relevance = 1
        else:
            relevance = len(prof_caps)

        if target_caps and relevance == 0:
            continue

        matches.append(
            {
                "project_id": pid,
                "name": prof["name"],
                "url": cat.get("url", vm.get("github_url")),
                "entity_type": prof["entity_type"],
                "primary_role": prof["primary_role"],
                "platforms": prof["platforms"],
                "supported_os": vm["supported_os"],
                "languages": prof["languages"],
                "cost_classification": vm["cost_classification"],
                "license_status": vm["license_status"],
                "license_spdx_hint": vm["license_spdx_hint"],
                "security_status": vm["security_status"],
                "trust_level": vm["trust_level"],
                "matched_capabilities": cap_hits,
                "relevance_score": relevance,
            }
        )

    matches.sort(key=lambda item: (-item["relevance_score"], item["project_id"]))

    gaps: list[str] = []
    if not matches:
        gaps.append(
            "No offline cataloged engine matched the requested capabilities/constraints; verify spelling or open a documented ADR gap."
        )

    result: dict[str, Any] = {
        "schema_version": "1.0",
        "mode": "offline-first",
        "query": query,
        "resolved_capabilities": target_caps,
        "status": "candidates" if matches else "no-match",
        "total_matches": len(matches),
        "quarantined_excluded_count": quarantined_excluded,
        "candidates": matches,
        "gaps": gaps,
        "note": "Offline discovery over reviewed catalog metadata only; native builds/benchmarks are NOT RUN.",
    }
    if include_code_hints and query.strip():
        result["code_discovery_hints"] = gis_code_discovery.search_knowledge_base(query)
    return result


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", default="", help="Arabic or English geospatial engineering requirement")
    parser.add_argument("--capability", action="append", default=[], help="Required atomic capability ID (repeatable or comma-separated)")
    parser.add_argument("--platform", default="", help="Platform/OS filter (windows, linux, web, android, ios, qgis, desktop)")
    parser.add_argument("--language", default="", help="Programming language filter")
    parser.add_argument("--license", dest="license_filter", default="", help="SPDX hint or license substring")
    parser.add_argument("--role", default="", help="Primary/secondary role filter")
    parser.add_argument("--cost-class", default="", help="Cost classification filter")
    parser.add_argument("--include-quarantined", action="store_true")
    parser.add_argument("--include-code-hints", action="store_true")
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--format", choices=("json", "markdown"), default="json")
    args = parser.parse_args(argv)

    caps = [c.strip() for raw in args.capability for c in raw.split(",") if c.strip()]
    report = discover(
        query=args.query,
        capabilities=caps,
        platform=args.platform,
        language=args.language,
        license_filter=args.license_filter,
        role=args.role,
        cost_class=args.cost_class,
        include_quarantined=args.include_quarantined,
        include_code_hints=args.include_code_hints,
    )
    if args.limit >= 0:
        report["candidates"] = report["candidates"][: args.limit]

    if args.format == "json":
        print(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True))
    else:
        print(f"# Engine Discovery ({report['status']}) — {report['total_matches']} matches")
        print(f"- **Resolved Capabilities:** {', '.join(report['resolved_capabilities']) or 'none'}")
        for item in report["candidates"]:
            print(
                f"- `{item['project_id']}` ({item['entity_type']} · {item['cost_classification']} · {item['license_spdx_hint']}): "
                f"caps={','.join(item['matched_capabilities']) or '-'}"
            )
        for gap in report["gaps"]:
            print(f"- **Gap:** {gap}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
