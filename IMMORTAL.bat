@echo off
title Project Chronos - IMMORTAL MODE
chcp 65001 >nul
color 0A

:START
echo.
echo ================================================================
echo    PROJECT CHRONOS - IMMORTAL WATCHDOG v3.0
echo    Auto-restarts on crash. Runs FOREVER.
echo    Press Ctrl+C to stop permanently.
echo ================================================================
echo.

REM Use embedded Python runtime if available, else system Python
if exist ".sovereign_runtime\python.exe" (
    .sovereign_runtime\python.exe immortal.py
) else (
    python immortal.py
)

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [IMMORTAL] Bot crashed with error code %ERRORLEVEL%. Restarting in 10 seconds...
    echo    Press Ctrl+C to stop permanently.
    echo.
    timeout /t 10 /nobreak >nul
    goto START
)

echo.
echo [IMMORTAL] Bot exited normally. Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto START
