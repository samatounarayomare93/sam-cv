@echo off
title RITA JOB AUTOMATOR - MAXIMUM POWER v2
color 0A
mode con:cols=130 lines=70
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
echo  ███████╗ ██████╗ ███╗   ██╗ █████╗ ██╗     ███████╗
echo  ██╔════╝██╔═══██╗████╗  ██║██╔══██╗██║     ██╔════╝
echo  ███████╗██║   ██║██╔██╗ ██║███████║██║     █████╗  
echo  ╚════██║██║   ██║██║╚██╗██║██╔══██║██║     ██╔══╝  
echo  ███████║╚██████╔╝██║ ╚████║██║  ██║███████╗███████╗
echo  ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝╚══════╝
echo.
echo  ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo                              RITA JOB AUTOMATOR - MAXIMUM POWER v2
echo  ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.
echo  [SYSTEM STATUS]
echo  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │  Telegram Dashboard.............. READY                                                          │
echo  │  Enhanced Scraper.............. READY (50+ sources)                                             │
echo  │  Email Engine.................. READY (Brevo + Gmail + Outlook)                                  │
echo  │  AI Filter..................... READY (Gemini + Groq)                                             │
echo  │  Auto-Retry System............. READY (Self-healing)                                             │
echo  │  Rate Limiting................. ACTIVE (Anti-ban protection)                                       │
echo  └────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  [SCRAPER SOURCES]
echo  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │  Lebanon:     Daleel Madani, HireLebanese                                                      │
echo  │  GCC:         Bayt, GulfTalent, Dubizzle, Wazajobs                                             │
echo  │  Global:      LinkedIn, Indeed, Glassdoor, Monster                                              │
echo  │  Email:       100+ patterns per company                                                        │
echo  │  Total:       50+ job sources worldwide                                                          │
echo  └────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  [TARGET SETTINGS]
echo  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │  Locations:   UAE, Saudi, Qatar, Kuwait, Oman, Bahrain, Lebanon, Europe, Americas             │
echo  │  Titles:      HR Manager, Operations, Recruiter, Admin, Office Manager, etc.                  │
echo  │  Salary:      Lebanon: $1500+, Global: $6000+                                                   │
echo  │  Keywords:     visa, sponsorship, relocation, housing, flight                                   │
echo  └────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.
echo  ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Install dependencies if needed
echo [CHECK] Installing dependencies...
pip install requests beautifulsoup4 python-dotenv tenacity duckduckgo-search -q 2>nul

REM Check environment file
if not exist ".env" (
    echo [WARNING] .env file not found! Creating template...
    (
        echo # Email Settings
        echo BREVO_API_KEY=your_brevo_api_key
        echo BREVO_SMTP_PASSWORD=your_brevo_smtp_password
        echo GMAIL_APP_PASSWORD=your_gmail_app_password
        echo.
        echo # Telegram
        echo TELEGRAM_BOT_TOKEN=your_telegram_bot_token
        echo TELEGRAM_CHAT_ID=your_chat_id
        echo.
        echo # AI
        echo GEMINI_API_KEY=your_gemini_api_key
        echo GROQ_API_KEY=your_groq_api_key
        echo.
        echo # Database
        echo SUPABASE_URL=your_supabase_url
        echo SUPABASE_KEY=your_supabase_key
    ) > .env
    echo [CREATED] .env template created! Please fill in your credentials.
)

echo.
echo  [SELECT MODE]
echo  ┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
echo  │  [1] FULL MODE         - Run with Telegram dashboard (Recommended)                                │
echo  │  [2] CONSOLE MODE      - Run without Telegram (for testing)                                      │
echo  │  [3] SCRAPER ONLY      - Test scraper without sending emails                                       │
echo  │  [4] CONFIG CHECK      - Verify configuration                                                    │
echo  │  [5] EXIT              - Quit                                                                    │
echo  └────────────────────────────────────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="Select mode (1-5): "

if "%choice%"=="1" goto:full
if "%choice%"=="2" goto:console
if "%choice%"=="3" goto:scraper
if "%choice%"=="4" goto:config
if "%choice%"=="5" exit

:full
echo.
echo [START] Running in FULL MODE with Telegram dashboard...
echo.
python main_bot.py
goto:end

:console
echo.
echo [START] Running in CONSOLE MODE...
echo.
python -c "import main_bot; import asyncio; asyncio.run(main_bot.console_scout_and_apply())"
goto:end

:scraper
echo.
echo [START] Testing Enhanced Scraper...
echo.
python enhanced_scraper.py
goto:end

:config
echo.
echo [CHECK] Verifying Configuration...
echo.
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

print('=' * 60)
print('RITA CONFIGURATION CHECK')
print('=' * 60)

checks = [
    ('Brevo API Key', bool(os.getenv('BREVO_API_KEY'))),
    ('Brevo SMTP Password', bool(os.getenv('BREVO_SMTP_PASSWORD'))),
    ('Gmail App Password', bool(os.getenv('GMAIL_APP_PASSWORD'))),
    ('Telegram Bot Token', bool(os.getenv('TELEGRAM_BOT_TOKEN'))),
    ('Telegram Chat ID', bool(os.getenv('TELEGRAM_CHAT_ID'))),
    ('Gemini API Key', bool(os.getenv('GEMINI_API_KEY'))),
    ('Groq API Key', bool(os.getenv('GROQ_API_KEY'))),
    ('Supabase URL', bool(os.getenv('SUPABASE_URL'))),
    ('Supabase Key', bool(os.getenv('SUPABASE_KEY'))),
]

all_ok = True
for name, ok in checks:
    status = 'OK' if ok else 'MISSING'
    print(f'  {name:.<40} {status}')
    if not ok:
        all_ok = False

print('=' * 60)
if all_ok:
    print('ALL CONFIGURATIONS SET! Ready to run.')
else:
    print('SOME CONFIGURATIONS MISSING! Update .env file.')
print('=' * 60)
"
pause
goto:end

:end
echo.
echo ════════════════════════════════════════════════════════════════════════════════════════════════════════════
echo [COMPLETE] Session finished!
echo ════════════════════════════════════════════════════════════════════════════════════════════════════════════
pause
