"""Conservative recommendations for bilingual GIS requests and local capabilities."""
import re
import unicodedata


# A route describes the requested deliverable, the skills responsible, and the
# capabilities that must be checked before using a particular implementation.
ROUTES = {
    "arcgis-toolbox": ("arcgis-toolbox-engineering", ("arcpy",), None),
    "arcgis-addin": ("gis-code-discovery", ("arcgis-pro-sdk",), None),
    "qgis-plugin": ("qgis-plugin-development", ("qgis",), None),
    "wpf-app": ("gis-desktop-application-development", ("dotnet",), None),
    "qt-app": ("gis-desktop-application-development", ("qt-sdk",), None),
    "landsat-processing": ("remote-sensing-pipelines", (), None),
    "basemap-license": ("geospatial-data-discovery", (), "geospatial-data-catalogs"),
    "snapping-audit": ("gis-ui-command-audit", (), "gis-desktop-e2e-testing"),
    "skill-quarantine": ("gis-security-guardian", (), None),
    "web-frontend": ("gis-ui-ux-design-testing", ("node", "python"), None),
}

MATCHES = {
    "arcgis-toolbox": (
        r"\barcpy\b|\.pyt\b|python toolbox|script tool|بايثون تول ?بوكس|تول ?بوكس.*بايثون",
    ),
    "arcgis-addin": (
        r"\baddin\b|\badd[ -]in\b|\bdaml\b|\barcgis pro sdk\b|زر.*(?:ريبون|شريط)|ribbon.*button|button.*ribbon",
        r"arcgis|ارك ?جي|\bdaml\b",
    ),
    "qgis-plugin": (
        r"qgis|كيو ?جي ?اس",
        r"plugin|بلج[ي]?ن|اضافه|processing provider|metadata\.txt",
    ),
    "wpf-app": (
        r"\bwpf\b|\.xaml\b|دبليو بي اف",
        r"standalone|desktop|window|app|build|design|مصمم|واجهه|مستقل|تطبيق|شاشه",
    ),
    "qt-app": (
        r"\bqt\b|pyside|pyqt|كيوت|كيو تي",
        r"standalone|desktop|window|app|build|design|مصمم|واجهه|مستقل|تطبيق|شاشه|\.ui\b",
    ),
    "landsat-processing": (
        r"landsat|لاندسات",
        r"ndvi|bands?|collection|pixel_qa|qa_pixel|حساب|باند|بندات|معالجه|مؤشر|سحب",
    ),
    "basemap-license": (
        r"basemap|map tiles|tile cache|خريطه (?:اساس|خلفيه)|بلاطات|بيز ماب",
        r"licen[cs]|terms|attribution|redistribut|رخص|ترخيص|نسب|توزيع|اوفلاين",
    ),
    "snapping-audit": (
        r"snapping|\bsnap\b|اسناب|سناب|التقاط",
        r"button|command|audit|doesn.t| broken|test|toggle|\bfix\b|زر|امر|مش شغال|مبيشتغلش|اختبر|اصلح",
    ),
    "skill-quarantine": (
        r"\bskills?\b|مهاره|اسكيل",
        r"quarantine|audit|sandbox|archive|عزل|حجر|مراجع|افحص",
    ),
}
VISUAL_DESIGN = re.compile(r"drag.and.drop|visual designer|رسم.*(?:الازرار|الواجهه)|سحب.*افلات|مصمم")
RESUME = re.compile(r"^(?:please )?(?:resume|continue|retry|كمل|اكمل|استكمل)(?:\s|$)")
BYPASS = re.compile(
    r"(?:ignore|skip|bypass|forge|fake) (?:the )?(?:prior instructions|approval|sandbox|permissions)|"
    r"(?:تجاهل|تخطي|تجاوز|زور) (?:الاذن|الصلاحيات|الموافقه|العزل|التعليمات)"
)
NEGATED = re.compile(r"\b(?:not|no|without|بدون|مش|بلاش)\s+(?:an?\s+|the\s+)?(?:arcpy|wpf|qt|qgis|plugin|sdk)\b")
CAPABILITIES = {"arcpy", "arcgis-pro-sdk", "qgis", "dotnet", "qt-sdk", "wpf-designer", "qt-designer", "node", "python"}
WEB_SKILLS = ("modern-web-guidance", "ui-ux-pro-max")
WEB_TARGET = re.compile(
    r"\b(?:html|css|javascript)\b|\.(?:html?|css|jsx|tsx|vue|svelte)\b|"
    r"\b(?:web (?:page|site|app(?:lication)?|ui|map|dashboard)|website|webpage|frontend|front-end|"
    r"landing page|webview2?|react (?:app|component|dashboard))\b|"
    r"صفحه (?:ويب|هبوط)|موقع (?:ويب|الكتروني|تعريفي)|تطبيق(?:ات)? ويب|واجهه ويب|خريطه ويب|فرونت ?اند"
)
UI_ACTION = re.compile(
    r"\b(?:build|create|make|design|implement|code|add|edit|update|fix|refactor|"
    r"modernize|redesign|review|improve|audit|convert|generate|change)\b|"
    r"اعمل|انش[ئي]|ابني|اكتب|صمم|نفذ|ضيف|اضف|عدل|غير|ظبط|طور|حسن|اصلح|حول|راجع"
)
NON_UI = re.compile(
    r"\b(?:backend[- ]only|server[- ]side only|plain text|copy[- ]only|"
    r"fix (?:an? |the )?(?:typo|spelling)|"
    r"(?:copy|translate|proofread|rename|inspect|open|read) (?:only )?(?:the )?(?:html|css|page))\b|"
    r"الباك ?اند فقط|النص فقط|ترجم النص|انسخ (?:الملف|النص)|اصلح خطا (?:مطبعي|املائي)"
)
BACKEND_TARGET = re.compile(
    r"\b(?:back[- ]?end|server[- ]side|api (?:routes?|endpoints?)|database migration)\b|"
    r"باك ?اند|مسار(?:ات)? الخادم|قاعده البيانات"
)
FRONTEND_DETAIL = re.compile(
    r"\b(?:html|css|frontend|front-end|full[- ]stack|forms?|buttons?|dialogs?|webview2?)\b|"
    r"واجهه|فرونت ?اند|نموذج|زر|نافذه"
)


