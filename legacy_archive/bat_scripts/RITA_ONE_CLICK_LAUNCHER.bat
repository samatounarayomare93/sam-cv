@echo off
title RITA JOB AUTOMATOR // PHOENIX REBIRTH
echo ==========================================
echo 🚀 RITA JOB AUTOMATOR: ONE-CLICK LAUNCHER
echo ==========================================
echo.

set PYTHON_EXE=.venv\Scripts\python.exe

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Virtual environment (.venv) not found!
    echo Running emergency repair...
    python -m venv .venv
    .venv\Scripts\python.exe -m pip install -r requirements.txt
)

echo [1/3] Running Preflight Checks...
"%PYTHON_EXE%" preflight_check.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Preflight failed. Check the logs above.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo [2/3] Verifying Database Connection...
"%PYTHON_EXE%" comprehensive_diagnostic_v2.py

echo.
echo [3/3] LAUNCHING MISSION...
echo Press Ctrl+C to stop the bot at any time.
echo.

:loop
"%PYTHON_EXE%" launch_main_bot.py
echo.
echo [WAIT] Mission complete. Sleeping for 2 hours before the next strike...
echo [TIP] Leave this window open for 24/7 autonomous hunting.
timeout /t 7200 /nobreak
goto loop
