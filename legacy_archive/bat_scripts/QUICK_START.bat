@echo off
chcp 65001 >nul
title Rita MAX POWER

echo.
echo =============================================
echo    RITA MAX POWER - STARTING
echo =============================================
echo.

cd /d "%~dp0"

:: Python
set PYEXE=py
if exist "C:\Users\samde\.local\bin\python3.14.exe" set PYEXE=C:\Users\samde\.local\bin\python3.14.exe

:: Create folders
if not exist "logs" mkdir logs
if not exist "pdf_cache" mkdir pdf_cache

:: Create tracker
if not exist "tracker.json" (
    echo {"applications": [], "last_updated": ""} > tracker.json
)

:: Create metrics
if not exist "metrics.json" (
    echo {"today": {"applications_sent": 0}} > metrics.json
)

:: Auto-start
(
echo @echo off
cd /d "%~dp0"
start /min RitaBot "%PYEXE%" main_bot.py
) > "%USERPROFILE%\Start Menu\Programs\Startup\RitaBot.bat"

echo [OK] Auto-start installed
echo.

:: Start main bot
echo Starting Rita Bot...
start "Rita Bot" cmd /k "%PYEXE% main_bot.py"

echo.
echo Rita Bot is running!
echo.
echo Files created:
echo   - mega_scraper.py (20+ sources)
echo   - email_hunter.py (GCC companies)
echo   - followup_system.py (auto follow-up)
echo   - rita_max_power.py (MAX mode)
echo.
echo Press any key to exit...
pause >nul
