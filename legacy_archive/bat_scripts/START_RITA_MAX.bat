@echo off
chcp 65001 >nul
color 0A
title RITA JOB AUTOMATOR - MAXIMUM POWER

echo.
echo  ██╗██████╗ ██╗██╗  ██╗██╗███████╗██╗  ██╗██╗   ██╗
echo  ██║██╔══██╗██║╚██╗██╔╝██║██╔════╝██║  ██║██║   ██║
echo  ██║██████╔╝██║ ╚███╔╝ ██║███████╗███████║██║   ██║
echo  ██║██╔═══╝ ██║ ██╔██╗ ██║╚════██║██╔══██║██║   ██║
echo  ██║██║     ██║██╔╝ ██╗██║███████║██║  ██║╚██████╔╝
echo  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝ ╚═════╝
echo.
echo  ═══════════════════════════════════════════════════════
echo   JOB AUTOMATOR v2 - MAXIMUM POWER EDITION
echo  ═══════════════════════════════════════════════════════
echo.

:: Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+
    echo [INFO] Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Get Python version
python --version

:: Check if pip is available
echo.
echo [INFO] Checking dependencies...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] pip not found, installing...
    python -m ensurepip --default-pip
)

:: Install required packages
echo.
echo [INFO] Installing/Updating dependencies...
python -m pip install --upgrade pip -q
python -m pip install python-dotenv requests beautifulsoup4 fpdf2 tenacity -q
python -m pip install python-telegram-bot duckduckgo-search -q
python -m pip install lxml html5lib -q

:: Check for .env file
if not exist .env (
    echo.
    echo [WARNING] .env file not found!
    echo [INFO] Creating default .env file...
    copy env.example .env >nul 2>&1
    if not exist env.example (
        echo # RITA Configuration > .env
        echo BREVO_API_KEY=your_brevo_api_key >> .env
        echo TELEGRAM_BOT_TOKEN=your_telegram_token >> .env
        echo TELEGRAM_CHAT_ID=your_chat_id >> .env
    )
    echo [INFO] Please edit .env with your credentials!
)

:: Check for CV file
if not exist Rita_Cordahi_CV.html (
    echo.
    echo [WARNING] CV file not found: Rita_Cordahi_CV.html
    echo [INFO] Please add your CV file to run the bot
)

:: Create necessary directories
if not exist logs mkdir logs
if not exist pdf_cache mkdir pdf_cache
if not exist recovery mkdir recovery
if not exist recovery\runtime_backups mkdir recovery\runtime_backups

:: Run health check
echo.
echo [INFO] Running system health check...
python -c "from self_healer import healer; h = healer.run_full_diagnostic(); print(f'    System Status: {h[\"overall\"]}')" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] Health check skipped (modules may be missing)
)

:: Show configuration status
echo.
echo [INFO] Configuration Status:
findstr /C:"BREVO_API_KEY" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo     [OK] Email Provider configured
) else (
    echo     [MISSING] Email Provider not configured
)

findstr /C:"TELEGRAM_BOT_TOKEN" .env >nul 2>&1
if %errorlevel% equ 0 (
    echo     [OK] Telegram configured
) else (
    echo     [MISSING] Telegram not configured
)

:: Launch the bot
echo.
echo [INFO] Starting RITA Job Automator...
echo ═══════════════════════════════════════════════════════
echo.
echo Press Ctrl+C to stop the bot
echo.
python main_bot.py
goto :end

:end
echo.
echo [INFO] RITA Job Automator stopped
pause
