# 🚀 Render.com Deployment Helper Script
# This script helps you deploy to Render.com automatically

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🚀 RENDER.COM DEPLOYMENT HELPER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "🔍 Checking prerequisites..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📋 DEPLOYMENT CHECKLIST" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if repository is initialized
if (Test-Path ".git") {
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "⚠️  Git repository not initialized" -ForegroundColor Yellow
    $initGit = Read-Host "Do you want to initialize Git? (y/n)"
    if ($initGit -eq "y") {
        git init
        Write-Host "✅ Git initialized" -ForegroundColor Green
    }
}

# Check if remote is set
$remotes = git remote -v 2>$null
if ($remotes) {
    Write-Host "✅ Git remote configured:" -ForegroundColor Green
    Write-Host $remotes -ForegroundColor Gray
} else {
    Write-Host "⚠️  No Git remote configured" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To add a remote, run:" -ForegroundColor Yellow
    Write-Host "git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git" -ForegroundColor Cyan
    Write-Host ""
    $addRemote = Read-Host "Do you want to add a remote now? (y/n)"
    if ($addRemote -eq "y") {
        $remoteUrl = Read-Host "Enter your GitHub repository URL"
        git remote add origin $remoteUrl
        Write-Host "✅ Remote added" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📦 PREPARING FOR DEPLOYMENT" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if there are uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "⚠️  You have uncommitted changes" -ForegroundColor Yellow
    Write-Host ""
    $commit = Read-Host "Do you want to commit all changes? (y/n)"
    if ($commit -eq "y") {
        git add .
        $commitMsg = Read-Host "Enter commit message (or press Enter for default)"
        if ([string]::IsNullOrWhiteSpace($commitMsg)) {
            $commitMsg = "Deploy to Render.com - $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
        }
        git commit -m $commitMsg
        Write-Host "✅ Changes committed" -ForegroundColor Green
    }
} else {
    Write-Host "✅ No uncommitted changes" -ForegroundColor Green
}

# Push to GitHub
Write-Host ""
$push = Read-Host "Do you want to push to GitHub? (y/n)"
if ($push -eq "y") {
    Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
    try {
        git push -u origin main 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Pushed to GitHub successfully" -ForegroundColor Green
        } else {
            # Try master branch if main fails
            git push -u origin master 2>&1
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✅ Pushed to GitHub successfully (master branch)" -ForegroundColor Green
            } else {
                Write-Host "⚠️  Push failed. You may need to authenticate with GitHub." -ForegroundColor Yellow
            }
        }
    } catch {
        Write-Host "⚠️  Push failed: $_" -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🌐 RENDER.COM DEPLOYMENT INSTRUCTIONS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Now follow these steps on Render.com:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Go to: https://render.com" -ForegroundColor Cyan
Write-Host "2. Sign in with GitHub" -ForegroundColor Cyan
Write-Host "3. Click 'New +' → 'Web Service'" -ForegroundColor Cyan
Write-Host "4. Select your repository: Sam_Job_Automator" -ForegroundColor Cyan
Write-Host "5. Configure:" -ForegroundColor Cyan
Write-Host "   - Name: sam-job-automator" -ForegroundColor Gray
Write-Host "   - Region: Frankfurt" -ForegroundColor Gray
Write-Host "   - Build Command: pip install -r requirements.txt" -ForegroundColor Gray
Write-Host "   - Start Command: python run.py" -ForegroundColor Gray
Write-Host "   - Instance Type: Free" -ForegroundColor Gray
Write-Host ""

Write-Host "6. Add Environment Variables (copy from below):" -ForegroundColor Cyan
Write-Host ""

# Read .env file and display
if (Test-Path ".env") {
    Write-Host "📋 Environment Variables from .env file:" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Gray
    
    $envContent = Get-Content ".env" | Where-Object { 
        $_ -notmatch "^#" -and 
        $_ -notmatch "^$" -and
        $_ -match "=" 
    }
    
    $criticalVars = @(
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "GROQ_API_KEY",
        "GEMINI_API_KEY",
        "ZOHO_SMTP_USER",
        "ZOHO_APP_PASSWORD",
        "GMAIL_SMTP_USER",
        "GMAIL_APP_PASSWORD",
        "USE_AI_ANALYSIS",
        "VERBOSE_LOGGING",
        "MAX_PARALLEL_STRIKES",
        "KEEP_ALIVE_ENABLED"
    )
    
    foreach ($line in $envContent) {
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            
            if ($criticalVars -contains $key) {
                Write-Host "$key=$value" -ForegroundColor Green
            }
        }
    }
    
    Write-Host "============================================" -ForegroundColor Gray
    Write-Host ""
    Write-Host "✅ Copy these variables to Render.com Environment section" -ForegroundColor Green
} else {
    Write-Host "⚠️  .env file not found" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "7. Click 'Create Web Service'" -ForegroundColor Cyan
Write-Host "8. Wait 2-3 minutes for deployment" -ForegroundColor Cyan
Write-Host "9. Test your bot: Send /start to @samcvbot on Telegram" -ForegroundColor Cyan
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🎉 READY TO DEPLOY!" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Open Render.com in browser
$openBrowser = Read-Host "Do you want to open Render.com in your browser? (y/n)"
if ($openBrowser -eq "y") {
    Start-Process "https://render.com"
    Write-Host "✅ Browser opened" -ForegroundColor Green
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📱 AFTER DEPLOYMENT" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Test your bot on Telegram:" -ForegroundColor Yellow
Write-Host "1. Open Telegram" -ForegroundColor Cyan
Write-Host "2. Search for: @samcvbot" -ForegroundColor Cyan
Write-Host "3. Send: /start" -ForegroundColor Cyan
Write-Host "4. If bot responds: ✅ Success!" -ForegroundColor Green
Write-Host "5. Turn off your PC - bot runs 24/7 on cloud!" -ForegroundColor Green
Write-Host ""

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "✅ SCRIPT COMPLETED" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Save environment variables to a separate file for easy copying
$envVarsFile = "render_env_vars.txt"
if (Test-Path ".env") {
    Write-Host "💾 Saving environment variables to: $envVarsFile" -ForegroundColor Yellow
    
    $envContent = Get-Content ".env" | Where-Object { 
        $_ -notmatch "^#" -and 
        $_ -notmatch "^$" -and
        $_ -match "=" 
    }
    
    $criticalVars = @(
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "TELEGRAM_BOT_TOKEN",
        "TELEGRAM_CHAT_ID",
        "GROQ_API_KEY",
        "GEMINI_API_KEY",
        "ZOHO_SMTP_USER",
        "ZOHO_APP_PASSWORD",
        "GMAIL_SMTP_USER",
        "GMAIL_APP_PASSWORD",
        "USE_AI_ANALYSIS",
        "VERBOSE_LOGGING",
        "MAX_PARALLEL_STRIKES",
        "MAX_QUALIFIED_LEADS_PER_CYCLE",
        "KEEP_ALIVE_ENABLED",
        "AI_CACHE_ENABLED",
        "FOLLOWUP_ENABLED"
    )
    
    $output = @()
    $output += "# Environment Variables for Render.com"
    $output += "# Copy and paste these into Render.com Environment section"
    $output += "# Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
    $output += ""
    
    foreach ($line in $envContent) {
        $parts = $line -split "=", 2
        if ($parts.Count -eq 2) {
            $key = $parts[0].Trim()
            $value = $parts[1].Trim()
            
            if ($criticalVars -contains $key) {
                $output += "$key=$value"
            }
        }
    }
    
    $output | Out-File -FilePath $envVarsFile -Encoding UTF8
    Write-Host "✅ Environment variables saved to: $envVarsFile" -ForegroundColor Green
    Write-Host "   Open this file and copy the variables to Render.com" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
