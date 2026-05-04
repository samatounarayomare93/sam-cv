@echo off
chcp 65001 >nul
color 0A
title 🚀 Super Easy Deployment

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo            🚀 SUPER EASY DEPLOYMENT - 5 MINUTES
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo.
echo  ✅ Everything is ready!
echo  ✅ I will open everything you need!
echo  ✅ Just follow the steps!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Press any key to start...
echo.
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 1: Opening Environment Variables
echo ═══════════════════════════════════════════════════════════════
echo.
echo  📝 Notepad will open with ALL your environment variables
echo  📝 Keep this window open - you'll need to copy from it!
echo.
timeout /t 2 >nul

start notepad.exe render_env_vars.txt

echo  ✅ Notepad opened!
echo.
echo  Press any key to continue...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 2: Opening Render.com
echo ═══════════════════════════════════════════════════════════════
echo.
echo  🌐 Your browser will open Render.com
echo  🌐 Sign in with GitHub when it opens
echo.
timeout /t 2 >nul

start https://render.com

echo  ✅ Browser opened!
echo.
echo  Press any key to continue...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 3: What to do on Render.com
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Follow these steps EXACTLY:
echo.
echo  1️⃣ Click "Sign In" or "Get Started"
echo     → Choose "Continue with GitHub"
echo     → Approve permissions
echo.
echo  2️⃣ Click the blue "New +" button (top right)
echo     → Select "Web Service"
echo.
echo  3️⃣ Find and select your repository:
echo     → Look for: "Sam_Job_Automator" or "sam-cv"
echo     → Click "Connect"
echo.
echo  4️⃣ Fill in the form with these EXACT values:
echo.
echo     ┌─────────────────────────────────────────────────┐
echo     │ Name: sam-job-automator                         │
echo     │ Region: Frankfurt                               │
echo     │ Branch: main                                    │
echo     │ Build Command: pip install -r requirements.txt  │
echo     │ Start Command: python run.py                    │
echo     │ Instance Type: Free                             │
echo     └─────────────────────────────────────────────────┘
echo.
echo  Press any key to see Step 5...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 5: Add Environment Variables
echo ═══════════════════════════════════════════════════════════════
echo.
echo  This is the MOST IMPORTANT step!
echo.
echo  On Render.com:
echo  1️⃣ Scroll down to "Environment Variables" section
echo  2️⃣ Click "Add from .env" button
echo  3️⃣ Go to the Notepad window (still open)
echo  4️⃣ Press Ctrl+A (select all)
echo  5️⃣ Press Ctrl+C (copy)
echo  6️⃣ Go back to Render.com
echo  7️⃣ Click in the text box
echo  8️⃣ Press Ctrl+V (paste)
echo  9️⃣ Click "Add" button
echo.
echo  ✅ All 14 variables will be added automatically!
echo.
echo  Press any key to see Step 6...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 6: Deploy!
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1️⃣ Scroll to the top of the page
echo  2️⃣ Click the big blue button: "Create Web Service"
echo  3️⃣ Wait 2-3 minutes (you'll see logs moving)
echo  4️⃣ When you see "Live" in green → SUCCESS! ✅
echo.
echo  Press any key to see Step 7...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 7: Test Your Bot!
echo ═══════════════════════════════════════════════════════════════
echo.
echo  1️⃣ Open Telegram on your phone or computer
echo  2️⃣ Search for: @samcvbot
echo  3️⃣ Send: /start
echo  4️⃣ Bot should reply immediately!
echo.
echo  If bot replies → ✅ SUCCESS! Everything works!
echo  If bot doesn't reply → Wait 5 minutes and try again
echo.
echo  Press any key to see final step...
pause >nul

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo  STEP 8: Turn Off Your PC! 🎉
echo ═══════════════════════════════════════════════════════════════
echo.
echo  ✅ Your bot is now running 24/7 on the cloud!
echo  ✅ You can turn off your computer!
echo  ✅ Bot will keep working!
echo  ✅ You'll get notifications on Telegram!
echo.
echo  Useful Telegram Commands:
echo  • /start  - Start bot
echo  • /status - Check bot status
echo  • /stats  - See statistics
echo  • /test   - Run diagnostics
echo  • /help   - Show all commands
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  🎊 CONGRATULATIONS! 🎊
echo.
echo  Your bot is now:
echo  ✅ Finding jobs automatically
echo  ✅ Analyzing with AI
echo  ✅ Generating custom CVs
echo  ✅ Sending professional emails
echo  ✅ Running 24/7 on cloud!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Need help? Open: README_DEPLOYMENT.md
echo.
echo  Press any key to close...
pause >nul
