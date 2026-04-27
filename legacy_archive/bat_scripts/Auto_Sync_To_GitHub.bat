@echo off
echo ==========================================
echo    Rita Job Automator - Auto Sync
echo ==========================================
cd /d "%~dp0"
echo Adding new files and modifications...
git add .
set datetime=%date% %time%
echo Committing changes...
git commit -m "Auto-Sync updates from Local Workspace"
echo.
echo Pushing to GitHub (Rita-Cordahi Account)...
echo.
git push origin main
echo.
echo ==========================================
echo    Sync Complete!
echo ==========================================
pause
