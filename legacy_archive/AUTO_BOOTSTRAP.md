# Auto Bootstrap

Run this for the most automatic setup and verification possible.

## PowerShell
```powershell
.\AUTO_BOOTSTRAP.ps1 -SendTestEmail
```

## Batch wrapper
```powershell
.\AUTO_BOOTSTRAP.bat -SendTestEmail
```

## Optional flags
- `-SkipInstall` to skip dependency installation
- `-SkipCompile` to skip compile smoke test
- `-RunBot` to start the bot after checks

## Recommended first run
```powershell
.\AUTO_BOOTSTRAP.ps1 -SendTestEmail
```
