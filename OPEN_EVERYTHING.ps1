# Open Everything for Deployment

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Opening Everything You Need" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. Open Environment Variables file
Write-Host "1. Opening Environment Variables..." -ForegroundColor Yellow
if (Test-Path "render_env_vars.txt") {
    Start-Process notepad.exe "render_env_vars.txt"
    Write-Host "   Done - Notepad opened" -ForegroundColor Green
} else {
    Write-Host "   ERROR: File not found!" -ForegroundColor Red
}

Start-Sleep -Seconds 2

# 2. Copy to clipboard
Write-Host ""
Write-Host "2. Copying to clipboard..." -ForegroundColor Yellow
try {
    $content = Get-Content "render_env_vars.txt" -Raw
    $content | Set-Clipboard
    Write-Host "   Done - Ready to paste!" -ForegroundColor Green
} catch {
    Write-Host "   Warning: Could not copy" -ForegroundColor Yellow
}

Start-Sleep -Seconds 2

# 3. Open Render.com
Write-Host ""
Write-Host "3. Opening Render.com..." -ForegroundColor Yellow
Start-Process "https://render.com"
Write-Host "   Done - Browser opened" -ForegroundColor Green

Start-Sleep -Seconds 2

# 4. Show instructions
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  NEXT STEPS" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "On Render.com:" -ForegroundColor Yellow
Write-Host "1. Sign in with GitHub" -ForegroundColor White
Write-Host "2. Click New + > Web Service" -ForegroundColor White
Write-Host "3. Select: Sam_Job_Automator" -ForegroundColor White
Write-Host "4. Fill:" -ForegroundColor White
Write-Host "   Name: sam-job-automator" -ForegroundColor Gray
Write-Host "   Region: Frankfurt" -ForegroundColor Gray
Write-Host "   Build: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   Start: python run.py" -ForegroundColor Gray
Write-Host "5. Add Environment Variables from Notepad" -ForegroundColor White
Write-Host "6. Click Create Web Service" -ForegroundColor White
Write-Host "7. Wait 3 minutes" -ForegroundColor White
Write-Host "8. Test: Send /start to @samcvbot" -ForegroundColor White
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
