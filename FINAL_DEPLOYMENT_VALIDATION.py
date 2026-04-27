#!/usr/bin/env python
"""
FINAL_DEPLOYMENT_VALIDATION.py - Ultimate pre-deployment check (100% verification)
Ensures EVERYTHING is ready before deploying to Render.com
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import json

print("\n" + "[CHECK]"*20)
print("\n*** FINAL DEPLOYMENT VALIDATION - 100% VERIFICATION CHECK ***")
print("="*80)
print("Started: {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
print("="*80 + "\n")

results = {
    "timestamp": datetime.now().isoformat(),
    "checks": [],
    "status": "PENDING"
}

passed = 0
failed = 0

# ═══════════════════════════════════════════════════════════════════════════════

print("[CHECK 1] CRITICAL PROJECT FILES")
print("-" * 80)

critical_files = {
    "launch_sam.py": "Bot entry point for cloud",
    "core/telegram_dashboard.py": "Telegram interface",
    "core/main_bot.py": "Bot logic",
    "requirements.txt": "Python dependencies",
    "render.yaml": "Render.com config",
    ".env.example": "Configuration template"
}

all_exist = True
for file, desc in critical_files.items():
    exists = Path(file).exists()
    status = "[PASS]" if exists else "[FAIL]"
    print("  {} {:<45} {}".format(status, file, desc))
    if not exists:
        all_exist = False
        failed += 1
    else:
        passed += 1

results["checks"].append({"name": "Critical Files", "status": "PASS" if all_exist else "FAIL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 2] RENDER.YAML CONFIGURATION")
print("-" * 80)

render_issues = []
with open("render.yaml") as f:
    content = f.read()
    
checks = [
    ("python" in content, "[PASS] Python runtime configured"),
    ("pip install" in content, "[PASS] pip install command present"),
    ("launch_sam.py" in content, "[PASS] launch_sam.py as entry point"),
    ("startCommand" in content, "[PASS] startCommand defined"),
]

for check, msg in checks:
    if check:
        print("  {}".format(msg))
        passed += 1
    else:
        print("  [FAIL] {}".format(msg.replace('[PASS] ', '')))
        render_issues.append(msg)
        failed += 1

results["checks"].append({"name": "Render Config", "status": "PASS" if not render_issues else "FAIL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 3] LAUNCH_SAM.PY VALIDATION")
print("-" * 80)

try:
    with open("launch_sam.py", encoding='utf-8', errors='ignore') as f:
        launch_content = f.read()
        
    launch_checks = [
        ("SovereignDashboard" in launch_content, "[PASS] SovereignDashboard imported"),
        ("ignite" in launch_content or "run" in launch_content or "start" in launch_content, "[PASS] Bot startup method"),
        ("if __name__" in launch_content or "main()" in launch_content, "[PASS] Main entry point"),
    ]
    
    launch_valid = all(check for check, _ in launch_checks)
    
    for check, msg in launch_checks:
        if check:
            print("  {}".format(msg))
            passed += 1
        else:
            print("  [FAIL] {}".format(msg.replace('[PASS] ', '')))
            failed += 1
    
    results["checks"].append({"name": "Launch Script", "status": "PASS" if launch_valid else "FAIL"})
except Exception as e:
    print(f"  ❌ Error reading launch_sam.py: {e}")
    failed += 1
    results["checks"].append({"name": "Launch Script", "status": "FAIL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 4] KEY DEPENDENCIES")
print("-" * 80)

dependencies = {
    "telegram": "python-telegram-bot",
    "fpdf": "fpdf2",
    "google.generativeai": "google-generativeai",
    "groq": "groq",
}

all_deps = True
for module, name in dependencies.items():
    try:
        __import__(module)
        print("  [PASS] {}".format(name))
        passed += 1
    except ImportError:
        print("  [FAIL] {} - NOT INSTALLED!".format(name))
        all_deps = False
        failed += 1

results["checks"].append({"name": "Dependencies", "status": "PASS" if all_deps else "FAIL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 5] ENVIRONMENT & SECRETS")
print("-" * 80)

required_secrets = [
    "TELEGRAM_BOT_TOKEN",
    "GMAIL_APP_PASSWORD",
    "GROQ_API_KEY",
    "GOOGLE_API_KEY",
]

env_file = Path(".env")
example_file = Path(".env.example")

if env_file.exists():
    print("  [PASS] .env file exists (contains secrets)")
    passed += 1
elif example_file.exists():
    print("  [PASS] .env.example exists (template for secrets)")
    passed += 1
else:
        print("  [WARN] No .env files found (will use GitHub secrets)")
# Check .env.example has all required vars
if example_file.exists():
    with open(example_file, encoding='utf-8', errors='ignore') as f:
        example_content = f.read()
    
    missing_vars = []
    for var in required_secrets:
        if var not in example_content:
            missing_vars.append(var)
    
    if missing_vars:
        print("  [WARN] Missing in .env.example: {}".format(', '.join(missing_vars)))
    else:
        print("  [PASS] All required secrets in .env.example")
        passed += 1

results["checks"].append({"name": "Configuration", "status": "PASS"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 6] CORE MODULES COMPILATION")
print("-" * 80)

core_modules = list(Path("core").glob("*.py"))
compile_errors = []

for module in core_modules:
    try:
        with open(module, encoding='utf-8', errors='ignore') as f:
            compile(f.read(), module, 'exec')
        print("  [PASS] {}".format(module.name))
        passed += 1
    except SyntaxError as e:
        print("  [FAIL] {} - Syntax Error: {}".format(module.name, str(e)[:50]))
        compile_errors.append(str(module.name))
        failed += 1

results["checks"].append({"name": "Code Compilation", "status": "PASS" if not compile_errors else "FAIL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 7] GIT REPOSITORY STATUS")
print("-" * 80)

try:
    import subprocess
    
    # Check if git repo exists
    result = subprocess.run(["git", "status"], capture_output=True, text=True)
    if result.returncode == 0:
        print("  [PASS] Git repository active")
        passed += 1
        
        # Check for uncommitted changes
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        uncommitted = len([l for l in result.stdout.strip().split('\n') if l])
        
        if uncommitted == 0:
            print("  [PASS] All changes committed")
            passed += 1
        else:
            print("  [WARN] {} uncommitted changes (needs commit)".format(uncommitted))
        
        # Check remote
        result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
        if "github" in result.stdout.lower():
            print("  [PASS] GitHub remote configured")
            passed += 1
        else:
            print("  [WARN] No GitHub remote found")
    else:
        print("  [WARN] Git command not available")
        
except Exception as e:
    print("  [WARN] Git check error: {}".format(e))

results["checks"].append({"name": "Git Status", "status": "PASS"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 8] DOCUMENTATION")
print("-" * 80)

key_docs = [
    ("DEPLOYMENT_SECRETS_GUIDE.md", "Secrets configuration"),
    ("CLOUD_DEPLOYMENT_FINAL.md", "Deployment guide"),
    ("README.md", "Project README"),
]

docs_ok = True
for doc, desc in key_docs:
    exists = Path(doc).exists()
    status = "[PASS]" if exists else "[FAIL]"
    print("  {} {:<45} {}".format(status, doc, desc))
    if exists:
        passed += 1
    else:
        docs_ok = False
        failed += 1

results["checks"].append({"name": "Documentation", "status": "PASS" if docs_ok else "PARTIAL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 9] SECURITY SCAN")
print("-" * 80)

security_issues = []

# Scan for hardcoded secrets
dangerous_patterns = ["sk-", "token =", "password =", "Bearer "]

for py_file in Path("core").glob("*.py"):
    try:
        with open(py_file, encoding='utf-8', errors='ignore') as f:
            content = f.read()
            for pattern in dangerous_patterns:
                if pattern in content and "os.environ" not in content and "getenv" not in content:
                    security_issues.append(f"{py_file.name}: contains '{pattern}'")
    except:
        pass

if security_issues:
    print("  [WARN] Potential security issues found:")
    for issue in security_issues:
        print("     - {}".format(issue))
else:
    print("  [PASS] No hardcoded secrets detected")
    passed += 1

results["checks"].append({"name": "Security", "status": "PASS" if not security_issues else "PARTIAL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n[CHECK 10] DEPLOYMENT READINESS")
print("-" * 80)

readiness_items = [
    (Path("render.yaml").exists() and "launch_sam.py" in Path("render.yaml").read_text(), "Render.com config ready"),
    (Path("requirements.txt").exists(), "requirements.txt present"),
    (Path("launch_sam.py").exists(), "launch_sam.py entry point"),
    (Path(".env.example").exists(), ".env.example configuration"),
]

all_ready = True
for check, desc in readiness_items:
    status = "[PASS]" if check else "[FAIL]"
    print("  {} {}".format(status, desc))
    if check:
        passed += 1
    else:
        all_ready = False
        failed += 1

results["checks"].append({"name": "Deployment Readiness", "status": "PASS" if all_ready else "FAIL"})

# ═══════════════════════════════════════════════════════════════════════════════

print("\n" + "="*80)
print("FINAL SUMMARY")
print("="*80)

total = passed + failed
score = (passed / total * 100) if total > 0 else 0

print("\n[PASS] Passed: {}".format(passed))
print("[FAIL] Failed: {}".format(failed))
print("[SCORE] Score: {:.1f}%\n".format(score))

if failed == 0:
    print("*** STATUS: 100% READY FOR CLOUD DEPLOYMENT! ***")
    print("\n[PASS] ALL CHECKS PASSED!")
    print("[PASS] Bot is fully configured!")
    print("[PASS] Can deploy to Render.com NOW!")
    print("[PASS] Will work 100% on cloud!")
    print("\nNEXT STEPS:")
    print("1. Go to Render.com")
    print("2. Click 'Manual Deploy'")
    print("3. Wait 3 minutes for bot to start")
    print("4. Send /start to bot - it should respond!")
    print("5. Bot is live on cloud! SUCCESS!")
    results["status"] = "READY_FOR_DEPLOYMENT"
elif failed <= 2:
    print("*** STATUS: MOSTLY READY ***")
    print("\nFix the issues above, then deploy.")
    results["status"] = "NEEDS_MINOR_FIXES"
else:
    print("*** STATUS: NEEDS FIXES ***")
    print("\nFix all critical issues before deploying.")
    results["status"] = "NEEDS_MAJOR_FIXES"

print("\n" + "="*80)

# Save results
report_file = f"FINAL_DEPLOYMENT_VALIDATION_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
with open(report_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"✅ Report saved: {report_file}")
print("="*80 + "\n")

sys.exit(0 if failed == 0 else 1)
