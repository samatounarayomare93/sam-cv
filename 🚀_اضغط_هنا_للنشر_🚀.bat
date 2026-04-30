@echo off
chcp 65001 >nul
color 0B

cls
echo.
echo ╔════════════════════════════════════════════════╗
echo ║                                                ║
echo ║        🚀 نشر تلقائي على Render.com 🚀        ║
echo ║                                                ║
echo ╔════════════════════════════════════════════════╗
echo.
echo.
echo هذا السكريبت رح يساعدك تنشر البوت على السحابة
echo.
echo شو رح يعمل:
echo   ✅ يفحص Git
echo   ✅ يحفظ التغييرات
echo   ✅ يرفع على GitHub
echo   ✅ يفتحلك Render.com
echo   ✅ يعطيك Environment Variables جاهزة
echo.
echo الوقت المتوقع: 2-3 دقائق
echo.
echo ════════════════════════════════════════════════
echo.

pause

cls
echo.
echo 🚀 بدء النشر...
echo.

powershell -ExecutionPolicy Bypass -File deploy_to_render.ps1

echo.
echo ════════════════════════════════════════════════
echo.
echo ✅ السكريبت خلص!
echo.
echo الخطوات التالية:
echo   1. افتح Render.com (رح ينفتح تلقائياً)
echo   2. سجل دخول بـ GitHub
echo   3. اعمل Web Service جديد
echo   4. انسخ Environment Variables من ملف render_env_vars.txt
echo   5. اضغط Deploy
echo   6. اختبر البوت: ابعت /start لـ @samcvbot
echo.
echo ════════════════════════════════════════════════
echo.

pause
