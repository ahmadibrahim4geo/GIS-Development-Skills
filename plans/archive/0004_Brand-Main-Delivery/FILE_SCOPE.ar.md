# مراجعة ملفات r11 قبل التنفيذ

الهدف تسليم مهارة GIS كاملة بهوية الحزمة المرسلة، وترتيب مساحة العمل محليًا، ورفع ملفات الإنتاج المراجعة إلى `main` مباشرة. هذه حدود الملفات المقترحة ضمن [مسودة r11](PLAN.json).

## تغييرات الموقع ودليل الاستخدام

| الملف | التغيير المقترح |
| --- | --- |
| `index.html` | مدخل يعرض الإضافات والأدوات لـArcGIS وQGIS، وتطبيقات سطح المكتب والويب، والاستشعار وتحليل البيانات والأتمتة. إبقاء KML/KMZ مسارًا ضمن التخصصات، وتقليل المساحة المخصصة له مع بقاء الرابط `#earth-kml` وموارده. |
| `README.md` و`README.ar.md` | اعتماد البانر الجديد وإظهار مجالات المشروع وطريقة البدء، مع إبقاء جملة المهمة المعتمدة وروابط المهارات وملفات الكتالوج. |
| `explorer.html` | توحيد الشعار والأيقونة وصورة مشاركة الرابط مع الموقع. المحافظة على مصدر البيانات والفلاتر وتبديل اللغة وكتلة المطور. |
| `AGENTS.md` و`PROJECT_STRUCTURE.md` و`.gitignore` | تحديث مرجع الهوية المعتمدة وتوثيق مجلدات الأصول والأرشيف واستبعاد المجلدات المحلية من النشر. |
| `assets/home-redesign.css` و`assets/brand-refresh.css` وملفات هوية `assets/brand/` | تطبيق ألوان الحزمة الجديدة مع فحص الموبايل واتجاه العربية. |
| اختبارات الواجهة والـREADME | تحديث اختبارات الشكل المرتبطة بالرمز القديم لتتحقق من الهوية الجديدة والأبعاد والربط، مع الإبقاء على فحوص السلوك والكتالوج. |

## مصدر الأصول ومسار الاستخدام

المصدر دائمًا `GIS_Development_Skills_Complete_Brand_Kit/` الموجود في الجذر. رصدت **94 ملفًا** في المجلد. تُنسخ أصول الإنتاج المختارة إلى المسارات التالية.

| الأصل داخل Brand Kit | الاستخدام المقترح داخل المشروع |
| --- | --- |
| `02_Lockups/Horizontal/lockup-on-dark.svg` | `assets/brand/logo-dark.svg` و`assets/brand/logo-compact-dark.svg` وواجهات التوافق `assets/logo.svg` و`assets/gis-brand-lockup.svg`. |
| `02_Lockups/Horizontal/lockup-on-light.svg` | `assets/brand/logo-light.svg` و`assets/brand/logo-compact-light.svg`. |
| `01_Logos/Reverse/logo-reverse.svg` | `assets/brand/icon.svg` و`assets/icon.svg`. |
| `04_App_Icons/app-icon.svg` | `assets/brand/favicon.svg`. |
| `03_Banners/Dark/banner-dark.svg` و`03_Banners/Light/banner-light.svg` | `assets/brand/banner-dark.svg` و`assets/brand/banner-light.svg` مع تحديث مسار التوافق `assets/readme-banner.svg`. |
| `06_GitHub_Ready/banner.png` و`06_GitHub_Ready/social-preview.png` | `assets/brand/banner.png` للـREADME، و`assets/brand/social-preview.png` لمشاركة رابط صفحات الموقع. |
| `07_Documentation/COLORS.json` ودليل الهوية | مرجع تحديث `assets/brand/palette.json` و`assets/brand/tokens.css` وملفات توثيق الأصول. |

نسبة البانر المعتمدة **6:1**. تبقى بطاقات وروابط التخصصات الحالية ما دام الموقع أو الـREADME يشير إليها. إعداد صورة المعاينة في صفحة مستودع GitHub إجراء إداري منفصل عن صورة مشاركة الموقع.

## الأرشيف المحلي

- النقل المقترح هو `GIS_Development_Skills_Execution_Package_2026-11-20/`، وفيه **32 ملفًا** وقت الجرد، إلى `Old - Safe to Remove/GIS_Development_Skills_Execution_Package_2026-11-20/`.
- تُحفظ نسخ من الرسومات التي تُستبدل تحت `Old - Safe to Remove/previous-brand-assets/` ببنيتها القديمة. تُكتب قائمة محتويات ومسارات الاسترجاع داخل الأرشيف.
- تقرير تدقيق الموارد المحلي يشير إلى الخطة القديمة الآن. نحتفظ باسم المرجع فيه ونحوّل الإحالة إلى توثيق تاريخي حتى تظل فحوص الروابط مستقلة عن مكان الأرشيف.
- `GIS_Development_Skills_Complete_Brand_Kit/` يبقى في موقعه وبنفس الاسم. تظل الخطط المعتمدة في `plans/archive/` والسجل في `.agent-development-log/` وأدلة الاختبار في مواضعها.
- أي عنصر إضافي يُنقل يحتاج دليلًا على انقطاع اعتمادات الموقع والحزمة والاختبارات عليه. يُفحص مرشح النشر في نسخة تحتوي على الملفات العامة فقط قبل وصف الأرشيف بأنه قابل للحذف.

