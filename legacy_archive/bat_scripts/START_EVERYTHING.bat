@echo off
chcp 65001 >nul
title Rita - Starting Everything...

:: ============================================
:: RITA FULL AUTOPILOT - ONE CLICK
:: ============================================
:: This will:
:: 1. Start the bot
:: 2. Install auto-start
:: 3. Open dashboard
:: ============================================

cd /d "%~dp0"

echo.
echo ================================================
echo    RITA FULL AUTOPILOT
echo ================================================
echo.
echo Starting everything for you...

:: Start the main bot
echo [1/3] Starting Rita Bot...
start "Rita Bot" cmd /c "python main_bot.py"
timeout /t 2 /nobreak >nul

:: Install auto-start
echo [2/3] Installing auto-start...
call INSTALL_AUTO_START.bat

:: Open dashboard
echo [3/3] Opening dashboard...
start http://localhost:8501

echo.
echo ================================================
echo    ALL DONE!
echo ================================================
echo.
echo Rita is now running!
echo Auto-start has been installed.
echo Dashboard should open in your browser.
echo.
echo Press any key to close this window...
pause >nul
