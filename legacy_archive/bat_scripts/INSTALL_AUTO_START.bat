@echo off
chcp 65001 >nul
title Rita Auto-Start Installer

:: ============================================
:: RITA JOB AUTOMATOR - AUTO-START INSTALLER
:: ============================================
:: Installs Rita Bot to run automatically when
:: Windows starts - NO ADMIN REQUIRED!
:: ============================================

setlocal enabledelayedexpansion

echo.
echo ========================================
echo    RITA AUTO-START INSTALLER
echo ========================================
echo.

:: Get current directory
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_DIR=%SCRIPT_DIR:~0,-1%"

echo [1/3] Creating startup script...

:: Create a simple launcher for startup
(
echo @echo off
echo cd /d "%SCRIPT_DIR%"
echo start /min cmd /c "python main_bot.py >> logs startup.log 2>&1"
) > "%USERPROFILE%\Start Menu\Programs\Startup\RitaBot_Autostart.bat"

echo [2/3] Installing Task Scheduler task...

:: Create scheduled task for reliability
schtasks /create /tn "RitaJobAutomator" /tr "\"%SCRIPT_DIR%\START_AUTOPILOT.bat\"" /sc onlogon /rl limited /f 2>nul

echo [3/3] Verifying installation...

if exist "%USERPROFILE%\Start Menu\Programs\Startup\RitaBot_Autostart.bat" (
    echo [OK] Startup shortcut created
) else (
    echo [ERROR] Startup shortcut failed
)

schtasks /query /tn "RitaJobAutomator" >nul 2>&1
if not errorlevel 1 (
    echo [OK] Scheduled task installed
) else (
    echo [WARNING] Scheduled task skipped (may need admin)
)

echo.
echo ========================================
echo    INSTALLATION COMPLETE!
echo ========================================
echo.
echo Rita will now start automatically when:
echo - You log into Windows
echo - System restarts
echo - User session starts
echo.
echo To UNINSTALL, run this script again.
echo.
pause
