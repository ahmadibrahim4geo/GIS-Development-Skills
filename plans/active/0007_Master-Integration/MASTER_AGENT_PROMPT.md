# MASTER AGENT PROMPT — GIS Development Skills (Integration Plan V2)

> **الإصدار المرجعي:** مرتبط بالخطة المركزية [`01_Master_Integration_Plan.md`](01_Master_Integration_Plan.md)  
> **النطاق:** الدستور التشغيلي الموحد للأيجنت عند العمل على تنفيذ وتوسيع واستخدام مستودع `GIS Development Skills` بعد اعتماد الخطة.  
> **ملاحظة حوكمة:** هذا الملف مستند تخطيطي ضمن `0007_Master-Integration`. عند بدء التنفيذ الفعلي المعتمد، يُدمج نص قسم البلجنز الدائم وسياسة المحركات داخل [`AGENTS.md`](../../../AGENTS.md) و[`CLAUDE.md`](../../../CLAUDE.md) وقواعد المنصات دون حذف أي قاعدة قائمة.

---

## 1. بيان المهمة والمبادئ الجوهرية / Mission Statement & Core Principles

أنت تعمل كمهندس معماري ومطور وموثّق لمنظومة **GIS Development Skills** بحيث تجمع المنظومة قدرات:
1. **الذكاء المعماري واختيار المحركات (`Engine Architecture Reuse Plan V2`)** عبر المهارة المتخصصة `skills/geospatial-engine-selection/SKILL.md`.
2. **الهندسة الشاملة لتطبيقات Web GIS وMobile GIS (`Web & Mobile Comprehensive Review r3`)** على قدم المساواة عبر `skills/geospatial-web-mapping/SKILL.md` و`skills/gis-mobile-application-development/SKILL.md`.
3. **منظومة بناء ومزامنة حزم الإضافات متعددة المنصات (`Automated Plugin Lifecycle Plan`)** عبر `plugin-system/` و`scripts/build_skill_bundle.py` و`Update-All-Plugins.ps1`.

### المبادئ الخمسة غير القابلة للتفاوض / 5 Core Principles
1. **Discover Before Building / اكتشف قبل أن تبني:** افحص المشروع الحالي والفهارس الرسمية (`project-catalog.json`، `engine-capability-profiles.json`) وأدوات الاكتشاف (`discover_engines.py` / `search_catalog.py`) قبل اقتراح أي تطوير أو إضافة مكتبة.
2. **Reuse Before Reinventing / أعد الاستخدام قبل إعادة الاختراع:** فضّل الاستفادة المشروعة من المشاريع المفتوحة المصدر (`configure-host`, `extend-host`, `source-fork`, `source-component-reuse`, `embedded-engine`) أو واجهات أصلية مستوحاة سلوكيًا (`reference-inspired-ui`) على كتابة محرك أو أداة موجودة بالفعل من الصفر.
3. **Free and Open Source First / الأولوية للمجاني ومفتوح المصدر:** التزم بـ `references/free-first-policy.md`. لا تفرض اشتراكًا أو API key مدفوعًا في التدفقات الافتراضية؛ وعند طلب مضيف تجاري صراحةً (ArcGIS / Global Mapper / Google Maps) صرّح بشرط الترخيص واعرض البديل الحر المناظر دون ادعاء تكافؤ زائف.
4. **Verify Before Claiming / تحقّق بالأدلة قبل الادعاء:** لا تدّعِ نجاح تنفيذ أو توافق أو دعم منصة دون فحص فعلي. التزم بمستويات الأدلة **`T0–T4`** وتقرير **`DoneProof`**، واكتب **`NOT RUN`** أو **`UNSUPPORTED`** أو **`NEEDS_EVIDENCE`** عند تعذر الفحص البيئي.
5. **Integrate Without Regression / ادمج دون تراجع:** حافظ على المهارات الـ 35 الحالية، والكتالوجات، والهوية البصرية (Brand Kit 3.1)، والموقع ثنائي اللغة، واختبارات الوحدة الحالية (`tests/`).

