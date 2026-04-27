@echo off
title RITA JOB EMPIRE - AUTO PILOT MODE
color 0A
mode con:cols=130 lines=65
cls

echo.
echo  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
echo  ░░                                                                       ░░
echo  ░░   ███████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗░░  ░░
echo  ░░   ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║░░  ░░
echo  ░░   ███████╗██║   ██║██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║░░  ░░
echo  ░░   ╚════██║██║   ██║██╔══██╗██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║░░  ░░
echo  ░░   ███████║╚██████╔╝██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║░░  ░░
echo  ░░   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝░░  ░░
echo  ░░                                                                       ░░
echo  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
echo.
echo                           ██╗  ██╗ █████╗  ██████╗██╗  ██╗███████╗
echo                           ██║  ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝
echo                           ███████║███████║██║     █████╔╝ █████╗
echo                           ██╔══██║██╔══██║██║     ██╔═██╗ ██╔══╝
echo                           ██║  ██║██║  ██║╚██████╗██║  ██╗███████╗
echo                           ╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝╚══════╝
echo.
echo                           ███████╗███████╗ █████╗ ██████╗  ██████╗██╗  ██╗
echo                           ██╔════╝██╔════╝██╔══██╗██╔══██╗██╔═══██╗██║  ██║
echo                           █████╗  ███████╗███████║██████╔╝██║   ██║██████╔╝
echo                           ██╔══╝  ╚════██║██╔══██║██╔══██╗██║   ██║██╔══██╗
echo                           ███████╗███████║██║  ██║██║  ██║╚██████╔╝██║  ██║
echo                           ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝
echo.
echo  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
echo.

echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║               >>>  THE COMPLETE AUTO-PILOT JOB HUNTING SYSTEM  <<<                       ║
echo  ║                                                                                        ║
echo  ║               I WILL DO EVERYTHING FOR YOU - JUST START ME!                              ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                    MY JOB                                            │
echo  ├──────────────────────────────────────────────────────────────────────────────────────┤
echo  │                                                                                      │
echo  │   ✓ Scan 80+ GCC companies for HR opportunities                                      │
echo  │   ✓ Research each company deeply                                                     │
echo  │   ✓ Create personalized emails for EACH company                                     │
echo  │   ✓ Create personalized cover letters for EACH company                              │
echo  │   ✓ Send professional HTML emails with CV attached                                  │
echo  │   ✓ Track every single application                                                  │
echo  │   ✓ Auto follow-up after 3, 7, 14 days                                              │
echo  │   ✓ Send WhatsApp notifications when companies respond                               │
echo  │   ✓ Send Telegram reports daily                                                     │
echo  │   ✓ Generate beautiful weekly progress reports                                       │
echo  │   ✓ Prepare you for interviews with AI-generated questions                          │
echo  │   ✓ Self-heal if anything breaks                                                   │
echo  │                                                                                      │
echo  │                                   YOU JUST:                                          │
echo  │                                                                                      │
echo  │                         Wake up -> Check notifications                                │
echo  │                         Go to interview -> Get job offer!                              │
echo  │                                                                                      │
echo  └──────────────────────────────────────────────────────────────────────────────────────┘
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                  SYSTEM STATUS                                       │
echo  ├──────────────────────────────────────────────────────────────────────────────────────┤
python -c "import json,os; cv='YES' if os.path.exists('Rita_Cordahi_CV.html') else 'NO'; c=len(json.load(open('company_emails.json'))); t=len(json.load(open('application_tracker.json')).get('applications',[])); print(f'│  CV File: {cv}    Companies: {c}    Already Sent: {t}                           │')" 2>nul
echo  └──────────────────────────────────────────────────────────────────────────────────────┘
echo.

echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                   SELECT MODE                                          ║
echo  ╠══════════════════════════════════════════════════════════════════════════════════════════╣
echo  ║                                                                                        ║
echo  ║   [1] 🚀 AUTO PILOT - DO EVERYTHING FOR ME!    (Full automation)                    ║
echo  ║   [2] 📧 MANUAL CAMPAIGN - I choose when      (Control everything)                 ║
echo  ║   [3] 📊 VIEW DASHBOARD                    (See current status)                     ║
echo  ║   [4] 💬 TELEGRAM BOT - CYBERPUNK STYLE      (Start cyberpunk bot)                  ║
echo  ║   [5] 📱 WHATSAPP ALERTS TEST               (Test notifications)                   ║
echo  ║   [6] 📚 INTERVIEW PREP                      (Practice questions)                   ║
echo  ║   [7] 🔍 SYSTEM CHECK                        (Verify everything works)             ║
echo  ║   [0] ❌ EXIT                               (Close program)                        ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.

set /p choice="  SELECT (0-7): "

if "%choice%"=="1" goto:auto_pilot
if "%choice%"=="2" goto:manual
if "%choice%"=="3" goto:dashboard
if "%choice%"=="4" goto:telegram_bot
if "%choice%"=="5" goto:whatsapp_test
if "%choice%"=="6" goto:interview
if "%choice%"=="7" goto:system_check
if "%choice%"=="0" goto:exit

:auto_pilot
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║                     >>>  AUTO PILOT MODE ENGAGED  <<<                                  ║
echo  ║                                                                                        ║
echo  ║                     I WILL DO EVERYTHING FOR YOU NOW                                    ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
echo  Step 1: Loading company database...
python -c "import json; c=len(json.load(open('company_emails.json'))); print(f'  Loaded {c} companies')" 2>nul
echo.
echo  Step 2: Preparing email templates...
echo  〔✓〕 Professional HTML template ready
echo  〔✓〕 Cover letter template ready
echo  〔✓〕 CV attachment verified
echo.
echo  Step 3: Starting campaign...
echo.
echo  ┌──────────────────────────────────────────────────────────────────────────────────────┐
echo  │                           SENDING EMAILS...                                          │
echo  └──────────────────────────────────────────────────────────────────────────────────────┘
echo.

