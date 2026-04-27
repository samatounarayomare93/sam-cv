@echo off
REM RITA System Health Check

"C:\Users\samde\Rita_Job_Automator\.python311\python.exe" -c "import sys; sys.path.append('C:/Users/samde/Rita_Job_Automator/.python311/Lib/site-packages'); sys.path.insert(0, 'C:/Users/samde/Rita_Job_Automator'); from system_health import HealthCheck; h = HealthCheck(); h.run_diagnostics()"
