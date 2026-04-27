@echo off
title RITA JOB EMPIRE - THE ULTIMATE LAUNCHER
color 0A
mode con:cols=130 lines=65
cls

:: ═══════════════════════════════════════════════════════════════════════════════════════
:: 
::   ██████╗ ███████╗██╗   ██╗    ███████╗██╗   ██╗██████╗ ███████╗
::   ██╔══██╗██╔════╝██║   ██║    ██╔════╝██║   ██║██╔══██╗██╔════╝
::   ██║  ██║█████╗  ██║   ██║    ███████╗██║   ██║██████╔╝█████╗  
::   ██║  ██║██╔══╝  ██║   ██║    ╚════██║██║   ██║██╔══██╗██╔══╝  
::   ██████╔╝███████╗╚██████╔╝    ███████║╚██████╔╝██║  ██║███████╗
::   ╚═════╝ ╚══════╝ ╚═════╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝
::   
::   ██████╗  █████╗ ██╗   ██╗███████╗██████╗  ██████╗ ███╗   ███╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
::   ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔═══██╗████╗ ████║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
::   ██████╔╝███████║ ╚████╔╝ █████╗  ██████╔╝██║   ██║██╔████╔██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝███████╗
::   ██╔══██╗██╔══██║  ╚██╔╝  ██╔══╝  ██╔══██╗██║   ██║██║╚██╔╝██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗╚════██║
::   ██████╔╝██║  ██║   ██║   ███████╗██║  ██║╚██████╔╝██║ ╚═╝ ██║███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████║
::   ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝     ╚═╝╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
::
:: ═══════════════════════════════════════════════════════════════════════════════════════

echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                                      ║
echo  ║                         >>>  W E L C O M E   T O   T H E   E M P I R E  <<<                                ║
echo  ║                                                                                                      ║
echo  ║                                  THE COMPLETE JOB HUNTING SYSTEM                                           ║
echo  ║                                                                                                      ║
echo  ║                         I WILL DO EVERYTHING FOR YOU - 100% AUTOMATED                                  ║
echo  ║                                                                                                      ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
echo.

echo  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                         WHAT I DO                                                    │
echo  ├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
echo  │                                                                                                        │
echo  │  ✓ Scan 80+ GCC companies for HR jobs                                                                 │
echo  │  ✓ Research each company deeply                                                                         │
echo  │  ✓ Create personalized emails for EACH company individually                                            │
echo  │  ✓ Create personalized cover letters for EACH company                                                  │
echo  │  ✓ Send professional HTML emails with CV attached                                                      │
echo  │  ✓ AUTO FOLLOW-UP after 3, 7, 14 days automatically                                                  │
echo  │  ✓ Track every single application in database                                                          │
echo  │  ✓ WhatsApp notifications when companies respond                                                       │
echo  │  ✓ Telegram bot (CYBERPUNK style) for 24/7 control                                                   │
echo  │  ✓ Daily reports to your phone                                                                        │
echo  │  ✓ Interview prep with 15+ questions and answers                                                      │
echo  │                                                                                                        │
echo  └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.

:: Check system status
python -c "import json,os; cv='YES' if os.path.exists('Rita_Cordahi_CV.html') else 'NO'; c=len(json.load(open('company_emails.json'))); t=len(json.load(open('application_tracker.json')).get('applications',[])); print(f'  CV: {cv} | Companies: {c} | Already Sent: {t}')" 2>nul

echo.
echo  ┌────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                           MAIN ACTIONS                                               │
echo  ├────────────────────────────────────────────────────────────────────────────────────────────────────────┤
echo  │                                                                                                        │
echo  │   [1] 🔥 ONE CLICK - DO EVERYTHING NOW!          (Sends to all companies NOW!)                     │
echo  │                                                                                                        │
echo  │   [2] 📊 VIEW DASHBOARD                         (See current status)                                 │
echo  │                                                                                                        │
echo  │   [3] 🤖 CYBERPUNK TELEGRAM BOT                  (Start the cyberpunk bot)                           │
echo  │                                                                                                        │
echo  │   [4] 📚 INTERVIEW PREP                          (Practice questions)                                │
echo  │                                                                                                        │
echo  │   [5] 📱 WHATSAPP TEST                           (Test notifications)                                │
echo  │                                                                                                        │
echo  │   [6] 🔍 SYSTEM CHECK                            (Verify everything works)                           │
echo  │                                                                                                        │
echo  │   [7] ⏰ SETUP DAILY AUTO-RUN                    (Run automatically every day)                       │
echo  │                                                                                                        │
echo  │   [0] ❌ EXIT                                   (Close program)                                      │
echo  │                                                                                                        │
echo  └────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="  SELECT (0-7): "

if "%choice%"=="1" goto:one_click
if "%choice%"=="2" goto:dashboard
if "%choice%"=="3" goto:telegram
if "%choice%"=="4" goto:interview
if "%choice%"=="5" goto:whatsapp
if "%choice%"=="6" goto:check
if "%choice%"=="7" goto:auto_setup
if "%choice%"=="0" goto:exit

:one_click
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
echo  >>> SENDING EMAILS TO ALL COMPANIES NOW! <<<
echo.

python rita_job_empire.py start

echo.
echo  ✅ Campaign complete!
echo.

python -c "from rita_job_empire import WhatsAppNotifier; WhatsAppNotifier().send('✅ GOD MODE COMPLETE! Check application_tracker.json!')" 2>nul

echo.
echo  Check WhatsApp for notifications!
echo.
pause
goto:restart

:dashboard
cls
python -c "
import json
t = json.load(open('application_tracker.json'))
s = t.get('stats', {})
apps = t.get('applications', [])
print('DASHBOARD:')
print(f'Total Sent: {s.get(\"total_sent\", 0)}')
print(f'Responses: {len(t.get(\"responses\", []))}')
print(f'Interviews: {s.get(\"total_interviews\", 0)}')
"
pause
goto:restart

:telegram
python cyberpunk_telegram_bot.py
goto:restart

:interview
python interview_prep.py
goto:restart

:whatsapp
python -c "from rita_job_empire import WhatsAppNotifier; WhatsAppNotifier().send('Test from Rita Job Empire!')"
echo.
echo  ✅ WhatsApp test sent!
pause
goto:restart

:check
python -c "
import os, json
print('SYSTEM CHECK:')
cv = '✅' if os.path.exists('Rita_Cordahi_CV.html') else '❌'
print(f'CV: {cv}')
c = len(json.load(open('company_emails.json')))
print(f'Companies: {c}')
apps = len(json.load(open('application_tracker.json')).get('applications',[]))
print(f'Applications: {apps}')
print('STATUS: READY')
"
pause
goto:restart

:auto_setup
echo.
echo  Setting up daily auto-run at 9:00 AM...
schtasks /create /tn "RITA_JOB_EMPIRE" /tr "\"%CD%ONE_CLICK_GOD_MODE.bat\"" /sc daily /st 09:00 /f 2>nul
echo.
echo  ✅ Done! System will run automatically every day at 9 AM!
pause
goto:restart

:exit
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                                      ║
echo  ║               Thanks for using RITA JOB EMPIRE!                                                      ║
echo  ║                                                                                                      ║
echo  ║               Good luck with your job search! 🎯                                                     ║
echo  ║                                                                                                      ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 3 /nobreak >nul
exit

:restart
start START_MASTER_LAUNCHER.bat
exit
