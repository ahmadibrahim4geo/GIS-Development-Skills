<#
.SYNOPSIS
  Opt-in installation of Git pre-commit check hook calling plugin-system validation.
.NOTES
  Never run implicitly during build or package steps. Respects user Git configuration.
#>
[CmdletBinding()]
param(
    [switch]$Force,
    [switch]$IncludePrePush
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$HookDir = Join-Path $RepoRoot '.git\hooks'
$PreCommitPath = Join-Path $HookDir 'pre-commit'
$PrePushPath = Join-Path $HookDir 'pre-push'

if (-not (Test-Path $HookDir)) {
    Write-Error "Git hooks directory not found at $HookDir"
    exit 5
}

if ((Test-Path $PreCommitPath) -and -not $Force) {
    Write-Error "Existing pre-commit hook present at $PreCommitPath. Pass -Force to overwrite."
    exit 5
}

$HookScript = @'
#!/bin/sh
python -B plugin-system/core/pipeline.py --check-only --no-report
status=$?
if [ "$status" -ne 0 ]; then
  echo "Plugin lifecycle check failed (exit $status). Run Update-All-Plugins.ps1 -BuildOnly."
  exit "$status"
fi
'@

[System.IO.File]::WriteAllText($PreCommitPath, ($HookScript -replace "`r`n", "`n"), (New-Object System.Text.UTF8Encoding($false)))
Write-Output "Opt-in Git pre-commit hook written to $PreCommitPath"

if ($IncludePrePush) {
    if ((Test-Path $PrePushPath) -and -not $Force) {
        Write-Error "Existing pre-push hook present at $PrePushPath. Pass -Force to overwrite."
        exit 5
    }
    [System.IO.File]::WriteAllText($PrePushPath, ($HookScript -replace "`r`n", "`n"), (New-Object System.Text.UTF8Encoding($false)))
    Write-Output "Opt-in Git pre-push hook written to $PrePushPath"
}
exit 0
