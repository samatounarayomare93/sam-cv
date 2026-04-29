@echo off
echo ╔══════════════════════════════════════════════════╗
echo ║  PROJECT CHRONOS - QUICK START                   ║
echo ╚══════════════════════════════════════════════════╝
echo.
echo [1/3] Checking system...
.\.sovereign_runtime\python.exe --version
if errorlevel 1 (
    echo ❌ Python runtime not found!
    pause
    exit /b 1
)
echo ✅ Python OK
echo.

echo [2/3] Running quick diagnostic...
.\.sovereign_runtime\python.exe -c "import os; print('✅ Environment OK' if os.path.exists('.env') else '❌ .env missing')"
echo.

echo [3/3] Starting bot...
echo.
echo ╔══════════════════════════════════════════════════╗
echo ║  Bot is starting...                              ║
echo ║  • Watch console for job discoveries             ║
echo ║  • Check Telegram @samcvbot for notifications    ║
echo ║  • Press Ctrl+C to stop                          ║
echo ╚══════════════════════════════════════════════════╝
echo.

.\.sovereign_runtime\python.exe run.py

pause