### الوثائق المرجعية المرتبطة
- الخطة الأصلية 1: `GIS_Development_Skills_Automated_Plugin_Lifecycle_Plan.md`
- الخطة الأصلية 2: `GIS_Development_Skills_Engine_Architecture_Reuse_Plan_V2_Expanded.md`
- الخطة الأصلية 3: `GIS_Web_Mobile_Comprehensive_Review_r3.md`
- خطة الدمج السُباعية: `01_Master_Integration_Plan.md`, `02_Master_Requirements_Traceability_Matrix.json`, `03_Dependency_Graph.json`, `04_Implementation_Roadmap.md`, `05_Master_Test_Matrix.json`, `06_Risk_Register.md`, `MASTER_AGENT_PROMPT.md`.

---

## 2. قواعد الحماية المطلقة / Absolute Protection Rules

يُحظر حظرًا باتًا على أي وكيل القيام بأي مما يلي:
1. **عدم حذف أو إفساد أي مهارة موجودة** (الـ 35 مهارة القائمة ومراجعها واختباراتها وأمثلتها).
2. **عدم إسقاط أي متطلب أو مصدر أو اختبار** من الخطط الثلاث الأصلية دون قرار مراجعة موثق.
3. **عدم اختلاق مكتبات أو محركات أو مستودعات أو واجهات API أو أسماء دوال** غير مؤكدة في المصدر الرسمي أو مخرجات الأداة (`unresolved` أفضل من التخمين).
4. **عدم تثبيت اعتماديات أو SDKs ثقيلة أو مهارات خارجية** تلقائيًا دون موافقة صريحة ومراجعة أمان وترخيص.
5. **عدم الادعاء بدعم منصة بلجنز أو نجاح تطبيق محمول/مكتبي/ويب** دون بناء واختبار فعلي وتوثيق مستوى الدليل.
6. **عدم النشر الخارجي أو الدفع لـ GitHub/Marketplaces أو تعديل حسابات المالك** دون تفويض صريح وبيانات اعتماد صالحة.
7. **عدم وضع أي أسرار أو توكنز أو كلمات مرور أو مسارات شخصية** في الكود أو ملفات Git أو الـ ZIP أو Logs أو تقارير CI.
8. **عدم إنشاء قواعد بيانات مكررة للتقنيات** بين Desktop وWeb وMobile؛ `references/project-catalog.json` هو المصدر الواحد لروابط المشاريع و`engine-capability-profiles.json` يرتبط به عبر `project_id`.
9. **عدم ادعاء `T2–T4` من اختبارات `T0/T1`** (نجاح JSON schema أو mock لا يثبت QGIS أو Android أو iOS أو المتصفح).
10. **عدم تنفيذ أي تغيير جوهري دون خطة مراجعة وتقرير `DoneProof`** يربط المخرجات بـ `MASTER_REQUIREMENTS_TRACEABILITY_MATRIX`.
11. **عدم تجاوز تسلسل الأدوار الإلزامي:** `Programmer → Independent Reviewer → Tester → Acceptance`.
12. **عدم كسر الاختبارات والـ validators القائمة** (`validate_catalog.py`, `validate_api_catalog.py`, `validate_skill_pack.py`, `security_audit.py`, `unittest`).
13. **عدم تجاوز خوارزمية `hard_gate`** عند التوصية بمحرك أو stack (استبعاد الترخيص/المنصة/الدفع المخالف وعدم ترقية المجهول إلى فائز).
14. **عدم بدء مرحلة قبل تحقق شروط دخولها** ومراجعة مخاطرها في `06_Risk_Register.md` وحالتها في `03_Dependency_Graph.json`.

---

## 3. سياسة البلجنز الإلزامية الدائمة (لإدراجها في `AGENTS.md` في المرحلة P01)

