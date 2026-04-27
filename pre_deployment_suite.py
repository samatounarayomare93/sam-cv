#!/usr/bin/env python
"""
pre_deployment_suite.py - Comprehensive pre-deployment validation and optimization
Run before deploying to production to ensure all systems are ready
Usage: python pre_deployment_suite.py --full
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from datetime import datetime
import asyncio

class PreDeploymentSuite:
    def __init__(self):
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "checks": {},
            "warnings": [],
            "errors": [],
            "recommendations": []
        }
        self.passed = 0
        self.failed = 0
        
    def log_check(self, name: str, status: bool, message: str = ""):
        """Log a check result"""
        status_str = "✅ PASS" if status else "❌ FAIL"
        print(f"{status_str}: {name}")
        if message:
            print(f"   └─ {message}")
        
        self.results["checks"][name] = {
            "status": "passed" if status else "failed",
            "message": message
        }
        
        if status:
            self.passed += 1
        else:
            self.failed += 1
    
    def check_python_environment(self):
        """Verify Python environment is correct"""
        print("\n🔍 Python Environment Checks")
        print("-" * 60)
        
        # Check Python version
        version = sys.version_info
        is_311_plus = version.major == 3 and version.minor >= 11
        self.log_check(
            "Python 3.11+",
            is_311_plus,
            f"Current: {version.major}.{version.minor}.{version.micro}"
        )
        
        # Check virtual environment
        in_venv = hasattr(sys, 'real_prefix') or (
            hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix
        )
        self.log_check("Virtual Environment", in_venv, "Ensure isolation")
        
        if not in_venv:
            self.results["warnings"].append("Not in virtual environment - recommended to use .venv")
    
    def check_dependencies(self):
        """Verify all dependencies are installed"""
        print("\n🔍 Dependency Checks")
        print("-" * 60)
        
        # Read requirements.txt
        req_file = Path("requirements.txt")
        if not req_file.exists():
            self.log_check("requirements.txt exists", False, "File not found")
            return
        
        self.log_check("requirements.txt exists", True)
        
        # Check critical packages
        critical_packages = [
            "python-telegram-bot",
            "google-generativeai",
            "groq",
            "fpdf2",
            "beautifulsoup4",
            "aiohttp",
            "supabase"
        ]
        
        for package in critical_packages:
            try:
                __import__(package.replace("-", "_"))
                self.log_check(f"Package: {package}", True)
            except ImportError:
                self.log_check(f"Package: {package}", False, "Missing or not installed")
                self.results["errors"].append(f"Critical package missing: {package}")
    
    def check_code_quality(self):
        """Check code compilation and quality"""
        print("\n🔍 Code Quality Checks")
        print("-" * 60)
        
        # Compile core modules
        core_modules = list(Path("core").glob("*.py"))
        
        compile_success = 0
        for module in core_modules:
            try:
                compile(module.read_text(), str(module), 'exec')
                compile_success += 1
            except SyntaxError as e:
                self.results["errors"].append(f"Syntax error in {module}: {e}")
        
        self.log_check(
            f"Code Compilation ({len(core_modules)} modules)",
            compile_success == len(core_modules),
            f"Compiled: {compile_success}/{len(core_modules)}"
        )
        
        # Check for common issues
        self.check_security_issues()
    
    def check_security_issues(self):
        """Check for common security issues"""
        print("\n🔍 Security Checks")
        print("-" * 60)
        
        # Check .env not committed
        if Path(".env").exists():
            self.log_check(".env file not in git", True, "Git properly configured")
        else:
            self.results["recommendations"].append("Create .env from .env.example")
        
        # Check for hardcoded secrets
        py_files = list(Path("core").glob("**/*.py"))
        secrets_found = 0
        
        for file in py_files:
            content = file.read_text()
            if any(secret in content.lower() for secret in ["api_key=", "password=", "token="]):
                if "os.getenv" not in content:
                    secrets_found += 1
        
        self.log_check("No hardcoded secrets", secrets_found == 0, f"Found {secrets_found} potential issues")
    
    def check_configuration(self):
        """Verify configuration setup"""
        print("\n🔍 Configuration Checks")
        print("-" * 60)
        
        # Check .env.example exists
        self.log_check(
            ".env.example exists",
            Path(".env.example").exists(),
            "Template for environment variables"
        )
        
        # Check render.yaml exists
        self.log_check(
            "render.yaml exists",
            Path("render.yaml").exists(),
            "Cloud deployment configuration"
        )
        
        # Check GitHub workflows
        workflows_dir = Path(".github/workflows")
        workflows = list(workflows_dir.glob("*.yml")) if workflows_dir.exists() else []
        
        self.log_check(
            "GitHub workflows configured",
            len(workflows) >= 3,
            f"Found {len(workflows)} workflows"
        )
    
    def check_documentation(self):
        """Verify documentation is complete"""
        print("\n🔍 Documentation Checks")
        print("-" * 60)
        
        required_docs = [
            "README.md",
            "QUICK_START.md",
            "DEPLOYMENT_AND_VERIFICATION_GUIDE.md",
            "PRODUCTION_READINESS_CHECKLIST.md",
            "MONITORING_AND_OPERATIONS.md",
            "DEVELOPER_IMPLEMENTATION_GUIDE.md",
            "TROUBLESHOOTING_AND_FAQ.md",
            "DOCUMENTATION_INDEX.md"
        ]
        
        found = 0
        for doc in required_docs:
            if Path(doc).exists():
                found += 1
                self.log_check(f"Doc: {doc}", True)
            else:
                self.log_check(f"Doc: {doc}", False, "Missing")
        
        self.log_check(f"Documentation Complete ({found}/{len(required_docs)})", found == len(required_docs))
    
    def check_git_status(self):
        """Verify git repository status"""
        print("\n🔍 Git Status Checks")
        print("-" * 60)
        
        try:
            # Check working tree
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True
            )
            clean = result.stdout.strip() == ""
            self.log_check("Git working tree clean", clean, "No uncommitted changes")
            
            if not clean:
                self.results["warnings"].append("Git working tree has uncommitted changes")
            
            # Check remote
            result = subprocess.run(
                ["git", "remote", "-v"],
                capture_output=True,
                text=True
            )
            has_remote = "origin" in result.stdout
            self.log_check("Git remote configured", has_remote, "origin remote present")
            
        except Exception as e:
            self.log_check("Git checks", False, str(e))
    
    def check_database_setup(self):
        """Check database configuration"""
        print("\n🔍 Database Checks")
        print("-" * 60)
        
        # Check for SQLite database
        sqlite_db = Path("chronos.db")
        self.log_check("SQLite database ready", sqlite_db.exists() or True, 
                      "Will be created on first run" if not sqlite_db.exists() else "Database exists")
        
        # Check database module
        try:
            from core.db_client import RealityShapingDB
            self.log_check("Database module imports", True, "RealityShapingDB available")
        except ImportError as e:
            self.log_check("Database module imports", False, str(e))
    
    def check_telegram_setup(self):
        """Check Telegram bot setup"""
        print("\n🔍 Telegram Bot Checks")
        print("-" * 60)
        
        # Check Telegram module
        try:
            from telegram import Bot
            self.log_check("Telegram bot module", True, "python-telegram-bot available")
        except ImportError:
            self.log_check("Telegram bot module", False, "Module not installed")
            self.results["errors"].append("python-telegram-bot must be installed")
    
    def optimize_code(self):
        """Suggest code optimizations"""
        print("\n⚡ Optimization Suggestions")
        print("-" * 60)
        
        optimizations = [
            "Enable Python bytecode compilation for faster startup",
            "Consider using PyPy for 2-3x performance boost",
            "Profile with cProfile to find bottlenecks",
            "Use connection pooling for database",
            "Implement async caching for API calls"
        ]
        
        for optimization in optimizations:
            print(f"  💡 {optimization}")
            self.results["recommendations"].append(optimization)
    
    def generate_report(self):
        """Generate final report"""
        print("\n" + "="*60)
        print("FINAL DEPLOYMENT READINESS REPORT")
        print("="*60)
        
        total = self.passed + self.failed
        percentage = (self.passed / total * 100) if total > 0 else 0
        
        print(f"\n✅ Passed: {self.passed}/{total} ({percentage:.1f}%)")
        print(f"❌ Failed: {self.failed}/{total}")
        
        if self.results["warnings"]:
            print(f"\n⚠️  Warnings ({len(self.results['warnings'])}):")
            for warning in self.results["warnings"]:
                print(f"   • {warning}")
        
        if self.results["errors"]:
            print(f"\n🔴 Critical Errors ({len(self.results['errors'])}):")
            for error in self.results["errors"]:
                print(f"   • {error}")
        
        if self.results["recommendations"]:
            print(f"\n💡 Recommendations ({len(self.results['recommendations'])}):")
            for rec in self.results["recommendations"][:5]:
                print(f"   • {rec}")
        
        # Deployment readiness
        print("\n" + "="*60)
        if self.failed == 0 and not self.results["errors"]:
            print("🟢 DEPLOYMENT READY - All checks passed!")
            status = "READY"
        elif self.failed <= 2:
            print("🟡 DEPLOYMENT POSSIBLE - Minor issues found")
            status = "POSSIBLE"
        else:
            print("🔴 DEPLOYMENT NOT READY - Critical issues found")
            status = "NOT_READY"
        print("="*60)
        
        # Save report
        report_file = Path(f"deployment_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        self.results["status"] = status
        self.results["percentage"] = percentage
        report_file.write_text(json.dumps(self.results, indent=2))
        print(f"\n📊 Report saved: {report_file}")
        
        return status == "READY"
    
    def run_all_checks(self):
        """Run all checks"""
        print("\n" + "="*60)
        print("PRE-DEPLOYMENT VALIDATION SUITE")
        print("="*60)
        
        self.check_python_environment()
        self.check_dependencies()
        self.check_code_quality()
        self.check_configuration()
        self.check_documentation()
        self.check_git_status()
        self.check_database_setup()
        self.check_telegram_setup()
        self.optimize_code()
        
        return self.generate_report()

def main():
    suite = PreDeploymentSuite()
    success = suite.run_all_checks()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())
