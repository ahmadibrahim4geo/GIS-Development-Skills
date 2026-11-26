# تقييم موارد ملحق A

21 نوفمبر 2026 بتوقيت القاهرة · P09 · المراجعة r6

راجعت الموارد الـ27 في جزء «موارد ومكتبات ومهارات للتقييم حسب الحاجة». حالة «مرجع» تعني مراجعة مصدره أو وثائقه. قبول التشغيل يخص الإجراء والنسخة اللي تم اختبارهما. تُراجع رخصة المنتج والخدمة والبيانات بصورة مستقلة عن رخصة كود المصدر. المرجع التاريخي للقائمة هو `SOURCE/MASTER_AGENT_EXECUTION_PLAN_ORIGINAL.md` من حزمة خطة 20 نوفمبر المحفوظة في الأرشيف المحلي.

| # | المورد | الحالة والاستخدام | المصدر |
| --- | --- | --- | --- |
| 1 | Agent Skills specification | مرجع لصيغة المهارات. اجتاز الفحص المحلي للحزمة ذات 35 مهارة. | [المواصفة](https://agentskills.io/specification) |
| 2 | OpenAI Skills | مرجع لتأليف وتقييم المهارات. رخصة Skill Creator هي Apache-2.0، وتُراجع الرخصة لكل مهارة. | [ترخيص المثال](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/LICENSE.txt) |
| 3 | Anthropic Skills | مرجع لتصميم المهارات. رخصة Canvas Design هي Apache-2.0. تُراجع شروط كل مهارة. | [ترخيص المثال](https://github.com/anthropics/skills/blob/main/skills/canvas-design/LICENSE.txt) |
| 4 | NVIDIA Skills | مرجع لمهام GPU والأداء. المستودع يعلن Apache-2.0 وCC-BY-4.0. راجع رخصة الملف المنتقى. | [المصدر](https://github.com/NVIDIA/skills#license) |
| 5 | NVIDIA SkillSpector | مرشح ماسح خارجي. رخصة المصدر Apache-2.0. التشغيل NOT RUN. | [الرخصة](https://github.com/NVIDIA/SkillSpector/blob/main/LICENSE) |
| 6 | Cisco Skill Scanner | مرشح ماسح خارجي. رخصة المصدر Apache-2.0. التشغيل NOT RUN. | [الرخصة](https://github.com/cisco-ai-defense/skill-scanner/blob/main/LICENSE) |
| 7 | Qt Agent Skills | مرجع لإصدار Qt المناسب. ملف الرخصة يذكر Qt Commercial أو BSD-3-Clause. تشغيل العميل NOT RUN. | [الرخصة](https://github.com/TheQtCompanyRnD/agent-skills/blob/main/LICENSE) |
| 8 | Superpowers | مرجع مراجعة وإثبات استُفيد منه في DoneProof. رخصة المستودع MIT. | [الرخصة](https://github.com/obra/superpowers/blob/main/LICENSE) · [المراجعة المحلية](../references/skill-creator-superpowers-review.md) |
| 9 | Esri Developer Agent Skills | مرجع SDK/API والمصادقة. فُحص Apache-2.0 عند b6fcac59. التثبيت والاتصال بـMCP وتشغيل الوكيل NOT RUN. | [README المثبت](https://github.com/Esri/esri-developer-agent-skills/blob/b6fcac59bf7febd4263d77132e3cfd22d6498a5e/README.md) · [الرخصة](https://github.com/Esri/esri-developer-agent-skills/blob/b6fcac59bf7febd4263d77132e3cfd22d6498a5e/LICENSE) |
| 10 | ArcGIS Pro SDK Snippets | مرجع C# لإضافات Pro. النسخة 22855e3 تعلن Pro 3.8 و.NET 10. يمكن الاستفادة من الفكرة وتكييفها مع الـSDK الفعلي. تشغيل الإضافة NOT RUN. | [README المثبت](https://github.com/Esri/arcgis-pro-sdk-snippets/blob/22855e3a7c238f2de542602272b2f896d59d50b5/README.md) · [Apache-2.0](https://github.com/Esri/arcgis-pro-sdk-snippets/blob/22855e3a7c238f2de542602272b2f896d59d50b5/License.txt) |
| 11 | ArcGIS Pro SDK Samples | مرجع بنية Add-in وRibbon وDockpane برخصة Apache-2.0. نسخة العينات 3.6.0 تطابق Pro 3.6 المثبّت. 3.8 مرجع لإصدار مختلف. اختبار الاختيار محلي، وبناء الإضافة وتشغيلها NOT RUN. | [مرجع 3.6](https://github.com/Esri/arcgis-pro-sdk-community-samples/blob/f403431c53ccf734bfd0c444b3191c92eb2b5a96/README.md) · [Apache-2.0](https://github.com/Esri/arcgis-pro-sdk-community-samples/blob/f403431c53ccf734bfd0c444b3191c92eb2b5a96/License.txt) · [مرجع 3.8](https://github.com/Esri/arcgis-pro-sdk-community-samples/blob/abd56c5b842318bf3da879c553d9283209cd27e7/README.md) |
| 12 | CesiumJS skills | مرجع مشاهد وكاميرا و3D Tiles تحت Apache-2.0. تشغيل مهارات العميل وعرض مشهد 3D NOT RUN. | [الرخصة](https://github.com/CesiumGS/cesiumjs-skills/blob/main/LICENSE) |
| 13 | Autodesk Platform Services skills | مرجع تكامل CAD/BIM مع APIs. رخصة المصدر MIT. تشغيل الخدمات والمصادقة NOT RUN. | [README](https://github.com/autodesk-platform-services/skills) · [الرخصة](https://github.com/autodesk-platform-services/skills/blob/main/LICENSE.md) |
| 14 | GDAL | شُغّل مع QGIS لإنتاج GeoTIFF والتحقق من CRS والمحاذاة. رخصة المصدر MIT-style، ومكونات التشغيل لها حقوقها. | [الوثائق](https://gdal.org/en/stable/) · [التجربة](P08_NATIVE_ACCEPTANCE.json) |
| 15 | PROJ | مرجع الإسقاط والتحويل تحت X/MIT. تحقق من شبكة التحويل والرخصة والنتيجة في المشروع المعني. | [الوثائق](https://proj.org/en/stable/) |
| 16 | QGIS | QGIS 4.2.3 مختبر لحفظ مشروع وإعادة فتحه وتصدير GeoJSON وGeoPackage ومعالجة الراستر. واجهة QGIS الكاملة NOT RUN. | [المصدر](https://qgis.org/) · [التجربة](E2E_ACCEPTANCE.md) |
| 17 | GRASS GIS | مرجع تحليل الحوض والراستر والمتجهات. تحقق خوارزمية الحزمة ورخصتها عند الاختيار. تشغيل GRASS المستقل NOT RUN. | [المشروع](https://grass.osgeo.org/) |
| 18 | OpenLayers | مرجع عرض خرائط الويب، BSD-2-Clause. تشغيل OpenLayers NOT RUN. | [المشروع والترخيص](https://openlayers.org/) |
| 19 | MapLibre | مرجع عرض خرائط الويب وتضمينها. اختُبر Chromium بعارض نقاط محلي. تشغيل MapLibre ومصادر البلاطات NOT RUN. | [المشروع](https://maplibre.org/) · [رخصة GL JS](https://github.com/maplibre/maplibre-gl-js/blob/main/LICENSE.txt) |
| 20 | Cesium | مرجع العرض ثلاثي الأبعاد. رخصة CesiumJS هي Apache-2.0 وشروط ion والأصول مستقلة. التشغيل NOT RUN. | [المصدر](https://cesium.com/) · [رخصة CesiumJS](https://github.com/CesiumGS/cesium/blob/main/LICENSE.md) |
| 21 | USGS Spectral Library | مرجع طيفي v7. السجل الرسمي يذكر CC0 1.0. استُخدم سجل الإصدار الرسمي بعد تعذر فتح رابط الدليل الأول. تجربة ATYAF على الأطياف NOT RUN. | [سجل الإصدار](https://www.usgs.gov/data/usgs-spectral-library-version-7-data) |
| 22 | Copernicus Data Space | مرجع اكتشاف مشاهد Copernicus. تُراجع حقوق المنتج والاعتماديات عند اختيار المشهد. طلب الخدمة وتنزيل البيانات NOT RUN. | [المصدر](https://dataspace.copernicus.eu/) |
| 23 | NASA JPL ECOSTRESS | مرجع طيفي v1.0 مع إشعار حقوق وطلب إسناد. تُراجع حقوق الملف قبل نقله. تشغيل البيانات وإعادة توزيعها NOT RUN. | [المكتبة](https://speclib.jpl.nasa.gov/) |
| 24 | Index Database | مرجع أسماء المؤشرات والباندات والاستشهادات. يُراجع تعريف المستشعر والورقة لكل مؤشر. حقوق قاعدة البيانات وخدمة API تتطلب مراجعة عند الاستعمال. | [قاعدة البيانات](https://www.indexdatabase.de/) |
| 25 | Visual Studio Community | رُصد VS Community 2022 عبر vswhere. نجح WPF باستخدام .NET SDK. IDE GUI والمصمم المرئي NOT RUN. | [المصدر](https://visualstudio.microsoft.com/vs/community/) · [الفحص المحلي](TOOLCHAIN_ACCEPTANCE.md) |
| 26 | VS Code | مرجع محرر. ذكر المستخدم تثبيته. مسار التنفيذ لم يتأكد بالمواقع المفحوصة. تثبيت الحزمة في المحرر NOT RUN. | [المصدر](https://code.visualstudio.com/) · [الفحص المحلي](ROUTER_DISTRIBUTION_ACCEPTANCE.md) |
| 27 | Qt Creator | مرجع IDE. رُصد Qt Designer المرفق مع QGIS بصورة مستقلة. تشغيل Qt Creator والمصمم مع مشروع NOT RUN. | [أدوات Qt](https://www.qt.io/development/tools) · [الفحص المحلي](ROUTER_DISTRIBUTION_ACCEPTANCE.md) |

تم التقييم بالقراءة فقط للمصادر الخارجية. الاختيار وقت التنفيذ يبدأ من القدرات المتاحة في بيئة المشروع ويرجع لمسار متوافق مع الهدف. أمثلة الإصدارات الأخرى تظل مفيدة للتعلّم، وتحتاج APIs والتبعيات إلى تحقق عند التكييف. [سجل مصادر الكود](../references/gis-code-sources.json)
