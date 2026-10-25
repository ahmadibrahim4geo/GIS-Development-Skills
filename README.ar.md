<p align="center">
  <img src="assets/brand/banner-dark.svg" alt="GIS Development Skills — The Heart of Geospatial Innovation" width="1200">
</p>

<p align="center"><sub>الهوية البصرية الرسمية: <a href="assets/brand/README.md">ملفات الهوية ودليل استخدامها</a> · <a href="assets/brand/logo-light.svg">الشعار الشفاف</a> · <a href="assets/brand/icon.svg">الأيقونة المستقلة</a></sub></p>



<p align="center">
  <a href="README.md">English</a> ·
  <a href="https://ahmadibrahim4geo.github.io/GIS-Development-Skills/">الموقع الإلكتروني</a> ·
  <a href="skills/gis-development/SKILL.md">المهارة الأساسية</a> ·
  <a href="CONTRIBUTING.md">المساهمة</a>
</p>


## مهارة سجل التطوير المرقّم وذاكرة المشروع — 25 أكتوبر 2026

أضفنا [Agent Development Journal](skills/agent-development-journal/SKILL.md) لتوثيق طلبات المستخدم، والخطوات المنفذة، والتعديلات والإلغاء، والاختبارات، في سجل مرقم مستقل **داخل المشروع نفسه**. تحفظ [أداة Python](scripts/development_journal.py) ملفات JSON مترابطة وتقارير Markdown وفهرسًا لحالة المشروع؛ ولا تحذف التقارير السابقة. راجع [دليل الاستعادة والتسجيل](references/agent-development-journal-guide.md) و[مراجع المهارات الخارجية](references/agent-memory-skill-references.md) و[التجربة المحلية](examples/development-journal/README.md).

الوكيل لازم يستدعي أداة التسجيل بعد كل عملية مهمة؛ ملف Skill وحده لا يسجل العمليات تلقائيًا. السجل لا يثبت أن التطبيق يعمل أو أن طلب تراجع عن كود نُفذ بالفعل.

## مهارة فهم وتنظيم وتوجيه طلبات المستخدم — 25 أكتوبر 2026

أضفنا [Prompt Intent & Execution Orchestrator](skills/prompt-intent-orchestrator/SKILL.md) لتفسير الكلام العفوي بالعامية المصرية والعربية والإنجليزية وتحويله إلى متطلبات ومهام واختبارات واضحة، ثم عرض نسخة الخطة للمستخدم للمراجعة والتعديل والاعتماد قبل التنفيذ. بعد ذلك يوجه الوكيل المهام إلى [مهارات GIS المتخصصة](skills/gis-development/SKILL.md) والأدوات المتاحة فعليًا مع [حارس الأمان](skills/gis-security-guardian/SKILL.md) وأدلة اختبار T0–T4.

راجع [دليل المراحل والموافقات](references/intent-orchestration-workflow.md) و[مثال ZEarth](examples/intent-orchestrator/README.md) و[فاحص الخطة المحلي](scripts/intent_router.py). الفاحص لا يستخدم نموذج ذكاء اصطناعي، ولا ينفذ التعليمات أو يتحقق من هوية صاحب الموافقة؛ هو فحص بنيوي فقط.

## طوّر أدوات وتطبيقات نظم المعلومات الجغرافية وفق منهجية يمكن التحقق منها.

مهارات تطوير برمجيات نظم المعلومات الجغرافية ومراجع مفتوحة المصدر، تشمل **21 مهارة قابلة للتثبيت** و**148 مرجعًا جغرافيًا** و**52 مصدرًا لواجهات البيانات والخدمات الجغرافية** و**24 دليلًا وبوابةً للبيانات**.

**تحسينات المجانية والعرض:** أصبحت [الواجهة](index.html) تعرض جميع المهارات الـ19، وزر «عرض المزيد» لكل النتائج، وفلترًا مجانيًا افتراضيًا لخدمات API (42 خدمة مجانية بشروط + خدمة واحدة للاستضافة الذاتية). الخيارات التجارية والتجريبية والمقيدة تُعرض عند اختيار «كل المستويات». راجع [سياسة المجاني أولًا](references/free-first-policy.md) لتفاصيل ترخيص ArcGIS وGlobal Mapper والبيانات والخدمات.

## الاستفادة من Google Earth Blog وتطوير الصور التاريخية — 25 أكتوبر 2026

