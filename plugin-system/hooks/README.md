# Developer Git & Agent Hooks (`plugin-system/hooks/`)

These hooks are **strictly opt-in** for contributors who want automatic pre-commit/pre-push plugin checks without affecting end-user bundles.

## Loop-Prevention Guarantee (`PL-T16`)

- Generated outputs inside `GIS-Development-Skills-Plugins/` and `reports/plugin-lifecycle/` are excluded from canonical source digest computation (`source-map.json`).
- Therefore a follow-up hook invocation after a completed build observes `UP_TO_DATE` and exits immediately with zero infinite rebuild loops.

## Optional Installation (Windows PowerShell)

```powershell
powershell -NoProfile -File .\plugin-system\hooks\install-git-hooks.ps1
powershell -NoProfile -File .\plugin-system\hooks\install-git-hooks.ps1 -IncludePrePush -Force
powershell -NoProfile -File .\plugin-system\hooks\register-scheduled-sync.ps1 -DryRun
```

- Agent lifecycle hook example (opt-in, loop-safe): [`agent-hooks.example.json`](agent-hooks.example.json)
- Scheduled check helper (opt-in, read-only `-CheckOnly`): [`register-scheduled-sync.ps1`](register-scheduled-sync.ps1)
