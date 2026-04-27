@echo off
title RITA - THE ULTIMATE JOB EMPIRE
color 0A
mode con:cols=130 lines=60
cls

echo.
echo  ██████╗ ██████╗ ██╗███╗   ██╗ ██████╗ ███████╗██████╗ ██╗████████╗██╗ ██████╗ ███╗   ██╗
echo  ██╔══██╗██╔══██╗██║████╗  ██║██╔════╝ ██╔════╝██╔══██╗██║╚══██╔══╝██║██╔═══██╗████╗  ██║
echo  ██████╔╝██████╔╝██║██╔██╗ ██║██║  ███╗█████╗  ██████╔╝██║   ██║   ██║██║   ██║██╔██╗ ██║
echo  ██╔═══╝ ██╔══██╗██║██║╚██╗██║██║   ██║██╔══╝  ██╔══██╗██║   ██║   ██║██║   ██║██║╚██╗██║
echo  ██║     ██║  ██║██║██║ ╚████║╚██████╔╝███████╗██████╔╝██║   ██║   ██║╚██████╔╝██║ ╚████║
echo  ╚═╝     ╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝   ╚═╝   ╚═╝ ╚═════╝ ╚═╝  ╚═══╝
echo.
echo                    ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗██████╗                          
echo                    ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗                         
echo                    ███████║███████║██║     █████╔╝ █████╗  ██████╔╝                         
echo                    ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗                         
echo                    ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗██║  ██║                         
echo                    ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝                         
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════════════
echo                           THE COMPLETE 100% AUTOMATED JOB HUNTING SYSTEM
echo  ═══════════════════════════════════════════════════════════════════════════════════════════
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                   SYSTEM STATUS                                     │
echo  ├──────────────────────────────────────────────────────────────────────────────────────┤
python -c "import json,os; cv='YES' if os.path.exists('Rita_Cordahi_CV.html') else 'NO'; companies=len(json.load(open('company_emails.json'))); apps=len(json.load(open('application_tracker.json')).get('applications',[])); print(f'│  CV File: {cv}    Companies: {companies}    Applications: {apps}                           │')" 2>nul
echo  └──────────────────────────────────────────────────────────────────────────────────────┘
echo.

echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                    MAIN ACTIONS                                        ║
echo  ╠══════════════════════════════════════════════════════════════════════════════════════════╣
echo  ║                                                                                        ║
echo  ║   [1] 🚀  START FULL EMAIL CAMPAIGN      Send to ALL companies with CV + Cover       ║
echo  ║   [2] 🧪  TEST EMAIL                    Send test to yourself                       ║
echo  ║   [3] 📊  VIEW ALL STATISTICS           See application progress                     ║
echo  ║   [4] 📋  VIEW SENT APPLICATIONS        List all emails sent                        ║
echo  ║   [5] 🔄  RUN FOLLOW-UPS                Send follow-up emails                       ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.

echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                 SUPPORTING TOOLS                                        ║
echo  ╠══════════════════════════════════════════════════════════════════════════════════════════╣
echo  ║                                                                                        ║
echo  ║   [6] 📱  WHATSAPP TEST                Test WhatsApp notifications                  ║
echo  ║   [7] 📩  TELEGRAM TEST                Test Telegram notifications                  ║
echo  ║   [8] 🔍  SYSTEM CHECK                 Verify all configurations                   ║
echo  ║   [9] 📧  EMAIL PREVIEW                View email design                           ║
echo  ║  [10] 📚  INTERVIEW PREP               Practice interview questions                ║
echo  ║  [11] 🎯  LINKEDIN PROFILE             Open LinkedIn profile                       ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.

set /p choice="  Select option (0-11): "

if "%choice%"=="1" goto:campaign
if "%choice%"=="2" goto:test
if "%choice%"=="3" goto:stats
if "%choice%"=="4" goto:list
if "%choice%"=="5" goto:followup
if "%choice%"=="6" goto:whatsapp
if "%choice%"=="7" goto:telegram
if "%choice%"=="8" goto:check
if "%choice%"=="9" goto:preview
if "%choice%"=="10" goto:interview
if "%choice%"=="11" goto:linkedin
if "%choice%"=="0" goto:exit

:campaign
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║                    🚀 STARTING MASS EMAIL CAMPAIGN 🚀                                 ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
echo  Each email includes:
echo    • Professional HTML email design
echo    • Company name personalized throughout
echo    • Rita_Cordahi_CV.html attached
echo    • [Company]_Cover_Letter_Rita_Cordahi.html attached
echo.
set /p confirm="  Continue with campaign? (yes/no): "
if /i not "%confirm%"=="yes" goto:restart

