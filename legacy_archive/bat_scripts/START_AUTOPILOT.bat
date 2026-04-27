@echo off
chcp 65001 >nul

:: Python path - try multiple options
set "PYTHON_EXE="
if exist "C:\Users\samde\.local\bin\python3.14.exe" set "PYTHON_EXE=C:\Users\samde\.local\bin\python3.14.exe"
if not defined PYTHON_EXE set "PYTHON_EXE=py"
if not defined PYTHON_EXE set "PYTHON_EXE=python"

echo Starting Rita Bot...

:: Change to script directory
cd /d "%~dp0"

:: Create directories
if not exist "logs" mkdir logs
if not exist "pdf_cache" mkdir pdf_cache

:: Launch bot
start "Rita Bot" cmd /c "%PYTHON_EXE% main_bot.py >> logs bot.log 2>&1"

echo Rita Bot launched! Check logs for status.
pause