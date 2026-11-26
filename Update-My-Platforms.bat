@echo off
setlocal
rem Invoke owner-private sync manager cleanly without forcibly bypassing host ExecutionPolicy.
powershell.exe -NoProfile -File "%~dp0Update-My-Platforms.ps1" %*
set "EXIT_CODE=%ERRORLEVEL%"
exit /b %EXIT_CODE%
