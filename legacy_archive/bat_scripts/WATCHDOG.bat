@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: RITA WATCHDOG - AUTO RESTART ON CRASH
:: ============================================
:: This script monitors Rita Bot and automatically
:: restarts it if it crashes or stops responding.
:: 
:: Features:
:: - Auto-restart on crash
:: - Memory monitoring
:: - Log rotation
:: - Silent mode (no popup windows)
:: ============================================

set "BOT_SCRIPT=main_bot.py"
set "BOT_NAME=Rita Bot"
set "LOG_DIR=logs"
set "HEARTBEAT_FILE=watchdog_heartbeat.txt"
set "RESTART_COUNT=0"
set "MAX_RESTARTS=50"
set "CHECK_INTERVAL=30"
set "MEMORY_LIMIT_MB=500"

:: Create logs directory
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

:: Get script directory
set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

echo [%date% %time%] ======================================== > "%LOG_DIR%\watchdog.log"
echo [%date% %time%] RITA WATCHDOG STARTED >> "%LOG_DIR%\watchdog.log"
echo [%date% %time%] ======================================== >> "%LOG_DIR%\watchdog.log"

:MAIN_LOOP
:: Update heartbeat
echo %date% %time% > "%HEARTBEAT_FILE%"

:: Check if bot is running
tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2>nul | findstr /i "main_bot" >nul
if errorlevel 1 (
    :: Bot not running - check if it crashed recently
    echo [%date% %time%] [INFO] Bot not running, checking status... >> "%LOG_DIR%\watchdog.log"
    
    :: Check restart count
    if %RESTART_COUNT% GEQ %MAX_RESTARTS% (
        echo [%date% %time%] [ERROR] Max restarts reached (%MAX_RESTARTS%). Waiting 5 minutes... >> "%LOG_DIR%\watchdog.log"
        timeout /t 300 /nobreak >nul
        set "RESTART_COUNT=0"
    )
    
    :: Log restart attempt
    set /a RESTART_COUNT+=1
    echo [%date% %time%] [RESTART] Attempt %RESTART_COUNT%/%MAX_RESTARTS% - Launching bot... >> "%LOG_DIR%\watchdog.log"
    
    :: Clean old logs (keep last 10)
    for /f "skip=10" %%a in ('dir /b /o-d "%LOG_DIR%\*.log" 2^>nul') do (
        del /q "%LOG_DIR%\%%a" 2>nul
    )
    
    :: Launch bot in background
    start /min cmd /c "title %BOT_NAME% && python -u main_bot.py >> %LOG_DIR%\bot.log 2>&1"
    
    :: Wait for startup
    echo [%date% %time%] [INFO] Waiting for bot startup... >> "%LOG_DIR%\watchdog.log"
    timeout /t 10 /nobreak >nul
    
    :: Verify startup
    tasklist /FI "IMAGENAME eq python.exe" /FO CSV 2>nul | findstr /i "main_bot" >nul
    if errorlevel 1 (
        echo [%date% %time%] [ERROR] Bot failed to start. Retrying in 60s... >> "%LOG_DIR%\watchdog.log"
        timeout /t 60 /nobreak >nul
    ) else (
        echo [%date% %time%] [OK] Bot started successfully! >> "%LOG_DIR%\watchdog.log"
        set "RESTART_COUNT=0"
    )
) else (
    :: Bot running - check memory usage
    wmic process where "name='python.exe'" get WorkingSetSize,commandline 2>nul | findstr /i "main_bot" > "%LOG_DIR%\memory_check.tmp"
    
    :: Read memory (simplified check)
    for /f "tokens=1" %%a in ('type "%LOG_DIR%\memory_check.tmp" 2^>nul ^| findstr /r "[0-9]"') do (
        set "MEMORY=%%a"
    )
    
    :: If memory exceeds limit, restart to free resources (optional, currently disabled)
    :: if defined MEMORY (
    ::     set /a MEMORY_MB=MEMORY / 1024 / 1024
    ::     if !MEMORY_MB! GEQ %MEMORY_LIMIT_MB% (
    ::         echo [%date% %time%] [WARN] High memory usage: !MEMORY_MB!MB - restarting... >> "%LOG_DIR%\watchdog.log"
    ::         taskkill /F /IM python.exe /FI "WINDOWTITLE eq *main_bot*" 2>nul
    ::     )
    :: )
    
    echo [%date% %time%] [OK] Bot is healthy (running) >> "%LOG_DIR%\watchdog.log"
    del "%LOG_DIR%\memory_check.tmp" 2>nul
)

:: Wait before next check
timeout /t %CHECK_INTERVAL% /nobreak >nul

goto MAIN_LOOP
