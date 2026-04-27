@echo off
title RITA EMAIL CAMPAIGN LAUNCHER
color 0A
mode con:cols=100 lines=50
cls

echo.
echo  ╔════════════════════════════════════════════════════════════════════╗
echo  ║         RITA JOB AUTOMATOR - EMAIL CAMPAIGN SYSTEM v2            ║
echo  ╚════════════════════════════════════════════════════════════════════╝
echo.

echo  [EMAIL DESIGN]
echo  ┌────────────────────────────────────────────────────────────────────┐
echo  │  Email Template: Professional HTML with dark theme               │
echo  │  - Company name personalized in header                           │
echo  │  - CV attached (HTML format)                                     │
echo  │  - Cover Letter attached (Personalized HTML)                       │
echo  │  - Subject: "[Job Title] | Rita Cordahi - HR & Operations"       │
echo  └────────────────────────────────────────────────────────────────────┘
echo.

echo  [COMPANIES LOADED]
echo  ┌────────────────────────────────────────────────────────────────────┐
python -c "import json; c=json.load(open('company_emails.json')); print(f'  Total Companies: {len(c)}'); banks=[x for x in c if any(k in x[\"company\"].lower() for k in [\"bank\",\"finance\"])]; print(f'  Banks/Finance: {len(banks)}'); gulf=[x for x in c if any(k in x[\"company\"].lower() for k in [\"dubai\",\"emirates\",\"abu\",\"qatar\",\"saudi\",\"kuwait\"])]; print(f'  GCC Companies: {len(gulf)}')" 2>nul || echo "  Load companies by running the script"
echo  └────────────────────────────────────────────────────────────────────┘
echo.

echo  [OPTIONS]
echo  ┌────────────────────────────────────────────────────────────────────┐
echo  │  [1] Send TEST EMAIL         - Send to your own email             │
echo  │  [2] Send to ALL COMPANIES   - Mass email campaign               │
echo  │  [3] Preview EMAIL DESIGN     - View the email template           │
echo  │  [4] Exit                    - Return to main menu                │
echo  └────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="Select option (1-4): "

if "%choice%"=="1" goto:test
if "%choice%"=="2" goto:all
if "%choice%"=="3" goto:preview
if "%choice%"=="4" exit

:test
echo.
echo  [SENDING TEST EMAIL]
echo  Sending to: sam.dev1@hotmail.com
echo.
python rita_email_system.py test
echo.
pause
goto:end

:all
echo.
echo  [WARNING] Mass email campaign starting...
echo  This will send emails to ALL companies in company_emails.json
echo.
set /p confirm="Continue? (yes/no): "
if /i not "%confirm%"=="yes" goto:end

echo.
echo  [STARTING EMAIL CAMPAIGN]
echo  Rate limit: 1 email every 3-5 seconds
echo  Estimated time: Calculating...
python -c "import json; c=json.load(open('company_emails.json')); print(f'  Companies: {len(c)}'); print(f'  Estimated time: {len(c)*4//60} minutes')"
echo.
python rita_email_system.py all
goto:end

:preview
echo.
echo  [PREVIEW] Opening email preview in browser...
start rita_email_preview.html
goto:end

:end
echo.
echo  ═════════════════════════════════════════════════════════════════════
echo  Campaign complete!
echo  ═════════════════════════════════════════════════════════════════════
pause
