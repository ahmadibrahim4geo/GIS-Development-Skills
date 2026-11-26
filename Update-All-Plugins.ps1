<#
.SYNOPSIS
  Unified GIS Development Skills multi-platform plugin builder, validator, and local sync orchestrator.
.DESCRIPTION
  Wraps plugin-system/core/pipeline.py across PowerShell 5.1+ and PowerShell 7+ while preserving
  exit codes (0, 2, 3, 4, 5), UTF-8 Arabic paths/spaces, and public/private isolation.
#>
[CmdletBinding()]
param(
    [switch]$CheckOnly,
    [switch]$BuildOnly,
    [switch]$Status,
    [switch]$Force,
    [string[]]$Platform = @(),
    [switch]$Rollback,
    [string]$Version = '',
    [switch]$PrepareRelease,
    [switch]$Publish,
    [switch]$Json,
    [string]$ReportLabel = 'PLUGIN_LIFECYCLE'
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$env:PYTHONUTF8 = '1'
$env:PYTHONIOENCODING = 'utf-8'

$RepoRoot = $PSScriptRoot
$PipelineScript = Join-Path $RepoRoot 'plugin-system\core\pipeline.py'

if (-not (Test-Path -LiteralPath $PipelineScript)) {
    Write-Error "Missing pipeline orchestrator: $PipelineScript"
    exit 5
}

$PythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $PythonCmd) { $PythonCmd = Get-Command python3 -ErrorAction SilentlyContinue }
if (-not $PythonCmd) { $PythonCmd = Get-Command py -ErrorAction SilentlyContinue }
if (-not $PythonCmd) {
    Write-Error "Python interpreter not found on PATH."
    exit 5
}

$PyArgs = @('-B', $PipelineScript, '--repo-root', $RepoRoot, '--report-label', $ReportLabel)
if ($CheckOnly) { $PyArgs += '--check-only' }
elseif ($BuildOnly) { $PyArgs += '--build-only' }
elseif ($Status) { $PyArgs += '--status' }
elseif ($Rollback) { $PyArgs += '--rollback' }
elseif ($PrepareRelease) { $PyArgs += '--prepare-release' }
elseif ($Publish) { $PyArgs += '--publish' }

if ($Force) { $PyArgs += '--force' }
if ($Version) { $PyArgs += @('--version', $Version) }
foreach ($p in $Platform) {
    if ($p) { $PyArgs += @('--platform', $p) }
}
if ($Json) { $PyArgs += '--json' }

& $PythonCmd.Source @PyArgs
$code = $LASTEXITCODE
exit $code
