# 🚀 Automatic Deployment Helper
# This script does EVERYTHING possible automatically

Write-Host ""
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "       🚀 AUTOMATIC DEPLOYMENT HELPER 🚀" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Step 1: Open render_env_vars.txt
Write-Host "📋 Step 1: Opening Environment Variables file..." -ForegroundColor Yellow
if (Test-Path "render_env_vars.txt") {
    Start-Process notepad.exe "render_env_vars.txt"
    Write-Host "✅ File opened in Notepad" -ForegroundColor Green
    Write-Host "   Keep this window open - you'll need to copy from it" -ForegroundColor Gray
} else {
    Write-Host "❌ render_env_vars.txt not found!" -ForegroundColor Red
    Write-Host "   Run SIMPLE_DEPLOY.bat first" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Start-Sleep -Seconds 2

# Step 2: Open Render.com
Write-Host "🌐 Step 2: Opening Render.com..." -ForegroundColor Yellow
Start-Process "https://render.com"
Write-Host "✅ Render.com opened in browser" -ForegroundColor Green

Write-Host ""
Start-Sleep -Seconds 3

# Step 3: Show instructions
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "       📝 FOLLOW THESE STEPS" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "On Render.com:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Sign in with GitHub" -ForegroundColor White
Write-Host ""
Write-Host "2. Click 'New +' → 'Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "3. Select repository: Sam_Job_Automator" -ForegroundColor White
Write-Host ""
Write-Host "4. Fill in:" -ForegroundColor White
Write-Host "   Name: sam-job-automator" -ForegroundColor Gray
Write-Host "   Region: Frankfurt" -ForegroundColor Gray
Write-Host "   Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   Start Command: python run.py" -ForegroundColor Gray
Write-Host "   Instance Type: Free" -ForegroundColor Gray
Write-Host ""
Write-Host "5. Add Environment Variables:" -ForegroundColor White
Write-Host "   - Click 'Add Environment Variable'" -ForegroundColor Gray
Write-Host "   - Copy from the Notepad window (render_env_vars.txt)" -ForegroundColor Gray
Write-Host "   - Paste each line (Key = Value)" -ForegroundColor Gray
Write-Host ""
Write-Host "6. Click 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "7. Wait 2-3 minutes for deployment" -ForegroundColor White
Write-Host ""
Write-Host "8. Test your bot:" -ForegroundColor White
Write-Host "   - Open Telegram" -ForegroundColor Gray
Write-Host "   - Send /start to @samcvbot" -ForegroundColor Gray
Write-Host "   - If bot responds: ✅ Success!" -ForegroundColor Green
Write-Host ""
Write-Host "9. Turn off your PC! 💻❌" -ForegroundColor White
Write-Host "   Bot runs 24/7 on cloud!" -ForegroundColor Green
Write-Host ""

Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Step 4: Copy environment variables to clipboard
Write-Host "💡 Bonus: Copying environment variables to clipboard..." -ForegroundColor Yellow
try {
    $envContent = Get-Content "render_env_vars.txt" -Raw
    $envContent | Set-Clipboard
    Write-Host "✅ Environment variables copied to clipboard!" -ForegroundColor Green
    Write-Host "   You can paste them directly on Render.com" -ForegroundColor Gray
} catch {
    Write-Host "⚠️  Could not copy to clipboard (not critical)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "       ✅ READY TO DEPLOY!" -ForegroundColor Green
Write-Host "════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Windows are open:" -ForegroundColor Yellow
Write-Host "  1. Notepad with Environment Variables" -ForegroundColor Gray
Write-Host "  2. Browser with Render.com" -ForegroundColor Gray
Write-Host ""
Write-Host "Follow the steps above to complete deployment!" -ForegroundColor Yellow
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')
