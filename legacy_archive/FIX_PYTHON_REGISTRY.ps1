# FIX_PYTHON_REGISTRY.ps1
# Run as Administrator to fix corrupted Python registry

Write-Host "Python Registry Fix" -ForegroundColor Cyan
Write-Host "=" * 60

$PythonPath = "HKLM:\SOFTWARE\Python"
$Python311Path = "HKLM:\SOFTWARE\Python\PythonCore\3.11"

# Function to fix registry path
function Fix-PythonPath {
    param($KeyPath, $InstallPath)
    
    if (Test-Path $KeyPath) {
        Write-Host "[FIXING] $KeyPath" -ForegroundColor Yellow
        
        # Set InstallPath
        $installPathKey = "$KeyPath\InstallPath"
        if (-not (Test-Path $installPathKey)) {
            New-Item -Path $installPathKey -Force | Out-Null
        }
        Set-ItemProperty -Path $installPathKey -Name "(Default)" -Value $InstallPath
        
        Write-Host "[FIXED] InstallPath: $InstallPath" -ForegroundColor Green
    }
}

# Fix Python 3.11
$CorrectPath = "C:\Users\samde\AppData\Local\Programs\Python\Python311"

if (Test-Path $Python311Path) {
    Write-Host "Found Python 3.11 in registry" -ForegroundColor Cyan
    
    # Check if path exists
    if (Test-Path $CorrectPath) {
        Write-Host "Correct path exists: $CorrectPath" -ForegroundColor Green
        Fix-PythonPath $Python311Path $CorrectPath
    } else {
        Write-Host "ERROR: Python not found at: $CorrectPath" -ForegroundColor Red
        Write-Host "Please reinstall Python 3.11" -ForegroundColor Yellow
    }
} else {
    Write-Host "Python 3.11 registry key not found" -ForegroundColor Yellow
    Write-Host "Registry may be in HKCU instead of HKLM"
}

# Also check HKCU
$Python311Path_HKCU = "HKCU:\SOFTWARE\Python\PythonCore\3.11"
if (Test-Path $Python311Path_HKCU) {
    Write-Host "Found in HKCU: $Python311Path_HKCU" -ForegroundColor Cyan
    Fix-PythonPath $Python311Path_HKCU $CorrectPath
}

Write-Host ""
Write-Host "Registry fix complete!" -ForegroundColor Green
Write-Host "Please restart your terminal and try again." -ForegroundColor Yellow

Read-Host "Press Enter to exit"