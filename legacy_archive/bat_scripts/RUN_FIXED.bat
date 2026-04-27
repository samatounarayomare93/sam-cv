@echo off
REM Shared launcher wrapper for the main bot entry point
cd /d "%~dp0"
python launch_main_bot.py
pause
