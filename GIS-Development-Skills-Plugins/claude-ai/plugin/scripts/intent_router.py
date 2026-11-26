#!/usr/bin/env python3
"""Offline intent route hints and structural plan/approval declaration validation.

NO LLM, remote call, execution, authorization, file writes or OS isolation.
Run with --text for conservative bilingual keyword hints, optionally with
--context, or --plan for a JSON draft. --gate checks declarations only.
"""
import argparse
import copy
import json
import re
import sys
from pathlib import Path, PurePosixPath

if __package__:
    from .contextual_routing import WEB_SKILLS, web_ui_requested
else:
    try:
        from scripts.contextual_routing import WEB_SKILLS, web_ui_requested
    except ModuleNotFoundError as exc:
        if exc.name != "scripts":
            raise
        from contextual_routing import WEB_SKILLS, web_ui_requested

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
DOMAINS = (
    ("modern-web-guidance", ("modern-web-guidance", "modern web guidance")),
    ("geospatial-engine-selection", (
        "engine selection", "select engine", "choose engine", "compare engines", "recommend stack",
        "build new application", "use existing program source", "engine replacement", "source fork",
        "source-fork", "source-component-reuse", "reference ui", "reference-inspired-ui", "multi-engine",
        "multi engine", "embedded-engine", "build vs reuse", "build-vs-reuse",
        "اختيار محرك", "مقارنة محركات", "بناء برنامج جديد", "بناء تطبيق جديد", "تطبيق مستقل من الصفر",
        "اعمل برنامج gis", "صمملي برنامج", "ابدأ من الصفر", "بدل ما تبدأ من الصفر", "اشتقاق",
        "فورك", "خد البرنامج", "خد qgis", "نضف qgis", "عدل على qgis", "شيل الأدوات", "نضّف qgis",
        "واجهة مثل arcgis", "عايز واجهة زي", "واجهه مثل", "شريط ريبون", "استبدال المحرك",
        "تغيير المحرك", "ابني على", "دمج محركين", "بديل مجاني لـ", "برنامج خفيف",
        "أداة صغيرة", "اداه صغيره", "تحويل إحداثيات فقط", "محرك ثلاثي الابعاد", "محرك خرائط"
    )),
    ("gis-code-discovery", ("code discovery", "gis code", "code snippet", "code snippets", "sdk snippet", "arcgis sdk", "pyqgis snippet", "gdal sample", "gis recipe", "كود جغرافي", "خوارزمية جغرافية", "مقتطفات برمجية", "وصفات برمجية", "أمثلة برمجية", "كود python", "python code", "تنبؤ مكاني", "خوارزمية تنبؤ", "spatial prediction", "spatial machine learning", "تعلم آلي مكاني", "كود بحثي", "كودًا بحثيًا", "كودا بحثيا", "أكواد بحثية", "research code", "scikit-map", "ponytail", "caveman", "token optimizer", "ترشيد توكنات", "هندسة سياق", "context engineering")),
    ("visual-asset-discovery-integration", ("thumbnail", "visual asset", "image search", "image sourcing", "official logo", "logos", "brand asset", "سامبنيل", "سنبنيل", "ثَمبنيل", "صورة مصغرة", "صورة لكل اختيار", "صور توضيحية", "شعار", "شعارات")),

("gis-architecture-visualization", ("archify", "architecture diagram", "workflow diagram", "draw a diagram", "interactive diagram", "visualize architecture", "diagram the", "ارسملي", "ارسم لي", "مخطط", "مين مسؤول عن مين", "وضحلي بنية", "وضّحلي بنية")),
    ("clean-room-reference-implementation", ("clean room", "clean-room", "reference software", "reference implementation", "feature parity", "reverse engineering", "الهندسة النظيفة", "الإطار المرجعي", "تحليل برنامج مرجعي", "دراسة برنامج مرجعي", "مضاهاة جوجل إيرث")),
    ("kml-kmz-engineering", ("kml", "kmz", "placemark", "كي ام ال", "كى ام ال", "ستايل km", "ملفات الكي")),
    ("gis-desktop-application-development", ("desktop", "standalone", "exe", "wpf", "زيرث", "zearth", "سطح المكتب", "برنامج مستقل", "تطبيق مستقل", "cad", "dark cad", "saribbon", "qt-ads", "lock-canvas-zoom", "كاد", "واجهة كاد", "برنامج كاد")),
    ("gis-mobile-application-development", ("android", "ios app", "iphone", "gnss", "offline sync", "mobile gis", "موبايل", "هاتف", "تطبيق جوال", "تطبيق أندرويد", "تطبيق اندرويد")),
    ("terrain-hydrology-lidar", ("terrain", "dem", "elevation", "lidar", "تضاريس", "ارتفاع", "المبالغة", "الترين", "sumo", "ladybug", "gully", "ponding", "runoff coefficient", "سيول", "تصريف أمطار", "شمس وظلال", "مسار الشمس")),
    ("coordinate-reference-systems", ("crs", "epsg", "projection", "grid", "graticule", "خطوط الطول", "دوائر العرض", "الإحداثي", "مسقط")),
    ("gis-cartography-symbology", ("symbol", "style", "icon", "symbology", "أيقون", "الرموز", "ألوان", "ملصق")),
    ("arcgis-toolbox-engineering", ("arcgis", "arcpy", "arcmap", "pyt", "أرك جي", "بايثون تول")),
    ("qgis-plugin-development", ("qgis plugin", "processing provider", "qgis extension", "إضافة qgis", "بلجن كيو جي")),
    ("qgis-engine-integration", ("qgis engine", "qgis core", "qgis libraries", "qgis standalone", "qgis runtime", "محرك qgis", "مكتبات qgis", "محرك كيو جي")),
    ("geospatial-web-mapping", ("cesium", "maplibre", "web map", "globe", "ثلاثية الأبعاد", "كرة أرضية")),
    ("remote-sensing-pipelines", ("sentinel", "landsat", "gee", "satellite", "الاستشعار", "مرئيات", "cog", "cloud optimized geotiff", "طبقة cog", "تغطية زمنية", "temporal coverage", "ndvi", "ndwi", "ndmi", "savi", "evi", "nbr", "spectral index", "spectral indices", "مؤشر طيفي", "مؤشرات طيفية", "كلوروفيل", "حريق", "مياه سطحية", "رطوبة النبات")),
    ("geospatial-data-processing", ("gdal", "geopandas", "raster", "vector", "راستر", "فيكتور", "earcut", "clipper2", "opendrive", "streetmix", "dag cascade", "تثليث", "توبولوجيا بارامترية", "ارتدادات")),
    ("spatial-databases", ("postgis", "spatialite", "spatial sql", "قواعد البيانات المكانية")),
    ("geospatial-api-integration", ("api", "geocod", "gazetteer", "أسماء الأماكن", "بحث عن الأماكن", "خدمة stac", "stac api", "واجهة برمجة")),
    ("geospatial-data-discovery", ("download data", "stac", "مصادر البيانات", "تنزيل بيانات", "خصائص التربة", "soil", "التربة", "land cover", "الغطاء الأرضي", "غطاء أرضي", "خرائط خصائص")),
    ("geospatial-ai-agents", ("agent", "geoai", "automation", "وكيل", "الذكاء الاصطناعي", "qundostack", "qundocommand", "cad copilot", "مساعد كاد", "تراجع آمن", "ctrl+z")),
    ("mcp-integration-and-tool-orchestration", ("mcp", "model context protocol", "mcp server", "mcp tools", "سيرفرات mcp", "سيرفر mcp", "توجيه الأدوات", "تكامل الأدوات")),
    ("geospatial-data-catalogs", ("data catalog", "data repository", "gis catalog", "stac catalog", "كتالوج البيانات", "فهرس البيانات", "مستودعات البيانات", "بيانات بيئية", "environmental data", "مستودعات البيانات البيئية", "مستودع بيانات", "opengeohub", "openlandmap", "مصدر بيانات مفتوح")),
    ("gis-internationalization-arabic", ("i18n", "localization", "arabic ui", "bilingual", "تعريب", "ثنائي اللغة", "تعدد اللغات")),
    ("system-capabilities-and-permissions", ("device permissions", "system permissions", "camera permission", "microphone permission", "bluetooth permission", "صلاحيات الجهاز", "أذونات الجهاز", "إذن الكاميرا")),
    ("gis-device-context", ("sunlight", "device location", "device time", "time zone", "solar position", "ضوء الشمس", "موقع الجهاز", "المنطقة الزمنية")),
    ("gis-ui-command-audit", ("command audit", "unwired command", "dead button", "ribbon audit", "audit icons", "فحص الأوامر", "جرد الأوامر", "أيقونات غير مربوطة", "الأزرار مش شغالة")),
    ("gis-desktop-e2e-testing", ("end-to-end desktop", "desktop e2e", "ui automation", "uiautomation", "flaUI", "webview2 testing", "اختبارات التفاعل", "اختبار تشغيل الواجهة", "اختبار تطبيق ويندوز")),
    ("gis-data-flow-diagnostics", ("data flow", "data lineage", "gis diagnostics", "trace id", "تدفق البيانات", "تتبع البيانات", "رحلة البيانات", "تشخيص تدفق")),
    ("gis-ui-ux-design-testing", ("ui/ux", "ui ux", "ux design", "usability testing", "accessibility audit", "تصميم واجهة", "تصميم الواجهة", "تجربة المستخدم", "اختبار قابلية الاستخدام")),
    ("global-mapper-development", ("global mapper", "جلوبال مابر", "جلوبال مابَر")),
)
RISKS = {"low", "medium", "high", "critical"}
SIDE_EFFECTS = {"read", "write", "network", "destructive"}
STATUSES = {"draft", "approved"}
REASONING_LEVELS = {"L0", "L1", "L2", "L3", "L4", "L5"}
IMPACT_CLASSES = {"I0", "I1", "I2", "I3", "I4"}
ORDINAL_LEVELS = {"low", "medium", "high", "unknown"}
REVIEW_MODES = {"INDEPENDENT_AGENT", "HUMAN_REVIEW", "SELF_REVIEW", "NOT_RUN"}
CLASSIFIER_DIMENSIONS = (
    "complexity", "uncertainty", "coupling", "reversibility",
    "scientific_impact", "security_impact", "external_effect",
    "environment_readiness", "scope_clarity", "user_requested_depth",
)
VISUALIZATION_SKILL = "gis-architecture-visualization"
VISUALIZATION_FIELDS = {
    "purpose": {"architecture-explanation", "feature-design", "cross-component-diagnosis", "structural-change"},
    "diagram_type": {"architecture", "workflow", "sequence", "dataflow", "lifecycle", "erd", "class", "tree", "timeline", "waterfall"},
    "evidence_basis": {"proposed", "source-reviewed", "runtime-observed"},
    "language": {"en", "ar"},
}
ARCHITECTURE_CHANGES = {"ui-reorganization", "ui-shell-migration", "engine-integration", "engine-replacement"}
ARCHITECTURE_ROLES = {"ui_framework": "ui-shell", "renderer": "map-renderer", "gis_engine": "geospatial-engine"}
TASK_CONTRACT_FIELDS = ("command_id", "trace_id", "input_artifact_id", "output_artifact_id",
                        "input_schema", "output_schema", "input_contract", "output_contract")


