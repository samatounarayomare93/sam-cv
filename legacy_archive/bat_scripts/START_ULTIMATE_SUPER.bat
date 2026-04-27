@echo off
title RITA ULTIMATE - SUPER HYPER MAXIMUM POWER ENGINE
color 0A
mode con:cols=140 lines=80
cls

echo.
echo  ██████╗ ███████╗███╗   ███╗██████╗ ██╗     ███████╗
echo  ██╔══██╗██╔════╝████╗ ████║██╔══██╗██║     ██╔════╝
echo  ██████╔╝█████╗  ██╔████╔██║██████╔╝██║     █████╗  
echo  ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝  
echo  ██║  ██║███████╗██║ ╚═╝ ██║██║     ███████╗███████╗
echo  ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝
echo.
echo  ███╗   ███╗██╗██████╗ ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗
echo  ████╗ ████║██║██╔══██╗████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝
echo  ██╔████╔██║██║██████╔╝██╔██╗ ██║██║██║  ███╗███████║   ██║   
echo  ██║╚██╔╝██║██║██╔═══╝ ██║╚██╗██║██║██║   ██║██╔══██║   ██║   
echo  ██║ ╚═╝ ██║██║██║     ██║ ╚████║██║╚██████╔╝██║  ██║   ██║   
echo  ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo                           ULTIMATE SUPER HYPER MAXIMUM POWER ENGINE - RITA CORDASHI
echo  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.
echo  [CONFIGURATION]
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                                                                 │
echo  │  🌍 COUNTRIES:        195 Countries Worldwide (Europe, Asia, Americas, Africa, Middle East, Oceania)            │
echo  │  📋 JOB PLATFORMS:   50+ Platforms (LinkedIn, Indeed, Glassdoor, Monster, Bayt, GulfTalent, etc.)         │
echo  │  📧 EMAIL PATTERNS:   100+ Patterns (English, German, French, Spanish, Chinese, Arabic, etc.)                 │
echo  │  🔄 SMTP PROVIDERS:   15+ Providers (Brevo, Gmail, Outlook, Yahoo, Zoho, Mailgun, SendGrid, SES, etc.)     │
echo  │  🤖 AI FILTERING:     Intelligent job matching with salary rules                                           │
echo  │  🛡️ ANTI-DETECTION:    User-Agent rotation, proxy support, rate limiting                                    │
echo  │  📊 REAL-TIME:        Live statistics and monitoring                                                        │
echo  │  🔧 SELF-HEALING:     Auto-retry on failures, automatic recovery                                           │
echo  │                                                                                                                 │
echo  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  [SCRAPER SOURCES]
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                                                                 │
echo  │  LEBANON:         Daleel Madani, HireLebanese                                                              │
echo  │  MIDDLE EAST:      Bayt, GulfTalent, Dubizzle, Wazajobs, MonsterGulf                                      │
echo  │  GLOBAL:          LinkedIn, Indeed, Glassdoor, Monster, CareerBuilder, ZipRecruiter                       │
echo  │  ASIA:            Naukri (India), 51job/Zhaopin (China), JobStreet (Southeast Asia)                       │
echo  │  EUROPE:          InfoJobs (Spain), StepStone (Germany), Jobs.cz (Czech), Pracuj.pl (Poland)                │
echo  │  AFRICA:           Careers24 (South Africa), Jobberman (Nigeria), Wuzzuf (Egypt)                            │
echo  │  AMERICAS:        Indeed (USA/Canada), Bumeran/Computrabajo (Latin America)                              │
echo  │                                                                                                                 │
echo  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  [TARGET SETTINGS]
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                                                                 │
echo  │  LOCATIONS:         UAE, Saudi Arabia, Qatar, Kuwait, Oman, Bahrain, Lebanon, Europe, Americas, Asia         │
echo  │  JOB TITLES:        HR Manager, Operations Manager, Recruiter, Admin, Office Manager, Customer Service    │
echo  │  SALARY:            Lebanon: $1500+, Global: $6000+                                                       │
echo  │  KEYWORDS:          visa, sponsorship, relocation, housing, flight allowance, benefits package              │
echo  │                                                                                                                 │
echo  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  [RATE LIMITS]
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                                                                 │
echo  │  MAX EMAILS/HOUR:    500                                                                                     │
echo  │  MAX APPLICATIONS:   1000/day                                                                               │
echo  │  DELAY BETWEEN:      2-5 seconds (random)                                                                   │
echo  │  SMTP ROTATION:      Automatic provider rotation                                                              │
echo  │                                                                                                                 │
echo  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Show menu
echo  [SELECT MODE]
echo  ┌─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                                                                 │
echo  │  [1] ULTIMATE ENGINE     - Full power: Scrape + Email + Auto-retry (Recommended)                            │
echo  │  [2] SCRAPER ONLY       - Test scraping without sending emails                                             │
echo  │  [3] EMAIL TEST        - Test email sending only                                                           │
echo  │  [4] STATUS CHECK      - View current statistics                                                            │
echo  │  [5] CONFIG CHECK      - Verify API keys and configuration                                                 │
echo  │  [6] EXIT              - Quit                                                                                 │
echo  │                                                                                                                 │
echo  └─────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="Select mode (1-6): "

