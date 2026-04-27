@echo off
setlocal

set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\" set "ROOT=%ROOT:~0,-1%"
set "SITE=%ROOT%\pydeps\Lib\site-packages"
set "ALT_PYTHON=C:\Program Files\AutoClaw\resources\python\python.exe"

echo ==============================================
echo Rita Job Automator - Local Starter
echo ==============================================

if not exist "%ALT_PYTHON%" (
    echo ERROR: AutoClaw Python not found at:
    echo %ALT_PYTHON%
    pause
    exit /b 1
)

if not exist "%SITE%" (
    echo ERROR: Local dependencies not found at:
    echo %SITE%
    echo Install deps first in pydeps.
    pause
    exit /b 1
)

rem Clear inherited Python env vars that can corrupt interpreter startup.
set "PYTHONHOME="
set "PYTHONPATH=%ROOT%;%SITE%"

echo Using Python: %ALT_PYTHON%
echo Using PYTHONPATH: %PYTHONPATH%
echo Starting bot...
echo.

"%ALT_PYTHON%" "%ROOT%\launch_main_bot.py"
set "EXIT_CODE=%ERRORLEVEL%"

echo.
echo Bot exited with code: %EXIT_CODE%
exit /b %EXIT_CODE%
