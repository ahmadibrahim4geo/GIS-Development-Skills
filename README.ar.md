# مهارات تطوير نظم المعلومات الجغرافية — GIS Development Skills

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

## البداية

بعد إنشاء المستودع العام ورفع ملفاته إلى GitHub:

```bash
npx skills add ahmadibrahim4geo/GIS-Development-Skills --skill gis-development
```

ولفحص قائمة المكتبات محليًا:

```bash
python scripts/validate_catalog.py
python scripts/search_catalog.py --query rust
```

> جميع الأمثلة البرمجية نقطة انطلاق ولا يُفترض تشغيلها داخل ArcGIS أو QGIS بنجاح دون اختبارها في الإصدار المستهدف. والمستودعات الخارجية ليست أجزاء من هذا المشروع ولا تُنقل منها الأكواد تلقائيًا.

**تاريخ إعداد الفهرس:** 24 أكتوبر 2026.  **المؤلف:** Ahmed Ibrahim.  **الحالة:** v0.2.0.

تعليمات النشر: [`PUBLISHING.md`](PUBLISHING.md).

اقرأ: [`SKILL.md`](skills/gis-development/SKILL.md) · [`CONTRIBUTING.md`](CONTRIBUTING.md) · [`README.md`](README.md).