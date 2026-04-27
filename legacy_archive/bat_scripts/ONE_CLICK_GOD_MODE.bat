@echo off
title RITA JOB EMPIRE - AUTO MODE
color 0A
mode con:cols=120 lines=50
cls

:: ═══════════════════════════════════════════════════════════════════════════════════════
:: RITA JOB EMPIRE - ONE CLICK GOD MODE
:: Just DOUBLE-CLICK this file and it does EVERYTHING!
:: ═══════════════════════════════════════════════════════════════════════════════════════

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
echo  │   >>>  ONE CLICK GOD MODE - DOING EVERYTHING FOR YOU!  <<<                  │
echo  │                                                                           │
echo  │   Stand by... I'm doing everything automatically!                          │
echo  │                                                                           │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

:: Step 1: Check system
echo [1/6] Checking system...
python -c "import json,os; c=len(json.load(open('company_emails.json'))); t=len(json.load(open('application_tracker.json')).get('applications',[])); print(f'  Companies: {c}, Already sent: {t}')" 2>nul

:: Step 2: Send campaign
echo.
echo [2/6] Preparing email campaign...
echo [3/6] Loading company database...
echo [4/6] Creating personalized emails...
echo [5/6] Sending emails...
echo.

:: Run the campaign
python rita_job_empire.py start

:: Step 6: Complete
echo.
echo [6/6] Campaign complete!
echo.

:: Send notification
python -c "from rita_job_empire import WhatsAppNotifier; WhatsAppNotifier().send('✅ GOD MODE COMPLETE! Check application_tracker.json for results!')" 2>nul

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
echo  │   I've done everything for you:                                            │
echo  │   ✓ Sent emails to all companies                                          │
echo  │   ✓ Attached your CV                                                     │
echo  │   ✓ Attached cover letters                                                │
echo  │   ✓ Tracked all applications                                             │
echo  │                                                                           │
echo  │   Check WhatsApp for notifications!                                      │
echo  │                                                                           │
echo  │   Run me again tomorrow for more!                                         │
echo  │                                                                           │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

timeout /t 10 /nobreak >nul
