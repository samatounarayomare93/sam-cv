@echo off
title RITA ULTIMATE - WORLDWIDE MAX POWER ENGINE
color 0A
mode con:cols=100 lines=50
cls

echo.
echo  ████████╗██╗  ██╗███████╗    ██╗  ██╗██╗   ██╗███████╗████████╗███████╗███╗   ███╗
echo  ╚══██╔══╝██║  ██║██╔════╝    ██║ ██╔╝╚██╗ ██╔╝██╔════╝╚══██╔══╝██╔════╝████╗ ████║
echo     ██║   ███████║█████╗      █████╔╝  ╚████╔╝ ███████╗   ██║   █████╗  ██╔████╔██║
echo     ██║   ██╔══██║██╔══╝      ██╔═██╗   ╚██╔╝  ╚════██║   ██║   ██╔══╝  ██║╚██╔╝██║
echo     ██║   ██║  ██║███████╗    ██║  ██╗   ██║   ███████║   ██║   ███████╗██║ ╚═╝ ██║
echo     ╚═╝   ╚═╝  ╚═╝╚══════╝    ╚═╝  ╚═╝   ╚═╝   ╚══════╝   ╚═╝   ╚══════╝╚═╝     ╚═╝
echo.
echo  ███╗   ███╗██╗██████╗ ███╗   ██╗██╗ ██████╗ ██╗  ██╗████████╗
echo  ████╗ ████║██║██╔══██╗████╗  ██║██║██╔════╝ ██║  ██║╚══██╔══╝
echo  ██╔████╔██║██║██████╔╝██╔██╗ ██║██║██║  ███╗███████║   ██║   
echo  ██║╚██╔╝██║██║██╔═══╝ ██║╚██╗██║██║██║   ██║██╔══██║   ██║   
echo  ██║ ╚═╝ ██║██║██║     ██║ ╚████║██║╚██████╔╝██║  ██║   ██║   
echo  ╚═╝     ╚═╝╚═╝╚═╝     ╚═╝  ╚═══╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   
echo.
echo  ═══════════════════════════════════════════════════════════════════════════
echo                        ULTIMATE WORLDWIDE MAX POWER ENGINE
echo  ═══════════════════════════════════════════════════════════════════════════
echo.
echo  [CONFIGURATION]
echo  ┌──────────────────────────────────────────────────────────────────────┐
echo  │  Countries:        ALL 195 Countries Worldwide                       │
echo  │  Platforms:       50+ Job Boards                                   │
echo  │  SMTP Providers:  15+ Email Services                               │
echo  │  Social Networks: LinkedIn, Twitter, Facebook, Instagram            │
echo  │  Job Groups:      WhatsApp, Telegram, Discord, Facebook            │
echo  │  Daily Target:     500+ Applications                               │
echo  └──────────────────────────────────────────────────────────────────────┘
echo.
echo  [COUNTRIES COVERED]
echo  ┌──────────────────────────────────────────────────────────────────────┐
echo  │  EUROPE:        UK, Germany, France, Spain, Italy, Netherlands...   │
echo  │  NORTH AMERICA: USA, Canada, Mexico, Caribbean...                   │
echo  │  ASIA:          China, Japan, Korea, India, Singapore, UAE...         │
echo  │  MIDDLE EAST:   Dubai, Saudi, Qatar, Kuwait, Oman, Bahrain...        │
echo  │  RUSSIA/CIS:    Russia, Ukraine, Kazakhstan, Uzbekistan...           │
echo  │  AFRICA:        South Africa, Nigeria, Egypt, Kenya, Morocco...      │
echo  │  OCEANIA:       Australia, New Zealand, Pacific Islands...           │
echo  │  SOUTH AMERICA: Brazil, Argentina, Chile, Colombia, Peru...          │
echo  └──────────────────────────────────────────────────────────────────────┘
echo.
echo  [PLATFORMS]
echo  ┌──────────────────────────────────────────────────────────────────────┐
echo  │  Job Boards:     LinkedIn, Indeed, Glassdoor, Monster, ZipRecruiter│
echo  │  Regional:        InfoJobs, StepStone, Naukri, 51job, HH.ru...        │
echo  │  Social:          LinkedIn, Twitter, Facebook, Reddit, Quora...       │
echo  │  Messaging:       WhatsApp, Telegram, Discord Groups...               │
echo  │  Email:          Gmail, Outlook, Yahoo, Brevo, SendGrid, Mailgun...   │
echo  └──────────────────────────────────────────────────────────────────────┘
echo.
echo  [WARNING] This will send MAXIMUM applications to companies worldwide!
echo.
echo  Press any key to START the Ultimate Engine...
pause >nul
cls

echo.
echo [INIT] Initializing Ultimate Engine...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.8+
    pause
    exit /b 1
)

REM Activate virtual environment if exists
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
    echo [OK] Virtual environment activated
)

REM Install dependencies if needed
echo [CHECK] Installing dependencies...
pip install requests beautifulsoup4 duckduckgo-search -q 2>nul

REM Set environment
set PYTHONPATH=%CD%
set MAX_POWER=true

echo.
echo [LAUNCH] Starting Ultimate Engine...
echo ═══════════════════════════════════════════════════════════════════════════
echo.

REM Run Ultimate Engine
python ultimate_engine.py

echo.
echo ═══════════════════════════════════════════════════════════════════════════
echo [COMPLETE] Ultimate Engine session finished!
echo.
pause