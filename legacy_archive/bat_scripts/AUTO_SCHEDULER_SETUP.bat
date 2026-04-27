@echo off
title RITA JOB EMPIRE - AUTO SCHEDULER
color 0A

:: ═══════════════════════════════════════════════════════════════════════════════════════
:: AUTO INSTALLER - Sets up the system to run daily automatically
:: ═══════════════════════════════════════════════════════════════════════════════════════

echo.
echo  ████████████████████████████████████████████████████████████████████████████
echo  █                                                                            █
echo  █   RITA JOB EMPIRE - AUTO SCHEDULER SETUP                                   █
echo  █                                                                            █
echo  █   This will set up Windows Task Scheduler to run your job campaign        █
echo  █   automatically EVERY DAY at 9:00 AM!                                     █
echo  █                                                                            █
echo  ████████████████████████████████████████████████████████████████████████████
echo.

echo  Setting up daily auto-run...
echo.

:: Create the scheduled task
schtasks /create /tn "RITA_JOB_EMPIRE" /tr "\"%CD%ONE_CLICK_GOD_MODE.bat\"" /sc daily /st 09:00 /f

if %errorlevel%==0 (
    echo.
    echo  ┌────────────────────────────────────────────────────────────────────────────┐
    echo  │                                                                            │
    echo  │   ✅ SUCCESS! Task scheduled!                                              │
    echo  │                                                                            │
    echo  │   RITA JOB EMPIRE will run automatically every day at 9:00 AM             │
    echo  │                                                                            │
    echo  │   To manage or remove the task:                                           │
    echo  │   1. Press Win + R                                                       │
    echo  │   2. Type: taskschd.msc                                                  │
    echo  │   3. Find "RITA_JOB_EMPIRE" and manage as needed                         │
    echo  │                                                                            │
    echo  └────────────────────────────────────────────────────────────────────────────┘
    echo.
) else (
    echo.
    echo  ┌────────────────────────────────────────────────────────────────────────────┐
    echo  │                                                                            │
    echo  │   ⚠️  Task may already exist or requires admin rights                   │
    echo  │                                                                            │
    echo  │   Try running as Administrator or check Task Scheduler manually          │
    echo  │                                                                            │
    echo  └────────────────────────────────────────────────────────────────────────────┘
    echo.
)

echo.
echo  Press any key to continue...
pause >nul
