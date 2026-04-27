@echo off
setlocal
echo.
echo    🦾 🛡️ PROJECT CHRONOS: ABSOLUTE REPAIR 3.0 🛰️ 🦾
echo    ===============================================
echo.
echo [1/5] 🛡️ Neutralizing corrupted artifacts...
if exist venv rmdir /s /q venv
if exist Lib rmdir /s /q Lib
if exist Include rmdir /s /q Include
if exist Scripts rmdir /s /q Scripts
echo.
echo [2/5] 🛰️ Building Fresh Virtual Environment...
set "ALT_PYTHON=C:\Program Files\AutoClaw\resources\python\python.exe"

if exist "%ALT_PYTHON%" (
    echo 🧬 Healthy Interpreter Detected in AutoClaw. Hijacking for Project Chronos...
    "%ALT_PYTHON%" -m venv venv
) else (
    python -m venv venv
)

if errorlevel 1 (
    echo.
    echo 💥 ERROR: No working Python engine found.
    echo Please ensure Python 3.11 is installed and "Add to PATH" is checked.
    pause
    exit /b
)
echo.
echo [3/5] 💎 Activating Chronos Core...
call venv\Scripts\activate
echo.
echo [4/5] 🚀 Loading Mission Critical Requirements...
pip install --upgrade pip
pip install -r requirements.txt
echo.
echo [5/5] 🛰️ CONDUCTING FINAL VERIFICATION STRIKE...
python verification_test.py
if errorlevel 1 (
    echo.
    echo ❌ VERIFICATION FAILED.
    echo Please resolve the errors above before launching the engine.
    pause
    exit /b
)

echo.
echo 🔥 LAUNCHING PROJECT CHRONOS FINAL STRIKE...
echo.
echo 🛰️ Mission Pulse initiating WITH RECOVERED TOKEN...
python main_bot.py
echo.
echo ✅ REPAIR COMPLETE. Check Telegram for Mission Yields.
pause
