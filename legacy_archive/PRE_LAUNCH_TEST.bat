@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0PRE_LAUNCH_TEST.ps1"
endlocal