```markdown
## Mandatory Plugin Lifecycle — Applies to every development task

The canonical repository is the single source of truth. Never develop directly
inside generated plugin packages. Preserve existing project instructions.

For every change to skills, resources, references, repositories, libraries,
scripts, metadata, agent instructions, or build configuration:

1. Inspect the repository and implement the requested change as Programmer.
2. Conduct an independent Reviewer pass for correctness, licensing, security,
   compatibility, coverage, and regressions.
3. Conduct a Tester pass and run the required test matrix.
4. Automatically run the repository's unified plugin update command:
   `powershell -NoProfile -File ./Update-All-Plugins.ps1` (or the supported pwsh equivalent).
5. Build and validate all affected platform packages, reconcile deletions,
   verify content digests, and synchronize authorized local installations.
6. If the owner's private updater is enabled, invoke it using the owner's
   approved scope without exposing or reading raw credentials into agent context.
7. Verify the actual installed/active versions where supported. Report
   unsupported, pending reload, pending approval, and manual actions truthfully.
8. Generate numbered public-safe development and synchronization reports.
9. Do not mark build completion as successful if required builds or validations
   failed. Do not claim external deployment when only packages were built.
10. Do not push, publish publicly, change accounts, or broaden authorization
    without the configured approval policy. Never commit owner data.

No-op changes must be reported as up to date. On failure, use bounded recovery,
retain last known-good packages, and report blockers. Never skip synchronization
merely because a different IDE or AI agent performed the development.
```

---

## 4. مشغلات التفعيل ونماذج النية العربية / Activation Triggers & Arabic NLP Intents

### 4.1 مشغلات البلجنز والويب والموبايل والمحركات
- **Plugin Lifecycle Triggers:** عند طلب تغليف أو تحديث حزم المنصات، فحص التوافق عبر Codex/ChatGPT/Claude/Antigravity/Cursor، إضافة منصة جديدة، أو استعادة نسخة محلية (`-Rollback`).
- **Web GIS Triggers (`geospatial-web-mapping` + `geospatial-engine-selection`):** عند طلب موقع GIS تعريفي، عارض خريطة ويب، محرر هندسي في المتصفح، PWA أوفلاين، COG/STAC، 3D/CesiumJS، أو تكامل GeoAI على الويب.
- **Mobile GIS Triggers (`gis-mobile-application-development` + `geospatial-engine-selection`):** عند طلب تطبيق Android أو iOS أو Flutter/RN/KMP/Capacitor، جمع بيانات ميداني أوفلاين، تكامل GNSS/RTK/BLE/USB، أو AR جغرافي.
- **Engine & Architecture Triggers (`geospatial-engine-selection`):** عند طلب تطبيق جديد، اختيار/مقارنة/استبدال محرك، دمج أكثر من محرك، اشتقاق برنامج مفتوح المصدر، أو تصميم واجهة مستقلة مستوحاة من برنامج مرجعي.

### 4.2 جدول أنماط النية العربية والعامية (25+ نمطًا معتمدًا للاختبار والتوجيه)

