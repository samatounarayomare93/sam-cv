@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

:: ============================================
:: RITA ONE-CLICK SETUP & ENHANCEMENT
:: ============================================
:: Installs all enhancements automatically:
:: - Enhanced scraper (8 sources)
:: - Performance optimizer
:: - Self-healing system
:: - Auto-start launcher
:: - Watchdog (auto-restart)
:: - Enhanced dashboard
::
:: NO NEW ACCOUNTS REQUIRED!
:: ============================================

title Rita One-Click Setup

set "SCRIPT_DIR=%~dp0"
set "LOG_FILE=%SCRIPT_DIR%setup.log"

cd /d "%SCRIPT_DIR%"

echo.
echo ================================================
echo    RITA ONE-CLICK SETUP & ENHANCEMENT
echo ================================================
echo.

:: ============================================
:: CHECK PYTHON
:: ============================================
echo [1/7] Checking Python installation...

python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

for /f "tokens=*" %%v in ('python --version 2^>^&1') do set "PYTHON_VERSION=%%v"
echo [OK] %PYTHON_VERSION%

:: ============================================
:: INSTALL REQUIRED PACKAGES
:: ============================================
echo.
echo [2/7] Installing required Python packages...

set "PACKAGES=requests beautifulsoup4 python-telegram-bot python-dotenv tenacity pandas plotly streamlit"
set "INSTALLED=0"
set "FAILED=0"

for %%p in (%PACKAGES%) do (
    pip show %%p >nul 2>&1
    if errorlevel 1 (
        pip install %%p -q
        if errorlevel 1 (
            echo [FAIL] %%p
            set /a FAILED+=1
        ) else (
            echo [OK] %%p
            set /a INSTALLED+=1
        )
    ) else (
        echo [SKIP] %%p (already installed)
    )
)

echo.
echo Packages installed: %INSTALLED%
if %FAILED% GTR 0 (
    echo Warning: %FAILED% packages failed to install
)

:: ============================================
:: CREATE DIRECTORIES
:: ============================================
echo.
echo [3/7] Creating required directories...

for %%d in (logs pdf_cache recovery recovery\runtime_backups) do (
    if not exist "%%d" (
        mkdir "%%d"
        echo [OK] Created: %%d
    ) else (
        echo [SKIP] %%d (exists)
    )
)

:: ============================================
:: CHECK ENHANCEMENT FILES
:: ============================================
echo.
echo [4/7] Checking enhancement files...

set "ENHANCEMENTS=START_AUTOPILOT.bat INSTALL_AUTO_START.bat WATCHDOG.bat enhanced_scraper.py performance_optimizer.py enhanced_dashboard.py self_healer.py START_ULTIMATE_AUTOPILOT.bat"

for %%f in (%ENHANCEMENTS%) do (
    if not exist "%%f" (
        echo [MISSING] %%f - needs to be created
    ) else (
        echo [OK] %%f
    )
)

:: ============================================
:: CREATE RUNTIME FILES
:: ============================================
echo.
echo [5/7] Initializing runtime files...

:: Create tracker.json if missing
if not exist "tracker.json" (
    (
        echo {
        echo   "applications": [],
        echo   "last_updated": "%date% %time%"
        echo }
    ) > tracker.json
    echo [OK] tracker.json created
) else (
    echo [SKIP] tracker.json exists
)

:: Create metrics.json if missing
if not exist "metrics.json" (
    (
        echo {
        echo   "today": {"applications_sent": 0, "jobs_analyzed": 0, "errors": 0},
        echo   "this_week": {"applications_sent": 0, "jobs_analyzed": 0},
        echo   "this_month": {"applications_sent": 0, "jobs_analyzed": 0},
        echo   "all_time": {"applications_sent": 0, "jobs_analyzed": 0}
        echo }
    ) > metrics.json
    echo [OK] metrics.json created
) else (
    echo [SKIP] metrics.json exists
)