def architecture_hints(request):
    """Flag a review question, never choose a host/engine from UI terminology."""
    text = request.casefold()
    signals = []
    if re.search(r"\bribbon\b|ريبون|ريبُن|الشريط|شريط الأدوات", text):
        signals.append("command-surface")
    if re.search(r"ui[.-]?js|ui framework|ui shell|frontend|front-end|محرك واجه|إطار واجه|اطار واجه", text):
        signals.append("ui-component-identity")
    if re.search(r"migrat|re-shell|replace.*engine|swap.*engine|حو[ّ]?ل.*واجه|نقل.*أدوات|استبد[ال].*محرك|دمج.*واجه", text):
        signals.append("architecture-change")
    isolated = bool(re.search(r"\b(change|rename|recolor)\b.*\b(label|colou?r|text|icon)\b|غي[ّ]?ر.*(لون|اسم|نص|أيقون)|غير.*(لون|اسم|نص|ايقون)", text))
    required = bool(signals) and not (isolated and not any(s != "command-surface" for s in signals))
    return {"required": required, "signals": signals,
            "basis": "lexical-hints-only", "delivery_model": "unresolved" if required else None,
            "next_step": "Host must distinguish source host, delivery host, changed component and protected behavior; inspect named components before selecting an adapter."}


def classify_reasoning_profile(dimensions):
    """Deterministically map explicit ordinal fields to L0-L5 and orthogonal I0-I4.

    Operates ONLY on structured JSON flags/ordinals; never parses raw natural
    language and never authorizes side effects or host permissions.
    """
    if not isinstance(dimensions, dict):
        raise ValueError("dimensions must be a JSON object")
    clean = {}
    high_defaults = {"reversibility", "scope_clarity", "environment_readiness"}
    for key in CLASSIFIER_DIMENSIONS:
        default_val = "high" if key in high_defaults else ("low" if key != "user_requested_depth" else None)
        val = dimensions.get(key, default_val)
        if key == "user_requested_depth":
            if val is not None and val not in REASONING_LEVELS and val not in ORDINAL_LEVELS:
                raise ValueError(f"invalid user_requested_depth: {val}")
            clean[key] = val
        else:
            if val not in ORDINAL_LEVELS:
                raise ValueError(f"{key} must be one of {sorted(ORDINAL_LEVELS)}")
            clean[key] = val

    read_only = bool(dimensions.get("read_only", False))
    multi_file = bool(dimensions.get("multi_file", False))
    unsupported = bool(dimensions.get("unsupported_or_forbidden", False))

    if unsupported:
        impact = "I4"
    elif clean["external_effect"] == "high" or clean["security_impact"] == "high" or (not read_only and clean["reversibility"] == "low"):
        impact = "I3"
    elif (not read_only and (multi_file or clean["coupling"] in ("medium", "high") or clean["scientific_impact"] == "high" or clean["external_effect"] == "medium" or clean["reversibility"] == "unknown")):
        impact = "I2"
    elif not read_only:
        impact = "I1"
    else:
        impact = "I0"

    if clean["scientific_impact"] == "high" and clean["uncertainty"] in ("high", "unknown"):
        depth = "L5"
    elif clean["coupling"] == "high" and clean["complexity"] == "high":
        depth = "L4"
    elif clean["uncertainty"] in ("high", "unknown") or (clean["complexity"] == "high" and clean["scope_clarity"] in ("low", "unknown")):
        depth = "L3"
    elif clean["complexity"] == "medium" or clean["coupling"] == "medium" or clean["scientific_impact"] == "medium" or multi_file or clean["environment_readiness"] in ("low", "unknown"):
        depth = "L2"
    elif not read_only:
        depth = "L1"
    else:
        depth = "L0"

    if impact in ("I3", "I4") and int(depth[1]) < 2:
        depth = "L2"

    warnings = []
    req_depth = clean.get("user_requested_depth")
    depth_map = {"low": "L1", "medium": "L2", "high": "L4", "unknown": "L3"}
    mapped_req = depth_map.get(req_depth, req_depth)
    if mapped_req in REASONING_LEVELS:
        if int(mapped_req[1]) > int(depth[1]):
            depth = mapped_req
        elif int(mapped_req[1]) < int(depth[1]):
            warnings.append(f"user_requested_depth '{req_depth}' cannot downgrade required workflow depth '{depth}' or security gate '{impact}'")

    methods = ["Adaptive Reasoning"]
    if clean["scientific_impact"] in ("medium", "high"):
        methods.append("Scientific Reasoning")
    if clean["uncertainty"] in ("high", "unknown"):
        methods.extend(["Uncertainty Management", "Root Cause Analysis"])
    if impact in ("I2", "I3") or depth in ("L4", "L5"):
        methods.extend(["Systems Thinking", "Decision Intelligence", "Critical Thinking"])

    return {
        "schema_version": "1.0",
        "reasoning_level": depth,
        "impact_class": impact,
        "requires_plan_review": impact in ("I2", "I3"),
        "requires_high_impact_gate": impact == "I3",
        "blocked": impact == "I4",
        "warnings": warnings,
        "recommended_methods": list(dict.fromkeys(methods)),
        "note": "Deterministic ordinal mapping only; host still owns semantic review and user authorization.",
    }


