<#
.SYNOPSIS
  Owner-private local synchronization configuration & status manager (strictly outside Git).
.DESCRIPTION
  Manages %LOCALAPPDATA%\GIS-Development-Skills\PluginSync\owner-config.json without writing credentials
  into the repository.
#>
[CmdletBinding()]
param(
    [switch]$Configure,
    [switch]$Status,
    [switch]$CheckOnly,
    [switch]$Json,
    [string]$OwnerConfigPath = ''
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

$RepoRoot = $PSScriptRoot
$DefaultOwnerPath = if ($env:LOCALAPPDATA) {
    Join-Path $env:LOCALAPPDATA 'GIS-Development-Skills\PluginSync\owner-config.json'
} else {
    Join-Path $HOME '.config\gis-development-skills\owner-config.json'
}

$ResolvedOwnerPath = if ($OwnerConfigPath) { $OwnerConfigPath } elseif ($env:GIS_SKILLS_OWNER_CONFIG) { $env:GIS_SKILLS_OWNER_CONFIG } else { $DefaultOwnerPath }
$ExamplePath = Join-Path $RepoRoot 'plugin-system\config\owner-config.example.json'

if ($Configure) {
    $parentDir = Split-Path -Parent $ResolvedOwnerPath
    if (-not (Test-Path -LiteralPath $parentDir)) {
        New-Item -ItemType Directory -Path $parentDir -Force | Out-Null
    }
    if (-not (Test-Path -LiteralPath $ResolvedOwnerPath)) {
        Copy-Item -LiteralPath $ExamplePath -Destination $ResolvedOwnerPath
        Write-Output "Initialized external owner-config template at $ResolvedOwnerPath (outside Git)."
    } else {
        Write-Output "Existing external owner-config preserved at $ResolvedOwnerPath."
    }
    exit 0
}

$PipelineScript = Join-Path $RepoRoot 'plugin-system\core\pipeline.py'
$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) { $PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $PythonCmd) { Write-Error "Python interpreter not found on PATH."; exit 5 }

$PyArgs = @('-B', $PipelineScript, '--repo-root', $RepoRoot, '--owner-config', $ResolvedOwnerPath)
if ($CheckOnly) { $PyArgs += '--check-only' }
else { $PyArgs += '--status' }
if ($Json) { $PyArgs += '--json' }

& $PythonCmd.Source @PyArgs
exit $LASTEXITCODE
