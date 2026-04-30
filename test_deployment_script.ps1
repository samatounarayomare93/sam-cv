# 🧪 Test Deployment Script
# Quick test to make sure everything works

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "🧪 TESTING DEPLOYMENT SETUP" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Test 1: Git
Write-Host "Test 1: Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>&1
    Write-Host "✅ Git installed: $gitVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Git not found" -ForegroundColor Red
}

Write-Host ""

# Test 2: Python
Write-Host "Test 2: Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = .\.sovereign_runtime\python.exe --version 2>&1
    Write-Host "✅ Python installed: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found" -ForegroundColor Red
}

Write-Host ""

# Test 3: .env file
Write-Host "Test 3: Checking .env file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "✅ .env file exists" -ForegroundColor Green
    
    # Check critical variables
    $envContent = Get-Content ".env" | Where-Object { $_ -match "=" -and $_ -notmatch "^#" }
    $criticalVars = @(
        "SUPABASE_URL",
        "TELEGRAM_BOT_TOKEN",
        "GROQ_API_KEY"
    )
    
    foreach ($var in $criticalVars) {
        $found = $envContent | Where-Object { $_ -match "^$var=" }
        if ($found) {
            Write-Host "  ✅ $var found" -ForegroundColor Green
        } else {
            Write-Host "  ❌ $var missing" -ForegroundColor Red
        }
    }
} else {
    Write-Host "❌ .env file not found" -ForegroundColor Red
}

Write-Host ""

# Test 4: Git repository
Write-Host "Test 4: Checking Git repository..." -ForegroundColor Yellow
if (Test-Path ".git") {
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
    
    # Check remote
    $remotes = git remote -v 2>$null
    if ($remotes) {
        Write-Host "✅ Git remote configured" -ForegroundColor Green
    } else {
        Write-Host "⚠️  No Git remote configured" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  Not a Git repository" -ForegroundColor Yellow
}

Write-Host ""

# Test 5: Required files
Write-Host "Test 5: Checking required files..." -ForegroundColor Yellow
$requiredFiles = @(
    "requirements.txt",
    "run.py",
    "render.yaml"
)

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✅ $file exists" -ForegroundColor Green
    } else {
        Write-Host "  ❌ $file missing" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "✅ TEST COMPLETED" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
