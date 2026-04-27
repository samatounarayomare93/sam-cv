@echo off
title RITA JOB EMPIRE v99 - GOD MODE
color 0A
mode con:cols=120 lines=50
cls

echo.
echo  ███████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗███████╗
echo  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║██╔════╝
echo  ███████╗██║   ██║██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║█████╗  
echo  ╚════██║██║   ██║██╔══██╗██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║██╔══╝  
echo  ███████║╚██████╔╝██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║███████╗
echo  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝╚══════╝
echo.
echo                    JOB EMPIRE v99 - THE COMPLETE AUTOMATED SYSTEM
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════
echo.

echo  [SYSTEM COMPONENTS]
echo  ┌──────────────────────────────────────────────────────────────────────────────┐
echo  │  [1] Job Scraper      - Scans 500+ sites for new jobs                       │
echo  │  [2] Email Campaign   - Sends personalized emails to all companies          │
echo  │  [3] WhatsApp Alerts  - Instant notifications on responses                  │
echo  │  [4] Telegram Control - 24/7 remote control and monitoring                 │
echo  │  [5] LinkedIn Auto    - Auto-apply and connect features                      │
echo  │  [6] Interview Prep   - AI-generated questions and answers                   │
echo  │  [7] Reports          - Weekly progress reports                             │
echo  │  [8] Self-Healing     - Auto-fixes and restarts                            │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

echo  [COMPANY DATABASE]
echo  ┌──────────────────────────────────────────────────────────────────────────────┐
python -c "import json; c=json.load(open('company_emails.json')); print(f'  Total Companies: {len(c)}')" 2>nul || echo "  Database ready"
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────┐
echo  │                            AVAILABLE ACTIONS                                  │
echo  ├──────────────────────────────────────────────────────────────────────────────┤
echo  │  [1] 🚀 START FULL CAMPAIGN    - Send to ALL companies                      │
echo  │  [2] 🧪 TEST EMAIL            - Send test to yourself                       │
echo  │  [3] 📊 VIEW STATS           - Check application stats                      │
echo  │  [4] 🔄 RUN FOLLOW-UPS       - Send follow-up emails                        │
echo  │  [5] 📱 TEST WHATSAPP        - Test WhatsApp notifications                  │
echo  │  [6] 📩 TEST TELEGRAM        - Test Telegram notifications                   │
echo  │  [7] 🔍 SYSTEM CHECK         - Verify all configurations                    │
echo  │  [8] 📋 VIEW APPLICATIONS    - List all sent applications                   │
echo  │  [0] ❌ EXIT                - Close program                                │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="  Select option (0-8): "

if "%choice%"=="1" goto:campaign
if "%choice%"=="2" goto:test
if "%choice%"=="3" goto:stats
if "%choice%"=="4" goto:followup
if "%choice%"=="5" goto:whatsapp
if "%choice%"=="6" goto:telegram
if "%choice%"=="7" goto:check
if "%choice%"=="8" goto:list
if "%choice%"=="0" goto:exit

:campaign
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════╗
echo  ║               🚀 STARTING MASS EMAIL CAMPAIGN 🚀                           ║
echo  ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
echo  This will send personalized emails to ALL companies in the database.
echo  Each email includes:
echo    - Professional HTML design
echo    - Company name personalized
echo    - CV attached
echo    - Cover letter attached
echo.
set /p confirm="  Continue? (yes/no): "
if /i not "%confirm%"=="yes" goto:menu

echo.
python rita_job_empire.py start
goto:end

:test
echo.
echo  Sending test email...
python rita_job_empire.py test
goto:end

:stats
echo.
echo  Retrieving statistics...
python -c "import json; t=json.load(open('application_tracker.json')); s=t.get('stats',{}); print(f'Total Sent: {s.get(\"total_sent\",0)}'); print(f'Responses: {s.get(\"total_responses\",0)}'); print(f'Interviews: {s.get(\"total_interviews\",0)}')"
goto:end

:followup
echo.
python rita_job_empire.py followup
goto:end

:whatsapp
echo.
python -c "from rita_job_empire import WhatsAppNotifier; WhatsAppNotifier().send('Test from Rita Job Empire!')"
echo.
echo  ✅ WhatsApp test sent!
goto:end

:telegram
echo.
python -c "from rita_job_empire import TelegramNotifier; TelegramNotifier().send('Test from Rita Job Empire!')"
echo.
echo  ✅ Telegram test sent!
goto:end

:check
echo.
echo  [SYSTEM CHECK]
echo  ──────────────────────────────────────────────────────────────────────
python -c "import os; print(f'CV File: {\"✅ Found\" if os.path.exists(\"Rita_Cordahi_CV.html\") else \"❌ MISSING\"}')"
python -c "import json; print(f'Companies: {len(json.load(open(\"company_emails.json\")))} loaded')"
python -c "import json; print(f'Applications: {len(json.load(open(\"application_tracker.json\")).get(\"applications\",[]))} tracked')"
echo  ──────────────────────────────────────────────────────────────────────
goto:end

:list
echo.
echo  [RECENT APPLICATIONS]
echo  ──────────────────────────────────────────────────────────────────────
python -c "import json; t=json.load(open('application_tracker.json')); [print(f\"[{a['id']}] {a['company']} - {a['status']}\") for a in t.get('applications',[])[-10:]]" 2>nul || echo "No applications yet"
echo  ──────────────────────────────────────────────────────────────────────
goto:end

:exit
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                              ║
echo  ║           Thanks for using RITA JOB EMPIRE v99!                              ║
echo  ║                                                                              ║
echo  ║           Good luck with your job search! 🎯                                 ║
echo  ║                                                                              ║
echo  ╚══════════════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 3 /nobreak >nul
exit

:end
echo.
echo  ═════════════════════════════════════════════════════════════════════════════════
pause
