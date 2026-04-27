#!/usr/bin/env python
"""
deployment_validator.py - Validates Project Chronos configuration before deployment
Usage: python deployment_validator.py
"""

import os
import sys
from pathlib import Path

def check_env_template():
    """Verify .env.example exists and is complete"""
    env_example = Path(".env.example")
    if not env_example.exists():
        return False, "❌ .env.example not found"
    
    content = env_example.read_text(encoding="utf-8")
    required_sections = [
        "SUPABASE_URL",
        "GEMINI_API_KEY",
        "TELEGRAM_BOT_TOKEN",
        "GMAIL_SMTP_USER",
        "BREVO_SMTP_LOGIN"
    ]
    
    missing = [s for s in required_sections if s not in content]
    if missing:
        return False, f"❌ Missing sections in .env.example: {', '.join(missing)}"
    
    return True, "✅ .env.example complete"

def check_launch_files():
    """Verify launch files exist"""
    required_files = [
        "launch_sam.py",
        "run.py",
        "requirements.txt"
    ]
    
    missing = [f for f in required_files if not Path(f).exists()]
    if missing:
        return False, f"❌ Missing files: {', '.join(missing)}"
    
    return True, "✅ All launch files present"

def check_core_modules():
    """Verify all core modules are present"""
    core_modules = [
        "core/main_bot.py",
        "core/telegram_dashboard.py",
        "core/ai_agent.py",
        "core/db_client.py",
        "core/smtp_engine.py",
        "core/pdf_generator.py"
    ]
    
    missing = [m for m in core_modules if not Path(m).exists()]
    if missing:
        return False, f"❌ Missing core modules: {', '.join(missing)}"
    
    return True, "✅ All core modules present"

def check_workflows():
    """Verify GitHub workflows are configured"""
    workflows = Path(".github/workflows")
    if not workflows.exists():
        return False, "❌ .github/workflows directory not found"
    
    required = ["ci_quality.yml", "job_bot.yml", "24_7_telegram_bot.yml"]
    missing = [w for w in required if not (workflows / w).exists()]
    
    if missing:
        return False, f"❌ Missing workflows: {', '.join(missing)}"
    
    return True, "✅ All workflows configured"

def check_documentation():
    """Verify critical documentation exists"""
    docs = [
        "README.md",
        "QUICK_START.md",
        "DEPLOYMENT_SECRETS_GUIDE.md",
        ".github/CONTRIBUTING.md"
    ]
    
    missing = [d for d in docs if not Path(d).exists()]
    if missing:
        return False, f"❌ Missing documentation: {', '.join(missing)}"
    
    return True, "✅ Documentation complete"

def main():
    print("\n" + "="*70)
    print("PROJECT CHRONOS - DEPLOYMENT VALIDATOR")
    print("="*70 + "\n")
    
    checks = [
        ("Environment Template", check_env_template),
        ("Launch Files", check_launch_files),
        ("Core Modules", check_core_modules),
        ("GitHub Workflows", check_workflows),
        ("Documentation", check_documentation),
    ]
    
    results = []
    for name, check in checks:
        passed, message = check()
        results.append((passed, message))
        print(f"{message}")
    
    print("\n" + "="*70)
    passed_count = sum(1 for p, _ in results if p)
    total_count = len(results)
    
    if passed_count == total_count:
        print(f"✅ DEPLOYMENT READY: All {total_count} checks passed!")
        print("\nNext steps:")
        print("1. Create .env from .env.example")
        print("2. Fill in all required credentials (see DEPLOYMENT_SECRETS_GUIDE.md)")
        print("3. Test locally: python run.py")
        print("4. Deploy to Render.com")
        print("="*70 + "\n")
        return 0
    else:
        print(f"❌ DEPLOYMENT NOT READY: {passed_count}/{total_count} checks passed")
        print("Please fix the issues above before deploying.")
        print("="*70 + "\n")
        return 1

if __name__ == "__main__":
    sys.exit(main())
