# GIS Development Skills — Generated Plugin Packages / حزم الإضافات المولدة

- **Version:** `0.3.5` (`01db0e0065535167dc194bc8e646c009c84ffe71`)
- **Canonical Source:** [Repository README](../README.md) · [AGENTS Policy](../AGENTS.md) · [Lifecycle Architecture](../plugin-system/README.md)
- **Important Rule:** Do not edit files in this folder by hand. Regenerate from canonical sources via `Update-All-Plugins.ps1` (or `python -B plugin-system/core/pipeline.py`).

| Platform | State | Phase Status | Notes |
|---|---|---|---|
| `portable` | `UP_TO_DATE` | `ACTIVE_P02` | Source digest and built manifest match; skipped rebuild. |
| `codex` | `UP_TO_DATE` | `ACTIVE_P09` | Source digest and built manifest match; skipped rebuild. |
| `chatgpt` | `UP_TO_DATE` | `ACTIVE_P09` | Source digest and built manifest match; skipped rebuild. |
| `claude-code` | `UP_TO_DATE` | `ACTIVE_P09` | Source digest and built manifest match; skipped rebuild. |
| `claude-ai` | `UP_TO_DATE` | `ACTIVE_P09` | Source digest and built manifest match; skipped rebuild. |
| `antigravity` | `UP_TO_DATE` | `ACTIVE_P09` | Source digest and built manifest match; skipped rebuild. |
| `cursor` | `UP_TO_DATE` | `ACTIVE_P09` | Source digest and built manifest match; skipped rebuild. |

## العربية / Quick Arabic Guide

- هذا المجلد يُبنى آليًا من مستودع المصدر الواحد (`skills/` و`references/` و`schemas/`).
- تدعم المنظومة حزمة **`portable-agent-plugin`** (من `P02`) إلى جانب المحولات الست المفعلة للعملاء (`codex`, `chatgpt`, `claude-code`, `claude-ai`, `antigravity`, `cursor`) في `P09`.
- أرشيفات `.zip` الكبيرة تُبنى محليًا داخل `*/artifacts/` وهي مستبعدة من التتبع في Git للحفاظ على خفة المستودع.
