@echo off
setlocal
powershell -ExecutionPolicy Bypass -File "%~dp0AUTO_BOOTSTRAP.ps1" %*
exit /b %errorlevel%
