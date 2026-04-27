@echo off
cd /d "%~dp0"
set "PYTHONPATH=%CD%;%CD%\pydeps\Lib\site-packages"
"C:\Program Files\AutoClaw\resources\python\python.exe" "%CD%\send_exact_production_test.py"