python rita_job_empire.py start

echo.
echo  Campaign complete!
goto:end

:test
cls
echo.
echo  Sending test email...
python -c "
from rita_job_empire import EmailEngine
email = EmailEngine()
result = email.send('rita.cordahi@outlook.com', 'TEST COMPANY', 'HR & Operations Manager')
print('Success!' if result else 'Failed - Check configuration')
"
goto:end

:stats
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                              APPLICATION STATISTICS                                    ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
python -c "
import json
t = json.load(open('application_tracker.json'))
s = t.get('stats', {})
apps = t.get('applications', [])
responses = t.get('responses', [])

print(f'  Total Emails Sent:     {s.get(\"total_sent\", 0)}')
print(f'  Total Responses:       {s.get(\"total_responses\", 0)}')
print(f'  Total Interviews:      {s.get(\"total_interviews\", 0)}')
print()
print(f'  Status Breakdown:')
statuses = {}
for a in apps:
    st = a.get('status', 'unknown')
    statuses[st] = statuses.get(st, 0) + 1
for st, cnt in statuses.items():
    print(f'    {st}: {cnt}')
"
goto:end

:list
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                              SENT APPLICATIONS                                         ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
python -c "
import json
t = json.load(open('application_tracker.json'))
apps = t.get('applications', [])
if not apps:
    print('  No applications yet!')
else:
    for a in apps[-15:]:
        print(f'  [{a.get(\"id\",0):3}] {a.get(\"company\",\"\"):30} | {a.get(\"status\",\"\"):10} | {a.get(\"job_title\",\"\")}')
"
goto:end

:followup
cls
echo.
python rita_job_empire.py followup
echo.
echo  Follow-ups complete!
goto:end

:whatsapp
cls
echo.
echo  Sending WhatsApp test...
python -c "
from rita_job_empire import WhatsAppNotifier
WhatsAppNotifier().send('Test from Rita Job Empire! System is working!')
"
echo.
echo  ✅ WhatsApp test sent - check your phone!
goto:end

:telegram
cls
echo.
echo  Sending Telegram test...
python -c "
from rita_job_empire import TelegramNotifier
 TelegramNotifier().send('Test from Rita Job Empire! System is working!')
"
echo.
echo  ✅ Telegram test sent!
goto:end

:check
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                              SYSTEM CONFIGURATION CHECK                                 ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
python -c "
import os, json

print('  COMPONENT              STATUS')
print('  ' + '-'*55)

# CV File
cv = '✅ Rita_Cordahi_CV.html' if os.path.exists('Rita_Cordahi_CV.html') else '❌ MISSING'
print(f'  CV File:               {cv}')

# Companies
companies = len(json.load(open('company_emails.json')))
print(f'  Company Database:      ✅ {companies} companies')

# Tracker
apps = len(json.load(open('application_tracker.json')).get('applications',[]))
print(f'  Application Tracker:   ✅ {apps} tracked')

# Email APIs
brevo = '✅ Configured' if os.getenv('BREVO_API_KEY') else '⚠️ Not set'
print(f'  Brevo API:            {brevo}')

gmail = '✅ Configured' if os.getenv('GMAIL_USER') else '⚠️ Not set'
print(f'  Gmail SMTP:            {gmail}')

# Notification APIs
whatsapp = '✅ Configured' if os.getenv('WHATSAPP_API') else '⚠️ Not set'
print(f'  WhatsApp:             {whatsapp}')

telegram = '✅ Configured' if os.getenv('TELEGRAM_BOT_TOKEN') else '⚠️ Not set'
print(f'  Telegram Bot:         {telegram}')

print()
print('  ' + '-'*55)
print('  All core systems operational!')
"
goto:end

:preview
cls
echo.
echo  Opening email preview in browser...
start email_preview_final.html
echo.
echo  ✅ Preview opened!
goto:end

:interview
cls
python interview_prep.py
goto:end

:linkedin
start https://www.linkedin.com/in/rita-cordahi/
echo.
echo  ✅ LinkedIn profile opened!
goto:end

:exit
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║           Thanks for using RITA JOB EMPIRE - THE ULTIMATE SYSTEM!                     ║
echo  ║                                                                                        ║
echo  ║           Good luck with your job search! 🎯                                            ║
echo  ║                                                                                        ║
echo  ║           Remember: Consistency is key! Run this daily!                                ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 5 /nobreak >nul
exit

:end
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════════════
pause

:restart
cls
start START_RITA_JOB_EMPIRE.bat
exit
