@echo off
REM RITA Job Automator - Isolated Python Launcher
REM Uses -I flag to ignore site.py and corrupted registry

echo ============================================================
echo RITA JOB AUTOMATOR - MAXIMUM POWER v2
echo ============================================================
echo.

REM Use py launcher with -I (isolated) flag
echo [START] Using Python launcher with isolated mode...
echo.

py -I -c "import sys; sys.path.append(r'%cd%'); exec(open(r'%cd%\main_bot.py').read())"

echo.
echo ============================================================
pause