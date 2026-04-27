@echo off
title PROJECT CHRONOS: TEMPORAL SELF-REPAIR
color 0C
echo ===================================================
echo 🚨 CHRONOS CORE ANOMALY DETECTED
echo 🔧 INITIATING DIVINE REPAIR SEQUENCE...
echo ===================================================
echo.

cd /d "%~dp0\.."

:: 1. Virtual Environment Validation
echo [1/4] Validating Virtual Environment...
if not exist ".venv" (
    echo [!] Environment Corrupted or Missing. Re-integrating...
    python -m venv .venv
    if errorlevel 1 (
        echo [X] FATAL: Python not found in PATH. Repair aborted.
        pause
        exit /b 1
    )
)

:: 2. Forced Dependency Sync
echo [2/4] Syncing System Dependencies...
call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [X] FATAL: Failed to activate virtual environment.
    pause
    exit /b 1
)

python -m pip install --upgrade pip
if exist "requirements.txt" (
    echo [!] Applying requirements.txt...
    pip install -r requirements.txt
) else (
    echo [!] requirements.txt missing. Reconstructive installation initiated...
    pip install aiohttp google-generativeai python-telegram-bot python-dotenv tenacity requests beautifulsoup4 fpdf
)

:: 3. Integrity Verification
echo [3/4] Verifying File Integrity...
if not exist ".env" (
    echo [!] ALERT: .env Vault missing. Re-creation required for operation.
)

:: 4. Relaunch Sequence
echo [4/4] System Sync Complete. Re-engaging Core Modules...
echo.
echo ===================================================
echo ✅ REPAIR SEQUENCE CONCLUDED. SYSTEMS REALIGNED.
echo ===================================================
timeout /t 5
exit
