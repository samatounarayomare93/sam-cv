@echo off
cd /d "%~dp0"
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
title RITA: INFINITE GOD MODE LOOP (Auto-Sync and Scrape)
color 0B
mode con:cols=140 lines=80
cls

echo ========================================================================================================
echo                                  RITA JOB AUTOMATOR - INFINITE GOD MODE
echo ========================================================================================================
echo.
echo  [WARNING] This loop will run infinitely. It will force-pull the latest code from GitHub,
echo            run the Super Ultimate Engine, push logs/SQLite back to GitHub, and repeat forever.
echo.

:LOOP_START
echo.
echo ========================================================================================================
echo  [PHASE 1] Synchronization (Force Pull)
echo ========================================================================================================
echo Stashing local uncommitted changes...
git stash
echo Force fetching from origin...
git fetch --all
echo Resetting local main to match origin...
git reset --hard origin/main
echo Pulling latest enhancements...
git pull origin main

echo.
echo ========================================================================================================
echo  [PHASE 2] System Diagnostics
echo ========================================================================================================
.venv\Scripts\python.exe system_verifier.py
if errorlevel 1 (
    echo [WARNING] Verification found some issues ^(like local SMTP blocks^). Proceeding with HTTP Fallbacks...
    ping 127.0.0.1 -n 3 > nul
)

echo.
echo ========================================================================================================
echo  [PHASE 3] Execution / Strike Mission (Ultimate Engine)
echo ========================================================================================================
echo Launching Ultimate Super Engine...
REM We run a limited scrape session so it eventually terminates and updates github.
.venv\Scripts\python.exe -c "import ultimate_super_engine; db = ultimate_super_engine.UltimateDatabase(); scraper = ultimate_super_engine.UltimateScraper(db); emailer = ultimate_super_engine.UltimateEmailEngine(db); print('Running Ultimate Automation Cycle...'); leads = scraper.scrape_all(); print(f'Found {len(leads)} leads. Proceeding to Email Engine cycle...'); emailer.process_pending_applications()"

echo.
echo ========================================================================================================
echo  [PHASE 4] Cloud Sovereign Upload (Push to Git)
echo ========================================================================================================
git add .
git commit -m "Auto-Sync: God Mode Engine Cycle Completed - Uploading State"
git push origin main
echo Push Complete.

echo.
echo ========================================================================================================
echo  [PHASE 5] Cooldown Phase
echo ========================================================================================================
echo Mission cycle complete. Cooling down for 5 minutes before next cycle to prevent aggressive ban...
ping 127.0.0.1 -n 301 > nul

goto LOOP_START
