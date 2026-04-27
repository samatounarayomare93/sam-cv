@echo off
setlocal

echo ==============================================
echo Rita Job Automator - Local Stopper
echo ==============================================

powershell -NoProfile -ExecutionPolicy Bypass -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' or Name='pythonw.exe'\" | Where-Object { $_.CommandLine -match 'main_bot\.main\(\)' -or $_.CommandLine -match 'main_bot\.py' } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }; Write-Host 'Stopped bot processes (if any).'"

echo Done.
exit /b 0