if "%choice%"=="1" goto:ultimate
if "%choice%"=="2" goto:scraper
if "%choice%"=="3" goto:email
if "%choice%"=="4" goto:status
if "%choice%"=="5" goto:config
if "%choice%"=="6" exit

:ultimate
echo.
echo [LAUNCH] Starting ULTIMATE SUPER HYPER MAXIMUM POWER ENGINE...
echo.
python ultimate_super_engine.py
pause
goto:end

:scraper
echo.
echo [LAUNCH] Starting Scraper Test...
python -c "
from ultimate_super_engine import UltimateScraper, UltimateDatabase
db = UltimateDatabase()
scraper = UltimateScraper(db)
leads = scraper.scrape_all()
print(f'Found {len(leads)} leads')
"
pause
goto:end

:email
echo.
echo [LAUNCH] Starting Email Test...
python -c "
from ultimate_super_engine import UltimateEmailEngine, UltimateDatabase
db = UltimateDatabase()
engine = UltimateEmailEngine(db)
result = engine.send_email('sam.dev1@hotmail.com', 'Test Subject', '<h1>Test</h1><p>This is a test email from Rita</p>')
print(f'Email sent: {result.success}')
"
pause
goto:end

:status
echo.
echo [STATUS] Current Statistics...
python -c "
from ultimate_super_engine import UltimateDatabase
db = UltimateDatabase()
stats = db.get_statistics()
print('=' * 50)
print('RITA ULTIMATE ENGINE - CURRENT STATUS')
print('=' * 50)
print(f'Total Applications: {stats[\"total_applications\"]}')
print(f'Total Companies: {stats[\"total_companies\"]}')
print(f'Total Emails: {stats[\"total_emails\"]}')
print(f'Total Leads: {stats[\"total_leads\"]}')
print(f'Today Applications: {stats[\"today_applications\"]}')
print('=' * 50)
"
pause
goto:end

:config
echo.
echo [CONFIG] Verifying Configuration...
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('=' * 60)
print('RITA ULTIMATE ENGINE - CONFIGURATION CHECK')
print('=' * 60)

checks = [
    ('Brevo SMTP User', 'BREVO_SMTP_LOGIN', True),
    ('Brevo SMTP Password', 'BREVO_SMTP_PASSWORD', True),
    ('Gmail SMTP User', 'GMAIL_SMTP_USER', False),
    ('Gmail App Password', 'GMAIL_APP_PASSWORD', False),
    ('Outlook User', 'OUTLOOK_USER', False),
    ('Outlook Password', 'OUTLOOK_PASSWORD', False),
    ('Telegram Bot Token', 'TELEGRAM_BOT_TOKEN', False),
    ('Telegram Chat ID', 'TELEGRAM_CHAT_ID', False),
    ('Supabase URL', 'SUPABASE_URL', False),
    ('Supabase Key', 'SUPABASE_KEY', False),
]

for name, key, required in checks:
    value = os.getenv(key, '')
    if value:
        if 'KEY' in key or 'PASSWORD' in key or 'SECRET' in key:
            masked = value[:8] + '...'
        else:
            masked = value
        print(f'  [OK] {name}: {masked}')
    else:
        if required:
            print(f'  [!!] {name}: REQUIRED - NOT SET')
        else:
            print(f'  [--] {name}: Not configured (optional)')

print('=' * 60)
print('Configuration check complete!')
"
pause
goto:end

:end
echo.
echo ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo [COMPLETE] Session finished!
echo ═══════════════════════════════════════════════════════════════════════════════════════════════════════════════
pause
