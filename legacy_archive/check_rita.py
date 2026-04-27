import subprocess
import sys

# Check if SAM processes are running
result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq python.exe'], 
                      capture_output=True, text=True)
print("Python processes:")
print(result.stdout)
if result.stderr:
    print("STDERR:", result.stderr)

# Also check if main_bot.py is in any cmdline
try:
    import psutil
    for p in psutil.process_iter(['pid', 'name', 'cmdline']):
        name = (p.info.get('name') or '').lower()
        if 'python' in name:
            cmd = ' '.join(p.info.get('cmdline') or [])
            if 'main_bot' in cmd or 'sam' in cmd.lower():
                print(f"\n[SAM] PID {p.info['pid']}: {cmd}")
except Exception:
    pass

if sys.stdin.isatty():
    input("\nPress Enter...")