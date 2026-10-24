<p align="center">
  <img src="assets/readme-banner.svg" alt="GIS Development Skills — The Heart of Geospatial Innovation" width="1200">
</p>

<p align="center">
  <a href="README.md">English</a> ·
  <a href="https://ahmadibrahim4geo.github.io/GIS-Development-Skills/">الموقع الإلكتروني</a> ·
  <a href="skills/gis-development/SKILL.md">المهارة الأساسية</a> ·
  <a href="CONTRIBUTING.md">المساهمة</a>
</p>

## طوّر أدوات وتطبيقات نظم المعلومات الجغرافية وفق منهجية يمكن التحقق منها.

مهارات تطوير برمجيات نظم المعلومات الجغرافية ومراجع مفتوحة المصدر، تشمل **7 مهارات متخصصة** و**104 مراجع جغرافية** و**18 مصدرًا لواجهات البيانات والخدمات الجغرافية**.

**الصفحة التعريفية:** [موقع المشروع على GitHub Pages](https://ahmadibrahim4geo.github.io/GIS-Development-Skills/) *(تُراجع حالة النشر في إعدادات Pages)* · [كود الواجهة](index.html) · [الشعار](assets/logo.svg) · [ملف المهارة](skills/gis-development/SKILL.md) · [الإبلاغ عن مشكلة أو اقتراح تطوير](https://github.com/ahmadibrahim4geo/GIS-Development-Skills/issues/new/choose).

**نبذة:** دليل عملي ومهارة قابلة للتثبيت لمساعدة المطورين والوكلاء البرمجيين على بناء واختبار أدوات نظم المعلومات الجغرافية، مع فهرس للمكتبات والمشروعات، ومصادر البيانات وواجهات GIS API، وقوالب جاهزة للانطلاق. المشروع لا يتضمن نسخًا من البرامج أو تراخيص استخدام الخدمات الخارجية.

مشروع مفتوح المصدر لإرشاد المطورين ووكلاء الذكاء الاصطناعي عند إنشاء أدوات GIS وإضافات ArcGIS وQGIS وبرامج GIS المستقلة وخرائط الويب والكرة الأرضية ثلاثية الأبعاد.

**هذا مشروع مهارة قابلة للتثبيت، وليس مجرد قائمة روابط.** يوجد ملف `SKILL.md` يحدد أسلوب العمل، ومراجع تقنية، وقوالب أولية، وفهرس قابل للبحث عن المشروعات مفتوحة المصدر.

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

كمان أضفنا أداة `scripts/validate_skill_pack.py` لمراجعة تعريفات كل المهارات، وروابط الملفات الداخلية، وملفات الموقع، وتطابق العدادات مع الفهارس. بقى المستودع يحتوي **7 مهارات** و**104 مشروعات مرجعية** و**37 خدمة بيانات**. [التقرير الفني](docs/TECHNICAL_AUDIT_2026-10-24.md) يوضح ما جرى اختباره وما زال يحتاج تشغيلًا حيًا داخل ArcGIS/QGIS وWindows.

```bash
python scripts/validate_skill_pack.py
python -m unittest discover -s tests -v
```

## توسعة واجهات GIS API المجانية — 24 أكتوبر 2026

أصبح لدينا **37 خدمة API موثقة بعد إضافة 19 خدمة** تغطي الحدود الإدارية (geoBoundaries)، السكان (WorldPop وWorld Bank)، الأسماء الجغرافية (GeoNames)، الحرائق والزلازل والأحداث الطبيعية (NASA FIRMS وEONET وUSGS)، صور الأقمار الصناعية (NASA CMR)، جودة الهواء (OpenAQ وOpen-Meteo)، تصريف الأنهار (GloFAS)، المسارات وتاريخ OSM (HeiGIT openrouteservice وohsome v2)، البيانات الإنسانية (HDX HAPI)، المد والجزر والبيانات البحرية والمناخية (NOAA)، والأحياء (iNaturalist).

الفهرس متاح عبر [دليل الخدمات](references/free-geospatial-apis.md)، و[ملف JSON](references/free-geospatial-apis.json)، و[مهارة اكتشاف البيانات](skills/geospatial-data-discovery/SKILL.md)، كما تظهر الخدمات تلقائيًا في بحث الصفحة الرئيسية. **المجانية لا تعني السماح باستخدام تجاري غير محدود**؛ يجب حفظ المفاتيح الشخصية بأمان وتوثيق مصدر كل بيانات ودقتها.

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

**تاريخ إعداد الفهرس:** 24 أكتوبر 2026.  **المؤلف:** Ahmed Ibrahim.  **الحالة:** v0.3.2.

تعليمات النشر: [`PUBLISHING.md`](PUBLISHING.md).

اقرأ: [`SKILL.md`](skills/gis-development/SKILL.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`README.md`](README.md).