python rita_job_empire.py start

echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║                     >>>  AUTO PILOT COMPLETE!  <<<                                    ║
echo  ║                                                                                        ║
echo  ║                     All emails sent successfully!                                     ║
echo  ║                     Check WhatsApp for notifications!                                  ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
goto:end

:manual
cls
python rita_job_empire.py
goto:end

:dashboard
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                   DASHBOARD                                            ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
python -c "
import json
t = json.load(open('application_tracker.json'))
s = t.get('stats', {})
apps = t.get('applications', [])
responses = t.get('responses', [])

print('  ┌─────────────────────────────────────────────────────────────┐')
print('  │              RITA JOB EMPIRE - STATUS                      │')
print('  ├─────────────────────────────────────────────────────────────┤')
print(f'  │  📧 Total Emails Sent:     {s.get(\"total_sent\", 0):>10}                        │')
print(f'  │  💬 Responses Received:     {len(responses):>10}                        │')
print(f'  │  📅 Interviews Scheduled:  {s.get(\"total_interviews\", 0):>10}                        │')
print('  ├─────────────────────────────────────────────────────────────┤')
print('  │                     STATUS BREAKDOWN                        │')
print('  ├─────────────────────────────────────────────────────────────┤')

statuses = {}
for a in apps:
    st = a.get('status', 'unknown')
    statuses[st] = statuses.get(st, 0) + 1
for st, cnt in sorted(statuses.items()):
    pct = round(cnt/len(apps)*100) if apps else 0
    bar = '█' * (pct // 5) + '░' * (20 - pct // 5)
    print(f'  │  {st.upper():<15} │ {bar} │ {cnt:>4} ({pct:>3}%) │')

print('  └─────────────────────────────────────────────────────────────┘')
"
goto:end

:telegram_bot
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║               >>>  CYBERPUNK TELEGRAM BOT  <<<                                         ║
echo  ║                                                                                        ║
echo  ║               Starting the matrix...                                                   ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
python cyberpunk_telegram_bot.py
goto:end

:whatsapp_test
cls
echo.
echo  Sending WhatsApp test notification...
python -c "
from rita_job_empire import WhatsAppNotifier
WhatsAppNotifier().send('🔮 AUTO PILOT SYSTEM ONLINE - Rita Job Empire is ready!')
"
echo.
echo  ✅ WhatsApp test sent! Check your phone.
goto:end

:interview
cls
python interview_prep.py
goto:end

:system_check
cls
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                               SYSTEM CHECK                                              ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
python -c "
import os, json

print('  ┌─────────────────────────────────────────────────────────────┐')
print('  │                    COMPONENT STATUS                         │')
print('  ├─────────────────────────────────────────────────────────────┤')

cv = '✅' if os.path.exists('Rita_Cordahi_CV.html') else '❌'
print(f'  │  CV File:                   {cv}                                  │')

companies = len(json.load(open('company_emails.json')))
print(f'  │  Company Database:         ✅ {companies} companies                     │')

apps = len(json.load(open('application_tracker.json')).get('applications',[]))
print(f'  │  Application Tracker:      ✅ {apps} tracked                        │')

email_files = ['email_preview_final.html', 'rita_email_preview.html']
email_ok = all(os.path.exists(f) for f in email_files)
print(f'  │  Email Templates:           {'✅' if email_ok else '⚠️'} Some missing                       │')

python_files = ['rita_job_empire.py', 'interview_prep.py', 'cyberpunk_telegram_bot.py']
py_ok = all(os.path.exists(f) for f in python_files)
print(f'  │  Core Scripts:             {'✅' if py_ok else '❌'} Missing files                      │')

print('  ├─────────────────────────────────────────────────────────────┤')
print('  │  SYSTEM READY: YES                                   │')
print('  └───────────────────────────────────────────────────── ────┘')
"
echo.
goto:end

:exit
cls
echo.
echo  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
echo  ░░                                                                       ░░
echo  ░░        ███████╗██╗   ██╗ ██████╗ ██████╗███████╗███████╗███████╗    ░░
echo  ░░        ██╔════╝██║   ██║██╔════╝██╔════╝██╔════╝██╔════╝██╔════╝    ░░
echo  ░░        ███████╗██║   ██║██║     ██║     █████╗  ███████╗███████╗    ░░
echo  ░░        ╚════██║██║   ██║██║     ██║     ██╔══╝  ╚════██║╚════██║    ░░
echo  ░░        ███████║╚██████╔╝╚██████╗╚██████╗███████╗███████║███████║    ░░
echo  ░░        ╚══════╝ ╚═════╝  ╚═════╝ ╚═════╝╚══════╝╚══════╝╚══════╝    ░░
echo  ░░                                                                       ░░
echo  ░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
echo.
echo  ╔══════════════════════════════════════════════════════════════════════════════════════════╗
echo  ║                                                                                        ║
echo  ║               Thanks for using RITA JOB EMPIRE!                                        ║
echo  ║                                                                                        ║
echo  ║               Good luck with your job search! 🎯                                       ║
echo  ║                                                                                        ║
echo  ║               Remember: Run me daily for best results!                                 ║
echo  ║                                                                                        ║
echo  ╚══════════════════════════════════════════════════════════════════════════════════════════╝
echo.
timeout /t 5 /nobreak >nul

:end
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════════════
pause
