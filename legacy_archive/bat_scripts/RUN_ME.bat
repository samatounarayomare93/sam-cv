@echo off
setlocal

echo ==============================================
echo Rita Job Automator - One Click Runner
echo ==============================================
echo.
echo [1/2] Stopping old bot instances...
call "%~dp0STOP_RITA_BOT_LOCAL.bat"
if errorlevel 1 (
    echo WARNING: Stop step returned a non-zero code. Continuing...
)

echo.
echo [2/2] Starting bot...
call "%~dp0START_RITA_BOT_LOCAL.bat"
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo Runner finished. Bot exit code: %EXIT_CODE%
exit /b %EXIT_CODE%
