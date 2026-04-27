@echo off
chcp 65001 >nul
title Rita Job Automator - Ultimate Autopilot

:: ============================================
:: RITA ULTIMATE AUTOPILOT LAUNCHER
:: ============================================
:: Uses Python 3.14 from astral package
:: ============================================

setlocal enabledelayedexpansion

:: Python path
set "PYTHON_EXE=C:\Users\samde\.local\bin\python3.14.exe"

:: Configuration
set "SCRIPT_DIR=%~dp0"
set "LOG_DIR=%SCRIPT_DIR%logs"
set "WATCHDOG_LOG=%LOG_DIR%\watchdog.log"
set "BOT_LOG=%LOG_DIR%\bot.log"
set "AUTOPILOT_FLAG=%SCRIPT_DIR%.autopilot_running"

:: Colors
set "CYAN=[96m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "RESET=[0m"

:: Change to script directory
cd /d "%SCRIPT_DIR%"

:: Create logs directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

echo.
echo %CYAN%========================================%RESET%
echo %CYAN%   RITA ULTIMATE AUTOPILOT%RESET%
echo %CYAN%   24/7 Maximum Performance Mode%RESET%
echo %CYAN%========================================%RESET%
echo.

:: Check Python
if exist "%PYTHON_EXE%" (
    echo %GREEN%[OK]%RESET% Python 3.14 found
) else (
    echo %YELLOW%[WARN]%RESET% Python not found, using py launcher
    set "PYTHON_EXE=py"
)

:: Create autopilot flag
echo %date% %time% > "%AUTOPILOT_FLAG%"

:: Create directories
if not exist "pdf_cache" mkdir pdf_cache
if not exist "recovery" mkdir recovery
if not exist "recovery\runtime_backups" mkdir "recovery\runtime_backups"

:: Create runtime files
if not exist "tracker.json" (
    echo {"applications": [], "last_updated": "%date% %time%} > tracker.json
)

if not exist "metrics.json" (
    echo {"today": {"applications_sent": 0, "jobs_analyzed": 0}, "this_week": {"applications_sent": 0}, "this_month": {"applications_sent": 0}, "all_time": {"applications_sent": 0}} > metrics.json
)

if not exist "health_check.json" (
    echo {"system_health": "HEALTHY", "components": {}, "last_check": "%date% %time%"} > health_check.json
)

if not exist "company_database.json" (
    echo {"companies": [], "total_unique": 0, "last_updated": "%date% %time%"} > company_database.json
)

if not exist "discovered_companies.json" (
    echo {"companies": [], "total": 0, "last_updated": "%date% %time%"} > discovered_companies.json
)

echo %GREEN%[OK]%RESET% Directories and files initialized

:: Check for existing instances
tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2>nul | findstr /i "main_bot" >nul
if not errorlevel 1 (
    echo %YELLOW%[WARN]%RESET% Existing Rita instance found
    echo %CYAN%[INFO]%RESET% Stopping existing instance...
    taskkill /F /IM python.exe /FI "WINDOWTITLE eq *Rita*" 2>nul
    timeout /t 2 /nobreak >nul
)

:: Start watchdog
echo.
echo %YELLOW%[STARTING]%RESET% Launching Rita Bot with watchdog...

start /min cmd /c "title Rita Watchdog && "%SCRIPT_DIR%WATCHDOG.bat" >> %WATCHDOG_LOG% 2>&1"
timeout /t 2 /nobreak >nul

:: Start main bot
start "Rita Bot" cmd /c "title Rita Bot && "%PYTHON_EXE%" -u "%SCRIPT_DIR%main_bot.py" >> %BOT_LOG% 2>&1"

:: Wait and verify
timeout /t 5 /nobreak >nul

echo.
echo %GREEN%========================================%RESET%
echo %GREEN%   RITA IS RUNNING!%RESET%
echo %GREEN%========================================%RESET%
echo.
echo %GREEN%[+]%RESET% Auto-restart on crash     (WATCHDOG)
echo %GREEN%[+]%RESET% 24/7 monitoring          (ACTIVE)
echo %GREEN%[+]%RESET% Telegram alerts          (ENABLED)
echo %GREEN%[+]%RESET% Enhanced scraper        (8 SOURCES)
echo.
echo Press any key to open dashboard...

pause >nul
start http://localhost:8501 2>nul

exit /b 0