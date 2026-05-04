@echo off
chcp 65001 >nul
color 0A
title 🤖 Automatic Deployment

cls
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo            🤖 AUTOMATIC RENDER.COM DEPLOYMENT
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  This script will:
echo  ✅ Open browser automatically
echo  ✅ Navigate to Render.com
echo  ✅ Fill in ALL form fields
echo  ✅ Add environment variables
echo  ✅ Deploy your bot!
echo.
echo  You only need to:
echo  ⚠️ Sign in to GitHub once (30 seconds)
echo.
echo  After that, everything is AUTOMATIC!
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo  Press any key to start...
pause >nul

echo.
echo 🚀 Starting automation...
echo.

.\.sovereign_runtime\python.exe auto_deploy_render.py

echo.
echo ═══════════════════════════════════════════════════════════════
echo  ✅ DONE!
echo ═══════════════════════════════════════════════════════════════
echo.
pause
