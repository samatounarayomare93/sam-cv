param(
    [int]$MaxRestarts = 0,
    [int]$RestartDelaySeconds = 8,
    [switch]$StopExisting = $true
)

$ErrorActionPreference = 'Stop'
$PSNativeCommandUseErrorActionPreference = $false
$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$site = Join-Path $root 'pydeps\Lib\site-packages'
$python = 'C:\Program Files\AutoClaw\resources\python\python.exe'
$logPath = Join-Path $root 'latest_run_final.log'
$runtimeLogPath = Join-Path $root 'latest_run_stream.log'
$runtimeErrLogPath = Join-Path $root 'latest_run_stream.err.log'
$lockPath = Join-Path $root '.main_bot.lock'

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $line = "[$ts] $Message"
    Write-Host $line
    Add-Content -Path $logPath -Value $line
}

if (Test-Path $logPath) {
    try {
        $size = (Get-Item $logPath).Length
        if ($size -gt 5MB) {
            $archive = Join-Path $root ("latest_run_final_" + (Get-Date -Format 'yyyyMMdd_HHmmss') + ".log")
            Move-Item -Path $logPath -Destination $archive -Force
        }
    } catch {
        Write-Host "[WARN] Could not rotate log file: $($_.Exception.Message)"
    }
}

if (-not (Test-Path $python)) {
    Write-Host "[FATAL] AutoClaw Python not found: $python"
    exit 1
}

if (-not (Test-Path $site)) {
    Write-Host "[FATAL] pydeps site-packages missing: $site"
    exit 1
}

if ($StopExisting) {
    Write-Log 'Stopping old bot instances before autopilot start...'
    Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'" |
    Where-Object { $_.CommandLine -match 'main_bot\.main\(\)' -or $_.CommandLine -match 'main_bot\.py' -or $_.CommandLine -match 'launch_main_bot\.py' } |
        ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
}

$env:PYTHONHOME = ''
$env:PYTHONPATH = "$root;$site"

Write-Log 'Running preflight check...'
& $python (Join-Path $root 'preflight_check.py')
if ($LASTEXITCODE -ne 0) {
    Write-Log "Preflight failed with code $LASTEXITCODE. Aborting autopilot."
    exit $LASTEXITCODE
}

$attempt = 0
$consecutiveFastFailures = 0
while ($true) {
    $attempt++
    Write-Log "Launching bot (attempt $attempt)..."
    $startTime = Get-Date

    # Heal stale lock left by abrupt process termination.
    if (Test-Path $lockPath) {
        $running = Get-CimInstance Win32_Process -Filter "Name='python.exe' or Name='pythonw.exe'" |
            Where-Object { $_.CommandLine -match 'main_bot\.main\(\)' -or $_.CommandLine -match 'main_bot\.py' -or $_.CommandLine -match 'launch_main_bot\.py' }
        if (-not $running) {
            try {
                Remove-Item -Path $lockPath -Force -ErrorAction Stop
                Write-Log 'Removed stale .main_bot.lock before relaunch.'
            } catch {
                Write-Log "Could not remove stale lock: $($_.Exception.Message)"
            }
        }
    }

    $pythonArgs = @('launch_main_bot.py')
    $proc = Start-Process -FilePath $python -ArgumentList $pythonArgs -WorkingDirectory $root -NoNewWindow -PassThru -Wait -RedirectStandardOutput $runtimeLogPath -RedirectStandardError $runtimeErrLogPath
    $code = $proc.ExitCode
    $runtimeSeconds = [int]((Get-Date) - $startTime).TotalSeconds

    if ($code -eq 0) {
        Write-Log 'Bot exited cleanly (code 0). Autopilot stopping.'
        break
    }

    if ($code -eq -1) {
        Write-Log "Bot exited via controlled handoff (code -1) after ${runtimeSeconds}s."
    } else {
        Write-Log "Bot exited unexpectedly with code $code after ${runtimeSeconds}s."
    }

    if ($runtimeSeconds -lt 20) {
        $consecutiveFastFailures++
    } else {
        $consecutiveFastFailures = 0
    }

    if ($MaxRestarts -gt 0 -and $attempt -ge $MaxRestarts) {
        if ($code -eq -1) {
            Write-Log "Reached MaxRestarts=$MaxRestarts after controlled process handoff (code -1). Stopping autopilot cleanly."
            exit 0
        }
        Write-Log "Reached MaxRestarts=$MaxRestarts. Stopping autopilot."
        exit $code
    }

    # Exponential backoff with cap to avoid hot crash loops.
    $multiplier = [Math]::Min([Math]::Pow(2, [Math]::Min($consecutiveFastFailures, 4)), 16)
    $wait = [int]([Math]::Min($RestartDelaySeconds * $multiplier, 120))

    if ($MaxRestarts -eq 0) {
        Write-Log "Restart policy: infinite retries enabled."
    }

    Write-Log "Restarting in $wait seconds..."
    [System.Threading.Thread]::Sleep($wait * 1000)
}

exit 0
