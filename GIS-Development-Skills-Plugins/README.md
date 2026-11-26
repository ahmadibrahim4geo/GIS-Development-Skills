# GIS Development Skills — Generated Plugin Packages / حزم الإضافات المولدة

- **Version:** `0.3.5` (`7c0eb7da684c2670d5e020cbcc6c3b9f6de751bd`)
- **Canonical Source:** [Repository README](../README.md) · [AGENTS Policy](../AGENTS.md) · [Lifecycle Architecture](../plugin-system/README.md)
- **Important Rule:** Do not edit files in this folder by hand. Regenerate from canonical sources via `Update-All-Plugins.ps1` (or `python -B plugin-system/core/pipeline.py`).

| Platform | State | Phase Status | Notes |
|---|---|---|---|
| `portable` | `BUILT` | `ACTIVE_P02` | Cleanly staged, validated, packaged, and atomically updated. |
| `codex` | `BUILT` | `ACTIVE_P09` | Cleanly staged, validated, packaged, and atomically updated. |
| `chatgpt` | `BUILT` | `ACTIVE_P09` | Cleanly staged, validated, packaged, and atomically updated. |
| `claude-code` | `BUILT` | `ACTIVE_P09` | Cleanly staged, validated, packaged, and atomically updated. |
| `claude-ai` | `BUILT` | `ACTIVE_P09` | Cleanly staged, validated, packaged, and atomically updated. |
| `antigravity` | `BUILT` | `ACTIVE_P09` | Cleanly staged, validated, packaged, and atomically updated. |
| `cursor` | `BUILT` | `ACTIVE_P09` | Cleanly staged, validated, packaged, and atomically updated. |

## العربية / Quick Arabic Guide

- هذا المجلد يُبنى آليًا من مستودع المصدر الواحد (`skills/` و`references/` و`schemas/`).
- تدعم المنظومة حزمة **`portable-agent-plugin`** (من `P02`) إلى جانب المحولات الست المفعلة للعملاء (`codex`, `chatgpt`, `claude-code`, `claude-ai`, `antigravity`, `cursor`) في `P09`.
- أرشيفات `.zip` الكبيرة تُبنى محليًا داخل `*/artifacts/` وهي مستبعدة من التتبع في Git للحفاظ على خفة المستودع.
