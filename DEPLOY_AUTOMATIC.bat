@echo off
chcp 65001 >nul
color 0B

cls
echo.
echo ════════════════════════════════════════════════
echo.
echo       🚀 نشر تلقائي كامل 🚀
echo.
echo ════════════════════════════════════════════════
echo.
echo.
echo هذا السكريبت رح يعمل كل شي ممكن تلقائياً!
echo.
echo شو رح يعمل:
echo   ✅ يفتح ملف Environment Variables
echo   ✅ ينسخهم للـ clipboard
echo   ✅ يفتح Render.com
echo   ✅ يعطيك تعليمات واضحة
echo.
echo الوقت المتوقع: 5 دقائق
echo.
pause

cls
echo.
echo 🚀 جاري التحضير...
echo.

powershell -ExecutionPolicy Bypass -File AUTO_DEPLOY_HELPER.ps1

echo.
echo ════════════════════════════════════════════════
echo ✅ السكريبت خلص!
echo ════════════════════════════════════════════════
echo.

pause