def normalize(request):
    normalized = unicodedata.normalize("NFKC", request).casefold()
    normalized = re.sub(r"[\u0640\u064b-\u065f]", "", normalized)
    normalized = normalized.translate(str.maketrans("أإآىة", "ااايه"))
    return " ".join(normalized.split())


def web_ui_requested(request):
    text = normalize(request)
    return bool(WEB_TARGET.search(text) and UI_ACTION.search(text) and not NON_UI.search(text)
                and (not BACKEND_TARGET.search(text) or FRONTEND_DETAIL.search(text)))


def inspect_context(context):
    if not isinstance(context, dict) or set(context) - {"delivery", "available", "resume_ref"}:
        raise ValueError("Context must use only delivery, available and resume_ref")
    delivery = context.get("delivery")
    if delivery is not None and (not isinstance(delivery, str) or delivery not in ROUTES):
        raise ValueError("Unknown delivery route")
    available = context.get("available", [])
    if not isinstance(available, list) or any(not isinstance(v, str) or v not in CAPABILITIES for v in available):
        raise ValueError("Unknown available capability")
    resume_ref = context.get("resume_ref")
    if resume_ref is not None and (not isinstance(resume_ref, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,80}", resume_ref)):
        raise ValueError("resume_ref must be a task identifier")
    return delivery, set(available), resume_ref


def recommend(request, context, known):
    """Return a preview. Context and capabilities are declarations supplied by the host."""
    delivery, available, resume_ref = inspect_context(context)
    text = normalize(request)
    candidate_text = NEGATED.sub(" ", text)
    matches = [
        name for name, patterns in MATCHES.items()
        if all(re.search(pattern, candidate_text) for pattern in patterns)
    ]
    web_ui = web_ui_requested(candidate_text) or delivery == "web-frontend"
    if web_ui and (not matches or delivery == "web-frontend"):
        matches.append("web-frontend")
    # A command audit supports delivery of a plugin; it is not a second host.
    plugin_command_audit = "snapping-audit" in matches and ("qgis-plugin" in matches or delivery == "qgis-plugin")
    if plugin_command_audit and delivery != "snapping-audit":
        matches.remove("snapping-audit")
    result = {
        "status": "NEEDS_CONTEXT", "delivery": None, "alternatives": matches,
        "owner_skill": None, "supporting_skills": [], "capabilities_to_verify": [],
        "fallback": None, "confidence": "unresolved", "dispatch": "HOST_REVIEW_REQUIRED",
        "reason": "The requested deliverable is unresolved.",
    }
    if BYPASS.search(text):
        result.update(status="REJECT_BYPASS", reason="The request asks to bypass a permission or review boundary.")
        return result
    if RESUME.match(text) and not matches:
        if resume_ref:
            result.update(status="RESUME_RECHECK", reason="Re-read saved scope, revision, permissions and inputs.",
                          resume_ref=resume_ref)
        else:
            result["reason"] = "Resume requires a project task reference."
        return result
    if (delivery and matches and delivery not in matches) or (len(matches) > 1 and not delivery):
        result.update(status="CONFLICT", reason="Confirm the intended deliverable before routing.")
        return result
    selected = delivery or next(iter(matches), None)
    if selected is None:
        return result
    owner, required, supporting = ROUTES[selected]
    if web_ui:
        result["required_web_skills"] = list(WEB_SKILLS)
        result["web_readiness"] = "BOTH_REQUIRED_BEFORE_USE"
        if selected != "web-frontend":
            required += ROUTES["web-frontend"][1]
    if selected == "qgis-plugin" and plugin_command_audit:
        supporting = "gis-ui-command-audit"
    required = list(required)
    designer = None
    if selected in ("wpf-app", "qt-app") and VISUAL_DESIGN.search(text):
        designer = "wpf-designer" if selected == "wpf-app" else "qt-designer"
        required.append(designer)
    if designer and designer not in available:
        result["fallback"] = "Confirm a compatible visual designer or ask whether source-based UI editing meets the request."
    elif any(item not in available for item in required):
        result["fallback"] = "Verify the matching runtime or perform source review while it is unavailable."
    status = "RECOMMENDED" if owner in known else "OWNER_UNAVAILABLE"
    result.update(
        delivery=selected, status=status, owner_skill=owner if owner in known else None,
        supporting_skills=[name for name in (supporting, "gis-security-guardian") if name in known],
        capabilities_to_verify=[name for name in required if name not in available],
        confidence="declared-delivery" if delivery else "matched-deliverable",
        reason="Route matches the declared delivery or a combination of framework and task signals."
        if status == "RECOMMENDED" else "The required skill is absent from the local inventory.",
    )
    if web_ui and "modern-web-guidance" in known:
        result["supporting_skills"].append("modern-web-guidance")
    return result