أضفنا [مرجعًا هندسيًا لوظائف Google Earth Pro](references/google-earth-pro-engineering.md) يستخلص أفكارًا مستقلة من [Google Earth Blog](https://www.gearthblog.com/): إدارة Places والمجلدات، وروابط NetworkLink والتصفية المكانية حسب Region/LOD، والجولات ثلاثية الأبعاد، والقطاعات التضاريسية، والطبقات الصورية. كما أضفنا [دليلًا لشريط الصور التاريخية](references/historical-imagery-timeline.md) يحدد شريطًا صغيرًا لا يحجب الخريطة، وتواريخ المشاهد المتاحة فعليًا، وحقوق مصادر الصور، والمقارنة بين تاريخين، وحفظ حالة البرنامج. تم ربط المرجعين بمهارات الديسكتوب والويب وKML/KMZ وبواجهة HTML بالعربية والإنجليزية.

**حدود التنفيذ:** دي مواصفات ودراسة مرجعية فقط، وليست تأكيدًا بأن الوظائف تعمل حاليًا داخل ZEarth. المدونة مصدر تاريخي مستقل؛ ولا تسمح بإعادة توزيع صور Google Earth داخل برامجنا.

## مصادر Esri الرسمية للمطورين — 25 أكتوبر 2026

أضفنا عشرة مستودعات رسمية جديدة إلى [دليل Esri](references/esri-open-source-integration.md) دون تكرار: أمثلة Pro SDK الموجهة إلى مساعدي البرمجة، وArcade، وحلول الأخطاء، وCAD/BIM، والتحليل الشبكي، وGeoportal وSTAC/MCP، وJavaScript، والبحث الجغرافي، والتضاريس، ومعالجة الصور.

ويوجد الآن [دليل فحص توافق Python مع ArcGIS Pro](references/esri-python-environment-compatibility.md) وسكربت محلي لا يغيّر البيئة، بالإضافة إلى [دليل اختيار ملفات Arcade](references/arcgis-arcade-profiles.md).

ترخيص الكود المفتوح لا يعني السماح المجاني بتشغيل ArcGIS أو امتداداته أو خدماته. لم ننسخ المحركات أو مفاتيح خدمات Esri، وما زال اختبار التشغيل داخل ArcGIS Pro مطلوبًا بشكل منفصل.

## مهارة GIS Security Guardian — الحماية المصاحبة للوكلاء (25 أكتوبر 2026)

أضفنا [**GIS Security Guardian**](skills/gis-security-guardian/SKILL.md) بصفتها **المهارة التاسعة عشرة**، وتعمل كسياسة حماية مصاحبة لجميع المسارات: فحص التعليمات الخارجية ومحاولات حقن الأوامر، ضبط الصلاحيات، حماية الملفات والمواقع والبيانات الحساسة، وتأمين التبعيات وواجهات API والمشروعات قبل التسليم. يضم [كتالوج أدوات الأمان](references/security/security-tools.json) 14 مشروعًا، مع بيان التراخيص وحدود التشغيل. تشمل الملفات الجديدة [الفحص المحلي دون مكتبات مدفوعة](scripts/security_audit.py)، و[فاحص أرشيفات ZIP/KMZ](scripts/security_guardian.py)، و[اختبارات الحماية](tests/test_security_guardian.py)، و[Workflow أمني](.github/workflows/security.yml)، و[سياسة الإبلاغ عن الثغرات](SECURITY.md). **هذه فحوصات أولية محلية وليست ضمانًا للأمان أو إثباتًا لتنفيذ الماسحات الخارجية**. تمت إضافة روابطها إلى [الواجهة ثنائية اللغة](index.html).

## تطوير مهارة KML/KMZ بالاستفادة من Google — 25 أكتوبر 2026

حدّثنا [مهارة هندسة KML/KMZ](skills/kml-kmz-engineering/SKILL.md) وربطناها بـ[دليل Google/OGC لتوافق الملفات وحفظ خصائصها](references/google-kml-kmz-compatibility.md) و[مثال KML تجريبي قابل للفحص محليًا](examples/kml-kmz/README.md). عند استيراد ملفات المستخدم لا يجوز للبرنامج فرض رموز أو ألوان جديدة؛ يجب الحفاظ على ألوان KML بصيغة `aabbggrr`، و`StyleMap`، والرموز، والمجلدات، والبيانات الوصفية، والارتفاعات، والأزمنة، وملفات الموارد داخل KMZ. وضع العرض الدقيق يختلف عن التحويل إلى طبقات GIS الذي قد يفقد بعض الخصائص؛ وأُضيفت ضوابط للأمان والحفظ وإعادة الفتح. **نجاح فحص XML لا يعني اكتمال اختبار العرض الفعلي داخل Google Earth أو ZEarth Desktop.**

## مهارتا الرموز الخرائطية وبيانات الجهاز — 25 أكتوبر 2026

أضفنا [GIS Cartography & Symbology](skills/gis-cartography-symbology/SKILL.md) لتنسيق رموز النقاط والخطوط والمساحات، وتدرجات الراستر، وتصميم الخرائط وتوافق ArcMap/Pro وQGIS وMapLibre وCesium. وأضفنا [GIS Device Context](skills/gis-device-context/SKILL.md) للتحقق من التاريخ والوقت والمنطقة الزمنية، وقراءة موقع الجهاز بعد الموافقة، واستخدام موقع المشهد منفصلًا في أدوات Sunlight والمحاكاة الزمنية. العدد الحالي **18 مهارة** ويشمل أيضًا [هندسة KML/KMZ](skills/kml-kmz-engineering/SKILL.md).

أضفنا [كتالوجًا مستقلاً لـ19 مصدرًا للاستايلات](references/cartographic-style-sources.json)، تتضمن [مكتبة ArcMap الخاصة بالمطور](https://github.com/ahmadibrahim4geo/ArcMap-Style-Collection) ومراجع QGIS وOS GeoDataViz وCARTOColors ومصادر تدرجات علمية، مع التمييز بين ترخيص الفهرس وتراخيص كل ملف. وفي [الصفحة ثنائية اللغة](index.html) يوجد تبويب للبحث في هذه المصادر. يوجد [مثال ألوان ورموز](examples/cartography/README.md) و[مثال للتوقيت والإحداثيات](examples/device-context/README.md) مع اختبارات محلية؛ ولا يعني نجاح اختبارات الملفات إثبات تشغيل GPS أو محرك الإضاءة الحقيقي.

**مدير أيقونات GIS موحد (25 أكتوبر 2026):** [المكتبة العامة للأيقونات](references/unified-gis-icon-manager.md) تخدم ArcGIS وQGIS وCesium والويب وبرامج سطح المكتب، مع **جزء متخصص لـKML/KMZ**؛ لا حاجة لمكتبة رموز مكررة. جرّب [نموذجًا مستقلًا بالعربية والإنجليزية لإنشاء SVG/PNG](examples/icon-manager/index.html)، ثم [تعبئة صورة PNG في KMZ جديد باستخدام Python](examples/icon-manager/export_new_kmz.py). أصبح الفهرس **21 مصدرًا** بإضافة Mapular كمرجع لفكرة مولد الأيقونات وStreamline كمصدر اكتشاف بتراخيص متنوعة (ممنوع ضم الأيقونات المجانية المقيدة إلى مكتبة قابلة لإعادة الاستخدام)، ودعم SVG/PNG الجديد من Map Icons Collection. **الاستيراد يحافظ على أيقونات وألوان KMZ الأصلية.** المثال ليس مثبتًا داخل ZEarth.

**أيقونات الخرائط والحفاظ على خصائص KML/KMZ:** أضفنا [ثماني مكتبات أيقونات مجانية/مفتوحة ومولد الأيقونات Cesium PinBuilder](references/map-marker-icon-library.md) إلى الكتالوج، موضحين تراخيص الأيقونات والخطوط والملحقات بصورة منفصلة. **يمنع تغيير رموز النقاط وألوان الخطوط والمساحات والشفافية والملصقات في أي KMZ مستورد تلقائيًا**؛ تنطبق المكتبات الجديدة فقط على العناصر الجديدة أو التعديلات التي اختارها المستخدم. راجع [قواعد الحفاظ على استايلات KML/KMZ الأصلية](references/kml-kmz-symbol-preservation.md) و[الاختبار المحلي لمقارنة الأنماط وصور KMZ](examples/kml-style-preservation/README.md)، بالإضافة إلى [دليل Google/OGC](references/google-kml-kmz-compatibility.md) الموجود مسبقًا.

## تحسينات عملية مجانية وتدقيق التراخيص — 25 أكتوبر 2026

أضفنا [سجل مراجعة ملفات التراخيص الأصلية](references/upstream-license-audit.md) و[أداة تدقيق تغطية مراجعتها](scripts/audit_license_catalog.py). تمت مراجعة ملفات ترخيص **8 مراجع من أصل 138**، ولا تزال تراخيص البقية بحاجة إلى تحقق مستقل؛ الترخيص البرمجي لا يمنح بالضرورة حقوق بيانات الأقمار الصناعية أو البرامج التجارية. وأنشأنا مثالين مجانيين يعملان محليًا دون اشتراك أو مفتاح API: [حساب الانحدار من DEM بخوارزمية Horn](examples/terrain-slope/README.md)، و[فحص عناصر STAC حسب التاريخ والموقع التقريبي ونسبة السحب](examples/stac-offline/README.md)، مع بيانات اصطناعية واختبارات مستقلة وحدود دقة معلنة. أضفنا روابط المهارات وموقع Index والاختبارات إلى خطة المزامنة.

## إضافة Blue Marble Geographics وGlobal Mapper — 25 أكتوبر 2026

أضفنا [مهارة Global Mapper Development](skills/global-mapper-development/SKILL.md) و[دليل Blue Marble والـSDK والمشروعات](references/blue-marble-global-mapper.md)، إلى جانب سبعة مستودعات Fork منشورة تحت حساب الشركة ومشروع مجتمعي لأمثلة سكربتات GMS. أصبحت المهارات **15** والمشروعات البرمجية **138**، مع بقاء **52 API** و**24 دليل بيانات** دون زيادة مصطنعة. وحدثنا [الصفحة الرئيسية](index.html) والـRouter ومهارات سطح المكتب والتضاريس والخرائط. **Global Mapper والـSDK برمجيات تجارية**، ووجود مستودعات عامة للشركة لا يعني أن محرك البرنامج متاح برخصة حرة.

## إضافة Earth View إلى مصادر تطوير GIS — 25 أكتوبر 2026

فحصنا [Earth View](https://github.com/colincode0/earth-view) وأضفناه إلى [دليل المشروعات](references/project-catalog.json) و[مراجعة هندسية متخصصة](references/earth-view-architecture.md) للكرة الأرضية ثلاثية الأبعاد ومصادر NASA GIBS وSentinel وتطبيق Electron. حدّثنا مهارات الخرائط وسطح المكتب والاستشعار عن بُعد وواجهات API، وربطنا المرجع الجديد بصفحة Index. لم نكرر NASA GIBS أو Copernicus لأنهما موجودان بالفعل في فهرس API. وأضفنا [منهجية تحديث موحدة](references/source-intake-workflow.md) للمراجع والمهارات وصفحتي الموقع بالعربية والإنجليزية. **لم يظهر ترخيص واضح للمشروع؛ الاستفادة مرجعية فقط دون نسخ كوده.**

## توسعة OpenGeoS ومستودعات البيانات الجغرافية — 25 أكتوبر 2026

أضفنا **24 دليلًا وبوابةً للبيانات الجغرافية** في فهرس منفصل عن **52 واجهة GIS API** و**129 مرجعًا برمجيًا**. يرتبط هذا الفهرس بمستودعك [GIS Data Repositories Professional 2026](https://github.com/ahmadibrahim4geo/gis-data-repositories-professional-2026) الذي يضم أكثر من 2660 مصدرًا وفق توثيقه، دون نسخ قائمته أو تكرار صيانتها. يمكنك البحث من [الواجهة الثنائية اللغة](index.html) ومراجعة [فهرس المصادر JSON](references/geospatial-data-repositories.json) و[دليل اختيار المصادر](references/geospatial-data-repositories.md). **وجود رابط في الدليل لا يثبت أن البيانات متاحة مجانًا أو قابلة للتنزيل أو الترخيص التجاري.**

أصبحت لدينا ثلاث مهارات جديدة: [مستودعات البيانات](skills/geospatial-data-catalogs/SKILL.md) و[وكلاء GeoAI](skills/geospatial-ai-agents/SKILL.md) و[التضاريس والهيدرولوجيا وLiDAR](skills/terrain-hydrology-lidar/SKILL.md)، مع [دليل التكامل المتقدم مع OpenGeoS](references/opengeos-advanced-integration.md) و[مثال بحث قابل للاختبار دون شبكة](examples/data-catalogs/README.md).

**توسعة البحث الجغرافي (25 أكتوبر 2026):** يضم فهرس الـ APIs الآن **52 خدمة**، منها **15 خدمة للبحث بالأسماء والعناوين والمعالم**، مصنفة من المفتوحة المصدر، والمجانية بشروط، والمجانية برصيد، إلى التجريبية والتجارية. انتبه: **2500 طلب يوميًا لدى OpenCage للتجربة فقط**، وخادم Nominatim العام يمنع الاقتراحات أثناء الكتابة. راجع [دليل البحث عن المواقع والمعالم](references/geocoding-place-search.md) و[كتالوج الخدمات](references/free-geospatial-apis.json).

**الصفحة التعريفية:** [موقع المشروع على GitHub Pages](https://ahmadibrahim4geo.github.io/GIS-Development-Skills/) *(تُراجع حالة النشر في إعدادات Pages)* · [كود الواجهة](index.html) · [الشعار](assets/logo.svg) · [ملف المهارة](skills/gis-development/SKILL.md) · [الإبلاغ عن مشكلة أو اقتراح تطوير](https://github.com/ahmadibrahim4geo/GIS-Development-Skills/issues/new/choose).

**نبذة:** دليل عملي ومهارة قابلة للتثبيت لمساعدة المطورين والوكلاء البرمجيين على بناء واختبار أدوات نظم المعلومات الجغرافية، مع فهرس للمكتبات والمشروعات، ومصادر البيانات وواجهات GIS API، وقوالب جاهزة للانطلاق. المشروع لا يتضمن نسخًا من البرامج أو تراخيص استخدام الخدمات الخارجية.

مشروع مفتوح المصدر لإرشاد المطورين ووكلاء الذكاء الاصطناعي عند إنشاء أدوات GIS وإضافات ArcGIS وQGIS وبرامج GIS المستقلة وخرائط الويب والكرة الأرضية ثلاثية الأبعاد.

**هذا مشروع مهارة قابلة للتثبيت، وليس مجرد قائمة روابط.** يوجد ملف `SKILL.md` يحدد أسلوب العمل، ومراجع تقنية، وقوالب أولية، وفهرس قابل للبحث عن المشروعات مفتوحة المصدر.

## النظام العملي لوكلاء تطوير GIS

أصبح [Core Skill](skills/gis-development/SKILL.md) موجّهًا مختصرًا للمهام، مع [حفظ التعليمات القديمة كاملة](references/gis-development-full-guidance.md) و[شجرة قرار](references/agent-decision-tree.md).

- [تقرير قبول GIS](templates/GIS_ACCEPTANCE_REPORT.md) و[التحقق من مستوى الإثبات](scripts/validate_evidence.py).
- [بيانات اختبار ونتائج متوقعة](fixtures/README.md) و[اختبارات ArcGIS Pro وQGIS داخل بيئتهما](native_tests/README.md).
- [أمان GIS](references/geospatial-security.md) و[الأداء](references/geospatial-performance.md) و[أمثلة الأخطاء قبل وبعد تصحيحها](references/gis-antipatterns.md).
- [بيان أعداد مركزي](references/repository-manifest.json) و[متابعة منفصلة لإتاحة الخدمات](docs/SERVICE_MONITORING.md).

جميع المهارات والمراجع والـAPI والشعار والواجهة السابقة محفوظة دون حذف. لا ندّعي نجاح اختبار برامج GIS الأصلية دون تشغيلها.

## تطبيقات GIS هندسية ومعيار الجودة — 24 أكتوبر 2026

**توسعة بإضافات جديدة فقط دون حذف أي مهارات أو قوالب أو مراجع أو تغيير الشعار والواجهة السابقة.** أصبح المشروع يضم **14 مهارة قابلة للتثبيت** و**129 مرجعًا جغرافيًا** و**52 خدمة GIS API** و**24 دليلًا للبيانات**.

- [مهارة قواعد البيانات المكانية](skills/spatial-databases/SKILL.md): PostGIS وSpatiaLite والفهارس وتحليل الاستعلامات.
- [مهارة معالجة البيانات الجغرافية](skills/geospatial-data-processing/SKILL.md): الراستر والفيكتور والتحقق من المساقط والوحدات.
- [مهارة الاستشعار عن بُعد](skills/remote-sensing-pipelines/SKILL.md): STAC وCOG وEarth Engine وجودة المرئيات.
- [أمثلة GIS عملية](examples/README.md): تدقيق الشبكات، وبيانات الطقس إلى GeoJSON، وتصدير ملفات PDF على دفعات، وأمثلة PostGIS وSTAC/COG.
- [معيار جودة المهارات](docs/QUALITY_BENCHMARK.md): درجات التحقق T0–T4 واختبارات التشغيل الفعلي.
- [دليل سير العمل الهندسي](references/production-workflows.md): خطوات آمنة وقابلة للتكرار.

بيانات فحص الشبكات والطقس بيانات اصطناعية قابلة للاختبار آليًا، ولا تعني نجاح تشغيل ArcGIS أو QGIS أو قواعد البيانات أو الخدمات الحية قبل تجربتها في بيئاتها الفعلية.

## دمج منظومة Esri للمساقط والمشروعات المفتوحة (24 أكتوبر 2026)

كان الفهرس قد بلغ **99 مشروعًا** قبل إضافة الأمثلة الستة بعد إضافة 15 مصدرًا جديدًا موثقًا من منظومة Esri وSpatialReference.org ومصادر CRS المكملة. المهارة المتخصصة الجديدة هي [coordinate-reference-systems](skills/coordinate-reference-systems/SKILL.md)، ويمكن تثبيتها بالأمر:

```powershell
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill coordinate-reference-systems
```

**التقسيم يتبع المصطلحات الرسمية لإزري**: `Favorites`، `Layers`، `Geographic Coordinate Systems`، `Projected Coordinate Systems`، `Vertical Coordinate Systems`، و`Custom` مع فصل الأفقي عن الرأسي. ويتضمن توثيق `Zone Series`، أكواد `WKID` و`latestWkid`، نطاق الاستخدام، المساقط والتحويلات الجيوديسية ودقتها.

- [الدليل الشامل لقاعدة مساقط Esri وموقع SpatialReference.org](references/esri-crs-and-spatialreference.md).
- [مصفوفة الاستفادة من مشروعات Esri المفتوحة](references/esri-open-source-integration.md).
- [أداة بحث وفحص ملفات Esri CSV/JSON](scripts/crs_catalog.py) تعمل محليًا بعد تنزيل ملفات المصادر؛ لا تحتوي على محرك التحويل التجاري ولا تعيد توزيع قاعدة البيانات كاملة.

```bash
python scripts/crs_catalog.py --source ./projection-engine-db-doc/csv --tree
python scripts/crs_catalog.py --source ./projection-engine-db-doc/csv --kind projcs --query Egypt
```

**ملاحظة مهمة:** شجرة المجلدات الجغرافية التفصيلية في واجهة ArcGIS Pro ليست متاحة كاملة في جداول Projection Engine المنشورة؛ تم الالتزام بالمسميات العليا الصحيحة، ولا تُعرض التقسيمات المستنتجة بوصفها نسخة رسمية حرفية. إجراء تحويل الإحداثيات يحتاج محركًا معتمدًا مثل PROJ أو ArcPy والتحقق من شبكات التحويل وحقوق استخدامها.

## الفئات الأساسية

- **ArcMap القديم:** نماذج متوافقة مع Python 2.7، دون استخدام خصائص Python 3.
- **ArcGIS Pro:** تطوير أدوات `.pyt` وArcPy مع التحقق من المعاملات ونتائج التنفيذ.
- **QGIS:** إضافات PyQGIS ومعالجات Processing.
- **التطبيقات المستقلة:** محركات GDAL وPROJ وGEOS، وRust/Tauri وQt وغيرها حسب المتطلبات.
- **خرائط 2D/3D:** MapLibre وCesiumJS وGeoLibre، مع مراجعة سياسات مصادر الخرائط والتضاريس.
- **الاستشعار عن بعد:** النماذج المفتوحة للتحليل والتصنيف ودمج البيانات المكانية.

## مراجعة تقنية وتحسينات المهارات — الإصدار v0.3.5

أضفنا مهارة سابعة متخصصة في [تطوير برامج GIS Desktop المستقلة](skills/gis-desktop-application-development/SKILL.md)، مع [دليل هندسة البرامج والاختبار والتوزيع](references/desktop-application-engineering.md)، يستفيد من التجارب الواقعية في مرصاد Desktop دون اعتبار النسخة التجريبية إصدارًا مستقرًا.

كمان أضفنا أداة `scripts/validate_skill_pack.py` لمراجعة تعريفات كل المهارات، وروابط الملفات الداخلية، وملفات الموقع، وتطابق العدادات مع الفهارس. بقى المستودع يحتوي **8 مهارات** و**104 مشروعات مرجعية** و**52 خدمة بيانات**. [التقرير الفني](docs/TECHNICAL_AUDIT_2026-10-24.md) يوضح ما جرى اختباره وما زال يحتاج تشغيلًا حيًا داخل ArcGIS/QGIS وWindows.

```bash
python scripts/validate_skill_pack.py
python -m unittest discover -s tests -v
```

## GEBCO_2026 — نموذج أعماق البحار والتضاريس العالمية المجاني

أضفنا خدمتين رسميتين للبيانات: **WMS** لعرض خرائط أعماق البحار وتضاريس الأرض، و**OPeNDAP عبر CEDA** لقراءة قيم الارتفاعات والأعماق الرقمية. الفاصل الشبكي 15 ثانية قوسية (نحو 463 متر عند خط الاستواء) وليس معناه دقة القياس الفعلية. القيم بالمتر موجبة لليابسة وسالبة للأعماق. وثقنا كذلك طبقة **TID** لتحديد مصدر وموثوقية الخلايا، وأداة التنزيل الرسمية لصيغ GeoTIFF وNetCDF وEsri ASCII. البيانات متاحة مجانًا حتى للاستخدام التجاري مع نسب المصدر؛ **ولا يجوز الاعتماد عليها لأغراض الملاحة البحرية والسلامة في البحر**. اقرأ [التفاصيل الفنية](references/free-geospatial-apis.md). العدد الحالي **52 خدمة GIS API و8 مهارات**.

## توسعة واجهات GIS API المجانية — 24 أكتوبر 2026

أصبح لدينا **37 خدمة API موثقة بعد إضافة 19 خدمة** تغطي الحدود الإدارية (geoBoundaries)، السكان (WorldPop وWorld Bank)، الأسماء الجغرافية (GeoNames)، الحرائق والزلازل والأحداث الطبيعية (NASA FIRMS وEONET وUSGS)، صور الأقمار الصناعية (NASA CMR)، جودة الهواء (OpenAQ وOpen-Meteo)، تصريف الأنهار (GloFAS)، المسارات وتاريخ OSM (HeiGIT openrouteservice وohsome v2)، البيانات الإنسانية (HDX HAPI)، المد والجزر والبيانات البحرية والمناخية (NOAA)، والأحياء (iNaturalist).

الفهرس متاح عبر [دليل الخدمات](references/free-geospatial-apis.md)، و[ملف JSON](references/free-geospatial-apis.json)، و[مهارة اكتشاف البيانات](skills/geospatial-data-discovery/SKILL.md)، كما تظهر الخدمات تلقائيًا في بحث الصفحة الرئيسية. **المجانية لا تعني السماح باستخدام تجاري غير محدود**؛ يجب حفظ المفاتيح الشخصية بأمان وتوثيق مصدر كل بيانات ودقتها.

تتوفر الآن [مهارة ثامنة متخصصة في دمج واجهات GIS API](skills/geospatial-api-integration/SKILL.md)، مكملة لمهارة اكتشاف البيانات، وتشرح إدارة مفاتيح API، والحصص، والأخطاء، وتوحيد الإحداثيات والوحدات، وتوثيق المصدر، واختبار المخرجات داخل ArcGIS وQGIS وDesktop.

~~~bash
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill geospatial-api-integration
~~~

## أمثلة واقعية من أدوات GIS الأصلية — v0.3.3

أضفنا **5 مستودعات من مشروعات أحمد إبراهيم** إلى فهرس المصادر، ليصبح الإجمالي **104 مشروعات**، مع مهارة سادسة لتطوير واختبار أدوات ArcGIS. وتشمل:

- [MIRSAD](https://github.com/ahmadibrahim4geo/MIRSAD): ثلاث حزم ArcGIS Python Toolbox للحسابات المناخية، ونواة مشتركة، ونسخة Desktop مستقلة ما زالت تحت التطوير.
- [CreateFlowArrow](https://github.com/ahmadibrahim4geo/Create-FlowArrow-Tool): أسهم واتجاهات الجريان وتدقيق شبكات الانحدار، مع معالجة خاصة لخطر التعديل المباشر للمدخلات.
- [Geological Cross-Section Toolbox](https://github.com/ahmadibrahim4geo/GeologicalCrossSectionToolbox): قطاعات جيولوجية وتضاريسية وأدلة وبيانات تدريبية.
- [ArcMap Style Collection](https://github.com/ahmadibrahim4geo/ArcMap-Style-Collection): مرجع للرموز والستايلات؛ تراخيص ملفات الجهات الأخرى تحتاج مراجعة مستقلة.
- [GIS Data Repositories Professional](https://github.com/ahmadibrahim4geo/gis-data-repositories-professional-2026): فهرس بيانات متعدد المصادر وأدوات تدقيق الروابط.

يمكن تثبيت [مهارة تطوير ArcGIS Toolbox](skills/arcgis-toolbox-engineering/SKILL.md)، وقراءة [دليل الحالات العملية والاختبارات](references/ahmad-ibrahim-gis-case-studies.md). الاختبار باستخدام ArcPy مقلّد لا يثبت تشغيل ArcMap أو ArcGIS Pro فعليًا؛ التحقق النهائي يتطلب تشغيلًا داخل البرامج ذاتها.

```bash
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill arcgis-toolbox-engineering
```

## إضافات برامج الدكتور Qiusheng Wu — الإصدار v0.3.2

راجعنا [دليل البرامج الذي نشره الدكتور](https://gishub.org/software/) وحددنا **40 مستودع GitHub غير مكرر**، وأضفناها إلى فهرس المشروع الذي أصبح يضم **84 مصدرًا**. تشمل المكتبات ArcGIS وQGIS وPython وGeoAI وRust/WebAssembly وMapLibre، بالإضافة إلى فهارس اكتشاف بيانات STAC وNASA وغيرها.

ولأننا نريد مهارات عملية، أضفنا ثلاثة ملفات `SKILL.md` جديدة قابلة للتثبيت مستقلة عن المهارة العامة:

- [مهارة اكتشاف البيانات الجغرافية](skills/geospatial-data-discovery/SKILL.md).
- [مهارة تطوير إضافات QGIS](skills/qgis-plugin-development/SKILL.md).
- [مهارة تطوير خرائط الويب وMapLibre](skills/geospatial-web-mapping/SKILL.md).

راجع [دليل الاختيار والتنفيذ](references/gishub-software.md) لمعرفة المكتبة المناسبة، والمتطلبات، والاختبارات والقيود. الروابط الموثقة ليست أكوادًا منسوخة، ولا تضمن صلاحية تراخيص الخدمات والمرئيات أو توافق المكتبات مع كل إصدار GIS.

## مستودعا EarthMapper اللذان تم التحقق منهما

- **[AliAlkazraji/EarthMapper](https://github.com/AliAlkazraji/EarthMapper):** مرجع مهم لخصائص تطبيق Windows GIS المبني على WPF وWebView2، لكن المستودع يعرض حاليًا `README.md` فقط؛ **الكود المصدري غير منشور ورخصة إعادة استخدام الكود غير موجودة**.
- **[HIT-SIRS/EarthMapper](https://github.com/HIT-SIRS/EarthMapper):** دراسة أكاديمية لتوليد الخرائط من الصور الفضائية والعكس. المستودع يعرض أوراقًا/صورًا ورخصة Apache-2.0، **وليس كودًا تنفيذيًا أو أوزان نموذج** في المراجعة الحالية.

أضفنا مراجع مكتبات مفيدة مثل NetTopologySuite، وWebView2Samples، وArcGIS Pro SDK وGeoAI وPySTAC وTiTiler وDuckDB، مع توضيح استخداماتها ومحاذير الترخيص. التفاصيل في [`earthmapper-case-studies.md`](references/earthmapper-case-studies.md) و[`dotnet-gis.md`](references/dotnet-gis.md).

## دليل تكامل GeoLibre (الإصدار v0.3.1)

أضفنا [`references/geolibre-integration.md`](references/geolibre-integration.md) لتوجيه مطوّري نظم المعلومات الجغرافية ووكلاء الذكاء الاصطناعي لاستخدام مهارة GeoLibre الرسمية وMCP وPython وواجهات تطوير Plugins، مع الاستفادة من معمارية التطبيق في فصل محركات الخرائط عن التحليل المكاني. لا ننقل كود الجهات الخارجية دون تراخيص واضحة ولا نخلط GeoLibre بإضافات ArcGIS أو QGIS.

## إضافات الإصدار v0.3.0

- **[GeoLibre R](https://github.com/opengeos/geolibre-r)**: مكتبة مفتوحة المصدر MIT لعرض وتطوير الخرائط داخل RStudio وShiny وQuarto.
- **[RustGIS](https://github.com/opengeos/RustGIS)**: برنامج GIS مكتوب بلغة Rust تحت Apache-2.0؛ يصلح مرجعًا لبناء تطبيقات الديسكتوب وأوامر الريبون والإضافات. مختلف عن منظومة GeoRust.
- **[دليل واجهات GIS المجانية والعامة](references/free-geospatial-apis.md)**: 18 خدمة للمناخ والارتفاعات والـDEM والصور الفضائية والخرائط الأساسية والبحث المكاني والتربة والتنوع الحيوي، مع نوع المفتاح وشروط المجانية وحدود الطلبات والتراخيص.

**تنبيه:** المجانية لا تعني حرية الاستخدام التجاري أو عددًا غير محدود من الطلبات أو حق التخزين دون اتصال. SoilGrids REST متوقفة مؤقتًا حسب الجهة، وبعض خدمات OpenStreetMap العامة مقيّدة بشدة.

## إعادة تصميم الصفحة الرئيسية بالكامل — 25 أكتوبر 2026

أعدنا تصميم [صفحة HTML الرئيسية](index.html#how-to-use) لتكون تجربة استخدام متكاملة بألوان فحمية داكنة وأخضر جغرافي وسماوي، مع شرح الخطوات الأربع داخل الصفحة نفسها. المستخدم يختار من 8 مسارات GIS ويحصل مباشرة على أمر تثبيت المهارة المناسبة ونموذج طلب مخصص بالعربية والإنجليزية يمكن نسخه، بالإضافة إلى مسار استخدام يدوي وأمثلة للتوثيق والاختبارات وأسئلة شائعة. لا يحتاج المستخدم إلى دخول ملفات المستودع لفهم البداية. تم **الاحتفاظ بقسم صورة واسم وبيانات المطور ووسائل التواصل بنفس هيكله ونصوصه**، مع تحديث الألوان فقط.

## كيفية الاستخدام — خطوات عملية بالعربية والإنجليزية

أصبحت الصفحة الرئيسية تحتوي على [How to Use](index.html#how-to-use) لتوضيح اختيار التخصص والتثبيت وكتابة طلب للوكيل ومراجعة الخطة وتوثيق الاختبارات، مع مثال جاهز للنسخ ومسار بديل للاستخدام اليدوي. كذلك تم تطوير [البداية السريعة بالمستكشف](explorer.html#get-started) وتوفير [دليل عربي مفصل](docs/HOW_TO_USE.ar.md) و[دليل إنجليزي](docs/HOW_TO_USE.md). **صفحات الموقع لا تشغّل أدوات GIS أو الوكيل بنفسها.**

## البداية

بعد إنشاء المستودع العام ورفع ملفاته إلى GitHub:

```bash
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill gis-development
```

ولفحص قائمة المكتبات محليًا:

```bash
python scripts/validate_catalog.py
python scripts/validate_api_catalog.py
python scripts/search_api_catalog.py --category satellite-imagery
python scripts/search_catalog.py --query rust
```

> جميع الأمثلة البرمجية نقطة انطلاق ولا يُفترض تشغيلها داخل ArcGIS أو QGIS بنجاح دون اختبارها في الإصدار المستهدف. والمستودعات الخارجية ليست أجزاء من هذا المشروع ولا تُنقل منها الأكواد تلقائيًا.

**تاريخ إعداد الفهرس:** 24 أكتوبر 2026.  **المؤلف:** Ahmed Ibrahim.  **الحالة:** توسعة إضافية بعد v0.3.5 دون إعلان إصدار برمجي جديد.

تعليمات النشر: [`PUBLISHING.md`](PUBLISHING.md).

اقرأ: [`SKILL.md`](skills/gis-development/SKILL.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`README.md`](README.md).

### المعجم الجغرافي العالمي — World Gazetteer

يوثّق [دليل World Gazetteer](references/world-gazetteer-reference-layer.md) البحث عن أسماء المواقع الجغرافية وطبقة **Reference Layers** المستقلة التي تُظهر الأسماء حسب مقياس الخريطة، مع دعم مصادر GeoNames المجانية والعمل دون اتصال، وتنظيم التسميات بحسب الأولوية، وخيارات اللغة العربية والإنجليزية دون تعديل ملفات KML/KMZ الأصلية. يوجد [مثال Python/SQLite قابل للاختبار](examples/gazetteer/README.md) للعرض ثنائي الأبعاد؛ **لم تُنجز بعد عملية الربط أو الاختبار داخل تطبيق ZEarth الفعلي**.
