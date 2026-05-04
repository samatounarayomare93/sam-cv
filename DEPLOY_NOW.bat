@echo off
chcp 65001 >nul
color 0A

echo ========================================
echo 🚀 RENDER.COM DEPLOYMENT HELPER
echo ========================================
echo.

echo 📤 Pushing code to GitHub...
git add .
git commit -m "Ready for Render deployment"
git push origin main

echo.
echo ========================================
echo ✅ CODE PUSHED TO GITHUB!
echo ========================================
echo.
echo 📋 NEXT STEPS:
echo.
echo 1️⃣ Notepad will open with Environment Variables
echo 2️⃣ Browser will open Render.com
echo 3️⃣ On Render.com:
echo    • Click "New +" → "Web Service"
echo    • Select: Sam_Job_Automator
echo    • Name: sam-job-automator
echo    • Region: Frankfurt
echo    • Build: pip install -r requirements.txt
echo    • Start: python run.py
echo    • Instance: Free
echo    • Add Environment Variables from Notepad
echo    • Click "Create Web Service"
echo.
echo 4️⃣ Wait 2-3 minutes
echo 5️⃣ Test: Send /start to @samcvbot
echo 6️⃣ Turn off PC! Bot runs 24/7! 🎉
echo.
echo ========================================
echo.

timeout /t 3 >nul

echo 📝 Opening Environment Variables...
start notepad.exe render_env_vars.txt

timeout /t 2 >nul

echo 🌐 Opening Render.com...
start https://render.com

echo.
echo ========================================
echo ✅ EVERYTHING IS READY!
echo ========================================
echo.
echo Follow the steps above to deploy!
echo.
pause