def available_skills(root=SKILLS):
    return {p.parent.name for p in Path(root).glob("*/SKILL.md")}


def route_hints(request, known=None):
    """Lexical hints only; do NOT treat as semantic extraction."""
    if known is None:
        known = available_skills()
    lowered = request.casefold()
    hits = [name for name, tokens in DOMAINS
            if name in known and any(token in lowered for token in tokens)]
    web_skills = list(WEB_SKILLS) if web_ui_requested(request) else []
    if web_skills:
        hits.extend(name for name in ("gis-ui-ux-design-testing", *WEB_SKILLS) if name in known)
    if "gis-security-guardian" in known:
        hits.append("gis-security-guardian")
    architecture_review = architecture_hints(request)
    # A request for ribbon/integration must reach intake even when no installed
    # domain keyword matches. Do not force a QGIS plugin or standalone engine.
    if architecture_review["required"] and "prompt-intent-orchestrator" in known:
        hits.append("prompt-intent-orchestrator")
    return {
        "schema_version": "1.0",
        "stage": "draft_hints_only",
        "original_request": request,
        "goal": None,
        "target": None,
        "desired_outcomes": [],
        "next_step": "Hosting AI must infer and show the user goal, deliverables, constraints and measurable success criteria; no execution from keywords.",
        "language_hint": "ar" if re.search(r"[\u0600-\u06ff]", request) else "en",
        "suggested_skills": list(dict.fromkeys(hits)),
        **({"required_web_skills": web_skills} if web_skills else {}),
        "requires_semantic_review": True,
        "architecture_review": architecture_review,
        "approval": "not_requested",
        "note": "Keyword matches only. A human/LLM must identify tasks, uncertainties, acceptance tests and obtain approval before tool dispatch."
    }


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _local_ref(value):
    """A project-relative reference only; no read, fetch or execution here."""
    if not _text(value) or "\\" in value or ":" in value or "\x00" in value:
        return False
    path = PurePosixPath(value)
    return bool(path.parts) and not path.is_absolute() and path.as_posix() == value and not any(p in (".", "..") for p in path.parts)


