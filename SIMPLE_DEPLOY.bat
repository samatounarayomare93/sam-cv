@echo off
chcp 65001 >nul
color 0B

cls
echo.
echo ════════════════════════════════════════════════
echo.
echo          🚀 نشر سريع على Render.com 🚀
echo.
echo ════════════════════════════════════════════════
echo.
echo.

echo هذا السكريبت رح يساعدك تنشر البوت
echo.
echo شو رح يعمل:
echo   1. يفحص Git
echo   2. يحفظ التغييرات
echo   3. يرفع على GitHub
echo   4. يفتح Render.com
echo   5. يحفظ Environment Variables
echo.

pause

echo.
echo ════════════════════════════════════════════════
echo 🔍 فحص النظام...
echo ════════════════════════════════════════════════
echo.

REM Check Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git غير منصب!
    echo.
    echo حمله من: https://git-scm.com/download/win
    echo.
    pause
    exit /b 1
)
echo ✅ Git منصب

echo.
echo ════════════════════════════════════════════════
echo 💾 حفظ التغييرات...
echo ════════════════════════════════════════════════
echo.

REM Add all files
git add .
echo ✅ ملفات محفوظة

REM Commit
git commit -m "Deploy to Render - %date% %time%"
if %errorlevel% equ 0 (
    echo ✅ تم الحفظ بنجاح
) else (
    echo ⚠️  لا توجد تغييرات جديدة
)

echo.
echo ════════════════════════════════════════════════
echo 🚀 رفع على GitHub...
echo ════════════════════════════════════════════════
echo.

REM Push to GitHub
git push -u origin main 2>nul
if %errorlevel% neq 0 (
    git push -u origin master 2>nul
)

if %errorlevel% equ 0 (
    echo ✅ تم الرفع على GitHub بنجاح!
) else (
    echo ⚠️  فشل الرفع - قد تحتاج تسجيل دخول GitHub
    echo.
    echo جرب:
    echo   1. GitHub Desktop: https://desktop.github.com
    echo   2. أو ضبط Git credentials
    echo.
)

echo.
echo ════════════════════════════════════════════════
echo 📋 حفظ Environment Variables...
echo ════════════════════════════════════════════════
echo.

REM Create env vars file
echo # Environment Variables for Render.com > render_env_vars.txt
echo # Copy these to Render.com Environment section >> render_env_vars.txt
echo # Generated: %date% %time% >> render_env_vars.txt
echo. >> render_env_vars.txt

REM Extract critical vars from .env
findstr /R "^SUPABASE_URL= ^SUPABASE_KEY= ^TELEGRAM_BOT_TOKEN= ^TELEGRAM_CHAT_ID= ^GROQ_API_KEY= ^GEMINI_API_KEY= ^ZOHO_SMTP_USER= ^ZOHO_APP_PASSWORD= ^GMAIL_SMTP_USER= ^GMAIL_APP_PASSWORD= ^USE_AI_ANALYSIS= ^VERBOSE_LOGGING= ^MAX_PARALLEL_STRIKES= ^KEEP_ALIVE_ENABLED=" .env >> render_env_vars.txt 2>nul

echo ✅ Environment Variables محفوظة في: render_env_vars.txt

echo.
echo ════════════════════════════════════════════════
echo 🌐 فتح Render.com...
echo ════════════════════════════════════════════════
echo.

start https://render.com

echo ✅ Render.com انفتح بالمتصفح

echo.
echo ════════════════════════════════════════════════
echo 📝 الخطوات التالية:
echo ════════════════════════════════════════════════
echo.
echo على Render.com:
echo   1. سجل دخول بـ GitHub
echo   2. اضغط "New +" ثم "Web Service"
echo   3. اختار repository: Sam_Job_Automator
echo   4. املأ:
echo      - Name: sam-job-automator
echo      - Region: Frankfurt
echo      - Build: pip install -r requirements.txt
echo      - Start: python run.py
echo   5. افتح ملف: render_env_vars.txt
echo   6. انسخ كل Environment Variables
echo   7. اضغط "Create Web Service"
echo   8. استنى 3 دقائق
echo   9. اختبر: ابعت /start لـ @samcvbot
echo.
echo ════════════════════════════════════════════════
echo ✅ جاهز للنشر!
echo ════════════════════════════════════════════════
echo.

pause