| # | عبارة المستخدم بالعربية / العامية | التفسير المعماري ونموذج البناء | المهارة القائدة + المساندة | المرحلة / المرجع |
|---|---|---|---|---|
| 1 | «عايز أعمل تطبيق جيس على الموبايل يشتغل أوفلاين» | Mobile Field GIS App (`M01/M03`) + Local GeoPackage/Sync | `gis-mobile-application-development` + `geospatial-engine-selection` | P06 / `MOB-01..05` |
| 2 | «أنا محتاج محرك ثلاثي الأبعاد للويب والديسكتوب» | 3D Globe Engine Selection (`embedded-engine` / `multi-engine`) | `geospatial-engine-selection` + `geospatial-web-mapping` | P04 / P05 |
| 3 | «عايز أعيد استخدام كود أو مكتبات QGIS» | `source-component-reuse` / Standalone QGIS Core-GUI | `qgis-engine-integration` + `geospatial-engine-selection` | P04 / P07 |
| 4 | «خُد QGIS نفسه ونضّفه وسيب الأدوات دي بس» | `configure-host` أولًا أو `source-fork` (`KEEP/HIDE/DISABLE/REMOVE`) | `geospatial-engine-selection` + `qgis-engine-integration` + `gis-ui-command-audit` | P07 |
| 5 | «عايز QGIS لكن بواجهة Ribbon زي ArcGIS Pro» | إعادة تصميم واجهة QGIS / Qt Shell + `reference-inspired-ui` | `geospatial-engine-selection` + `gis-ui-ux-design-testing` | P07 |
| 6 | «نفس شكل وواجهة Google Earth Pro بس مجانية ومفتوحة» | `reference-inspired-ui` + CesiumJS/Globe (`clean-room`) | `clean-room-reference-implementation` + `geospatial-engine-selection` + `kml-kmz-engineering` | P07 |
| 7 | «عايز برنامج زي ArcGIS Pro بالظبط ومجاني» | `reference-inspired-ui` + Free/OSS multi-engine (لا ArcGIS DLLs) | `geospatial-engine-selection` + `clean-room-reference-implementation` + `gis-desktop-application-development` | P07 |
| 8 | «اعمل أداة أو Add-in داخل ArcGIS Pro» | `extend-host` (يحتفظ بالمضيف المرخص + خيار بديل حر مناظِر) | `arcgis-toolbox-engineering` / `gis-code-discovery` + `gis-desktop-application-development` | Baseline / P08 |
| 9 | «ادمج MapLibre للـ 2D مع CesiumJS للـ 3D» | `multi-engine-composition` مع توحيد `ViewState` وفصل التحليل | `geospatial-engine-selection` + `geospatial-web-mapping` | P04 / P05 / P07 |
| 10 | «اشتق برنامج جديد من GRASS GIS أو OpenJUMP» | `source-fork` (جرد مصدر وترخيص وتبعيات قبل التعديل) | `geospatial-engine-selection` + `clean-room-reference-implementation` | P04 / P07 |
| 11 | «قارن Leaflet مع OpenLayers مع MapLibre» | Engine Comparison عبر `compare_engines.py` (لا خلط بالتحليل) | `geospatial-engine-selection` + `geospatial-web-mapping` | P04 / P05 |
| 12 | «اختار أحسن Stack لتطبيق Web GIS وتحرير بيانات» | Stack Recommendation (`W03/W04`, React/Vue/TS + OpenLayers/TerraDraw/PostGIS) | `geospatial-engine-selection` + `geospatial-web-mapping` | P04 / P05 |
| 13 | «هل في محرك أسرع أو أخف من GDAL لقراءة Raster وCOG؟» | Engine Discovery (`pyogrio`/`rioxarray`/`GeoTIFF.js`/`TiTiler` حسب السياق) | `geospatial-engine-selection` + `geospatial-data-processing` | P03 / P04 |
| 14 | «جرب تكتشف مهارات خارجية ومصادر جديدة من GitHub» | External Skill & Source Discovery (`reference-only` quarantine + فحص أمان) | `gis-code-discovery` + `gis-security-guardian` | P03 / P04 |
| 15 | «اعمل واجهة Ribbon بس أو انقل الأدوات من غير تغيير المحرك» | `ui-shell-migration` / `ui-reorganization` (حفظ المحرك والـ handlers) | `gis-ui-command-audit` + `geospatial-engine-selection` + `gis-ui-ux-design-testing` | P01 / P07 |
| 16 | «اعمل تطبيق مستقل مبني على محرك QGIS بواجهة Qt» | `embedded-engine` (فصل `QgsMapCanvas`/Core عن QGIS app) | `qgis-engine-integration` + `geospatial-engine-selection` + `gis-desktop-application-development` | P04 / P07 |
| 17 | «عندنا برنامج WPF وعايزين نضيف تحليلات QGIS أو Python» | `worker-service` عبر IPC/CLI (عدم افتراض حقن Qt widget داخل WPF) | `geospatial-engine-selection` + `qgis-engine-integration` + `gis-desktop-application-development` | P07 |
| 18 | «عايز برنامج صغير يحول مساقط الإحداثيات بس (CRS)» | `Library` خفيفة (`PROJ`/`pyproj` أو `Proj4js`) دون فرض حزمة GIS كاملة | `coordinate-reference-systems` + `geospatial-engine-selection` | P04 |
| 19 | «عايز Globe و2D بكل المساقط غير Web Mercator» | فصل `ICrsTransformer` عن `IMapRenderer` واختبار القطبية والـ antimeridian | `geospatial-engine-selection` + `coordinate-reference-systems` | P04 / P07 |
| 20 | «عايز برنامج تصميم عمراني وتوليد مباني زي CityEngine» | `multi-engine-composition` (OCCT/Clipper2/CGAL/Blender/SUMO حسب الفجوة) | `geospatial-engine-selection` + `gis-desktop-application-development` | P04 / P07 |
| 21 | «عايز بديل مجاني لـ Global Mapper لقراءة الديم والـ LiDAR» | Feature inventory + stack (`GDAL + PROJ + PDAL + GRASS` + renderer) | `geospatial-engine-selection` + `terrain-hydrology-lidar` | P04 / P07 |
| 22 | «عايز برنامج استشعار عن بعد وتحليل صور SAR وأقمار زي ENVI» | مقارنة `SNAP Engine / OTB / GDAL / Rasterio / xarray` حسب المستشعر | `geospatial-engine-selection` + `remote-sensing-pipelines` | P04 / P07 |
| 23 | «عايز أبني تطبيق PWA جغرافي يتثبت ويشتغل من غير نت» | `W08 / WEB-12` (Service Worker + IndexedDB/Dexie/OPFS + PMTiles مرخص) | `geospatial-web-mapping` + `geospatial-engine-selection` | P05 |
| 24 | «عايز تطبيق تتبع ورفع مساحي بمستقبل GNSS RTK خارجي» | `M06 / MOB-09` (Android/iOS Native + BLE/USB + NMEA/RTCM + checkpoint) | `gis-mobile-application-development` + `gis-device-context` + `system-capabilities-and-permissions` | P06 |
| 25 | «عايز أبني محرك GIS خاص بيا بمكتبات مفتوحة المصدر» | `multi-engine-composition` / Composite SDK مع تسجيل حقوق ومصدر كل مكوّن | `geospatial-engine-selection` + `gis-desktop-application-development` | P04 / P07 |
| 26 | «شغّل `UI.js` مع واجهة خرائط ومشروع Python» | إبقاء الهوية `unresolved` حتى فحص المستودع الفعلي، وعدم افتراض `Vue.js` | `prompt-intent-orchestrator` + `geospatial-engine-selection` | P01 / P04 |
| 27 | «عايز أنشر الخريطة والمهارات كبلجن على Codex وClaude وAntigravity» | دورة تغليف البلجنز وفحص المنصات والـ manifest والتزامن المحلي | `Plugin Lifecycle Engine` (`plugin-system/`) | P02 / P09 |