def validate_architecture(task, prefix):
    """Validate declared intent separately from renderer configuration."""
    if "architecture" not in task:
        return []
    declaration = task["architecture"]
    fields = {"schema_version", "change_type", "source_host", "target_host", *ARCHITECTURE_ROLES,
              "integration_mode", "preserved_invariants", "command_inventory_ref", "flow_spec_ref"}
    if not isinstance(declaration, dict):
        return [prefix + ".architecture must be an object"]
    errors = []
    pref = prefix + ".architecture"
    if set(declaration) != fields:
        errors.append(pref + " must contain exactly the documented architecture fields")
    if declaration.get("schema_version") != "1.0":
        errors.append(pref + ".schema_version must be 1.0")
    change_type = declaration.get("change_type")
    if not isinstance(change_type, str) or change_type not in ARCHITECTURE_CHANGES:
        errors.append(pref + ".change_type is invalid")
    for key in ("source_host", "target_host"):
        if not _text(declaration.get(key)):
            errors.append(pref + "." + key + " must name a host or explicitly say unresolved")
    for key, role in ARCHITECTURE_ROLES.items():
        component = declaration.get(key)
        if not isinstance(component, dict):
            errors.append(pref + "." + key + " must declare component identity")
            continue
        if set(component) != {"name", "role", "status", "source_ref", "version"}:
            errors.append(pref + "." + key + " has missing or unknown identity fields")
        if not _text(component.get("name")) or component.get("role") != role:
            errors.append(pref + "." + key + " needs a name and role " + role)
        state = component.get("status")
        if state not in ("unresolved", "source-reviewed"):
            errors.append(pref + "." + key + ".status is invalid")
        for name in ("source_ref", "version"):
            value = component.get(name)
            if value is not None and not _text(value):
                errors.append(pref + "." + key + "." + name + " must be text or null")
            if state == "source-reviewed" and not _text(value):
                errors.append(pref + "." + key + "." + name + " is required for source-reviewed identity")
    if declaration.get("integration_mode") not in ("in-process", "worker-ipc", "service", "unresolved"):
        errors.append(pref + ".integration_mode is invalid")
    invariants = declaration.get("preserved_invariants")
    if not isinstance(invariants, list) or not invariants or any(not _text(v) for v in invariants):
        errors.append(pref + ".preserved_invariants must be nonempty strings")
    for key in ("command_inventory_ref", "flow_spec_ref"):
        value = declaration.get(key)
        if value is not None and not _local_ref(value):
            errors.append(pref + "." + key + " must be a safe project-relative path or null")
    return errors


