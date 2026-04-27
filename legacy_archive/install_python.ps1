# Rita Python Installer Script
# Downloads and installs Python with proper PATH settings

$ErrorActionPreference = 'Continue'

Write-Host "Rita Python Installer" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""

# Check if Python is available
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
$pyCmd = Get-Command py -ErrorAction SilentlyContinue

if ($pythonCmd) {
    Write-Host "[OK] Python found: $pythonCmd" -ForegroundColor Green
    & python --version
    exit 0
}

if ($pyCmd) {
    Write-Host "[OK] Python launcher found: $pyCmd" -ForegroundColor Green
    & py --version
    exit 0
}

# Check if Python is installed but not in PATH
$pythonPaths = @(
    "C:\Users\samde\AppData\Local\Programs\Python\Python311\python.exe",
    "C:\Python311\python.exe",
    "C:\Program Files\Python311\python.exe",
    "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
)

foreach ($path in $pythonPaths) {
    if (Test-Path $path) {
        Write-Host "[FOUND] Python at: $path" -ForegroundColor Yellow
        
        # Add to PATH for current session
        $pythonDir = Split-Path $path
        $env:PATH = "$pythonDir;$env:PATH"
        
        # Make it permanent
        [Environment]::SetEnvironmentVariable("PATH", "$pythonDir;$([Environment]::GetEnvironmentVariable('PATH','User'))", 'User')
        
        Write-Host "Added to PATH. Testing..." -ForegroundColor Yellow
        & $path --version
        exit 0
    }
}

# If not found, download and install
Write-Host "[DOWNLOAD] Downloading Python 3.11..." -ForegroundColor Cyan
$installerPath = "$env:TEMP\python-installer.exe"

try {
    Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe" -OutFile $installerPath -TimeoutSec 120
    
    Write-Host "[INSTALL] Installing Python..." -ForegroundColor Cyan
    
    # Run installer with flags for user install with PATH
    $proc = Start-Process -FilePath $installerPath -ArgumentList "/quiet InstallAllUsers=0 PrependPath=1 Include_pip=1" -PassThru -Wait
    
    Write-Host "[DONE] Python installed" -ForegroundColor Green
    
    # Refresh PATH
    $env:PATH = "$env:LOCALAPPDATA\Programs\Python\Python311;$env:LOCALAPPDATA\Programs\Python\Python311\Scripts;$env:PATH"
    
    # Test
    $newPython = "$env:LOCALAPPDATA\Programs\Python\Python311\python.exe"
    if (Test-Path $newPython) {
        & $newPython --version
    }
    
} catch {
    Write-Host "[ERROR] Installation failed: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to close..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')