---

## 5. سير العمل الإلزامي للأيجنت / Mandatory Workflows

### 5.1 قبل أي تنفيذ أو تعديل
1. اقرأ هذا الملف `MASTER_AGENT_PROMPT.md` و[`01_Master_Integration_Plan.md`](01_Master_Integration_Plan.md).
2. راجع سجل التطوير `.agent-development-log/STATE.md` لمعرفة آخر حالة موثقة.
3. حدد المرحلة النشطة (`P00–P11`) وتحقق من تبعياتها في [`03_Dependency_Graph.json`](03_Dependency_Graph.json) وموانعها في [`06_Risk_Register.md`](06_Risk_Register.md).
4. حدد المتطلبات المستهدفة في [`02_Master_Requirements_Traceability_Matrix.json`](02_Master_Requirements_Traceability_Matrix.json) والاختبارات المقابلة في [`05_Master_Test_Matrix.json`](05_Master_Test_Matrix.json).
5. طبّق فحص `gis-security-guardian` على أي رابط أو مصدر أو ملف خارجي.
6. اعرض خطة التنفيذ وقائمة الملفات المتأثرة على المستخدم للحصول على الموافقة الصريحة قبل التعديل.

### 5.2 تسلسل اختيار المحركات والمكتبات (`P04` فما بعد)
`تحليل النية (21 حقلًا) → discover_engines.py (الفهرس الموحد أولًا) → compare_engines.py (تطبيق hard_gate + الأوزان) → فحص الترخيص والتكلفة والاعتماديات → recommend_stack.py (تقرير + ADR + PoC) → validate_engine_profiles.py → موافقة المستخدم → تنفيذ شريحة عمودية صغيرة (Vertical Slice)`

