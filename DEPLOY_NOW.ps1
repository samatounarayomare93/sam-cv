# 🚀 DEPLOY NOW - One Click Deployment Helper
# This script opens everything you need to deploy to Render.com

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🚀 RENDER.COM DEPLOYMENT HELPER" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Push latest code to GitHub
Write-Host "📤 Step 1: Pushing latest code to GitHub..." -ForegroundColor Yellow
git add .
git commit -m "Ready for Render deployment - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Code pushed to GitHub successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️ Git push had some issues, but continuing..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "📋 WHAT TO DO NEXT:" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1️⃣ A Notepad window will open with your Environment Variables" -ForegroundColor White
Write-Host "2️⃣ Your browser will open Render.com" -ForegroundColor White
Write-Host "3️⃣ Follow these steps on Render.com:" -ForegroundColor White
Write-Host ""
Write-Host "   ▶ Click 'New +' → 'Web Service'" -ForegroundColor Cyan
Write-Host "   ▶ Select repository: Sam_Job_Automator" -ForegroundColor Cyan
Write-Host "   ▶ Fill in:" -ForegroundColor Cyan
Write-Host "      • Name: sam-job-automator" -ForegroundColor Gray
Write-Host "      • Region: Frankfurt" -ForegroundColor Gray
Write-Host "      • Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "      • Start Command: python run.py" -ForegroundColor Gray
Write-Host "      • Instance Type: Free" -ForegroundColor Gray
Write-Host ""
Write-Host "   ▶ Scroll to 'Environment Variables' section" -ForegroundColor Cyan
Write-Host "   ▶ Copy ALL variables from Notepad" -ForegroundColor Cyan
Write-Host "   ▶ Paste them in Render (one by one or use 'Add from .env')" -ForegroundColor Cyan
Write-Host "   ▶ Click 'Create Web Service'" -ForegroundColor Cyan
Write-Host ""
Write-Host "4️⃣ Wait 2-3 minutes for deployment" -ForegroundColor White
Write-Host "5️⃣ Test: Send /start to @samcvbot on Telegram" -ForegroundColor White
Write-Host "6️⃣ Turn off your PC! Bot runs 24/7 on cloud! 🎉" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Wait 3 seconds so user can read
Start-Sleep -Seconds 3

# Step 2: Open environment variables in Notepad
Write-Host ""
Write-Host "📝 Opening Environment Variables in Notepad..." -ForegroundColor Yellow
Start-Process notepad.exe -ArgumentList "render_env_vars.txt"

# Wait 2 seconds
Start-Sleep -Seconds 2

# Step 3: Open Render.com
Write-Host "🌐 Opening Render.com in your browser..." -ForegroundColor Yellow
Start-Process "https://render.com"

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ EVERYTHING IS READY!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Follow the steps above to complete deployment!" -ForegroundColor White
Write-Host ""
Write-Host "Need help? Open: ابدأ_الآن_START_NOW.md" -ForegroundColor Yellow
Write-Host ""

# Keep window open
Write-Host "Press any key to close this window..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
