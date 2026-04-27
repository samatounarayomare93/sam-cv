@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo =============================================
echo    RITA JOB AUTOMATOR
echo =============================================
echo.

set PY=C:\Users\samde\.local\bin\python3.14.exe

:: Remove any old lock file
if exist ".main_bot.lock" del ".main_bot.lock"

:: Initialize files
if not exist "tracker.json" (
    echo {"applications": [], "last_updated": ""} > tracker.json
)

if not exist "metrics.json" (
    echo {"today": {"applications_sent": 0}} > metrics.json
)

if not exist "health_check.json" (
    echo {"system_health": "HEALTHY"} > health_check.json
)

echo [OK] Files initialized
echo.
echo Starting Rita Bot...
echo.
echo Press Ctrl+C to stop
echo.

:: Run console mode first to test
start "Rita Console" cmd /k "cd /d "%~dp0" && "%PY%" console_mode.py"

:: Then start main bot
timeout /t 3 /nobreak >nul
start "Rita Bot" cmd /k "cd /d "%~dp0" && "%PY%" main_bot.py"

echo Rita Bot windows should be opening now!
pause
