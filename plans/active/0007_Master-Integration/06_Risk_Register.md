# GIS Development Skills — Master Risk Register / سجل المخاطر الرئيسي

> **الحالة:** `DRAFT — للمراجعة والاعتماد مع الخطة 0007`  
> **التاريخ:** 2026-11-25  
> **النطاق:** المخاطر التقنية، الأمنية، التنظيمية، البيئية، ومخاطر التراخيص والاختبار عبر المراحل `P00–P11`.

---

## 1. ملخص المخاطر الموحد / Consolidated Risk Matrix

| Risk ID | الوصف / Description | المصدر | الاحتمالية (Prob) | الأثر (Impact) | المرحلة | استراتيجية التخفيف / Mitigation | المالك / Owner | الحالة |
|---|---|---|---|---|---|---|---|---|
| **RISK-01** | تغيّر سريع في صيغ ومواصفات Plugin لمنصات Codex وClaude وAntigravity وCursor | Plugin Lifecycle §6 | HIGH | HIGH | P02, P09 | فحص الوثائق الرسمية الـ 19 وCLI `--help` قبيل بناء كل Adapter؛ حصر التغييرات داخل `plugin-system/adapters/` وعقد `platforms.json` | Release / Adapter Maintainer | OPEN |
| **RISK-02** | نقص أو عدم دقة توثيق المنصة حول المزامنة المحلية أو حدود Marketplace | Plugin Lifecycle §6 | MEDIUM | HIGH | P09 | عدم افتراض دعم أي أمر غير مختبر؛ إرجاع `UNSUPPORTED` أو `MANUAL_ACTION_REQUIRED` صراحة في التقرير | Tester / Adapter Maintainer | OPEN |
| **RISK-03** | تسريب بيانات المالك أو مفاتيح API أو مسارات شخصية في Git أو ZIP أو Logs أو CI Artifacts | Plugin Lifecycle §8 | LOW | CRITICAL | P02, P09, P10 | عزل `owner-config.json` في `%LOCALAPPDATA%`، تفعيل allowlist صارمة في `build_skill_bundle.py`، فحص `git check-ignore` و`git ls-files` ومراجعة تنقيح التقارير | Security Guardian | OPEN |
| **RISK-04** | تأخر أو تعثر اعتماد النشر في المتاجر الخارجية أو حسابات المؤسسات (Enterprise approval/MFA) | Plugin Lifecycle §6, §8 | HIGH | MEDIUM | P09, P11 | فصل البناء والمزامنة المحلية تمامًا عن النشر الخارجي (`autoPublicPublish: false`) بحيث لا يتوقف التطوير المحلي أو CI | Owner / Release Maintainer | OPEN |
| **RISK-05** | كسر أدوات التحقق الحالية (`validate_catalog.py` / `tests/`) أو الموقع (`index.html`/`explorer.html`) عند إضافة `project_id` لـ `project-catalog.json` | Engine V2 §1, §8.2; r3 §18.3 | MEDIUM | CRITICAL | P03, P08 | تنفيذ الترحيل بصورة additive-only؛ الإبقاء على الحقول الإلزامية الـ 9 وقواعد `URL_PATTERN` في `validate_catalog.py`؛ تشغيل `validate_catalog.py` و`test_landing_page.py` فور كل تعديل | Programmer / Reviewer | OPEN |
| **RISK-06** | استمرار الرابط الخاطئ لـ `DuckDB Spatial` (`UDS-LIB-004` يشير لـ `duckdb/duckdb-skills` ويزعم `security_rating: safe`) وانتقاله لملفات القدرات | Engine V2 §1 (ص46) + فحص الجرد | HIGH | HIGH | P03 | إصلاح `UDS-LIB-004` بإسناد `https://github.com/duckdb/duckdb-spatial` لملف القدرات وتصحيح تصنيف مستودع المهارات إلى نوعه الفعلي؛ مراجعة جميع المزاعم المطلقة في السجل العمراني (78 مصدرًا) | Source Researcher / Security Guardian | OPEN |
| **RISK-07** | ازدواج وتكرار التقنيات بين سجلات Desktop (`project-catalog.json`، `urban-design-source-registry.json`) وWeb وMobile (`r3`) | User Req #4; V2 §8.2; r3 §18.3 | HIGH | HIGH | P03, P05, P06 | فرض قاعدة Single Source of Truth: تسجيل المستودع مرة واحدة في `project-catalog.json` بتوحيد GitHub URL، وربط خصائص المنصات والقدرات عبر `project_id` في `engine-capability-profiles.json` مع اختبارات `dedup` آلية | Knowledge Base Architect | OPEN |
| **RISK-08** | هلوسة أو اختلاق مكتبات/مستودعات/واجهات API أو دوال غير موجودة فعليًا أثناء التوصية أو توسيع الفهارس | Engine V2 §22.2, §28; User Req #9 | MEDIUM | CRITICAL | P03, P04, P07 | تطبيق درجات الادعاء السبع (`unresolved..target-verified`)؛ استخدام `engine_repo_metadata.py` (فحص `api.github.com` فقط) و`hard_gate` لإبقاء غير المؤكد `unknown`/`needs-evidence` ومنع توصيته كجاهز | Source Researcher / Tester | OPEN |
| **RISK-09** | تضارب دلالي بين حقول `urban-design-source-registry.json` (78 مصدرًا) و`engine-capability-profiles.json` | Engine V2 §1 | MEDIUM | MEDIUM | P03 | إنشاء جدول ربط (crosswalk) عبر `project_id` وإبقاء السجل العمراني سليمًا دون حذف حقوله أو إفساد أدواته، مع توثيق قيود الثقة والترخيص | Knowledge Base Architect | OPEN |
| **RISK-10** | تضخم ملفات `SKILL.md` واستنزاف نافذة سياق الوكيل بسبب إدراج 200+ مكتبة و38 قالبًا في ملفات المهارات مباشرة | Web/Mobile r3 §18.5; V2 §14 | HIGH | HIGH | P04, P05, P06 | تطبيق Progressive Disclosure صارم: إبقاء `skills/*/SKILL.md` موجزة (<180 سطرًا، وصف ≤1024 حرفًا) وترحيل كل الموسوعات والقوالب والجداول إلى ملفات متخصصة تحت `references/` | Skill Architect / Reviewer | OPEN |
| **RISK-11** | تحميل الموجه المركزي `skills/gis-development/SKILL.md` تفاصيل تنفيذية مفرطة أو إضعاف توجيهه الحالي | User Req #2; AGENTS.md | MEDIUM | HIGH | P08 | الإبقاء على `gis-development/SKILL.md` جدول توجيه رشيقًا يربط بالمهارة الجديدة `geospatial-engine-selection` ويمرّر التحقق التلقائي via `audit_skill_graph.py` | Architect / Reviewer | OPEN |
| **RISK-12** | تراجع وكسر في بعض المهارات الـ 35 أو اختبارات الوحدة الـ 75 القائمة أو واجهة Explorer/Wizard بعد التكامل | User Req #8, #9 | MEDIUM | HIGH | P08, P10 | تشغيل مجموعة `ANTI-REG-001..010` + كامل `python -m unittest discover -s tests -v` + `validate.yml` محليًا بعد كل مرحلة كبرى | Tester | OPEN |
| **RISK-13** | تداخل نطاق `geospatial-engine-selection` مع `gis-development` و`gis-code-discovery` و`qgis-engine-integration` | Engine V2 §14.1 | MEDIUM | MEDIUM | P04, P08 | فصل عقود الملكية بوضوح: اختيار المعمارية والمحرك (`geospatial-engine-selection`) ≠ التوجيه العام (`gis-development`) ≠ بحث الوصفات والأكواد (`gis-code-discovery`) ≠ تنفيذ QGIS (`qgis-engine-integration`) | Architect | OPEN |
| **RISK-14** | عدم اتساق تنسيق Progressive Disclosure وروابط المراجع عند تغليف الحزم عبر `build_skill_bundle.py` | Plugin Lifecycle §4 | MEDIUM | HIGH | P02, P08, P09 | اختبار فحص الروابط الداخلية و`ALLOWED_ROOT_DIRECTORIES` في `build_skill_bundle.py` في `P02` ثم في كل مرحلة لاحقة | Programmer / Tester | OPEN |
| **RISK-15** | استحالة بناء وتوقيع تطبيقات iOS/iPadOS (`MOB-02`, `MOB-QA-02`) في بيئة تطوير Windows محلية | Web/Mobile r3 §16.3 + Baseline | HIGH | MEDIUM | P06, P10 | التصريح المباشر بالقيود البيئية وتسجيل اختبارات البناء والتشغيل الفعلي لـ iOS كـ `NOT RUN` (لا `PASS` من Flutter Web أو ملفات Swift نظرية) | Mobile Owner / Tester | ACCEPTED_LIMITATION |
| **RISK-16** | غياب Android SDK / `adb` / `flutter` / `xcodebuild` أو أجهزة GNSS/RTK/BLE فعلية أثناء التطوير | `0006/PLAN.md` + Baseline | HIGH | MEDIUM | P06, P10 | فحص جاهزية الـ Toolchain أولًا (`toolchain_discovery.py`)؛ تنفيذ اختبارات العقود `T0/T1` محليًا، ووسم `T2–T4` غير المتوفرة بـ `NOT RUN` مع تحديد شروط تشغيلها | Tester / Device QA | ACCEPTED_LIMITATION |
| **RISK-17** | فرض خدمات تجارية مدفوعة أو استغلال شروط Free Tier مضللة (Cesium ion, ArcGIS Online, Google Maps, Mapbox, OSM tile scraping) | V2 §12; r3 §14, §16.5 | MEDIUM | CRITICAL | P03, P04, P05, P06 | فصل رخصة الكود عن رخصة البيانات والخدمة؛ فرض بوابة `free_only` افتراضيًا؛ حظر تنزيل بلاطات `tile.openstreetmap.org` للأوفلاين؛ توفير بيانات صناعية ومحلية (`PMTiles`/`GeoPackage`) للاختبار دون API Key | Security Guardian / Architect | OPEN |
| **RISK-18** | مخاطر أمنية أو حقن تعليمات (Prompt Injection) في الـ 50+ مهارة ومستودع خارجي المرشح (`V2 §26`, `r3 §13`, `New Skill/`) | V2 §26; r3 §13; AGENTS.md | HIGH | CRITICAL | P03, P04, P08 | حجر كل المصادر الخارجية كـ `reference-only` في `external-agent-skills-registry.json` و`New Skill/`؛ مراجعة الأذونات والتراخيص والاعتماديات (مع فحص `SkillSpector` الاختياري عند الإتاحة) ومنع التثبيت أو التنفيذ التلقائي | Security Guardian | OPEN |
| **RISK-19** | الخلط بين نجاح اختبارات JSON/Mock/Schema (`T0/T1`) وإثبات التشغيل الأصلي للمحركات والتطبيقات (`T2–T4`) | User Req #8; DoneProof | HIGH | CRITICAL | P04–P11 | تطبيق `validate_evidence_tiers.py` و`verify_completion.py`؛ فصل مخرجات `mock` عن `native_tests` وإجبار وسم `NOT RUN` عند غياب المضيف أو المتصفح أو الجهاز | Acceptance / Reviewer | OPEN |
| **RISK-20** | اختبارات عدم التراجع الحالية لا تغطي المسارات الجديدة للـ Engine Selection وقوالب الويب والموبايل والبلجنز | User Req #8 | MEDIUM | HIGH | P10 | إضافة مجموعة `ANTI-REG-001..010` ودمج `validate_engine_profiles.py` واختبارات `plugin-system/tests/` داخل `.github/workflows/validate.yml` | Tester | OPEN |
| **RISK-21** | تنفيذ اختبارات `E01–E40` يعتمد على جاهزية السكربتات الستة وملفات القدرات مسبقًا | Engine V2 §14.3, §17 | MEDIUM | HIGH | P04, P10 | احترام التبعيات في `03_Dependency_Graph.json`: إغلاق `P03` ثم بناء السكربتات الـ 6 في `P04` قبل تفعيل التحقق الشامل في `P10` | Project Coordinator | OPEN |
| **RISK-22** | اختبارات واجهة الويب الحقيقية (`WEB-QA-01..15` وPWA) تتطلب متصفحًا فعليًا وخدمة محلية وPlaywright | Web/Mobile r3 §19.2, §19.4 | MEDIUM | MEDIUM | P05, P10 | إعداد خادم محلي معزول (localhost) واستخدام بيانات محلية/Mock؛ وفي حال غياب المتصفح/Playwright وسم T3 بـ `NOT RUN` دون الادعاء | Web Tester | OPEN |
| **RISK-23** | تعذر التحقق الميداني الحقيقي لدقة GNSS/RTK (`MOB-QA-04/05`) أو ARCore/ARKit (`MOB-14`) بالمقارنة مع المحاكيات | Web/Mobile r3 §8, §19.3 | HIGH | MEDIUM | P06, P10 | الفصل التام بين اختبارات المحاكي (`simulator GNSS != field accuracy`) واختبارات المستقبل الخارجي (`NMEA/RTCM checkpoint`)؛ عدم ادعاء دقة سنتيمترية دون قياس مرجعي | Mobile Tester | OPEN |
| **RISK-24** | اتساع نطاق المراحل `P00–P11` (3 خطط + 160+ متطلب + 180+ اختبار) واحتمال تعثر التسليم إذا نُفذت دفعة واحدة بلا تدرج | User Req #7 | HIGH | HIGH | P00–P11 | تقسيم التنفيذ إلى 12 مرحلة متماسكة ببوابات قبول (`Programmer → Reviewer → Tester → Acceptance`)، وتشغيل المسارات المستقلة (`P05` Web و`P06` Mobile و`P07` Source Reuse بعد `P04`) بتوازٍ منضبط | Coordinator | OPEN |
| **RISK-25** | تعقيد الترحيل العكسي لعقد المعمارية (`ui-engine-architecture-contract.md` v1 → v2) وكسر `validate_architecture_flow.py` أو `intent_router.py` | Engine V2 §14.2 | MEDIUM | HIGH | P01, P04 | الحفاظ على مصدّق `v1.0` سليمًا كما هو في `validate_architecture_flow.py`، وإضافة مخطط `v2.0` منفصل بمُحوّل `v1→v2` واختبارات `test_engine_architecture_migration.py` و`E23–E24` | Architect / Programmer | OPEN |
| **RISK-26** | تعقيد خوارزمية تفكيك وتنظيف مصدر QGIS (`src/app/`, C++ signals/slots, dynamic QActions) دون كسر الحفظ أو CRS أو Undo | Engine V2 §5, §24 | HIGH | HIGH | P07 | تطبيق الترتيب الآمن الإلزامي (`HIDE → TEST → DISABLE → REMOVE only with proof`)؛ حماية الأوامر الـ 16 الأساسية وجمع `static` + `runtime` inventory دون اعتبار `grep` وحده كافيًا | UI Source / QGIS Engineer | OPEN |
| **RISK-27** | فشل التوافق والـ ABI والـ Threading والـ CRS عند تركيب عدة محركات (مثل Qt/QGIS مع WPF/.NET أو CesiumJS مع 2D projected view) | Engine V2 §11, §31; E05, E27, E38 | HIGH | HIGH | P04, P07 | فرض عقود الحدود (`DatasetRef`, `worker-ipc`, `WebView bridge`) وتحديد `thread_owner` و`async_policy` في Flow Spec؛ منع دمج إصدارات DLL متعارضة داخل عملية واحدة | Integration Engineer | OPEN |
| **RISK-28** | تعارض تراخيص عند تركيب المحركات (مثل `GPL-2.0-or-later` لـ QGIS مع تطبيق خاص أو مع وحدات Qt أو أصول خرائط تجارية) | Engine V2 §5.1, §12.2, §34; E12, E38 | HIGH | CRITICAL | P03, P04, P07, P09 | تشغيل بوابة الترخيص لكل نسخة ومكوّن وتبعية متعدية؛ طلب مراجعة قانونية واضحة وحظر التوزيع المدمج غير المتوافق وإنتاج `THIRD_PARTY_NOTICES` و`SBOM` قبل التسليم | License Reviewer | OPEN |
| **RISK-29** | انزلاق تصميم `reference-inspired-ui` (مثل واجهة ArcGIS Pro أو Google Earth Pro) إلى نسخ صور أو أيقونات أو DLLs أو ملفات DAML مملوكة | Engine V2 §6.1, E02, E40, E45 | MEDIUM | CRITICAL | P07, P10 | تطبيق مهارة `clean-room-reference-implementation`: حصر الإلهام في مواصفة التدفقات السلوكية فقط، واستخدام أصول حرة مستقلة (مثل Lucide / Material Symbols بعد فحص رخصها) وهوية أصلية مستقلة | Security / License Reviewer | OPEN |
| **RISK-30** | نشر تغييرات أو إصدارات عامة أو تعديل حسابات المالك على GitHub/Marketplaces دون موافقة أو صلاحية من المالك | Plugin Lifecycle §1, §8; Engine V2 §0; r3 §22 | LOW | CRITICAL | P02, P09, P11 | إغلاق النشر التلقائي افتراضيًا (`autoPublicPublish: false`)، عدم استخدام `pull_request_target` بصلاحيات كتابة، واستلزام موافقة المالك الصريحة قبل `-Publish` أو `git push` | Security Guardian / Release Owner | OPEN |

