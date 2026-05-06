@echo off
title ?? Project Chronos - IMMORTAL MODE
chcp 65001 >nul
color 0A

:START
echo.
echo ---------------------------------------------------------------
echo    ?? PROJECT CHRONOS - IMMORTAL MODE
echo    Restarts automatically if crash occurs
echo ---------------------------------------------------------------
echo.

python immortal.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ?? Bot crashed or exited with error. Restarting in 10 seconds...
    echo    Press Ctrl+C to stop permanently.
    echo.
    timeout /t 10 /nobreak >nul
    goto START
)

echo.
echo ?? Bot exited normally. Restarting in 5 seconds...
timeout /t 5 /nobreak >nul
goto START