def architecture_blockers(declaration):
    """Discovery gaps, NOT a runtime check or an authenticated action gate."""
    blockers = []
    for key in ("source_host", "target_host", "integration_mode"):
        if re.search(r"\b(unknown|unresolved|unverified|uninspected)\b|غير (معروف|محسوم|محدد)|مجهول", declaration[key].casefold()):
            blockers.append(key + " is unresolved")
    blockers.extend(key + " identity/version is unresolved" for key in ARCHITECTURE_ROLES
                    if declaration[key]["status"] == "unresolved")
    for key in ("command_inventory_ref", "flow_spec_ref"):
        if declaration[key] is None:
            blockers.append(key + " requires discovery before implementation")
    return blockers


def validate_visualization(task, prefix):
    """Validate an optional declared handoff, never infer or execute a diagram."""
    selected = task.get("skills")
    has_skill = isinstance(selected, list) and VISUALIZATION_SKILL in selected
    if not has_skill and "visualization" not in task:
        return []
    errors = []
    if not has_skill:
        errors.append(prefix + ".visualization requires selecting " + VISUALIZATION_SKILL)
    declaration = task.get("visualization")
    if not isinstance(declaration, dict):
        return errors + [prefix + ".visualization must declare purpose, diagram_type, evidence_basis and language"]
    for key, choices in VISUALIZATION_FIELDS.items():
        value = declaration.get(key)
        if not isinstance(value, str) or value not in choices:
            errors.append(prefix + ".visualization." + key + " is missing or invalid")
    if set(declaration) - set(VISUALIZATION_FIELDS):
        errors.append(prefix + ".visualization contains unknown fields")
    return errors


