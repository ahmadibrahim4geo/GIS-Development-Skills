# OpenAI Codex (CLI / Desktop) (`codex`)

- **Plugin ID:** `ahmadibrahim4geo.gis-development-skills`
- **Version:** `0.3.5` (`42de4a246a2db1f7d33cc746da9cd3a0f1718a91`)
- **Phase Status:** `ACTIVE_P09`
- **Manifest:** [plugin/.codex-plugin/plugin.json](plugin/.codex-plugin/plugin.json)
- **Parity Report:** [parity-report.json](parity-report.json)
- **Local ZIP Artifact:** `artifacts/gis-development-skills-codex.zip` (`artifacts/gis-development-skills-codex.zip.sha256`)
- **Hooks Contract:** Lifecycle hooks are explicitly omitted/stripped (`supports_hooks: false`).

## English — Installation, Verification & Uninstall

1. **Verify integrity locally:** `python -B ../../scripts/build_skill_bundle.py --check plugin`
2. **Platform installation:** Register `.agents/plugins/marketplace.json` in your Codex workspace or add `GIS-Development-Skills-Plugins/codex/plugin` directly for local Codex CLI / Desktop discovery.
3. **Submission boundary:** Remote/portal uploads remain `PREPARED_FOR_SUBMISSION` / `MANUAL_ACTION_REQUIRED` until manually uploaded or authorized.
4. **Rollback / Uninstall:** Remove the synced copy or run `python -B ../../plugin-system/core/pipeline.py --rollback --platform codex`.

## العربية — التثبيت والتحقق والإزالة

- **توافق المنصة:** يتم استبعاد خطافات دورة الحياة غير المدعومة صراحةً (`supports_hooks: false`).
- **التثبيت والمزامنة:** سجّل فهرس `.agents/plugins/marketplace.json` في مساحة عمل Codex أو أشر مباشرة إلى المجلد `GIS-Development-Skills-Plugins/codex/plugin` مع الحفاظ على سياسة `AGENTS.md`.
- **التحقق دون اتصال:** نفّذ `python -B ../../scripts/build_skill_bundle.py --check plugin` ثم راجع تقرير التكافؤ [parity-report.json](parity-report.json).
- **الإزالة أو التراجع:** احذف النسخة المثبتة لدى العميل أو استرجع آخر نسخة سليمة عبر `--rollback --platform codex`.

- [Canonical Repository Guide](../../README.md) · [Plugins Index](../index.json)
