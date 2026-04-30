@echo off
chcp 65001 >nul
color 0B

cls
echo.
echo ════════════════════════════════════════════════
echo          🧪 اختبار النظام 🧪
echo ════════════════════════════════════════════════
echo.

echo جاري فحص النظام...
echo.

powershell -ExecutionPolicy Bypass -File test_deployment_script.ps1

pause