def validate_plan(plan, known=None, require_approved=False):
    """Return structural errors, never execute the plan."""
    if known is None:
        known = available_skills()
    errors = []
    if not isinstance(plan, dict):
        return ["Plan must be a JSON object"]
    if plan.get("schema_version") != "1.0":
        errors.append("schema_version must be 1.0")
    for field in ("request_id", "revision", "original_request"):
        if not _text(plan.get(field)):
            errors.append(field + " must be a nonempty string")
    if plan.get("language") not in ("ar", "en"):
        errors.append("language must be ar or en")
    status = plan.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        errors.append("status must be draft or approved")
    for field in ("assumptions", "open_questions"):
        val = plan.get(field)
        if not isinstance(val, list) or any(not _text(x) for x in val):
            errors.append(field + " must be a list of strings")
    for field in ("constraints", "non_goals", "material_unknowns", "inferred_assumptions", "preferences", "explicit_requirements", "protected_inputs"):
        if field in plan and (not isinstance(plan[field], list) or any(not _text(v) for v in plan[field])):
            errors.append(field + " must be a list of nonempty strings")
    if "approval_evidence_ref" in plan:
        aer = plan.get("approval_evidence_ref")
        if not (_text(aer) or (isinstance(aer, dict) and bool(aer))):
            errors.append("approval_evidence_ref must be a nonempty string or object when provided")
    if "intent_revision" in plan and not _text(plan.get("intent_revision")):
        errors.append("intent_revision must be a nonempty string when provided")
    if "reasoning_level" in plan and plan.get("reasoning_level") not in REASONING_LEVELS:
        errors.append("reasoning_level must be one of L0..L5")
    impact_class = plan.get("impact_class")
    if "impact_class" in plan:
        if impact_class not in IMPACT_CLASSES:
            errors.append("impact_class must be one of I0..I4")
        elif impact_class == "I4":
            errors.append("impact_class I4 is forbidden or unsupported and cannot pass workflow gate")
    if "decision_capsules" in plan:
        capsules = plan["decision_capsules"]
        if not isinstance(capsules, list):
            errors.append("decision_capsules must be a list")
        else:
            for idx, cap in enumerate(capsules):
                if not isinstance(cap, dict):
                    errors.append(f"decision_capsules[{idx}] must be an object")
                    continue
                for req in ("decision_id", "question", "selection", "short_rationale"):
                    if not _text(cap.get(req)):
                        errors.append(f"decision_capsules[{idx}].{req} must be a nonempty string")
                rm = cap.get("review_mode")
                if rm is not None and rm not in REVIEW_MODES:
                    errors.append(f"decision_capsules[{idx}].review_mode is invalid")
    approval = plan.get("approval")
    if not isinstance(approval, dict):
        approval = {}
        errors.append("approval must be an object")
    for field in ("approved_by_user", "high_risk_approved"):
        if type(approval.get(field)) is not bool:
            errors.append("approval." + field + " must be boolean")
    if not isinstance(approval.get("approved_revision"), (str, type(None))):
        errors.append("approval.approved_revision must be string or null")
    tasks = plan.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        return errors + ["tasks must be a nonempty array"]
    ids = set()
    depends = {}
    high_risk = (impact_class == "I3")
    for n, task in enumerate(tasks):
        pref = "tasks[" + str(n) + "]"
        if not isinstance(task, dict):
            errors.append(pref + " must be an object")
            continue
        ident = task.get("id")
        if not _text(ident) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,39}", ident):
            errors.append(pref + ".id is invalid")
            continue
        if ident in ids:
            errors.append("duplicate task ID: " + ident)
        ids.add(ident)
        for field in ("title", "description", "kind"):
            if not _text(task.get(field)):
                errors.append(pref + "." + field + " must be a nonempty string")
        if task.get("priority") not in ("must", "should", "could"):
            errors.append(pref + ".priority invalid")
        risk = task.get("risk")
        if not isinstance(risk, str) or risk not in RISKS:
            errors.append(pref + ".risk invalid")
        if risk in ("high", "critical"):
            high_risk = True
        selected = task.get("skills")
        if not isinstance(selected, list) or not selected or any(not _text(x) or x not in known for x in selected):
            errors.append(pref + ".skills contain unknown or missing skill")
        if isinstance(selected, list) and "gis-security-guardian" not in selected:
            errors.append(pref + ".skills must include gis-security-guardian")
        errors.extend(validate_visualization(task, pref))
        errors.extend(validate_architecture(task, pref))
        for field in TASK_CONTRACT_FIELDS:
            if field not in task:
                continue
            value = task[field]
            if field.endswith(("schema", "contract")):
                if not (_text(value) or isinstance(value, dict) and bool(value)):
                    errors.append(pref + "." + field + " must be a schema/reference object or nonempty text")
            elif not _text(value):
                errors.append(pref + "." + field + " must be nonempty text")
        deps = task.get("depends_on")
        if not isinstance(deps, list) or any(not _text(x) for x in deps):
            errors.append(pref + ".depends_on must be string array")
            deps = []
        if ident in deps:
            errors.append(pref + " cannot depend on itself")
        if len(deps) != len(set(deps)):
            errors.append(pref + " contains duplicate dependencies")
        depends[ident] = deps
        contracts = task.get("handoff_contracts", [])
        if not isinstance(contracts, list):
            errors.append(pref + ".handoff_contracts must be an array")
        else:
            seen_contracts = set()
            for item in contracts:
                if (not isinstance(item, dict) or set(item) != {"from_task", "contract_ref"}
                        or not _text(item.get("from_task")) or item["from_task"] not in deps
                        or not _local_ref(item.get("contract_ref"))):
                    errors.append(pref + ".handoff_contracts needs a dependency from_task and local contract_ref")
                elif item["from_task"] in seen_contracts:
                    errors.append(pref + ".handoff_contracts has duplicate dependency contract")
                else:
                    seen_contracts.add(item["from_task"])
        criteria = task.get("acceptance_criteria")
        if not isinstance(criteria, list) or not criteria or any(not _text(x) for x in criteria):
            errors.append(pref + ".acceptance_criteria must be nonempty string array")
        tools = task.get("tools", [])
        if not isinstance(tools, list):
            errors.append(pref + ".tools must be array")
            continue
        for item in tools:
            if not isinstance(item, dict) or not _text(item.get("tool_id")) or not isinstance(item.get("side_effect"), str) or item["side_effect"] not in SIDE_EFFECTS:
                errors.append(pref + ".tools entries need tool_id and valid side_effect")
            elif item["side_effect"] == "destructive":
                high_risk = True
    for ident, deps in depends.items():
        for dep in deps:
            if dep not in ids:
                errors.append(ident + " depends on missing task " + dep)
    visiting, visited = set(), set()
    def walk(node):
        if node in visiting:
            errors.append("dependency cycle at " + node)
            return
        if node in visited:
            return
        visiting.add(node)
        for dep in depends.get(node, []):
            if dep in depends:
                walk(dep)
        visiting.remove(node)
        visited.add(node)
    for ident in depends:
        walk(ident)
    has_write_or_network = any(
        isinstance(t, dict) and isinstance(t.get("tools"), list) and any(
            isinstance(tool, dict) and tool.get("side_effect") in ("write", "network", "destructive")
            for tool in t["tools"]
        )
        for t in tasks
    )
    if impact_class == "I0" and (high_risk or has_write_or_network):
        errors.append("impact_class I0 cannot declare high/critical risks or mutating/network/destructive tools")
    if impact_class == "I1" and high_risk:
        errors.append("impact_class I1 cannot declare high/critical risks or destructive tools")
    if require_approved or status == "approved":
        if status != "approved" or approval.get("approved_by_user") is not True:
            errors.append("execution gate: plan is not user-approved")
        if not _text(plan.get("revision")) or approval.get("approved_revision") != plan.get("revision"):
            errors.append("execution gate: approval revision mismatch")
        if high_risk and approval.get("high_risk_approved") is not True:
            errors.append("execution gate: high-risk permission not declared")
    return errors



# A deterministic plan compiler: it organizes an agent-reviewed goal and its
# specialist tasks; it does NOT interpret natural language or execute tools.
WORKFLOW_PHASES = (
    "RECEIVED", "INTERPRETED", "DRAFTED", "AWAITING_REVIEW",
    "APPROVED", "ROUTED", "PREFLIGHT", "EXECUTING",
    "VERIFYING", "REPORTED",
)


def validate_goal_brief(plan):
    """Require a human/AI-authored and reviewable user outcome before routing."""
    if not isinstance(plan, dict):
        return ["Goal brief must be a JSON object"]
    errors = []
    if not _text(plan.get("goal")):
        errors.append("goal must describe the intended user outcome")
    if not _text(plan.get("target")):
        errors.append("target must describe the deliverable or project")
    for key in ("desired_outcomes", "success_criteria"):
        values = plan.get(key)
        if not isinstance(values, list) or not values or any(not _text(v) for v in values):
            errors.append(key + " must be a nonempty string array")
    # Existing plan v1 fields remain compatible; the goal-first workflow
    # requires these additional fields only when compiling a workflow.
    return errors


