@echo off
REM RITA Job Automator - Embedded Python Launcher
REM Uses python311.zip (embedded standard library) to bypass broken installation

echo ============================================================
echo RITA JOB AUTOMATOR - MAXIMUM POWER v2
echo ============================================================
echo.

REM Check for embedded Python zip
if not exist "python311.zip" (
    echo [ERROR] python311.zip not found!
    echo [FIX] Download Python embedded from python.org
    pause
    exit /b 1
)

echo [OK] Found embedded Python: python311.zip
echo [START] Launching RITA with embedded standard library...
echo ============================================================

REM Set PYTHONPATH to include the embedded zip and project
set PYTHONPATH=.;python311.zip;python311.zip\Lib;python311.zip\DLLs
set PYTHONHOME=%cd%

"C:\Program Files\Python311\python.exe" main_bot.py

echo.
pause