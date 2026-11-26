# الدليل الهندسي العربي الموحد لتطبيقات Web GIS و Mobile GIS (`W01–W12` · `M01–M10`)

> مرجع عملي ثنائي السياق يربط بين [`docs/WEB_GIS_GUIDE.md`](WEB_GIS_GUIDE.md) و[`docs/MOBILE_GIS_GUIDE.md`](MOBILE_GIS_GUIDE.md) ومهارتي [`geospatial-web-mapping`](../skills/geospatial-web-mapping/SKILL.md) و[`gis-mobile-application-development`](../skills/gis-mobile-application-development/SKILL.md).

## 1. التمييز الهندسي قبل اختيار التقنية

- **موقع تعريفي بخريطة != تطبيق Web GIS كامل:** لعرض خفيف على GitHub Pages استخدم مسارات نسبية (`./`) وقائمة جداول متاحة بلوحة المفاتيح (`W01`/`WEB-01`).
- **تطبيق Web GIS متقدم (`W03`–`W10`):** استخدم `OpenLayers` مع `Proj4js` للتحرير والإسقاطات المخصصة، و`CesiumJS` للمشاهد ثلاثية الأبعاد `3D Tiles` مع تعامل صريح مع تعطل التضاريس.
- **تطبيق PWA != تطبيق موبايل أصلي (`W08 != M01/M02`):** تطبيق الويب التقدمي يفتقر لثبات التتبع الخلفي `GNSS` ومنافذ `BLE/USB RTK` وتخزين `Keystore/Keychain`؛ و**`WebView`/`Expo Go` لا يعادلان تطبيقًا أصليًا مختبرًا**.
- **بوابة `macOS / Xcode` الإلزامية لـ `iOS`:** على بيئة `Windows` أو `Linux`، تظل اختبارات بناء وتوقيع `iOS` (`MOB-QA-02`) في حالة **`NOT RUN`** بصراحة كاملة.

## 2. القواعد الذهبية للبيانات، التزامن، والأمان الميداني

1. **نظام التزامن الموحد ذو الـ 15 حقلًا (`REQ-WM-042`):** لا تعتمد الكتابة فوق النسخ الأحدث أعمى (`No blind LWW`)؛ خزّن `project_id, layer_id, feature_id, op_id, base_revision, geometry, attributes, crs, client_timestamp, server_timestamp, device_id, attachment_manifest, deletion_tombstone, checksum, sync_state` في قاعدة محلية ذرية (`IndexedDB/Dexie` للويب، `SQLite WAL` للموبايل) واحفظ نسختي التعارض ليحسمها المستخدم.
2. **حظر سحب بلاطات OpenStreetMap العام (`WEB-QA-07` / `MOB-QA-20`):** يُحظر التخزين المسبق الجماعي من `tile.openstreetmap.org`؛ استخدم أرشيفات `PMTiles`/`MBTiles` مرخصة أو مستضافة ذاتيًا مع الإسناد الواضح.
3. **دقة الإحداثيات والارتفاع والخصوصية (`GIS-015` / `MOB-QA-04, 10`):** افصل بوضوح بين الارتفاع الإهليلجي `WGS84` والارتفاع الأورثومتري (`EGM2008`)، ووسم قراءات `GNSS` المتقادمة أو الوهمية `Mock`، وجرّد بيانات موقع الكاميرا `EXIF GPS` افتراضيًا ما لم يوافق المستخدم صراحةً، واضمن عمل الإدخال اليدوي عند رفض إذن الموقع.
4. **واجهة عربية `RTL` مع أرقام إحداثيات `LTR`:** اعرض القوائم والنماذج باتجاه `dir="rtl"` مع عزل أرقام الإحداثيات (`30.0444, 31.2357`) ورموز `EPSG` والتوقيت `UTC` داخل مقاطع `LTR` (`\u2066...\u2069`) واحترم مقاسات اللمس الآمنة (`>=48dp` / `>=44pt`).

## 3. التحقق الصادق حسب بيئة التشغيل الحالية

- **الويب (`T1` عبر Node + Python):** شغّل `node --test tests/web-gis/web_gis_contract.test.mjs` و`python -B -m unittest tests.test_web_gis_expansion -v`؛ وتبقى اختبارات المتصفح الرسومية (`Playwright/Chromium`) `NOT RUN` إذا غاب المتصفح.
- **الموبايل (`T1` عبر SQLite + Python):** شغّل `python -B -m unittest tests.test_gis_mobile_application tests.test_gis_mobile_device_evidence tests.test_mobile_gis_expansion -v` و`python -B scripts/validate_mobile_device_evidence.py examples/mobile-gis/device-acceptance.example.json`؛ وتبقى اختبارات الأجهزة الحقيقية والمحاكيات وأدوات `Android SDK` / `Xcode` موسومة **`NOT_RUN`** عند غيابها.
