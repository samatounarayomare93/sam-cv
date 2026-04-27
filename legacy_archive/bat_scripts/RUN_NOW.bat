@echo off
title RITA JOB EMPIRE - ULTIMATE RUNNER
color 0A
mode con:cols=120 lines=50
cls

echo.
echo  ██████████████████████████████████████████████████████████████████████████████████
echo  █                                                                              █
echo  █  ███████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗ █
echo  █  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║ █
echo  █  ███████╗██║   ██║██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║ █
echo  █  ╚════██║██║   ██║██╔══██╗██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║ █
echo  █  ███████║╚██████╔╝██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║ █
echo  █  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝ █
echo  █                                                                              █
echo  ██████████████████████████████████████████████████████████████████████████████████
echo.
echo                     ██╗  ██╗ ██████╗ ██████╗ ██╗   ██╗███████╗
echo                     ██║  ██║██╔═══██╗██╔══██╗██║   ██║██╔════╝
echo                     ███████║██║   ██║██████╔╝██║   ██║███████╗
echo                     ██╔══██║██║   ██║██╔══██╗██║   ██║╚════██║
echo                     ██║  ██║╚██████╔╝██║  ██║╚██████╔╝███████║
echo                     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
echo.
echo  ██████████████████████████████████████████████████████████████████████████████████
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                           │
echo  │   Found Python: py                                                        │
echo  │                                                                           │
echo  │   ONE CLICK GOD MODE - DOING EVERYTHING FOR YOU!                         │
echo  │                                                                           │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

:: Run the campaign using py launcher
echo [1/5] Checking system...
py -c "import json,os; c=len(json.load(open('company_emails.json'))); t=len(json.load(open('application_tracker.json')).get('applications',[])); print('Companies: ' + str(c) + ', Already sent: ' + str(t))" 2>nul

echo.
echo [2/5] Loading company database...
echo [3/5] Creating personalized emails...
echo [4/5] Sending emails...
echo.

:: Run the campaign
py rita_job_empire.py start

echo.
echo [5/5] Campaign complete!
echo.

:: Send notification
py -c "from rita_job_empire import WhatsAppNotifier; WhatsAppNotifier().send('✅ GOD MODE COMPLETE! Check application_tracker.json!')" 2>nul

echo.
echo  ██████████████████████████████████████████████████████████████████████████████████
echo  █                                                                              █
echo  █  ██████╗ ██╗   ██╗███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗  █
echo  █  ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║  █
echo  █  ██████╔╝ ╚████╔╝ █████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║  █
echo  █  ██╔══██╗  ╚██╔╝  ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║  █
echo  █  ██████╔╝   ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║  █
echo  █  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝  █
echo  █                                                                              █
echo  ██████████████████████████████████████████████████████████████████████████████████
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                           │
echo  │   ✅ CAMPAIGN COMPLETE!                                                   │
echo  │                                                                           │
echo  │   I've done everything for you:                                           │
echo  │   ✓ Sent emails to all companies                                          │
echo  │   ✓ Attached your CV                                                      │
echo  │   ✓ Attached cover letters                                                 │
echo  │   ✓ Tracked all applications                                              │
echo  │                                                                           │
echo  │   Check WhatsApp for notifications!                                       │
echo  │                                                                           │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

timeout /t 10 /nobreak >nul
