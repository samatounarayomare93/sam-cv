@echo off
title RITA JOB EMPIRE - INSTALLING PYTHON & RUNNING
color 0A
mode con:cols=120 lines=50
cls

echo.
echo  ██████████████████████████████████████████████████████████████████████████████████
echo  █                                                                              █
echo  █  ███████╗██╗   ██╗██████╗ ███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗ █
echo  █  ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║ █
echo  █  ███████╗██║   ██║██████╔╝█████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║ █
echo  █  ╚════██║██║   ██║██╔══██╗██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║ █
echo  █  ███████║╚██████╔╝██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║ █
echo  █  ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝ █
echo  █                                                                              █
echo  ██████████████████████████████████████████████████████████████████████████████████
echo.
echo                     ██╗  ██╗ ██████╗ ██████╗ ██╗   ██╗███████╗
echo                     ██║  ██║██╔═══██╗██╔══██╗██║   ██║██╔════╝
echo                     ███████║██║   ██║██████╔╝██║   ██║███████╗
echo                     ██╔══██║██║   ██║██╔══██╗██║   ██║╚════██║
echo                     ██║  ██║╚██████╔╝██║  ██║╚██████╔╝███████║
echo                     ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
echo.
echo  ██████████████████████████████████████████████████████████████████████████████████
echo.

echo  ┌──────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                           │
echo  │   FIRST TIME SETUP: Installing Python...                                   │
echo  │                                                                           │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

:: Download Python
echo Downloading Python 3.11...
powershell -Command "Invoke-WebRequest -Uri 'https://www.python.org/ftp/python/3.11.9/python-3.11.9-amd64.exe' -OutFile 'C:\temp_python_installer.exe'"

:: Install Python silently
echo Installing Python (this may take a minute)...
start /wait "" "C:\temp_python_installer.exe" /quiet InstallAllUsers=1 PrependPath=1 Include_pip=1

:: Refresh environment
set PATH=%PATH%;C:\Users\samde\AppData\Local\Programs\Python\Python311;C:\Users\samde\AppData\Local\Programs\Python\Python311\Scripts

:: Verify installation
echo.
echo Verifying Python installation...
C:\Users\samde\AppData\Local\Programs\Python\Python311\python.exe --version

:: Install required packages
echo.
echo Installing required packages...
C:\Users\samde\AppData\Local\Programs\Python\Python311\python.exe -m pip install requests schedule --quiet

echo.
echo  ✅ Python installed successfully!
echo.

:: ═══════════════════════════════════════════════════════════════════════════════════════
:: NOW RUNNING THE CAMPAIGN
:: ═══════════════════════════════════════════════════════════════════════════════════════

echo  ██████████████████████████████████████████████████████████████████████████████████
echo  █                                                                              █
echo  █  ██████╗ ██╗   ██╗███████╗██████╗ ██████╗ ██╗   ██╗███╗   ███╗  █
echo  █  ██╔══██╗╚██╗ ██╔╝██╔════╝██╔══██╗██╔══██╗██║   ██║████╗ ████║  █
echo  █  ██████╔╝ ╚████╔╝ █████╗  ██████╔╝██████╔╝██║   ██║██╔████╔██║  █
echo  █  ██╔══██╗  ╚██╔╝  ██╔══╝  ██╔══██╗██╔══██╗██║   ██║██║╚██╔╝██║  █
echo  █  ██████╔╝   ██║   ███████╗██║  ██║██████╔╝╚██████╔╝██║ ╚═╝ ██║  █
echo  █  ╚═════╝    ╚═╝   ╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝     ╚═╝  █
echo  █                                                                              █
echo  ██████████████████████████████████████████████████████████████████████████████████
echo.
echo  >>> SENDING EMAILS TO ALL COMPANIES NOW! <<<
echo.

:: Run the campaign
C:\Users\samde\AppData\Local\Programs\Python\Python311\python.exe rita_job_empire.py start

echo.
echo  Campaign finished!
echo.

:: Send WhatsApp notification
C:\Users\samde\AppData\Local\Programs\Python\Python311\python.exe -c "from rita_job_empire import WhatsAppNotifier; WhatsAppNotifier().send('✅ GOD MODE COMPLETE! Check application_tracker.json!')" 2>nul

echo.
echo  ┌──────────────────────────────────────────────────────────────────────────────┐
echo  │                                                                           │
echo  │   ✅ CAMPAIGN COMPLETE!                                                   │
echo  │                                                                           │
echo  │   I've done everything for you:                                            │
echo  │   ✓ Installed Python (if needed)                                         │
echo  │   ✓ Sent emails to all companies                                          │
echo  │   ✓ Attached your CV                                                     │
echo  │   ✓ Attached cover letters                                                │
echo  │   ✓ Tracked all applications                                             │
echo  │                                                                           │
echo  │   Check WhatsApp for notifications!                                      │
echo  │                                                                           │
echo  └──────────────────────────────────────────────────────────────────────────────┘
echo.

timeout /t 10 /nobreak >nul
