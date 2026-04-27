@echo off
title [🛰️ PROJECT CHRONOS: HIVE LAUNCHER] - Absolute Dominance
color 0B
echo ==========================================================
echo    PROJECT CHRONOS: PHASE SINGULARITY (THE HIVE)         
echo ==========================================================
echo.
echo [📡] INITIALIZING: Synchronizing swarm nodes...
echo.

REM 1. Start the Command Center (Dashboard)
echo [🖥️] RADAR: Starting Command Center Dashboard...
start "Project Chronos - Command Center" powershell -NoExit -Command "cd rita-command-center; npm run dev"

REM 2. Wait for Dashboard to warm up
timeout /t 5 /nobreak >nul

REM 3. Start the Robot Swarm (Main Bot)
echo [🤖] SWARM: Starting Autonomous Bot Hive...
start "Project Chronos - Swarm Hive" powershell -NoExit -Command ".\.sovereign_runtime\python.exe core/main_bot.py"

echo.
echo ==========================================================
echo [🛰️ ] SWARM IS LIVE. ABSOLUTE DOMINANCE ACHIEVED.
echo     Dashboard: http://localhost:3000
echo     Hive Mind: ACTIVE
echo ==========================================================
echo.
echo Press any key to shutdown the Launcher (processes will remain running).
pause >nul