---

## 2. مصفوفة حرارة المخاطر / Risk Heat Map Summary

| الاحتمالية \ الأثر | **CRITICAL** | **HIGH** | **MEDIUM** | **LOW** |
|---|---|---|---|---|
| **HIGH** | RISK-18, RISK-19, RISK-28 | RISK-01, RISK-06, RISK-07, RISK-10, RISK-24, RISK-26, RISK-27 | RISK-04, RISK-15, RISK-16, RISK-23 | 0 |
| **MEDIUM** | RISK-05, RISK-08, RISK-17, RISK-29 | RISK-02, RISK-11, RISK-12, RISK-14, RISK-20, RISK-21, RISK-25 | RISK-09, RISK-13, RISK-22 | 0 |
| **LOW** | RISK-03, RISK-30 | 0 | 0 | 0 |

*(الإجمالي: 30 خطرًا — 9 حَرِجة `CRITICAL`، 14 عالية `HIGH`، 7 متوسطة `MEDIUM`).*

---

## 3. موانع البدء الإلزامية قبل كل مرحلة / Mandatory Pre-Phase Risk Blockers

| قبل بدء المرحلة | المخاطر الواجب ضبط بواباتها أولًا | شرط الرفع (Gate Release Condition) |
|---|---|---|
| **P01** | RISK-25 | تثبيت عدم تعديل قواعد `validate_architecture_flow.py` لـ `v1.0` بصورة كاسرة |
| **P02** | RISK-03, RISK-14, RISK-30 | إقرار قواعد `.gitignore` وعزل `owner-config.json` وإغلاق النشر التلقائي قبل أول تشغيل لـ `Update-All-Plugins` |
| **P03** | RISK-05, RISK-06, RISK-07, RISK-08, RISK-09, RISK-18 | حفظ `project_id` ضمن مخطط لا يكسر `validate_catalog.py`، تفعيل حجر `reference-only` للمصادر والمهارات الخارجية، ووضع مهمة إصلاح `DuckDB Spatial` كأول تذكرة |
| **P04** | RISK-10, RISK-13, RISK-17, RISK-27, RISK-28 | تطبيق `hard_gate` وبوابة الترخيص الصارمة وعقود الحدود، وتحديد حدود الملكية لـ `geospatial-engine-selection` |
| **P05** | RISK-10, RISK-17, RISK-22 | فرض Progressive Disclosure لقوالب `WEB-01..18`، وحظر تخزين بلاطات OSM القياسية، واستخدام fixtures مجانية محلية |
| **P06** | RISK-15, RISK-16, RISK-17, RISK-23 | التصريح بقيود بيئة iOS على Windows وقيود محاكيات GNSS في وثائق المرحلة قبل كتابة أي سطر |
| **P07** | RISK-26, RISK-27, RISK-28, RISK-29 | إلزامية Clean-Room Specification للواجهات المرجعية وقواعد فحص GPL/LGPL والتدرج الآمن (`HIDE → DISABLE → REMOVE`) |
| **P08** | RISK-05, RISK-11, RISK-12 | مرور فحوص `audit_skill_graph.py` و`test_contextual_routing.py` و`test_landing_page.py` على بيئة معزولة |
| **P09** | RISK-01, RISK-02, RISK-03, RISK-04, RISK-30 | فحص الوثائق الرسمية الـ 19 وCLI help لكل منصة متوفرة وعدم ادعاء نشر خارجي من البناء المحلي |
| **P10 & P11** | RISK-12, RISK-19, RISK-20, RISK-21, RISK-30 | مرور جميع اختبارات الـ Regression، ووسم `NOT RUN` الصادق لأي بيئة غائبة، ومراجعة مستقلة + `DoneProof` قبل إعلان الإنجاز |