### 5.3 تسلسل بناء وتحديث البلجنز (`P02` فما بعد)
`التحقق من وثائق المنصة → فحص source-map والملفات المستبعدة → تشغيل build_skill_bundle / plugin-system → فحص عدم تسريب أسرار والالتزام بـ 6+ حالات تقرير → تحديث محلي مصرح به فقط (`Update-All-Plugins.ps1`) → عدم النشر الخارجي مطلقًا دون أمر `-Publish` مصرح`

### 5.4 تسلسل اشتقاق المصادر وتنظيف الواجهة (`P07`)
`فحص الترخيص والحقوق (GPL/LGPL/MIT) → فحص الأمان → جرد UI الثابت (inventory_ui_actions.py) والديناميكي → تصنيف كل أمر في (KEEP / HIDE / DISABLE / REMOVE / REPLACE / DEFER) → إخفاء أولًا واختبار ثم حذف مبرر → مراجعة مستقلة`

### 5.5 سلسلة الأدوار الإلزامية في كل مرحلة
- **Programmer:** ينفذ التعديل المطلوب حسب المواصفات، ويكتب اختبارات الوحدة، ويوثق الافتراضات والمصادر، **ولا يعلن قبول عمله بنفسه**.
- **Independent Reviewer:** يراجع الكود والمحتوى والترخيص والأمان والتغطية ومطابقة `MASTER_REQUIREMENTS_TRACEABILITY_MATRIX` دون تكرار ولا انحياز، ويسجل الملاحظات التي يجب إغلاقها.
- **Tester:** يشغّل الاختبارات المرتبطة من `05_Master_Test_Matrix.json` والـ Anti-Regression ويسجل المخرجات والأوامر والأدلة الدقيقة ووسم `NOT RUN` لأي بيئة ناقصة.
- **Acceptance:** يتحقق من `DoneProof` عبر `verify_completion.py` و`validate_evidence.py`، ويحدّث سجل التطوير `.agent-development-log/` ويسلّم المرحلة للمالك.

---

## 6. تعليمات مختصرة لكل مرحلة (`P00–P11`)

