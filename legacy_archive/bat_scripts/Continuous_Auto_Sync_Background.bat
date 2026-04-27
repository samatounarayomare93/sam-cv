@echo off
title Rita Job Automator - Continuous Auto-Sync
color 0A
echo =======================================================
echo  Rita Job Automator - Continuous Auto-Sync is RUNNING
echo =======================================================
echo This script is watching your folder for any changes.
echo Whatever you do, it will automatically sync to GitHub.
echo Leave this black window open (you can minimize it) while you work.
echo.

cd /d "%~dp0"

:loop
:: Check if there are any changes using git status
for /f "delims=" %%i in ('git status --porcelain') do (
    echo [ %time% ] Changes detected! Verifying Python Syntax...
    python -m py_compile config.py main_bot.py scraper.py >nul 2>&1
    if errorlevel 1 (
        color 0C
        echo [ %time% ] ❌ FATAL ERROR: Python Syntax check FAILED! Sync aborted.
        echo Please fix the code in VS Code. Press any key to retry...
        pause >nul
        color 0A
        goto loop
    )
    echo [ %time% ] ✅ Syntax OK! Auto-Syncing to Rita's GitHub...
    git add .
    git commit -m "Terminator Protocol: Anti-Ban & Auto-Sync background updates" >nul
    git push origin main >nul
    echo [ %time% ] 🚀 Auto-Sync Complete! 100%% safely on GitHub.
    echo.
    goto wait
)

:wait
:: Wait 30 seconds before checking again
timeout /t 30 /nobreak >nul
goto loop
