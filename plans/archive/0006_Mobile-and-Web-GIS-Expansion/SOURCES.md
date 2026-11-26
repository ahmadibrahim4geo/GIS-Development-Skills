# أول دفعة لمراجعة مصادر Mobile وWeb GIS

تمت مراجعة الصفحات العامة والمستودعات في 22 نوفمبر 2026. الرصد هنا يثبت توفر المصدر المبيّن. تشغيل العينة أو قبول الرخصة للاستخدام المقصود يتبع التنفيذ.

## مشروعات ومكتبات وأمثلة

| الاستخدام | مصدر أو مشروع | ما يدخل في الخطة |
| --- | --- | --- |
| خريطة ويب عادية أو عارض بيانات | [MapLibre GL JS Examples](https://maplibre.org/maplibre-gl-js/docs/examples/) · [Leaflet Examples](https://leafletjs.com/examples.html) | المحركات موجودة في الكتالوج. أضف وصفة عرض طبقة GeoJSON وفحص اختيار المعلم والمصدر والنسب على بيانات محلية |
| تحرير وإسقاطات وخدمات خرائط | [OpenLayers Draw and Modify Features](https://openlayers.org/en/latest/examples/draw-and-modify-features.html) · [OGC API Features](https://www.ogc.org/standards/ogcapi-features/) | فحص تحرير وهندسة، ومسار واضح بين خريطة العرض وواجهة البيانات. اختبر محور الإحداثيات والصيغة عند تكييف العينة |
| 3D وخرائط تفاعلية متقدمة | [CesiumJS Sandcastle](https://sandcastle.cesium.com/) · [deck.gl](https://github.com/visgl/deck.gl) | مرجع لعرض 3D أو كثافة البيانات عند طلبهما. راجع رخصة كل مجموعة بيانات وخدمة على حدة |
| تطبيقات Web GIS مكتملة | [MapStore2](https://github.com/geosolutions-it/MapStore2) · [Lizmap](https://github.com/3liz/lizmap-web-client) · [GeoNode](https://github.com/GeoNode/geonode) | المشروعات موجودة. ضع روابط لأنماط لوحات الخرائط، نشر مشروع QGIS، وكاتالوج البيانات. راجع رخصة أي مكوّن قبل اقتباسه |
| بناء محرك عرض للموبايل | [MapLibre Native وأمثلته](https://maplibre.org/projects/native/) · [MapLibre Flutter](https://github.com/maplibre/flutter-maplibre) · [MapLibre React Native](https://maplibre.org/maplibre-react-native/docs/setup/getting-started/) | MapLibre Native موجود. قارن إضافات Flutter وReact Native عند الحاجة إلى واجهة مشتركة. طابِق بنية React Native وإصدار المحرك مع المثال |
| جمع ميداني ومزامنة QGIS | [QField](https://docs.qfield.org/) · [Mergin Maps Mobile](https://github.com/MerginMaps/mobile) | موجودان في الكتالوج. أضف دليل ممارسات لقواعد الملفات والنماذج والمزامنة. راجع شروط QGIS وQt والمزامنة المستضافة حسب المسار |
| جمع حقول ونماذج | [ODK Collect](https://github.com/getodk/collect) · [دليل الخرائط دون اتصال](https://docs.getodk.org/collect-offline-maps/) | مرشح إضافة كمشروع مرجعي لنماذج Android وخرائط MBTiles المحلية |
| مورّد يقدم أمثلة Web وNative | [Esri JavaScript Samples](https://developers.arcgis.com/javascript/latest/sample-code/) · [Kotlin Offline Edit/Sync](https://developers.arcgis.com/kotlin/sample-code/edit-and-sync-features-with-feature-service/) · [Swift Offline Edit/Sync](https://developers.arcgis.com/swift/v200/sample-code/edit-and-sync-features-with-feature-service/) | راجع ملفات عينات الويب والجوال والنسخ ورخص الكود. اختبر Offline بأسلوب مرتبط بالخدمة والمنتج المختار بعد التحقق من الترخيص |
| نماذج المنصة الأصلية | [Android Offline-first](https://developer.android.com/topic/architecture/data-layer/offline-first) · [Apple Maps Sample Code](https://developer.apple.com/maps/sample-code/) · [Flutter learning resources](https://docs.flutter.dev/reference/learning-resources) | مراجع لإدارة الحالة وتخزين البيانات وبناء الواجهة. أضف رابطًا مباشرًا للملف والإصدار لكل وصفة مقبولة |
| خادم بلاطات وبيانات محلية | [Martin](https://maplibre.org/martin/) · [PMTiles](https://docs.protomaps.com/pmtiles/) · [PostGIS](https://postgis.net/docs/) · [TiTiler](https://github.com/developmentseed/titiler) | استخدم PMTiles/Martin للمتجهات أو TiTiler للراستر/COG في تجربة اختيارية. اختبر النطاقات، CORS وNoData حسب المصدر |
| خرائط وبيانات البداية | [Natural Earth Terms](https://www.naturalearthdata.com/about/terms-of-use/) · [سياسة بلاطات OpenStreetMap](https://operations.osmfoundation.org/policies/tiles/) | بيانات صناعية وبيانات مفتوحة موثقة للتمرين، مع تثبيت المصدر والإصدار. خادم بلاطات OSM القياسي يحظر التنزيل الجماعي والأوفلاين. استخدم أرشيفًا أو مزودًا مصرحًا به للاستخدام دون اتصال |

## مهارات خارجية للمراجعة قبل التفعيل

| المرشح | الاستخدام المحتمل | حالة الجاهزية |
| --- | --- | --- |
| [MapLibre Agent Skills](https://github.com/maplibre/maplibre-agent-skills/tree/2e0349b12eda2c86faff8e1380e1620d82cb97b2) | إرشادات MapLibre GL JS من المجتمع، تكمل مسار الويب | سجل 0004، MIT بحسب المستودع، مراجعة تنفيذ وصلاحيات معلّقة |
| [Google Maps Platform Agent Skills](https://github.com/googlemaps/agent-skills/tree/e7538f369afc18acbd9bde2cdcb9b7a7be6d7978) | تخصص Google Maps للويب وAndroid وiOS، وخدمات الخرائط والبحث والتوجيه | سجل 0005، Apache-2.0 بحسب المستودع، تُفحص الحسابات وطرق التشغيل عند اختيار المنتج |
| [Android Developer Skills](https://github.com/android/skills/tree/c72942584fff970dac86ced78b367fce0c441e52) | ابدأ بمهارتي Compose Adaptive وTesting Setup من الكتالوج الرسمي | سجل 0006، Apache-2.0 بحسب المستودع، Android SDK ومتطلبات التوافق والاختبار معلّقة. [كتالوج Android الرسمي](https://developer.android.com/tools/agents/android-skills/browse) |
| [Esri Developer Agent Skills](https://github.com/Esri/esri-developer-agent-skills/blob/b6fcac59bf7febd4263d77132e3cfd22d6498a5e/README.md) | توجيه مشروط لمشروعات ArcGIS. راجع محتوى كل مهارة مقابل نوع SDK | سجل 0002 موجود، يُعاد استخدامه كمصدر للمراجعة |

يُسجل فرق التغطية عن مهاراتنا، وحدود المنصة، والملفات التابعة والتبعيات والأذونات والبصمة والاختبار لكل مهارة نختارها. لتشغيل أي مرشح يلزم مصدر مُراجع، تصريح تشغيل، وفحص من جلسة حقيقية.

## شركات وخدمات بخيارات مجانية أو تجريبية أو تجارية

| المزود | الجزء الذي نراجعه | المقارنة المطلوبة |
| --- | --- | --- |
| Esri | عينات JavaScript وKotlin وSwift وFlutter، وArcGIS Location Platform | فرّق بين ترخيص العينة وSDK واستحقاقات الحساب وخدمات ArcGIS Online أو Enterprise. [التسعير](https://location.arcgis.com/pricing/) · [Flutter SDK](https://developers.arcgis.com/flutter/) |
| Google Maps Platform | الخرائط على Web وAndroid وiOS وPlaces وRoutes | راجع الحصص لكل SKU وإعداد الفوترة وقيود التخزين والنسب وتقييد المفتاح. [التسعير](https://mapsplatform.google.com/pricing/) · [Android SDK](https://developers.google.com/maps/documentation/android-sdk/overview) |
| Mapbox | خرائط الويب والموبايل، البحث وخرائط الأوفلاين | الوحدات والحصص والشروط تختلف حسب المنتج. راجع حق التخزين والتوزيع والنسب. [التسعير](https://www.mapbox.com/pricing) · [Android Offline](https://docs.mapbox.com/android/maps/guides/offline/) |
| MapTiler | استضافة البلاطات والجيوكودينج مع محرك يعرض المصدر | صفحة التسعير تصف Free للاختبار وإثبات الفكرة والاستعمال الشخصي أو غير التجاري. اختر خطة أو بديل استضافة ذاتية ملائمًا للإنتاج. [التسعير](https://www.maptiler.com/cloud/pricing/) |
| Apple | MapKit لتطبيقات Apple وMapKit JS للويب | راجع حساب المطور والـtokens والحصص وشروط أي استخدام أوفلاين. [Apple Maps on the Web](https://developer.apple.com/maps/web/) · [أمثلة Apple](https://developer.apple.com/maps/sample-code/) |

تتسجل الحصة كوصف بتاريخ المراجعة، ونرجع لصفحة السعر وشروط الخدمة لحظة الاختيار. رخصة المحرك أو كود العينة مستقلة عن رخصة بيانات البلاطات والخدمة المستضافة.
