@echo off
chcp 65001 >nul
color 0E
title RITA - SYSTEM HEALTH CHECK

echo.
echo  ═══════════════════════════════════════════════════════
echo   RITA JOB AUTOMATOR - HEALTH CHECK
echo  ═══════════════════════════════════════════════════════
echo.

:: Check Python
echo [1/8] Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo     [FAIL] Python not found!
    goto :failed
) else (
    python --version >nul 2>&1
    echo     [OK] Python installed
)

:: Check dependencies
echo.
echo [2/8] Checking dependencies...
python -c "import requests; import bs4; import fpdf" 2>nul
if %errorlevel% neq 0 (
    echo     [FAIL] Core dependencies missing!
    echo     Run: pip install requests beautifulsoup4 fpdf2
    goto :failed
) else (
    echo     [OK] Core dependencies installed
)

:: Check optional dependencies
python -c "import telegram; import tenacity; import duckduckgo_search" 2>nul
if %errorlevel% neq 0 (
    echo     [WARN] Some optional dependencies missing
    echo     Run: pip install python-telegram-bot tenacity duckduckgo-search
) else (
    echo     [OK] All optional dependencies installed
)

:: Check configuration
echo.
echo [3/8] Checking configuration files...
if not exist config.py (
    echo     [FAIL] config.py not found!
    goto :failed
) else (
    echo     [OK] config.py exists
)

if not exist .env (
    echo     [WARN] .env file not found!
) else (
    echo     [OK] .env file exists
)

:: Check directories
echo.
echo [4/8] Checking directories...
for %%d in (logs pdf_cache recovery recovery\runtime_backups) do (
    if not exist %%d (
        mkdir %%d 2>nul
        echo     [CREATED] %%d
    ) else (
        echo     [OK] %%d exists
    )
)

:: Check critical files
echo.
echo [5/8] Checking critical modules...
for %%m in (database scraper smtp_engine system_health self_healer ai_agent pdf_generator uplink) do (
    if not exist %%m.py (
        echo     [FAIL] %%m.py not found!
        set FAILED=1
    ) else (
        echo     [OK] %%m.py exists
    )
)

:: Test imports
echo.
echo [6/8] Testing module imports...
python -c "
import sys
sys.path.insert(0, '.')
try:
    import config
    print('     [OK] config imported')
except Exception as e:
    print(f'     [FAIL] config: {e}')

try:
    import database
    print('     [OK] database imported')
except Exception as e:
    print(f'     [FAIL] database: {e}')

try:
    import scraper
    print('     [OK] scraper imported')
except Exception as e:
    print(f'     [FAIL] scraper: {e}')
" 2>nul

:: Check credentials
echo.
echo [7/8] Checking credentials...
python -c "
import os
from dotenv import load_dotenv
load_dotenv()

brevo = os.getenv('BREVO_API_KEY', '')
telegram = os.getenv('TELEGRAM_BOT_TOKEN', '')

if brevo and brevo != 'your_brevo_api_key':
    print('     [OK] Brevo API configured')
else:
    print('     [WARN] Brevo API not configured')

if telegram and telegram != 'your-telegram-bot-token':
    print('     [OK] Telegram configured')
else:
    print('     [WARN] Telegram not configured')
" 2>nul

:: Network test
echo.
echo [8/8] Testing network connectivity...
python -c "
import requests
try:
    r = requests.get('https://www.google.com', timeout=5)
    print('     [OK] Internet connection working')
except Exception as e:
    print(f'     [WARN] Internet may not be available: {e}')
" 2>nul

echo.
echo  ═══════════════════════════════════════════════════════
echo   HEALTH CHECK COMPLETE
echo  ═══════════════════════════════════════════════════════
echo.
echo Summary:
echo   - All checks passed: Ready to run
echo   - Warnings indicate optional features
echo   - Failures need to be fixed before running
echo.
echo Press any key to exit...
pause >nul
goto :end

:failed
echo.
echo  ═══════════════════════════════════════════════════════
echo   HEALTH CHECK FAILED
echo  ═══════════════════════════════════════════════════════
echo.
echo Please fix the issues above before running RITA.
echo.
pause

:end
