# 🚀 GitHub Push Helper Script
# This script automatically commits and pushes your code to GitHub

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📦 GITHUB PUSH HELPER" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git is not installed!" -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""

# Check if we're in a Git repository
if (-not (Test-Path ".git")) {
    Write-Host "⚠️  Not a Git repository!" -ForegroundColor Yellow
    Write-Host ""
    $init = Read-Host "Do you want to initialize Git? (y/n)"
    if ($init -eq "y") {
        git init
        Write-Host "✅ Git initialized" -ForegroundColor Green
    } else {
        Write-Host "❌ Cannot proceed without Git repository" -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
}

Write-Host ""

# Check for remote
$remotes = git remote -v 2>$null
if (-not $remotes) {
    Write-Host "⚠️  No Git remote configured!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "You need to add a GitHub repository." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://github.com/new" -ForegroundColor Gray
    Write-Host "2. Create a new repository (e.g., Sam_Job_Automator)" -ForegroundColor Gray
    Write-Host "3. Copy the repository URL" -ForegroundColor Gray
    Write-Host ""
    
    $addRemote = Read-Host "Do you want to add a remote now? (y/n)"
    if ($addRemote -eq "y") {
        $remoteUrl = Read-Host "Enter your GitHub repository URL (e.g., https://github.com/username/repo.git)"
        if ($remoteUrl) {
            git remote add origin $remoteUrl
            Write-Host "✅ Remote added: $remoteUrl" -ForegroundColor Green
        } else {
            Write-Host "❌ No URL provided" -ForegroundColor Red
            Write-Host ""
            Write-Host "Press any key to exit..." -ForegroundColor Gray
            $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
            exit 1
        }
    } else {
        Write-Host "❌ Cannot proceed without remote" -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 1
    }
} else {
    Write-Host "✅ Git remote configured:" -ForegroundColor Green
    Write-Host $remotes -ForegroundColor Gray
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "📋 CHECKING STATUS" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check status
$status = git status --porcelain
if ($status) {
    Write-Host "📝 Uncommitted changes found:" -ForegroundColor Yellow
    Write-Host ""
    git status --short
    Write-Host ""
} else {
    Write-Host "✅ No uncommitted changes" -ForegroundColor Green
    Write-Host ""
    $pushOnly = Read-Host "Do you want to push existing commits? (y/n)"
    if ($pushOnly -eq "y") {
        Write-Host ""
        Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow
        git push -u origin main 2>&1
        if ($LASTEXITCODE -ne 0) {
            git push -u origin master 2>&1
        }
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Pushed successfully!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Push failed. Check your credentials." -ForegroundColor Yellow
        }
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 0
    } else {
        Write-Host "❌ Nothing to do" -ForegroundColor Red
        Write-Host ""
        Write-Host "Press any key to exit..." -ForegroundColor Gray
        $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
        exit 0
    }
}

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "💾 COMMITTING CHANGES" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Get commit message
Write-Host "Enter commit message (or press Enter for default):" -ForegroundColor Yellow
$commitMsg = Read-Host
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Update: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
}

Write-Host ""
Write-Host "📦 Adding all files..." -ForegroundColor Yellow
git add .

Write-Host "💾 Committing with message: $commitMsg" -ForegroundColor Yellow
git commit -m $commitMsg

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Committed successfully!" -ForegroundColor Green
} else {
    Write-Host "⚠️  Commit failed" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Press any key to exit..." -ForegroundColor Gray
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🚀 PUSHING TO GITHUB" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "🚀 Pushing to GitHub..." -ForegroundColor Yellow

# Try main branch first
git push -u origin main 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Main branch failed, trying master..." -ForegroundColor Yellow
    git push -u origin master 2>&1
}

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "✅ SUCCESS!" -ForegroundColor Green
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Your code is now on GitHub!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Go to: https://render.com" -ForegroundColor Cyan
    Write-Host "2. Sign in with GitHub" -ForegroundColor Cyan
    Write-Host "3. Create a new Web Service" -ForegroundColor Cyan
    Write-Host "4. Select your repository" -ForegroundColor Cyan
    Write-Host "5. Deploy!" -ForegroundColor Cyan
    Write-Host ""
    
    $openRender = Read-Host "Do you want to open Render.com now? (y/n)"
    if ($openRender -eq "y") {
        Start-Process "https://render.com"
        Write-Host "✅ Browser opened" -ForegroundColor Green
    }
} else {
    Write-Host ""
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host "⚠️  PUSH FAILED" -ForegroundColor Yellow
    Write-Host "============================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Possible reasons:" -ForegroundColor Yellow
    Write-Host "1. You need to authenticate with GitHub" -ForegroundColor Gray
    Write-Host "2. The repository doesn't exist" -ForegroundColor Gray
    Write-Host "3. You don't have permission to push" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Solutions:" -ForegroundColor Yellow
    Write-Host "1. Set up GitHub authentication:" -ForegroundColor Cyan
    Write-Host "   git config --global user.name 'Your Name'" -ForegroundColor Gray
    Write-Host "   git config --global user.email 'your@email.com'" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Or use GitHub Desktop (easier):" -ForegroundColor Cyan
    Write-Host "   Download from: https://desktop.github.com" -ForegroundColor Gray
    Write-Host ""
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
