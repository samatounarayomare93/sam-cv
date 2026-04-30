@echo off
chcp 65001 >nul
color 0B

echo ============================================
echo 🚀 AUTOMATIC DEPLOYMENT HELPER
echo ============================================
echo.

echo This script will help you deploy to Render.com
echo.
echo What it does:
echo 1. Checks your Git setup
echo 2. Commits your changes
echo 3. Pushes to GitHub
echo 4. Opens Render.com for deployment
echo 5. Shows you the environment variables to copy
echo.

pause

echo.
echo ============================================
echo 📦 Running deployment script...
echo ============================================
echo.

powershell -ExecutionPolicy Bypass -File deploy_to_render.ps1

echo.
echo ============================================
echo ✅ Script completed!
echo ============================================
echo.

pause
