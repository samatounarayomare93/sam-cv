@echo off
title [👑 PROJECT CHRONOS: ABSOLUTE SINGULARITY]
color 0b

echo.
echo  ╔══════════════════════════════════════════════════╗
echo  ║  ███╗   ███╗██╗██╗██╗████████╗███████╗██╗ ██████╗ ║
echo  ║  ████╗ ████║██║██║██║╚══██╔══╝██╔════╝██║██╔═══██╗║
echo  ║  ██╔████╔██║██║██║██║   ██║   █████╗  ██║██║   ██║║
echo  ║  ██║╚██╔╝██║██║██║██║   ██║   ██╔══╝  ██║██║   ██║║
echo  ║  ██║ ╚═╝ ██║██║██║██║   ██║   ██║     ██║╚██████╔╝║
echo  ║  ╚═╝     ╚═╝╚═╝╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ║
echo  ╚══════════════════════════════════════════════════╝
echo.
echo           IGNITING ABSOLUTE SINGULARITY 3.0
echo.

:: 1. Cleanup old instances
echo [🛡️] AGENT: Scrubbing stale swarm nodes...
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /IM node.exe /T >nul 2>&1

:: 2. Launch the Telegram Command Center (New!)
echo [📱] TELEGRAM: Launching C2 Sovereign Interface...
start "Project Chronos - Telegram Bot" ".\.sovereign_runtime\python.exe" "launch_rita.py"

:: 3. Launch the Eternal Watchdog (Handles Scraping Swarm)
echo [👻] WATCHDOG: Initializing Resurrection Protocol...
start /min "Project Chronos - Watchdog" ".\.sovereign_runtime\python.exe" "core\watchdog.py"

:: 4. Launch the Sovereign Console (Web Dashboard)
echo [🖥️] CONSOLE: Synchronizing Neural UI...
cd rita-command-center
start /min "Project Chronos - Web Dashboard" cmd /c "npm run dev"
cd ..

:: 5. Launch Intelligence Handshake
echo [🌐] UPLINK: Opening Telegram Web...
start https://web.telegram.org/k/#@ritacv_bot

echo.
echo [✅] PROTOCOL: ABSOLUTE SINGULARITY ACTIVE.
echo [✅] EVERYTHING IS RUNNING AT 1,000,000,000,000,000%.
echo.
pause
