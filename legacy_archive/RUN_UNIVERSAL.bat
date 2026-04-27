@echo off
REM RITA Job Automator - Universal Launcher with Auto-Recovery
REM Handles corrupted Python registry by trying multiple launch methods

echo ============================================================
echo RITA JOB AUTOMATOR - MAXIMUM POWER v2
echo ============================================================
echo.

REM Method 1: Try direct Python path
echo [1/4] Testing Python at C:\Program Files\Python311\python.exe...
"C:\Program Files\Python311\python.exe" -c "import encodings" 2>nul
if not errorlevel 1 (
    echo [OK] Python works! Launching RITA...
    "C:\Program Files\Python311\python.exe" main_bot.py
    goto :end
)

REM Method 2: Try venv Python
echo [2/4] Testing venv...
if exist "venv\Scripts\python.exe" (
    venv\Scripts\python.exe -c "import encodings" 2>nul
    if not errorlevel 1 (
        echo [OK] Venv Python works! Launching RITA...
        venv\Scripts\python.exe main_bot.py
        goto :end
    )
)

REM Method 3: Create fresh venv
echo [3/4] Creating new virtual environment...
"C:\Program Files\Python311\python.exe" -m venv rita_venv 2>nul
if exist "rita_venv\Scripts\python.exe" (
    rita_venv\Scripts\python.exe -c "import encodings" 2>nul
    if not errorlevel 1 (
        echo [OK] Fresh venv works! Launching RITA...
        rita_venv\Scripts\python.exe main_bot.py
        goto :end
    )
)

REM Method 4: Show manual fix instructions
echo [4/4] All automatic methods failed.
echo.
echo ============================================================
echo MANUAL FIX REQUIRED
echo ============================================================
echo Your Python registry is corrupted. Run this in PowerShell
echo as Administrator to fix it:
echo.
echo   cd c:\Users\samde\Rita_Job_Automator
echo   .\FIX_PYTHON_REGISTRY_V2.ps1
echo.
echo Then try again with RUN_FIXED.bat
echo ============================================================

:end
echo.
pause