---

## 4. مؤشرات الإنذار المبكر وخطة الاستجابة السريعة حسب الفئة / Category Triggers & Escalation

| فئة المخاطر | المعرفات | مؤشر الإنذار المبكر (Early Warning Trigger) | إجراء التصعيد الفوري (Escalation Response) |
|---|---|---|---|
| **1. منصات البلجنز الخارجية (`External Platforms`)** | `RISK-01`, `RISK-02`, `RISK-03`, `RISK-04` | فشل `agy plugin validate` أو تغيير حقول `.codex-plugin` / `.claude-plugin` أو كشف رمز/مسار خاص في فحص staged | إيقاف المزامنة الخارجية للهدف المتضرر، تفعيل Rollback المعزول، تحديث `platforms.json` فقط داخل Adapter مع توثيق `MANUAL_ACTION_REQUIRED` |
| **2. سلامة البيانات والفهارس (`Data & Catalog Integrity`)** | `RISK-05`, `RISK-06`, `RISK-07`, `RISK-08`, `RISK-09` | فشل `validate_catalog.py`، بقاء `duckdb-skills` في `UDS-LIB-004`، وجود URL مكرر، أو مرشح غير موثق بمظهر `verified` | وقف التعديل على `project-catalog.json`، إعادة `engine-capability-profiles.json` لحالة `reference-only`/`unresolved`، وإلغاء تمرير `P03` حتى صفر أخطاء |
| **3. بنية المهارات والتوجيه (`Skill & Repo Structure`)** | `RISK-10`, `RISK-11`, `RISK-12`, `RISK-13`, `RISK-14` | تجاوز `SKILL.md` حد الإيجاز، فشل `audit_skill_graph.py`، أو تعطل رابط/عداد في `index.html` | نقل الجداول إلى `references/*.md` (Progressive Disclosure)، ضبط جدول التوجيه في `gis-development`، وإعادة فحص `test_landing_page.py` |
| **4. البيئة والأجهزة والتكلفة (`Environment & Cost`)** | `RISK-15`, `RISK-16`, `RISK-17`, `RISK-18` | طلب تشغيل iOS IPA على Windows، محاولة استدعاء API Key مدفوع، أو مهارة خارجية تحوي سكربت تثبيت غير مراجَع | وسم المهمة `NOT RUN` مع السبب البيئي، التبديل الإلزامي للـ local zero-key fixture، وحجر المهارة تحت `New Skill/` مع فحص `Security Guardian` |
| **5. الاختبارات والأدلة (`Testing & Evidence`)** | `RISK-19`, `RISK-20`, `RISK-21`, `RISK-22`, `RISK-23` | تقرير يوسم `T2–T4` بـ `PASS` اعتمادًا على اختبار JSON/Mock أو محاكي GNSS بدل جهاز فعلي | رفض التقرير عبر `validate_evidence_tiers.py` وإعادة التوثيق بوصف `NOT RUN` أو `T1` الصادق مع فصل مخرجات المحاكاة |
| **6. النطاق والتعقيد التقني (`Timeline & Complexity`)** | `RISK-24`, `RISK-25`, `RISK-26`, `RISK-27` | كسر اختبارات `v1.0` في `validate_architecture_flow.py`، كسر ميزة أساسية في QGIS بعد حذف مكون، أو تعارض ABI/CRS في multi-engine | الرجوع إلى مخطط `v1.0` أو الترتيب الآمن `HIDE → DISABLE`, وعزل المحرك المتعارض خلف `worker-ipc` بعقد `DatasetRef` صريح |
| **7. التراخيص والحوكمة والنشر (`Compliance & IP`)** | `RISK-28`, `RISK-29`, `RISK-30` | خلط GPL مع تطبيق مغلق، اقتباس أصول/أيقونات ArcGIS أو Google المحمية، أو محاولة نشر `-Publish` / `git push` بلا موافقة | حظر الدمج/التوزيع عبر `hard_gate` و`Clean-Room` حتى معالجة الترخيص وتوليد `THIRD_PARTY_NOTICES` والحصول على تفويض المالك المكتوب |