def ordered_tasks(tasks):
    """Stable topological ordering for a plan already validated against cycles."""
    tasks_by_id = {task["id"]: task for task in tasks}
    resolved, order = set(), []
    while len(resolved) < len(tasks):
        ready = [task for task in tasks
                 if task["id"] not in resolved
                 and all(dep in resolved for dep in task["depends_on"])]
        if not ready:
            raise ValueError("No valid task order (cycle or missing dependency)")
        for task in ready:
            order.append(tasks_by_id[task["id"]])
            resolved.add(task["id"])
    return order


def compile_workflow(plan, known=None, require_approved=False):
    """Emit an execution *blueprint* only. No shell, I/O writes or auth check.

    An AI hosting agent must semantically review the goal, verify the user's
    actual authorization, check installed tools and enforce side-effect limits.
    """
    errors = validate_plan(plan, known=known, require_approved=require_approved)
    errors.extend(validate_goal_brief(plan))
    if isinstance(plan, dict):
        for i, task in enumerate(plan.get("tasks", []) if isinstance(plan.get("tasks"), list) else []):
            if not isinstance(task, dict):
                continue
            selected = task.get("skills")
            owner = task.get("owner_skill")
            if not isinstance(owner, str) or not isinstance(selected, list) or owner not in selected or owner in (
                    "gis-security-guardian", "completion-evidence", "agent-development-journal",
                    "prompt-intent-orchestrator", "gis-development"):
                errors.append("tasks[{}].owner_skill must be a selected accountable domain specialist".format(i))
            if isinstance(selected, list) and selected and all(
                    skill in ("gis-security-guardian", "agent-development-journal",
                              "completion-evidence", "prompt-intent-orchestrator", "gis-development") for skill in selected):
                errors.append("tasks[{}] has no accountable domain specialist".format(i))
    result = {
        "schema_version": "1.0",
        "kind": "workflow_preview_only",
        "valid": not errors,
        "request_id": plan.get("request_id") if isinstance(plan, dict) else None,
        "revision": plan.get("revision") if isinstance(plan, dict) else None,
        "intent_revision": plan.get("intent_revision", plan.get("revision")) if isinstance(plan, dict) else None,
        "reasoning_level": plan.get("reasoning_level", "L2") if isinstance(plan, dict) else None,
        "impact_class": plan.get("impact_class", "I2") if isinstance(plan, dict) else None,
        "original_request": plan.get("original_request") if isinstance(plan, dict) else None,
        "goal": plan.get("goal") if isinstance(plan, dict) else None,
        "target": plan.get("target") if isinstance(plan, dict) else None,
        "desired_outcomes": plan.get("desired_outcomes") if isinstance(plan, dict) else None,
        "success_criteria": plan.get("success_criteria") if isinstance(plan, dict) else None,
        **{key: copy.deepcopy(plan[key]) for key in (
            "constraints", "non_goals", "assumptions", "open_questions",
            "material_unknowns", "inferred_assumptions", "preferences",
            "decision_capsules", "explicit_requirements", "protected_inputs",
            "approval_evidence_ref"
        ) if isinstance(plan, dict) and key in plan},
        "phases": list(WORKFLOW_PHASES),
        "status": "BLOCKED" if errors else "AWAITING_HOST_AUTHORIZATION" if require_approved else "AWAITING_REVIEW",
        "approval_declarations_checked": bool(require_approved and not errors),
        "authenticated_user_approval": False,
        "host_permissions_verified": False,
        "can_execute": False,
        "note": "Reviewable, ordered blueprint only. An authenticated host must check approval, tool availability, repository scope and security at dispatch.",
        "errors": errors,
        "steps": [],
        "handoffs": [],
    }
    if errors:
        return result
    task_order = ordered_tasks(plan["tasks"])
    for step_number, task in enumerate(task_order, start=1):
        owner = task["owner_skill"]
        step = {
            "step": step_number,
            "task_id": task["id"],
            "title": task["title"],
            "description": task["description"],
            "priority": task["priority"],
            "kind": task["kind"],
            "owner_skill": owner,
            "skills": task["skills"],
            "depends_on": task["depends_on"],
            "risk": task["risk"],
            "candidate_tools": task.get("tools", []),
            "acceptance_criteria": task["acceptance_criteria"],
            "status": "NOT_STARTED",
            "preflight": ["host tool availability", "host authorization", "GIS/data/license compatibility",
                          "security guardian", "data preservation and rollback"],
            "verification": "T0/T1 where possible; T2-T4 only on real target runtimes",
            "completion_gate": "completion-evidence (DoneProof); validate each acceptance criterion against fresh results",
            "journal_owner": "agent-development-journal",
        }
        for key in TASK_CONTRACT_FIELDS:
            if key in task:
                step[key] = copy.deepcopy(task[key])
        if "architecture" in task:
            step["architecture"] = copy.deepcopy(task["architecture"])
            step["architecture_blockers"] = architecture_blockers(task["architecture"])
            step["architecture_status"] = "NEEDS_DISCOVERY" if step["architecture_blockers"] else "REQUIRES_PREFLIGHT"
            step["preflight"].append("inspect referenced command inventory and validate_architecture_flow.py on flow_spec_ref; verify actual component/runtime compatibility")
        if "visualization" in task:
            step["visualization"] = {
                **task["visualization"],
                "renderer": "archify",
                "artifact_owner": VISUALIZATION_SKILL,
                "status": "NOT_STARTED",
                "runtime_verified": False,
                "gis_execution_proven": False,
            }
            step["preflight"].append("actual Node.js, Archify runtime and browser availability; local output and source privacy")
            if "architecture" in task:
                step["visualization"]["flow_spec_ref"] = task["architecture"]["flow_spec_ref"]
        result["steps"].append(step)
        contracts = {item["from_task"]: item["contract_ref"] for item in task.get("handoff_contracts", [])}
        for dep in task["depends_on"]:
            edge = {"from_task": dep, "to_task": task["id"], "kind": "task_dependency"}
            if dep in contracts:
                edge["contract_ref"] = contracts[dep]
            result["handoffs"].append(edge)
    return result


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    action = p.add_mutually_exclusive_group(required=True)
    action.add_argument("--text", help="Unstructured input; get lexical skill hints, NOT AI understanding")
    action.add_argument("--plan", type=Path, help="Structured JSON plan drafted by an agent or human")
    action.add_argument("--classify-profile", type=Path, help="Classify explicit ordinal dimensions JSON into L0-L5 and I0-I4 (no NLP)")
    p.add_argument("--format", choices=("text", "json"), default="text")
    p.add_argument("--context", type=Path, help="Optional delivery and runtime declarations; requires --text")
    p.add_argument("--gate", action="store_true", help="Check declared revision-scoped approval; never execute")
    p.add_argument("--workflow", action="store_true", help="Compile a goal-first dependency-ordered workflow preview; requires --plan, never executes")
    p.add_argument("--mcp-inventory", type=Path, help="Optional unverified MCP/native tool inventory for read-only capability preview; requires --workflow")
    args = p.parse_args(argv)
    if args.context and args.text is None:
        p.error("--context requires --text")
    if args.mcp_inventory and (not args.workflow or args.plan is None):
        p.error("--mcp-inventory requires --plan and --workflow")
    if args.classify_profile is not None:
        try:
            dims = json.loads(args.classify_profile.read_text(encoding="utf-8"))
            profile = classify_reasoning_profile(dims)
        except (OSError, ValueError) as exc:
            print("Invalid dimensions file: " + str(exc), file=sys.stderr)
            return 2
        if args.format == "json":
            print(json.dumps(profile, ensure_ascii=False, indent=2))
        else:
            print(f"Profile: {profile['reasoning_level']} / {profile['impact_class']} (plan_review={profile['requires_plan_review']}, high_impact_gate={profile['requires_high_impact_gate']})")
        return 1 if profile["blocked"] else 0
    if args.text is not None:
        if args.gate:
            p.error("--gate requires --plan")
        if args.workflow:
            p.error("--workflow requires --plan")
        out = route_hints(args.text)
        if args.context:
            try:
                if __package__:
                    from .contextual_routing import recommend
                else:
                    from contextual_routing import recommend
                context = json.loads(args.context.read_text(encoding="utf-8"))
                out["contextual_route"] = recommend(args.text, context, available_skills())
            except (OSError, ValueError) as exc:
                print("Invalid route context: " + str(exc), file=sys.stderr)
                return 2
        if args.format == "json":
            print(json.dumps(out, ensure_ascii=False, indent=2))
        else:
            print("Possible skills (keyword hints only):", ", ".join(out["suggested_skills"]))
            print(out["note"])
            if args.context:
                recommendation = out["contextual_route"]
                print("Context preview:", recommendation["status"], recommendation["delivery"] or "")
                print(recommendation["reason"])
        return 0
    try:
        plan = json.loads(args.plan.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        print("Invalid plan file: " + str(exc), file=sys.stderr)
        return 2
    if args.workflow:
        blueprint = compile_workflow(plan, require_approved=args.gate)
        if args.mcp_inventory and blueprint["valid"]:
            try:
                if __package__:
                    from .mcp_tool_router import route_plan
                else:
                    from mcp_tool_router import route_plan
                inventory = json.loads(args.mcp_inventory.read_text(encoding="utf-8"))
                blueprint["tool_route_preview"] = route_plan(plan, inventory)
                blueprint["tool_routing_note"] = "Candidate capabilities only; no live MCP discovery, authorization or invocation."
            except (OSError, ValueError, TypeError) as exc:
                blueprint["valid"] = False
                blueprint["status"] = "BLOCKED"
                blueprint["errors"].append("MCP inventory preview invalid: " + str(exc))
        if args.format == "json":
            print(json.dumps(blueprint, ensure_ascii=False, indent=2))
        else:
            print("Goal:", blueprint["goal"])
            print("Target:", blueprint["target"])
            print("Status:", blueprint["status"])
            for item in blueprint["steps"]:
                print("{step}. {task_id} [{owner_skill}] after {depends_on} - {title}".format(**item))
            for issue in blueprint["errors"]:
                print("ERROR:", issue)
            print(blueprint["note"])
        return 0 if blueprint["valid"] else 1
    errors = validate_plan(plan, require_approved=args.gate)
    if args.format == "json":
        print(json.dumps({"valid": not errors, "approved_gate_declared": bool(args.gate and not errors),
                          "errors": errors, "note": "No execution or authenticated approval is performed."}, indent=2))
    else:
        for issue in errors:
            print("ERROR: " + issue)
        if not errors:
            print("Plan structure valid" + ("; approval declarations present (NOT authenticated)" if args.gate else "; review still required"))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
