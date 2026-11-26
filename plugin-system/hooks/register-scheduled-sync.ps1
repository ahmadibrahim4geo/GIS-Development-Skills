<#
.SYNOPSIS
  Opt-in Windows Scheduled Task registration for periodic read-only plugin digest checks.
.NOTES
  Never run automatically during package builds. Default action performs check-only parity without network publishing.
#>
[CmdletBinding()]
param(
    [string]$TaskName = 'GIS-Development-Skills-Plugin-Check',
    [switch]$Unregister,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$RepoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')

if ($Unregister) {
    if ($DryRun) {
        Write-Output "[DryRun] Would unregister scheduled task: $TaskName"
        exit 0
    }
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false -ErrorAction SilentlyContinue
    Write-Output "Unregistered scheduled task (if present): $TaskName"
    exit 0
}

$CmdArgs = "-NoProfile -File `"$RepoRoot\Update-All-Plugins.ps1`" -CheckOnly -Json"
if ($DryRun) {
    Write-Output "[DryRun] Scheduled Task '$TaskName' -> powershell.exe $CmdArgs"
    exit 0
}

$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $CmdArgs -WorkingDirectory $RepoRoot
$Trigger = New-ScheduledTaskTrigger -Daily -At 09:00AM
Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Description 'Opt-in read-only GIS Development Skills plugin parity check' -Force | Out-Null
Write-Output "Registered opt-in daily read-only check task '$TaskName'."
exit 0
