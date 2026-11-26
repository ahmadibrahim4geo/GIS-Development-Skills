# Portable Agent Plugin (`portable`)

- **Plugin ID:** `ahmadibrahim4geo.gis-development-skills`
- **Version:** `0.3.5` (`cb46a75f15026752760e0e489f4ec4520bffdd7d`)
- **Phase Status:** `ACTIVE_P02`
- **Manifest:** [plugin/plugin.json](plugin/plugin.json)
- **Parity Report:** [parity-report.json](parity-report.json)
- **Local ZIP Artifact:** `artifacts/gis-development-suite.zip` (`artifacts/gis-development-suite.zip.sha256`)
- **Hooks Contract:** Lifecycle hooks are explicitly omitted/stripped (`supports_hooks: false`).

## English — Installation, Verification & Uninstall

1. **Verify integrity locally:** `python -B ../../scripts/build_skill_bundle.py --check plugin`
2. **Platform installation:** Extract `artifacts/gis-development-suite.zip` or copy `plugin/` directly into any Agent Skills-compatible environment.
3. **Submission boundary:** Remote/portal uploads remain `PREPARED_FOR_SUBMISSION` / `MANUAL_ACTION_REQUIRED` until manually uploaded or authorized.
4. **Rollback / Uninstall:** Remove the synced copy or run `python -B ../../plugin-system/core/pipeline.py --rollback --platform portable`.

## العربية — التثبيت والتحقق والإزالة

- **توافق المنصة:** يتم استبعاد خطافات دورة الحياة غير المدعومة صراحةً (`supports_hooks: false`).
- **التثبيت والمزامنة:** فك ضغط `artifacts/gis-development-suite.zip` أو انسخ مجلد `plugin/` إلى أي عميل يدعم Agent Skills.
- **التحقق دون اتصال:** نفّذ `python -B ../../scripts/build_skill_bundle.py --check plugin` ثم راجع تقرير التكافؤ [parity-report.json](parity-report.json).
- **الإزالة أو التراجع:** احذف النسخة المثبتة لدى العميل أو استرجع آخر نسخة سليمة عبر `--rollback --platform portable`.

- [Canonical Repository Guide](../../README.md) · [Plugins Index](../index.json)