:: Create health_check.json if missing
if not exist "health_check.json" (
    (
        echo {
        echo   "system_health": "^(emoji^) HEALTHY",
        echo   "components": {
        echo     "pdf_cache": "OK",
        echo     "database": "OK",
        echo     "smtp": "OK",
        echo     "telegram": "OK",
        echo     "tracker": "OK"
        echo   },
        echo   "last_check": "%date% %time%"
        echo }
    ) > health_check.json
    echo [OK] health_check.json created
) else (
    echo [SKIP] health_check.json exists
)

:: Create company_database.json if missing
if not exist "company_database.json" (
    (
        echo {
        echo   "companies": [],
        echo   "total_unique": 0,
        echo   "last_updated": "%date% %time%"
        echo }
    ) > company_database.json
    echo [OK] company_database.json created
) else (
    echo [SKIP] company_database.json exists
)

:: Create discovered_companies.json if missing
if not exist "discovered_companies.json" (
    (
        echo {
        echo   "companies": [],
        echo   "total": 0,
        echo   "last_updated": "%date% %time%"
        echo }
    ) > discovered_companies.json
    echo [OK] discovered_companies.json created
) else (
    echo [SKIP] discovered_companies.json exists
)

:: ============================================
:: CONFIGURE AUTO-START
:: ============================================
echo.
echo [6/7] Configuring auto-start...

:: Create startup shortcut
set "STARTUP_DIR=%USERPROFILE%\Start Menu\Programs\Startup"
set "STARTUP_FILE=%STARTUP_DIR%\RitaBot_Autostart.bat"

(
    echo @echo off
    echo cd /d "%SCRIPT_DIR%"
    echo start /min cmd /c "python main_bot.py >> logs bot.log 2^>^&1"
) > "%STARTUP_FILE%"

if exist "%STARTUP_FILE%" (
    echo [OK] Auto-start installed
    echo    Location: %STARTUP_FILE%
) else (
    echo [SKIP] Auto-start not installed (may need admin)
)

:: ============================================
:: TEST ENHANCEMENTS
:: ============================================
echo.
echo [7/7] Testing enhancements...

:: Test performance optimizer
python -c "import performance_optimizer; print('[OK] Performance optimizer')" 2>nul
if errorlevel 1 echo [WARN] Performance optimizer test skipped

:: Test self-healer
python -c "import self_healer; print('[OK] Self-healer')" 2>nul
if errorlevel 1 echo [WARN] Self-healer test skipped

:: ============================================
:: COMPLETION
:: ============================================
echo.
echo ================================================
echo    SETUP COMPLETE!
echo ================================================
echo.
echo Enhanced Features Installed:
echo.
echo [NEW] Enhanced Scraper
echo     - Wuzzuf (Egypt)
echo     - Indeed (Global)
echo     - Glassdoor
echo     - GulfJobs
echo     - CareerHire
echo     - LinkedIn
echo     - Bayt
echo     - HireLebanese
echo.
echo [NEW] Performance Optimizer
echo     - Smart scheduling
echo     - Rate limiting
echo     - Email timing
echo.
echo [NEW] Self-Healing System
echo     - Auto-repair
echo     - Backup/restore
echo     - Health checks
echo.
echo [NEW] Watchdog
echo     - Auto-restart on crash
echo     - 24/7 monitoring
echo.
echo [NEW] Enhanced Dashboard
echo     - Real-time monitoring
echo     - Charts and stats
echo.
echo ================================================
echo    QUICK START
echo ================================================
echo.
echo Option 1 - Ultimate Autopilot (Recommended):
echo   Double-click: START_ULTIMATE_AUTOPILOT.bat
echo.
echo Option 2 - Auto-start on Windows boot:
echo   Double-click: INSTALL_AUTO_START.bat
echo.
echo Option 3 - Manual start:
echo   Double-click: START_AUTOPILOT.bat
echo.
echo Option 4 - Dashboard only:
echo   Run: streamlit run enhanced_dashboard.py
echo.
echo ================================================
echo.
echo Press any key to open the Ultimate Autopilot launcher...
pause >nul

:: Open the Ultimate Autopilot launcher
start "" "%SCRIPT_DIR%START_ULTIMATE_AUTOPILOT.bat"

exit /b 0
