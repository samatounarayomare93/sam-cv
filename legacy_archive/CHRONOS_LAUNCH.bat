@echo off
title PROJECT CHRONOS: ALPHA & OMEGA
color 0B
echo ===================================================
echo 👑 PROJECT CHRONOS - ROYAL DIVINE SUPREMACY
echo ===================================================
echo.
echo [1] Launching Alpha Orchestrator and Surveillance...
echo.

cd /d "%~dp0"
if not exist ".venv" (
    echo [!] Virtual Environment Missing. Triggering Auto-Repair...
    call "scripts\CHRONOS_REPAIR.bat"
)
call ".venv\Scripts\activate.bat"

:: Start Orchestrator silently in separate window
start "CHRONOS ORCHESTRATOR" cmd /c "python core\main_bot.py"

:: Start Healer
start "CHRONOS HEALER" cmd /c "python core\self_healer.py"

echo ✅ Core Engaged.
echo.
echo [2] Igniting Command Center UI...
echo.

cd ui
start http://localhost:3000
npm run dev

goto eof
