@echo off
chcp 65001 >nul
cls

echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🚀 PROJECT CHRONOS - QUICK START
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo.

:MENU
echo ┌───────────────────────────────────────────────────────────────────────────┐
echo │                                                                           │
echo │  Choose an option:                                                        │
echo │                                                                           │
echo │  [1] ✅ Check System Health                                               │
echo │  [2] 📧 Test Email Providers                                              │
echo │  [3] 🚀 Start Bot (Normal Mode)                                           │
echo │  [4] ♾️  Start Bot (Immortal Mode - Recommended)                          │
echo │  [5] 📊 View Logs                                                         │
echo │  [6] 🔧 Run Diagnostics                                                   │
echo │  [7] 🌐 Deploy to Cloud (Render.com)                                      │
echo │  [8] 📚 Open Documentation                                                │
echo │  [9] ❌ Exit                                                               │
echo │                                                                           │
echo └───────────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="Enter your choice (1-9): "

if "%choice%"=="1" goto HEALTH_CHECK
if "%choice%"=="2" goto EMAIL_TEST
if "%choice%"=="3" goto START_NORMAL
if "%choice%"=="4" goto START_IMMORTAL
if "%choice%"=="5" goto VIEW_LOGS
if "%choice%"=="6" goto DIAGNOSTICS
if "%choice%"=="7" goto DEPLOY
if "%choice%"=="8" goto DOCS
if "%choice%"=="9" goto EXIT

echo.
echo ❌ Invalid choice! Please enter a number between 1 and 9.
echo.
timeout /t 2 >nul
cls
goto MENU

:HEALTH_CHECK
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    ✅ CHECKING SYSTEM HEALTH...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
python enhanced_health_check.py
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
cls
goto MENU

:EMAIL_TEST
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    📧 TESTING EMAIL PROVIDERS...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
python email_provider_health.py
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
cls
goto MENU

:START_NORMAL
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🚀 STARTING BOT (NORMAL MODE)...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo Press Ctrl+C to stop the bot
echo.
python run.py
pause
cls
goto MENU

:START_IMMORTAL
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    ♾️  STARTING BOT (IMMORTAL MODE)...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo ⚠️  IMMORTAL MODE: Bot will auto-restart on any crash!
echo Press Ctrl+C to stop the bot
echo.
python immortal.py
pause
cls
goto MENU

:VIEW_LOGS
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    📊 VIEWING LOGS...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
if exist logs\orchestrator.log (
    type logs\orchestrator.log | more
) else (
    echo ❌ No logs found! Start the bot first.
)
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
cls
goto MENU

:DIAGNOSTICS
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🔧 RUNNING DIAGNOSTICS...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
python diagnostic.py
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
cls
goto MENU

:DEPLOY
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    🌐 DEPLOY TO CLOUD (RENDER.COM)
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo Step 1: Push code to GitHub
echo ────────────────────────────────────────────────────────────────────────────
git add .
git commit -m "Ready for deployment"
git push
echo.
echo Step 2: Open Render.com
echo ────────────────────────────────────────────────────────────────────────────
start https://render.com
echo.
echo Step 3: Follow these instructions:
echo ────────────────────────────────────────────────────────────────────────────
echo 1. Sign in with GitHub
echo 2. Click "New +" → "Web Service"
echo 3. Select repository: Sam_Job_Automator
echo 4. Fill in:
echo    - Name: sam-cv-bot
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: python run.py
echo 5. Add Environment Variables from .env file
echo 6. Click "Create Web Service"
echo.
echo Step 4: Opening .env file for reference...
echo ────────────────────────────────────────────────────────────────────────────
notepad .env
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
pause
cls
goto MENU

:DOCS
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    📚 OPENING DOCUMENTATION...
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo Choose documentation to open:
echo.
echo [1] START_HERE_README.md (Quick Start)
echo [2] COMPREHENSIVE_IMPROVEMENTS.md (All Improvements)
echo [3] دليل_البدء_السريع_ULTIMATE.md (Arabic Quick Start)
echo [4] الملخص_النهائي_ULTIMATE.md (Arabic Summary)
echo [5] WHAT_TO_DO_NOW.txt (Simple Guide)
echo [6] Back to Main Menu
echo.
set /p doc_choice="Enter your choice (1-6): "

if "%doc_choice%"=="1" start START_HERE_README.md
if "%doc_choice%"=="2" start COMPREHENSIVE_IMPROVEMENTS.md
if "%doc_choice%"=="3" start دليل_البدء_السريع_ULTIMATE.md
if "%doc_choice%"=="4" start الملخص_النهائي_ULTIMATE.md
if "%doc_choice%"=="5" start WHAT_TO_DO_NOW.txt
if "%doc_choice%"=="6" cls & goto MENU

timeout /t 2 >nul
cls
goto MENU

:EXIT
cls
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo                    👋 GOODBYE!
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
echo Thank you for using Project Chronos!
echo Your CV automation system is ready to work 24/7!
echo.
echo To start the bot, run: python immortal.py
echo.
echo ═══════════════════════════════════════════════════════════════════════════════
echo.
timeout /t 3 >nul
exit