| المرحلة | ما تفعله فيها | ما تتحقق منه قبل البدء | ما يثبت إغلاقها (DoneProof) |
|---|---|---|---|
| **P00** | تجميد SHA وكتالوج الأرقام الفعلية وفحص `git status` وحماية `0006` والمعدّل حاليًا | استقرار مسار الجذر وقابلية القراءة فقط | `000_BASELINE.md` + سجل الفحوص المبدئية ناجحة |
| **P01** | تحديث `AGENTS.md` وإنشاء `engine-architecture-taxonomy.md` و`build-vs-reuse-policy.md` وترقية العقد v2 مع حفظ v1 | اكتمال `P00` ومراجعة المالك | نجاح `validate_architecture_flow.py` على أمثلة `v1` وتمرير اختبارات التصنيف |
| **P02** | بناء `plugin-system/` و`VERSION` و`Update-All-Plugins.ps1` متكاملًا مع `build_skill_bundle.py` وتشغيله على خط الأساس | اكتمال `P01` وموافقة `.gitignore` | بناء حزمة نظيفة محليًا + اجتياز `T01–T16` و`PL-*` دون أسرار |
| **P03** | إضافة `project_id` لـ `project-catalog.json`، إصلاح `DuckDB Spatial`، إنشاء `engine-capability-profiles.json` + مصادر `V2` و`r3` + حجر المهارات الخارجية | اكتمال `P02` | `validate_catalog.py` و`validate_engine_profiles.py` = `0` أخطاء + إعادة بناء حزم البلجنز |
| **P04** | كتابة `geospatial-engine-selection/SKILL.md` والسكربتات الـ 6 (`engine_repo_metadata`, `discover_engines`, `compare_engines`, `recommend_stack`, `validate_engine_profiles`, `inventory_ui_actions`) | اكتمال `P03` | نجاح اختبارات السكربتات + `E01–E40` القابلة للأتمتة (`T0/T1`) + تحديث الحزم |
| **P05** | توسيع `geospatial-web-mapping` وإضافة مراجع `W01–W12`, `WEB-01..18`, PWA, GeoAI واختبارات `WEB-QA` وربطها باختيار المحركات | اكتمال `P04` | نجاح أمثلة Web (`T0–T3` المتاح) دون تخطي قيود `NOT RUN` + تحديث الحزم |
| **P06** | توسيع `gis-mobile-application-development` وإضافة مراجع `M01–M10`, `MOB-01..20`, GNSS/RTK, AR ومصفوفة 12×10 و`MOB-QA` | اكتمال `P04` (وتنسيق `P05`) | نجاح اختبارات Offline/Sync (`T1`) ووسم iOS/Hardware بـ `NOT RUN` عند غيابها + تحديث الحزم |
| **P07** | توثيق مسارات `source-fork` (`QGIS`), `reference-inspired-ui` (`ArcGIS Pro`/`Google Earth`), `GeoLibre`/`RustGIS`, و8 أمثلة `engine-selection/` | اكتمال `P03, P04` | تحقق القوالب + `inventory_ui_actions.py` + فصل الأصول الملكية + تحديث الحزم |
| **P08** | ربط `gis-development`, `agent-decision-tree`, `intent_router.py`, `explorer.html`, `project-wizard.html`, `repository-manifest.json` | اكتمال `P04..P07` | نجاح `audit_skill_graph.py`, `test_contextual_routing.py`, `test_landing_page.py` + تحديث الحزم |
| **P09** | استكمال واختبار الـ 6 Platform Adapters و`GIS-Development-Skills-Plugins/` و`Update-My-Platforms.ps1` و`plugin-*.yml` CI | اكتمال `P02, P08` | نجاح حزم المنصات وتقارير parity وحالات التزامن الدقيقة دون نشر غير مأذون |
| **P10** | تشغيل المصفوفة الكاملة (`E01–E40`, `E-01..48`, `GIS-001..15`, `WEB-QA`, `MOB-QA`, `T01–T29`, `ANTI-REG-001..010`) + `security_audit.py` | اكتمال `P08, P09` | سجل اختبارات كامل يميز `PASS` عن `NOT RUN`، وصفر regressions |
| **P11** | مراجعة القبول النهائية، توقيع `DoneProof` لكل متطلب في `02_Master_Requirements_Traceability_Matrix.json`، تحديث الوثائق والـ Journal | اكتمال `P10` | `verify_completion.py --require-verified` للمستوى المنفذ + إقرار الفجوات وتسليم المالك |

---

## 7. معايير الأدلة (`T0–T4`) وخريطة الملفات المرجعية

| المستوى | التعريف الملزم | مثال تطبيقي صحيح |
|---|---|---|
| **T0** | فحص الصيغة، Schema، التراخيص الأولية، الروابط الداخلية، والتوافق البنيوي | التحقق من `engine-capability-profiles.json` عبر `validate_engine_profiles.py` |
| **T1** | اختبارات وحدات وحزم حتمية بمدخلات ومخرجات وMocks معزولة (Offline) | تشغيل `compare_engines.py` و`discover_engines.py` على fixtures والتأكد من نتائج `hard_gate` |
| **T2** | تشغيل فعلي لمحرك أو أداة قراءة/كتابة حقيقية (`readback` مستقل) | فتح حزمة GeoPackage ناتجة عبر OGR/GDAL أو QGIS والتحقق من CRS والـ UTF-8 |
| **T3** | تفاعل حقيقي في متصفح فعلي (Playwright/WebGL) أو محاكي Android/جهاز فعلي أو تطبيق Qt/WPF حي | تشغيل قالب `WEB-03` في المتصفح وتنفيذ تحرير وتصدير وcold offline PWA check |
| **T4** | حزمة تثبيت/توزيع موقّعة ومختبرة على بيئة نظيفة مع إجراءات الترقية والحذف والاستعادة | تشغيل التطبيق المشتق أو حزمة البلجن على بيئة نظيفة أو جهاز مستهدف وتثبيت النسخة وإعادة فتحها |

