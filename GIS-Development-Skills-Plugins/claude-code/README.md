# Claude Code (`claude-code`)

- **Plugin ID:** `ahmadibrahim4geo.gis-development-skills`
- **Version:** `0.3.5` (`01db0e0065535167dc194bc8e646c009c84ffe71`)
- **Phase Status:** `ACTIVE_P09`
- **Manifest:** [plugin/.claude-plugin/plugin.json](plugin/.claude-plugin/plugin.json)
- **Parity Report:** [parity-report.json](parity-report.json)
- **Local ZIP Artifact:** `artifacts/gis-development-skills-claude-code.zip` (`artifacts/gis-development-skills-claude-code.zip.sha256`)
- **Hooks Contract:** Includes opt-in, loop-safe lifecycle hook metadata (`supports_hooks: true`).

## English — Installation, Verification & Uninstall

1. **Verify integrity locally:** `python -B ../../scripts/build_skill_bundle.py --check plugin`
2. **Platform installation:** Add `.claude-plugin/marketplace.json` or install `GIS-Development-Skills-Plugins/claude-code/plugin` via Claude Code (`user`, `project`, or `local` scope) while keeping bundled references intact.
3. **Submission boundary:** Remote/portal uploads remain `PREPARED_FOR_SUBMISSION` / `MANUAL_ACTION_REQUIRED` until manually uploaded or authorized.
4. **Rollback / Uninstall:** Remove the synced copy or run `python -B ../../plugin-system/core/pipeline.py --rollback --platform claude-code`.

## العربية — التثبيت والتحقق والإزالة

- **توافق المنصة:** يدعم بيانات الخطافات الاختيارية الآمنة ضد التكرار (`supports_hooks: true`).
- **التثبيت والمزامنة:** ثبّت من فهرس `.claude-plugin/marketplace.json` أو من المجلد `GIS-Development-Skills-Plugins/claude-code/plugin` عبر Claude Code ضمن نطاق `user` أو `project` أو `local`.
- **التحقق دون اتصال:** نفّذ `python -B ../../scripts/build_skill_bundle.py --check plugin` ثم راجع تقرير التكافؤ [parity-report.json](parity-report.json).
- **الإزالة أو التراجع:** احذف النسخة المثبتة لدى العميل أو استرجع آخر نسخة سليمة عبر `--rollback --platform claude-code`.

- [Canonical Repository Guide](../../README.md) · [Plugins Index](../index.json)
