# Cursor (`cursor`)

- **Plugin ID:** `ahmadibrahim4geo.gis-development-skills`
- **Version:** `0.3.5` (`01db0e0065535167dc194bc8e646c009c84ffe71`)
- **Phase Status:** `ACTIVE_P09`
- **Manifest:** [plugin/.cursor-plugin/plugin.json](plugin/.cursor-plugin/plugin.json)
- **Parity Report:** [parity-report.json](parity-report.json)
- **Local ZIP Artifact:** `artifacts/gis-development-skills-cursor.zip` (`artifacts/gis-development-skills-cursor.zip.sha256`)
- **Hooks Contract:** Lifecycle hooks are explicitly omitted/stripped (`supports_hooks: false`).

## English — Installation, Verification & Uninstall

1. **Verify integrity locally:** `python -B ../../scripts/build_skill_bundle.py --check plugin`
2. **Platform installation:** Import `GIS-Development-Skills-Plugins/cursor/plugin` via Cursor Plugins or copy repo `.cursor/rules/gis-development-skills.mdc` into your Cursor workspace rules directory (honors Cursor team/import controls).
3. **Submission boundary:** Remote/portal uploads remain `PREPARED_FOR_SUBMISSION` / `MANUAL_ACTION_REQUIRED` until manually uploaded or authorized.
4. **Rollback / Uninstall:** Remove the synced copy or run `python -B ../../plugin-system/core/pipeline.py --rollback --platform cursor`.

## العربية — التثبيت والتحقق والإزالة

- **توافق المنصة:** يتم استبعاد خطافات دورة الحياة غير المدعومة صراحةً (`supports_hooks: false`).
- **التثبيت والمزامنة:** استورد المجلد `GIS-Development-Skills-Plugins/cursor/plugin` في Cursor أو اعتمد ملف القواعد `.cursor/rules/gis-development-skills.mdc` مع الالتزام بضوابط استيراد الفريق.
- **التحقق دون اتصال:** نفّذ `python -B ../../scripts/build_skill_bundle.py --check plugin` ثم راجع تقرير التكافؤ [parity-report.json](parity-report.json).
- **الإزالة أو التراجع:** احذف النسخة المثبتة لدى العميل أو استرجع آخر نسخة سليمة عبر `--rollback --platform cursor`.

- [Canonical Repository Guide](../../README.md) · [Plugins Index](../index.json)
