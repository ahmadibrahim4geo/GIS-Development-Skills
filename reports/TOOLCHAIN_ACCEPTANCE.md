# قبول فحص أدوات التطوير وبناء WPF

20 نوفمبر 2026 بتوقيت القاهرة · P05 / S5 · المراجعة r4

| الفحص | النتيجة المرصودة |
| --- | --- |
| Windows و.NET | Windows 11 x64، وSDK 10.0.300، وWindowsDesktop Runtime 10.0.8 أثناء التشغيل. |
| Workloads | منع العزل قراءة Windows Service Control Manager. نفذنا استعلام dotnet workload list في نطاق القراءة الذي سمح به المضيف، فعاد ناجحًا بقائمة workloads إضافية فارغة. |
| Visual Studio | اكتشف vswhere نسخة Community 2022 بإصدار 17.14.37710.0. استعلامات معرّفات .NET Desktop وNative Desktop وVC Tools الأربعة لم تُرجع instance مطابقًا. |
| مكونات GIS | قُرئت موارد إصدارات ملفات QGIS 4.2.3.0 وArcGIS Pro 3.6.0.59527 وQt المرفق مع QGIS. سجّل التقرير أيضًا Python 3.13.7 من بيانات ArcGIS Conda وNode v26.7.0 من استعلام الإصدار. |
| قالب وبناء | أنشأ .NET القالب المثبّت WPF، وأنهى restore بقائمة مصادر NuGet فارغة، وبنى net10.0-windows. المراحل الخمس عادت برمز 0. |
| تشغيل وإعادة قراءة | أُنشئت نافذة Windows فعلية. فعّل AutomationPeer زر القراءة مرة واحدة، وقرأ التطبيق شبكة QGIS السابقة بعرض وارتفاع 2، وEPSG:4326، وNoData -9999 وثلاث خلايا صالحة. |

نُفذ البناء في مجلد مؤقت. تطابقت بصمات مدخل QGIS ونسخته داخل المشروع.
وثّق الإيصال بصمة الملف المجمّع وقيم القراءة. بقي تشغيل واجهة Visual
Studio واختبار WPF من عميل UI Automation خارجي وبناء Qt والترخيص الفعلي
لـArcGIS وتجربة التثبيت على جهاز نظيف NOT RUN. نمط المراجعة SAME_AGENT_REVIEW.

[الإيصال وفحص الـSDK](P05_TOOLCHAIN_EVIDENCE.json) · [خطوات إعادة اختبار WPF](../native_tests/README.md#windows-wpf-toolchain-acceptance)
