@echo off
chcp 65001 >nul
title 🚀 Rita Job Automator - Complete Setup
color 0A

echo ╔══════════════════════════════════════════════════════════════════╗
echo ║           🚀 RITA JOB AUTOMATOR - COMPLETE SETUP                 ║
echo ║              0 Investment  24/7 Cloud  Maximum Performance       ║
echo ╚══════════════════════════════════════════════════════════════════╝
echo.
echo This will setup everything automatically!
echo.
echo Requirements:
echo  - GitHub account (with repo: samatounarayomare93/sam-cv)
echo  - Render account (2 services)
echo  - Free API keys (Gemini, Telegram, Brevo)
echo.
echo.
pause

:: Check if PowerShell is available
where powershell >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ PowerShell not found! Please install PowerShell.
    pause
    exit /b 1
)

:: Run the setup script
echo.
echo 🚀 Starting setup...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0setup.ps1"

if %errorlevel% neq 0 (
    echo.
    echo ❌ Setup failed! Check errors above.
    pause
    exit /b 1
)

echo.
echo ✅ Setup complete!
echo.
pause