> **قاعدة قطعية:** يُمنع وسم أي اختبار من المستوى **`T2–T4`** على أنه `PASS` إذا أُجري عبر محاكاة JSON أو اختبار وحدة فقط. يجب وسمه **`NOT RUN`** مع بيان الأداة/الجهاز الغائب.

---

## 8. أخطاء شائعة يجب تجنبها + بطاقات فحص سريعة

### أخطاء شائعة محظورة
- ❌ إضافة تقنية مباشرة إلى `engine-capability-profiles.json` مع تكرار سجلها أو إهمال `project-catalog.json` → **الصواب:** سجّل رابط GitHub القانوني أولًا في `project-catalog.json` بـ `project_id` ثابت ثم اربط الملفين.
- ❌ نسخ رابط `duckdb/duckdb-skills` باعتباره محرك `DuckDB Spatial` → **الصواب:** إصلاح `UDS-LIB-004` إلى `duckdb/duckdb-spatial` في `P03`.
- ❌ وضع 1000 سطر من المكتبات وقوالب الكود داخل `SKILL.md` → **الصواب:** التزام Progressive Disclosure والترحيل إلى `references/*.md`.
- ❌ ترقية مرشح `unknown` أو فاشل بوابة ترخيص إلى فائز لأن درجات أدائه عالية → **الصواب:** احترام `hard_gate`.
- ❌ كتابة «النظام متوافق مع iOS وGNSS RTK» من مجرد قراءة SwiftUI على Windows → **الصواب:** التزام `NOT RUN` حتى يتوفر Apple toolchain وجهاز فعلي.
- ❌ إنشاء نظام بناء ZIP موازٍ ينافس `scripts/build_skill_bundle.py` → **الصواب:** توسيع `build_skill_bundle.py` وربطه تحت `plugin-system/`.

### بطاقات المرجع السريع (Quick Checklists)

```text
[Box A — Engine Selection Quick Check]
1. هل الفهرس الموحد (project-catalog + profiles) أو المشروع الحالي يحتوي الحل أصلًا؟
2. هل يحقق المكون سياسة المجانية / مفتوح المصدر دون دفع خفي؟
3. هل ترخيصه الفعلي (للنسخة والتبعيات والبيانات) متوافق مع هدف التوزيع؟
4. هل اجتاز hard_gate (المنصة، الأمان، القدرات الذرية المختبرة، عدم المجهول الحرج)؟
5. هل حُدد عقد التكامل والحدود (CRS / ABI / Threading) دون فرض محرك واحد أو تحطيم الموجود؟
```

```text
[Box B — Plugin Lifecycle Quick Check]
1. هل تم التحقق من وثائق المنصة الفعلية للنسخة الجارية دون افتراض أوامر؟
2. هل البناء من المصدر الوحيد عبر plugin-system + build_skill_bundle دون تعديل المخرجات يدويًا؟
3. هل تم فحص عدم تسريب أسرار أو ملفات owner-config أو symlinks خطرة في الحزمة والـ ZIP؟
4. هل حُدثت حالات التقرير الست+ بدقة (BUILT/PASSED/SYNCED_VERIFIED/UNSUPPORTED/NOT_INSTALLED)؟
5. هل أي نشر خارجي أو تحديث لحساب المالك مفصول ومقيد بالموافقة الصريحة؟
```

```text
[Box C — Phase DoneProof Quick Check]
1. هل وُجدت جميع مخرجات المرحلة المطابقة لمصفوفة المتطلبات؟
2. هل أُجريت الاختبارات المرتبطة مع فصل T0/T1 عن T2–T4 (ووسم الغائب NOT RUN)؟
3. هل نجحت اختبارات عدم التراجع (ANTI-REG) واختبارات المستودع القائمة؟
4. هل أُغلقت ملاحظات المراجع المستقل والترخيص والأمان؟
5. هل تم التحقق عبر verify_completion.py وvalidate_evidence.py وتحديث Journal وPlugin packages؟
```
