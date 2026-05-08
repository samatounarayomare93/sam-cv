# =============================================================================
# Initialize-EdgeDebugNode.ps1
# Remote Node Discovery & Initialization Controller
# Establishes a CDP bridge to an active Microsoft Edge instance.
# =============================================================================

param(
    [int]$DebugPort = 9222,
    [string]$UserDataDir = "C:\temp\EdgeDebug"
)

$CDP_BASE = "http://localhost:$DebugPort"

function Test-EdgeDebugNode {
    <#
    .SYNOPSIS
        Probes the CDP endpoint to verify the Remote Node is online and responsive.
    #>
    try {
        $response = Invoke-RestMethod -Uri "$CDP_BASE/json/version" -TimeoutSec 3 -ErrorAction Stop
        return $response
    } catch {
        return $null
    }
}

function Get-EdgeDebugPort {
    <#
    .SYNOPSIS
        Scans running msedge.exe processes for an active --remote-debugging-port argument.
    #>
    $processes = Get-CimInstance Win32_Process -Filter "name = 'msedge.exe'" |
        Select-Object ProcessId, CommandLine

    foreach ($proc in $processes) {
        if ($proc.CommandLine -match '--remote-debugging-port=(\d+)') {
            return [int]$Matches[1]
        }
    }
    return $null
}

function Get-ActiveTabs {
    <#
    .SYNOPSIS
        Enumerates all active tabs (pages) on the Remote Node.
        Returns tab objects with WebSocket debug URLs.
    #>
    try {
        $tabs = Invoke-RestMethod -Uri "$CDP_BASE/json" -TimeoutSec 5 -ErrorAction Stop
        return $tabs | Where-Object { $_.type -eq "page" }
    } catch {
        Write-Error "Failed to enumerate tabs. Is the Remote Node online?"
        return $null
    }
}

# --- MAIN EXECUTION ---

Write-Host "`n[*] Edge Remote Debug Bridge — Node Discovery" -ForegroundColor Cyan
Write-Host "    Target Port : $DebugPort" -ForegroundColor DarkGray
Write-Host "    CDP Endpoint : $CDP_BASE`n" -ForegroundColor DarkGray

# Phase 1: Check if Edge is already running with debug port
$activePort = Get-EdgeDebugPort

if ($null -eq $activePort) {
    Write-Warning "No msedge.exe process found with --remote-debugging-port."
    Write-Host "`n[!] To bring the Remote Node online, run:" -ForegroundColor Yellow
    Write-Host "    start msedge --remote-debugging-port=$DebugPort --user-data-dir=`"$UserDataDir`"" -ForegroundColor Green
    Write-Host "`n    Or use this PowerShell command:" -ForegroundColor Yellow
    Write-Host "    Start-Process msedge -ArgumentList '--remote-debugging-port=$DebugPort', '--user-data-dir=$UserDataDir'" -ForegroundColor Green
    exit 1
} else {
    Write-Host "[+] Remote Node detected on port: $activePort" -ForegroundColor Green
}

# Phase 2: Verify CDP endpoint is responsive
$nodeInfo = Test-EdgeDebugNode
if ($null -eq $nodeInfo) {
    Write-Error "Remote Node process exists but CDP endpoint is not responding on port $DebugPort."
    Write-Host "    Edge may have been launched without --remote-debugging-port. Relaunch required." -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] CDP Handshake successful." -ForegroundColor Green
Write-Host "    Browser  : $($nodeInfo.Browser)" -ForegroundColor DarkGray
Write-Host "    V8 Engine: $($nodeInfo.'V8-Version')" -ForegroundColor DarkGray
Write-Host "    Protocol : $($nodeInfo.'Protocol-Version')`n" -ForegroundColor DarkGray

# Phase 3: Enumerate active tabs
$tabs = Get-ActiveTabs
if ($null -eq $tabs -or $tabs.Count -eq 0) {
    Write-Warning "Remote Node is online but no page tabs were found."
    exit 1
}

Write-Host "[+] Active Tabs on Remote Node:" -ForegroundColor Cyan
$index = 0
foreach ($tab in $tabs) {
    Write-Host "    [$index] $($tab.title)" -ForegroundColor White
    Write-Host "        URL : $($tab.url)" -ForegroundColor DarkGray
    Write-Host "        WS  : $($tab.webSocketDebuggerUrl)" -ForegroundColor DarkGray
    $index++
}

Write-Host "`n[*] Bridge ready. Use Send-EdgeCommand.ps1 to interact with a tab." -ForegroundColor Cyan
