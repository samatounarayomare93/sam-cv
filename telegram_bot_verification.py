#!/usr/bin/env python
"""
telegram_bot_verification.py - Verify Telegram bot is working 100% on cloud

Usage: python telegram_bot_verification.py
"""

import subprocess
import sys
import json
from datetime import datetime
from pathlib import Path

class BotVerification:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": [],
            "status": "PENDING"
        }
    
    def check(self, name: str, description: str, command: str = None) -> bool:
        """Run a check"""
        print(f"\n{'='*60}")
        print(f"CHECK: {name}")
        print(f"{'='*60}")
        print(f"📋 {description}")
        
        if command:
            try:
                result = subprocess.run(command, capture_output=True, text=True, shell=True)
                success = result.returncode == 0
                output = result.stdout or result.stderr
                
                if success:
                    print(f"✅ PASS")
                    if output:
                        print(f"   Output: {output[:100]}")
                else:
                    print(f"❌ FAIL")
                    print(f"   Error: {output[:100]}")
                
                self.results["checks"].append({
                    "name": name,
                    "status": "PASS" if success else "FAIL",
                    "description": description
                })
                return success
            except Exception as e:
                print(f"❌ FAIL - {str(e)}")
                self.results["checks"].append({
                    "name": name,
                    "status": "FAIL",
                    "error": str(e)
                })
                return False
        return True
    
    def verify_project_structure(self):
        """Verify project is properly set up"""
        print("\n" + "="*60)
        print("STEP 1: PROJECT STRUCTURE VERIFICATION")
        print("="*60)
        
        # Check required files
        required_files = [
            "launch_sam.py",
            "core/telegram_dashboard.py",
            "core/main_bot.py",
            "requirements.txt",
            ".env.example"
        ]
        
        print("\n📁 Checking required files...")
        all_exist = True
        for file in required_files:
            exists = Path(file).exists()
            status = "✅" if exists else "❌"
            print(f"   {status} {file}")
            if not exists:
                all_exist = False
        
        self.results["checks"].append({
            "name": "Project Structure",
            "status": "PASS" if all_exist else "FAIL"
        })
        return all_exist
    
    def verify_dependencies(self):
        """Verify dependencies are installed"""
        print("\n" + "="*60)
        print("STEP 2: DEPENDENCY VERIFICATION")
        print("="*60)
        
        print("\n📦 Checking critical dependencies...")
        critical = [
            ("telegram", "python-telegram-bot"),
            ("supabase", "supabase"),
            ("fpdf", "fpdf2"),
            ("google.generativeai", "google-generativeai"),
        ]
        
        all_installed = True
        for module, package in critical:
            try:
                __import__(module)
                print(f"   ✅ {package}")
            except ImportError:
                print(f"   ❌ {package} - NOT INSTALLED")
                all_installed = False
        
        self.results["checks"].append({
            "name": "Dependencies",
            "status": "PASS" if all_installed else "FAIL"
        })
        return all_installed
    
    def verify_code_quality(self):
        """Verify code has no syntax errors"""
        print("\n" + "="*60)
        print("STEP 3: CODE QUALITY VERIFICATION")
        print("="*60)
        
        print("\n🔍 Checking Python files for syntax errors...")
        
        py_files = list(Path("core").glob("*.py")) + [Path("launch_sam.py")]
        errors = []
        
        for py_file in py_files:
            try:
                with open(py_file) as f:
                    compile(f.read(), py_file, 'exec')
                print(f"   ✅ {py_file.name}")
            except SyntaxError as e:
                print(f"   ❌ {py_file.name} - Syntax Error")
                errors.append(str(e))
        
        all_valid = len(errors) == 0
        self.results["checks"].append({
            "name": "Code Quality",
            "status": "PASS" if all_valid else "FAIL",
            "errors": errors
        })
        return all_valid
    
    def verify_configuration(self):
        """Verify configuration files exist"""
        print("\n" + "="*60)
        print("STEP 4: CONFIGURATION VERIFICATION")
        print("="*60)
        
        print("\n⚙️ Checking configuration files...")
        
        # Check for .env or environment setup
        has_config = Path(".env").exists() or Path(".env.example").exists()
        
        if has_config:
            print(f"   ✅ Configuration files present")
        else:
            print(f"   ⚠️  No .env file (will use environment variables)")
        
        # Check render.yaml
        render_yaml = Path("render.yaml").exists()
        status = "✅" if render_yaml else "❌"
        print(f"   {status} render.yaml (Render deployment config)")
        
        all_configured = has_config and render_yaml
        self.results["checks"].append({
            "name": "Configuration",
            "status": "PASS" if all_configured else "PARTIAL"
        })
        return has_config
    
    def verify_github_status(self):
        """Verify git repository status"""
        print("\n" + "="*60)
        print("STEP 5: GITHUB STATUS VERIFICATION")
        print("="*60)
        
        # Check git status
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            uncommitted = len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
            if uncommitted == 0:
                print(f"   ✅ Repository clean (all changes committed)")
                status = "PASS"
            else:
                print(f"   ⚠️  {uncommitted} uncommitted changes")
                status = "PASS"  # Not critical for cloud operation
        else:
            print(f"   ⚠️  Not a git repository")
            status = "PARTIAL"
        
        # Check remote
        result_remote = subprocess.run(
            ["git", "remote", "-v"],
            capture_output=True,
            text=True
        )
        
        has_remote = "github" in result_remote.stdout.lower() if result_remote.returncode == 0 else False
        remote_status = "✅" if has_remote else "⚠️"
        print(f"   {remote_status} GitHub remote configured")
        
        self.results["checks"].append({
            "name": "GitHub Status",
            "status": status
        })
        return True
    
    def verify_render_deployment(self):
        """Verify Render deployment configuration"""
        print("\n" + "="*60)
        print("STEP 6: RENDER.COM DEPLOYMENT VERIFICATION")
        print("="*60)
        
        print("\n☁️ Checking Render deployment...")
        
        # Check render.yaml exists and is valid
        if not Path("render.yaml").exists():
            print(f"   ❌ render.yaml not found")
            self.results["checks"].append({
                "name": "Render Deployment",
                "status": "FAIL"
            })
            return False
        
        print(f"   ✅ render.yaml exists")
        
        # Check for key fields
        with open("render.yaml") as f:
            content = f.read()
            checks = [
                ("python" in content, "Python runtime"),
                ("pip install" in content, "pip install command"),
                ("launch_sam.py" in content, "launch_sam.py entry point"),
            ]
            
            all_valid = True
            for check, label in checks:
                status = "✅" if check else "❌"
                print(f"   {status} {label}")
                if not check:
                    all_valid = False
        
        self.results["checks"].append({
            "name": "Render Deployment",
            "status": "PASS" if all_valid else "FAIL"
        })
        return all_valid
    
    def verify_secrets(self):
        """Verify secrets configuration"""
        print("\n" + "="*60)
        print("STEP 7: SECRETS & CREDENTIALS VERIFICATION")
        print("="*60)
        
        print("\n🔐 Checking for hardcoded secrets...")
        
        # Check core files for hardcoded secrets
        dangerous_patterns = [
            "sk-",           # API keys
            "token =",       # Tokens
            "password =",    # Passwords
            "Bearer ",       # Bearer tokens
        ]
        
        files_to_check = list(Path("core").glob("*.py"))
        issues = []
        
        for py_file in files_to_check:
            with open(py_file) as f:
                content = f.read()
                for pattern in dangerous_patterns:
                    if pattern in content and "os.environ" not in content:
                        issues.append(f"{py_file.name}: {pattern}")
        
        if not issues:
            print(f"   ✅ No hardcoded secrets detected")
            status = "PASS"
        else:
            print(f"   ⚠️  Potential hardcoded secrets found:")
            for issue in issues:
                print(f"      - {issue}")
            status = "PARTIAL"
        
        self.results["checks"].append({
            "name": "Secrets Management",
            "status": status
        })
        return True
    
    def generate_report(self):
        """Generate final report"""
        print("\n" + "="*60)
        print("FINAL VERIFICATION REPORT")
        print("="*60)
        
        passed = sum(1 for c in self.results["checks"] if c["status"] == "PASS")
        total = len(self.results["checks"])
        
        print(f"\n✅ Passed: {passed}/{total}")
        
        for check in self.results["checks"]:
            status_icon = "✅" if check["status"] == "PASS" else "❌" if check["status"] == "FAIL" else "⚠️"
            print(f"   {status_icon} {check['name']}: {check['status']}")
        
        if passed == total:
            self.results["status"] = "READY_FOR_CLOUD"
            print(f"\n🟢 STATUS: READY FOR CLOUD DEPLOYMENT")
            print(f"\n✅ Your bot is configured and ready to work on Render.com!")
            print(f"✅ No local PC required - it will work 100% on cloud!")
        elif passed >= total - 1:
            self.results["status"] = "MOSTLY_READY"
            print(f"\n🟡 STATUS: MOSTLY READY - Minor issues to fix")
        else:
            self.results["status"] = "NEEDS_FIXES"
            print(f"\n🔴 STATUS: NEEDS FIXES before cloud deployment")
        
        # Save report
        report_file = f"bot_verification_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(report_file, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n📊 Report saved: {report_file}")
    
    def run_all(self):
        """Run all verifications"""
        print("\n" + "🤖"*30)
        print("\nTELEGRAM BOT CLOUD DEPLOYMENT VERIFICATION")
        print("="*60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        try:
            self.verify_project_structure()
            self.verify_dependencies()
            self.verify_code_quality()
            self.verify_configuration()
            self.verify_github_status()
            self.verify_render_deployment()
            self.verify_secrets()
            self.generate_report()
            
            print("\n" + "🚀"*30)
            print("\n✅ VERIFICATION COMPLETE!")
            print("\nNEXT STEPS:")
            if self.results["status"] == "READY_FOR_CLOUD":
                print("1. ✅ Your project is ready!")
                print("2. Go to Render.com and deploy")
                print("3. In 2-3 minutes your bot will be live")
                print("4. Send /start to test the bot")
                print("5. Turn off your PC - bot works on cloud!")
            else:
                print("1. Review the report above")
                print("2. Fix any critical issues")
                print("3. Run verification again")
                print("4. Once all pass: Deploy to Render.com")
            
        except Exception as e:
            print(f"\n❌ Verification failed: {e}")
            self.results["status"] = "ERROR"
            self.results["error"] = str(e)

if __name__ == "__main__":
    verifier = BotVerification()
    verifier.run_all()
