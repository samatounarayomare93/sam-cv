@echo off
setlocal

echo ==============================================
echo Rita Job Automator - Maximum Autopilot
echo ==============================================

rem Protect launcher from globally broken Python environment variables.
set "PYTHONHOME="
set "PYTHONPATH="

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0MAXIMUM_AUTOPILOT.ps1" -MaxRestarts 0 -RestartDelaySeconds 8 -StopExisting
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo Autopilot finished with exit code: %EXIT_CODE%
exit /b %EXIT_CODE%
