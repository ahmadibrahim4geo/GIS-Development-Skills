@echo off
setlocal
rem Invoke PowerShell script cleanly without forcibly bypassing host ExecutionPolicy.
powershell.exe -NoProfile -File "%~dp0Update-All-Plugins.ps1" %*
set "EXIT_CODE=%ERRORLEVEL%"
exit /b %EXIT_CODE%