## القائمة الحرفية المقترحة لملفات GitHub

**98 مسارًا** في القائمة الأولية. تتضمن 69 ملفًا مرشحًا من تحديثات المهارة المحلية السابقة و29 ملفًا للهوية والواجهة واختباراتها. الأسماء أدناه هي قائمة السماح للمراجعة. يتحدد العدد الفعلي من فرق الملفات المتغيرة فقط عند التنفيذ.

```text
.gitignore
AGENTS.md
CLAUDE.md
PROJECT_STRUCTURE.md
PUBLISHING.md
README.ar.md
README.md
assets/README.md
assets/brand-refresh.css
assets/brand/README.md
assets/brand/banner-dark.svg
assets/brand/banner-light.svg
assets/brand/banner.png
assets/brand/favicon.svg
assets/brand/icon.svg
assets/brand/logo-compact-dark.svg
assets/brand/logo-compact-light.svg
assets/brand/logo-dark.svg
assets/brand/logo-light.svg
assets/brand/palette.json
assets/brand/showcase.html
assets/brand/social-preview.png
assets/brand/tokens.css
assets/gis-brand-lockup.svg
assets/home-redesign.css
assets/icon.svg
assets/logo.svg
assets/readme-banner.svg
docs/SKILL_DISTRIBUTION.md
examples/remote-sensing/synthetic_index_calculator.py
explorer.html
fixtures/expected/p03-science.json
fixtures/expected/p04-planar-slope.asc
fixtures/landsat8-l2-pixels.json
index.html
native_tests/README.md
native_tests/arcgis_pro_acceptance.py
native_tests/qgis_project_roundtrip.py
native_tests/qgis_scientific_readback.py
native_tests/run_wpf_toolchain.py
native_tests/web-geojson-readback.html
native_tests/web_geojson_readback.py
native_tests/wpf-toolchain/InvokeWindow.cs
native_tests/wpf-toolchain/MainWindow.xaml
native_tests/wpf-toolchain/MainWindow.xaml.cs
references/agent-context-memory-architecture.md
references/arcgis-pro.md
references/engineering-role-registry.json
references/engineering-role-workflow.md
references/esri-open-source-integration.md
references/free-first-policy.md
references/gis-code-recipes.json
references/gis-code-sources.json
references/intent-orchestration-workflow.md
references/portable-execution-guidance.md
references/project-catalog.json
references/project-governance-workflow.md
references/remote-sensing-sensor-band-mappings.md
references/token-optimization-triad.md
scripts/build_skill_bundle.py
scripts/contextual_routing.py
scripts/engineering_workflow.py
scripts/gis_code_discovery.py
scripts/intent_router.py
scripts/native_toolchain.py
scripts/project_governance.py
scripts/project_readiness.py
scripts/project_structure.py
scripts/render_trial_dashboard.py
scripts/security_audit.py
scripts/security_guardian.py
scripts/skill_intake.py
scripts/skill_readiness.py
scripts/test_runs.py
scripts/toolchain_advice.py
scripts/toolchain_discovery.py
scripts/verify_completion.py
scripts/verify_engineering_workflow.py
skills/geospatial-ai-agents/SKILL.md
skills/gis-code-discovery/SKILL.md
skills/gis-desktop-application-development/SKILL.md
skills/gis-development/SKILL.md
skills/prompt-intent-orchestrator/SKILL.md
tests/test_code_discovery.py
tests/test_contextual_routing.py
tests/test_engineering_workflow.py
tests/test_home_redesign.py
tests/test_interactive_hub.py
tests/test_landing_page.py
tests/test_project_governance.py
tests/test_project_readiness.py
tests/test_readme_layout.py
tests/test_remote_sensing_indices.py
tests/test_skill_distribution.py
tests/test_skill_intake.py
tests/test_skill_readiness.py
tests/test_test_runs.py
tests/test_toolchain_discovery.py
```

تبقى حزمة التصميم الكاملة، وخطة التشغيل الأصلية، و`Old - Safe to Remove/`، و`New Skill/`، و`testing data/`، و`testing results/`، و`dist/`، والخطط وسجلات وإثباتات العمل غير المنشورة خارج قائمة الرفع. تُستثنى مخرجات الاختبار المحلية، بينما تتضمن القائمة ثلاثة مدخلات اختبار اصطناعية من `fixtures/` لازمة لفحوص المهارة.

قُرئ `main` من موصل GitHub ورأسه `42de4a246a2db1f7d33cc746da9cd3a0f1718a91`. عند التنفيذ تُعاد مطابقة الرأس قبل رفع تحديث مباشر إلى `main` وتُراجع نتيجة CI على SHA المنشور. تظل القواعد الإدارية للمستودع هي التي تحدد قبول الرفع.

## طلب KML/KMZ أثناء التنفيذ

يشمل التسليم `skills/kml-kmz-engineering/SKILL.md` بعد تجميع خطوات التشغيل فيه حسب طلب المستخدم. تظل المراجع والاختبارات الحالية متاحة بمساراتها. كما يشمل `tests/test_repository_internal_links.py` لحصر فحص الروابط في ملفات العمل بعيدًا عن أرشيف المستخدم وحزمة الهوية الأصلية.

الفرق الفعلي قبل النشر كان 99 ملفًا. بقي `tests/test_interactive_hub.py` مطابقًا لأساس GitHub، فاستُبعد من فرق الرفع.
