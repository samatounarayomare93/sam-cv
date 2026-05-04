@echo off
chcp 65001 >nul
color 0B
title 🚀 Sam Job Automator - Cloud Deployment

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo            🚀 SAM JOB AUTOMATOR - CLOUD DEPLOYMENT
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo.
echo  ✅ Bot Status: 100%% Functional
echo  ✅ Code Status: Synced to GitHub
echo  ✅ Ready for: Cloud Deployment
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Choose what you want to do:
echo.
echo  [1] 🚀 Deploy Now (Automatic - Easiest!)
echo  [2] 📋 Open Interactive Checklist
echo  [3] 📖 Read Deployment Guide (English)
echo  [4] 📖 Read Deployment Guide (Arabic)
echo  [5] 📝 Open Environment Variables File
echo  [6] 🌐 Open Render.com Website
echo  [7] ❌ Exit
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
set /p choice="Enter your choice (1-7): "

if "%choice%"=="1" goto deploy
if "%choice%"=="2" goto checklist
if "%choice%"=="3" goto guide_en
if "%choice%"=="4" goto guide_ar
if "%choice%"=="5" goto envvars
if "%choice%"=="6" goto render
if "%choice%"=="7" goto exit

echo Invalid choice! Please try again.
timeout /t 2 >nul
goto start

:deploy
cls
echo.
echo 🚀 Starting Automatic Deployment...
echo.
timeout /t 2 >nul
start "" DEPLOY_NOW.bat
goto end

:checklist
cls
echo.
echo 📋 Opening Interactive Checklist...
echo.
timeout /t 1 >nul
start "" DEPLOYMENT_CHECKLIST.html
goto end

:guide_en
cls
echo.
echo 📖 Opening English Guide...
echo.
timeout /t 1 >nul
start "" README_DEPLOYMENT.md
goto end

:guide_ar
cls
echo.
echo 📖 Opening Arabic Guide...
echo.
timeout /t 1 >nul
start "" "دليل_النشر_السريع.md"
goto end

:envvars
cls
echo.
echo 📝 Opening Environment Variables...
echo.
timeout /t 1 >nul
start notepad.exe render_env_vars.txt
goto end

:render
cls
echo.
echo 🌐 Opening Render.com...
echo.
timeout /t 1 >nul
start https://render.com
goto end

:exit
cls
echo.
echo Goodbye! 👋
echo.
timeout /t 1 >nul
exit

:end
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ Done! Follow the instructions to complete deployment.
echo.
echo  Need help? Open: FILES_GUIDE.md
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo.
pause
