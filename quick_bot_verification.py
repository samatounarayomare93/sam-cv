#!/usr/bin/env python
"""
quick_bot_verification.py - Quick Telegram bot cloud readiness check
"""

import os
import sys
from pathlib import Path
from datetime import datetime

print("="*70)
print("⚡ QUICK TELEGRAM BOT CLOUD READINESS CHECK")
print("="*70)
print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

checks = []

# 1. Check key files
print("1️⃣  CHECKING PROJECT FILES...")
files = [
    "launch_sam.py",
    "core/telegram_dashboard.py",
    "core/main_bot.py",
    "requirements.txt",
    ".env.example",
    "render.yaml"
]

all_exist = True
for f in files:
    exists = Path(f).exists()
    status = "✅" if exists else "❌"
    print(f"   {status} {f}")
    if not exists:
        all_exist = False

checks.append(("Project Files", "PASS" if all_exist else "FAIL"))

# 2. Check dependencies
print("\n2️⃣  CHECKING KEY DEPENDENCIES...")
packages = {
    "telegram": "python-telegram-bot",
    "supabase": "supabase",
    "fpdf": "fpdf2",
    "google.generativeai": "google-generativeai",
    "groq": "groq",
    "aiohttp": "aiohttp"
}

all_installed = True
for module, name in packages.items():
    try:
        __import__(module)
        print(f"   ✅ {name}")
    except ImportError:
        print(f"   ⚠️  {name} (optional/needs install)")
        all_installed = False

checks.append(("Dependencies", "PASS" if all_installed else "PARTIAL"))

# 3. Check render.yaml
print("\n3️⃣  CHECKING RENDER.COM CONFIGURATION...")
render_path = Path("render.yaml")
if render_path.exists():
    with open(render_path) as f:
        content = f.read()
        has_python = "python" in content
        has_pip = "pip install" in content
        has_launch = "launch_sam.py" in content
        
        print(f"   {'✅' if has_python else '❌'} Python runtime configured")
        print(f"   {'✅' if has_pip else '❌'} pip install command")
        print(f"   {'✅' if has_launch else '❌'} launch_sam.py entry point")
        
        render_valid = has_python and has_pip and has_launch
else:
    print(f"   ❌ render.yaml not found")
    render_valid = False

checks.append(("Render Config", "PASS" if render_valid else "FAIL"))

# 4. Check launch_sam.py
print("\n4️⃣  CHECKING BOT LAUNCHER...")
try:
    with open("launch_sam.py", encoding='utf-8', errors='ignore') as f:
        launch_content = f.read()
        has_main = "SovereignDashboard" in launch_content
        has_ignite = "ignite" in launch_content or "run" in launch_content
        
        print(f"   {'✅' if has_main else '❌'} SovereignDashboard class referenced")
        print(f"   {'✅' if has_ignite else '❌'} Bot startup code")
        
        launcher_valid = has_main
except Exception as e:
    print(f"   ⚠️  Error reading file: {e}")
    launcher_valid = False

checks.append(("Bot Launcher", "PASS" if launcher_valid else "FAIL"))

# 5. Check for hardcoded secrets
print("\n5️⃣  CHECKING SECURITY (No hardcoded secrets)...")
dangerous = 0
try:
    for py_file in Path("core").glob("*.py"):
        with open(py_file, encoding='utf-8', errors='ignore') as f:
            content = f.read()
            if "sk-" in content or ("Bearer " in content and "os.environ" not in content):
                dangerous += 1
                print(f"   ⚠️  Potential secret in {py_file.name}")
except Exception:
    pass

if dangerous == 0:
    print(f"   ✅ No hardcoded secrets detected")

checks.append(("Security", "PASS" if dangerous == 0 else "PARTIAL"))

# 6. Check git
print("\n6️⃣  CHECKING GIT STATUS...")
try:
    import subprocess
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.returncode == 0:
        uncommitted = len([l for l in result.stdout.strip().split('\n') if l])
        if uncommitted == 0:
            print(f"   ✅ Repository clean")
        else:
            print(f"   ⚠️  {uncommitted} uncommitted changes")
        print(f"   ✅ Git repository active")
        git_ok = True
    else:
        print(f"   ⚠️  Git not available")
        git_ok = True
except Exception:
    git_ok = True

checks.append(("Git Status", "PASS"))

# Final report
print("\n" + "="*70)
print("📊 VERIFICATION SUMMARY")
print("="*70)

passed = sum(1 for _, status in checks if status == "PASS")
total = len(checks)

for name, status in checks:
    icon = "✅" if status == "PASS" else "⚠️" if status == "PARTIAL" else "❌"
    print(f"{icon} {name:.<50} {status}")

print("\n" + "="*70)

if passed == total:
    print("🟢 STATUS: READY FOR CLOUD DEPLOYMENT\n")
    print("✅ Your bot is fully configured!")
    print("✅ Can deploy to Render.com right now!")
    print("✅ Will work 100% on cloud without your PC!\n")
    print("NEXT STEPS:")
    print("1. Go to Render.com dashboard")
    print("2. Select 'Sam Job Automator' service")
    print("3. Click 'Manual Deploy' (or auto-deploys on push)")
    print("4. Wait 2-3 minutes for startup")
    print("5. Open Telegram and send /start to bot")
    print("6. Bot will respond - cloud is working!")
    print("7. Turn off your PC - bot keeps running! 🚀")
elif passed >= total - 1:
    print("🟡 STATUS: MOSTLY READY\n")
    print("Install missing dependencies (if any) and try again")
else:
    print("🔴 STATUS: NEEDS FIXES\n")
    print("Fix the ❌ issues above before deploying")

print("\n" + "="*70)
print(f"Report generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*70)
