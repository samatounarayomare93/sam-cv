# FIX_PYTHON_REGISTRY.ps1 - Run as Administrator
# Fixes corrupted Python registry that points to project folder instead of actual installation

Write-Host "Python Registry Fix" -ForegroundColor Cyan
Write-Host "=" * 70
Write-Host ""

$CorrectPath = "C:\Program Files\Python311"

# Check and fix HKLM
$HKLMKey = "HKLM:\SOFTWARE\Python\PythonCore\3.11\InstallPath"
$HKCUKey = "HKCU:\SOFTWARE\Python\PythonCore\3.11\InstallPath"

$FixedAny = $false

function Fix-RegistryPath($KeyPath, $InstallPath) {
    if (Test-Path $KeyPath) {
        $CurrentValue = Get-ItemProperty -Path $KeyPath -Name "(Default)" -ErrorAction SilentlyContinue
        $Current = $CurrentValue."(Default)"
        
        Write-Host "  Found key: $KeyPath" -ForegroundColor Yellow
        Write-Host "  Current value: $Current"
        Write-Host "  Correct value: $InstallPath"
        Write-Host ""
        
        if ($Current -ne $InstallPath) {
            Write-Host "[FIXING] Updating to correct path..." -ForegroundColor Green
            Set-ItemProperty -Path $KeyPath -Name "(Default)" -Value $InstallPath
            Write-Host "[OK] Fixed!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "[OK] Already correct" -ForegroundColor Green
            return $false
        }
    } else {
        Write-Host "  Key not found: $KeyPath" -ForegroundColor Gray
        return $false
    }
}

# Fix HKLM (requires Admin)
if (Test-Path $HKLMKey) {
    Write-Host "[HKLM] Checking..." -ForegroundColor Cyan
    $fixed = Fix-RegistryPath $HKLMKey $CorrectPath
    if ($fixed) { $FixedAny = $true }
} else {
    Write-Host "[HKLM] Python 3.11 key not found (may be HKCU only)" -ForegroundColor Gray
}

Write-Host ""

# Fix HKCU
if (Test-Path $HKCUKey) {
    Write-Host "[HKCU] Checking..." -ForegroundColor Cyan
    $fixed = Fix-RegistryPath $HKCUKey $CorrectPath
    if ($fixed) { $FixedAny = $true }
} else {
    Write-Host "[HKCU] Python 3.11 key not found" -ForegroundColor Gray
}

Write-Host ""
Write-Host "=" * 70
if ($FixedAny) {
    Write-Host "[SUCCESS] Registry updated!" -ForegroundColor Green
    Write-Host "Please close and re-open Cursor/terminal, then try again." -ForegroundColor Yellow
} else {
    Write-Host "[INFO] Registry appears correct" -ForegroundColor Cyan
    Write-Host "If Python still fails, check the .pth file override." -ForegroundColor Yellow
}

Write-Host "=" * 70
Read-Host "Press Enter to exit"