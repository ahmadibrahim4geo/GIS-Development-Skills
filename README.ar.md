<p align="center"><img src="assets/logo.svg" alt="شعار مشروع GIS Development Skills" width="440"></p>
<p align="center"><strong>مهارات ومراجع مفتوحة المصدر لتطوير برمجيات وأدوات نظم المعلومات الجغرافية.</strong></p>

# مهارات تطوير نظم المعلومات الجغرافية — GIS Development Skills

**واجهة المشروع:** [ملف الموقع الرئيسي (`index.html`)](index.html) · [الشعار والهوية](assets/). يمكن نشر الصفحة التفاعلية عبر GitHub Pages من إعدادات المستودع.

مشروع مفتوح المصدر لإرشاد المطورين ووكلاء الذكاء الاصطناعي عند إنشاء أدوات GIS وإضافات ArcGIS وQGIS وبرامج GIS المستقلة وخرائط الويب والكرة الأرضية ثلاثية الأبعاد.

**هذا مشروع مهارة قابلة للتثبيت، وليس مجرد قائمة روابط.** يوجد ملف `SKILL.md` يحدد أسلوب العمل، ومراجع تقنية، وقوالب أولية، وفهرس قابل للبحث عن المشروعات مفتوحة المصدر.

## الفئات الأساسية

- **ArcMap القديم:** نماذج متوافقة مع Python 2.7، دون استخدام خصائص Python 3.
- **ArcGIS Pro:** تطوير أدوات `.pyt` وArcPy مع التحقق من المعاملات ونتائج التنفيذ.
- **QGIS:** إضافات PyQGIS ومعالجات Processing.
- **التطبيقات المستقلة:** محركات GDAL وPROJ وGEOS، وRust/Tauri وQt وغيرها حسب المتطلبات.
- **خرائط 2D/3D:** MapLibre وCesiumJS وGeoLibre، مع مراجعة سياسات مصادر الخرائط والتضاريس.
- **الاستشعار عن بعد:** النماذج المفتوحة للتحليل والتصنيف ودمج البيانات المكانية.

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

**تاريخ إعداد الفهرس:** 24 أكتوبر 2026.  **المؤلف:** Ahmed Ibrahim.  **الحالة:** v0.3.1.

تعليمات النشر: [`PUBLISHING.md`](PUBLISHING.md).

اقرأ: [`SKILL.md`](skills/gis-development/SKILL.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`README.md`](README.md).