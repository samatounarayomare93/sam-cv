@echo off
chcp 65001 >nul

:: Check Python
python --version >nul 2>&1
if not errorlevel 1 goto :READY

echo Python not found. Installing...

:: Download Python
echo Downloading Python...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile '%USERPROFILE%\Downloads\python-setup.exe'"

echo Installing Python...
start /wait "" "%USERPROFILE%\Downloads\python-setup.exe" /quiet InstallAllUsers=0 PrependPath=1 Include_pip=1

:: Refresh environment
set PATH=%USERPROFILE%\AppData\Local\Programs\Python\Python311;%USERPROFILE%\AppData\Local\Programs\Python\Python311\Scripts;%PATH%

:READY
echo.
echo Python is ready!
python --version
echo.
pause