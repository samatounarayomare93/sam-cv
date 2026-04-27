param(
    [switch]$SendTestEmail,
    [switch]$RunBot,
    [switch]$SkipInstall,
    [switch]$SkipCompile
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest

function Write-Step($text) {
    Write-Host "`n=== $text ===" -ForegroundColor Cyan
}

function Test-Command($name) {
    return [bool](Get-Command $name -ErrorAction SilentlyContinue)
}

function Ensure-Python {
    Write-Step 'Checking Python runtime'
    $python = $null

    if (Test-Command py) {
        try {
            & py -3 --version | Write-Host
            $python = 'py -3'
        } catch {
            $python = $null
        }
    }

    if (-not $python -and (Test-Command python)) {
        try {
            & python --version | Write-Host
            $python = 'python'
        } catch {
            $python = $null
        }
    }

    if (-not $python) {
        throw 'Python launcher not found or broken. Repair Python 3.11 first.'
    }

    try {
        & py -3 -c "import encodings; print('encodings ok')" | Write-Host
    } catch {
        throw 'Python stdlib is broken. Repair/reinstall Python before continuing.'
    }

    return $python
}

function Ensure-Venv {
    Write-Step 'Ensuring virtual environment'
    $venvPython = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
    if (-not (Test-Path $venvPython)) {
        Write-Host 'Creating .venv...' -ForegroundColor Yellow
        & py -3 -m venv .venv
    }
    if (-not (Test-Path $venvPython)) {
        throw 'Failed to create .venv.'
    }
    return $venvPython
}

function Install-Dependencies($venvPython) {
    if ($SkipInstall) {
        Write-Step 'Skipping dependency install'
        return
    }
    Write-Step 'Installing dependencies'
    & $venvPython -m pip install --upgrade pip setuptools wheel
    & $venvPython -m pip install -r requirements.txt
}

function Compile-SmokeTest($venvPython) {
    if ($SkipCompile) {
        Write-Step 'Skipping compile smoke test'
        return
    }
    Write-Step 'Running compile smoke test'
    & $venvPython -m py_compile `
        core\main_bot.py `
        core\orchestrator.py `
        core\ai_agent.py `
        core\db_client.py `
        core\follow_up_engine.py `
        core\lead_schema.py `
        core\lead_processor.py `
        core\scrape_service.py `
        core\smtp_engine.py `
        core\cv_tailor.py `
        core\run_reporter.py `
        core\scheduler.py
}

function Show-Preflight($venvPython) {
    Write-Step 'Preflight summary'
    & $venvPython -c "from core.orchestrator import AlphaOrchestrator; print(AlphaOrchestrator.validate_preflight())"
}

function Send-TestMail($venvPython) {
    if (-not $SendTestEmail) { return }
    Write-Step 'Sending test email to sam.dev1@hotmail.com'
    & $venvPython -c "from core.smtp_engine import send_test_email; print(send_test_email())"
}

function Run-Bot($venvPython) {
    if (-not $RunBot) { return }
    Write-Step 'Starting bot'
    & $venvPython core\main_bot.py
}

try {
    Set-Location $PSScriptRoot
    $pythonLauncher = Ensure-Python
    $venvPython = Ensure-Venv
    Install-Dependencies $venvPython
    Compile-SmokeTest $venvPython
    Show-Preflight $venvPython
    Send-TestMail $venvPython
    Run-Bot $venvPython
    Write-Host "`nAll requested bootstrap steps completed." -ForegroundColor Green
} catch {
    Write-Host "`nBOOTSTRAP FAILED: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
