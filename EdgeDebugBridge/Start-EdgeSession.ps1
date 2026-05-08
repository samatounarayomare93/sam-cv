# =============================================================================
# Start-EdgeSession.ps1
# One-command session bootstrap — runs discovery, loads the controller,
# and drops you into an interactive loop against the selected tab.
# =============================================================================

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Load the Network Controller
. "$ScriptDir\Send-EdgeCommand.ps1"

# Run node discovery
Write-Host "`n[*] Initializing Remote Node Discovery..." -ForegroundColor Cyan
& "$ScriptDir\Initialize-EdgeDebugNode.ps1"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Remote Node is offline. Aborting session."
    exit 1
}

# Select target tab
$global:ActiveTab = Select-EdgeTab

if ($null -eq $global:ActiveTab) {
    Write-Error "No tab selected. Aborting."
    exit 1
}

Write-Host "`n[+] Active Tab locked:" -ForegroundColor Green
Write-Host "    Title : $($global:ActiveTab.title)" -ForegroundColor White
Write-Host "    URL   : $($global:ActiveTab.url)" -ForegroundColor DarkGray
Write-Host "    WS    : $($global:ActiveTab.webSocketDebuggerUrl)`n" -ForegroundColor DarkGray

Write-Host "============================================================" -ForegroundColor DarkCyan
Write-Host "  Edge Remote Debug Session Active" -ForegroundColor Cyan
Write-Host "  Use `$global:ActiveTab as the -Tab parameter, e.g.:" -ForegroundColor DarkGray
Write-Host ""
Write-Host "  Invoke-EdgeClick     -Tab `$global:ActiveTab -Selector '#login-btn'" -ForegroundColor Yellow
Write-Host "  Invoke-EdgeExtract   -Tab `$global:ActiveTab -Selector 'h1'" -ForegroundColor Yellow
Write-Host "  Invoke-EdgeFill      -Tab `$global:ActiveTab -Selector '#email' -Value 'user@example.com'" -ForegroundColor Yellow
Write-Host "  Invoke-EdgeJS        -Tab `$global:ActiveTab -Script 'document.title'" -ForegroundColor Yellow
Write-Host "  Invoke-EdgeNavigate  -Tab `$global:ActiveTab -Url 'https://example.com'" -ForegroundColor Yellow
Write-Host "  Invoke-EdgeScreenshot -Tab `$global:ActiveTab" -ForegroundColor Yellow
Write-Host "============================================================`n" -ForegroundColor DarkCyan
