@echo off
setlocal enabledelayedexpansion

echo ========================================
echo Testing Rich Email Template Send
echo ========================================
echo.

"C:\Program Files\AutoClaw\resources\python\python.exe" "%~dp0direct_send_test.py"

if %ERRORLEVEL% equ 0 (
    echo.
    echo ✅ Test complete! Check sam.dev1@hotmail.com
    echo.
) else (
    echo.
    echo ❌ Test failed with error code: %ERRORLEVEL%
    echo.
)

pause
