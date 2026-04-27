@echo off
title RITA JOB EMPIRE - AUTO INSTALL & RUN
color 0A

echo.
echo  INSTALLING PYTHON...
echo.

:: Create temp directory
if not exist "C:\temp_rita" mkdir "C:\temp_rita"

:: Download Python
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'C:\temp_rita\python.exe'"

:: Install silently
echo Installing Python (please wait)...
start /wait "" "C:\temp_rita\python.exe" /quiet InstallAllUsers=1 PrependPath=1

:: Refresh path
set PATH=C:\Python311;C:\Python311\Scripts;%PATH%

:: Verify
C:\Python311\python.exe --version

:: Install packages
echo Installing packages...
C:\Python311\python.exe -m pip install requests schedule --quiet

echo.
echo  ✅ PYTHON INSTALLED!
echo.

:: Now run the campaign
echo  RUNNING EMAIL CAMPAIGN...
echo.

C:\Python311\python.exe rita_job_empire.py start

echo.
echo  ✅ DONE!
echo.
pause
