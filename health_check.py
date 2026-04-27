#!/usr/bin/env python
"""
health_check.py - Real-time health monitoring for Project Chronos
Usage: python health_check.py [--continuous] [--interval 30]
"""

import asyncio
import sys
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
import subprocess

class HealthCheck:
    def __init__(self):
        self.checks_passed = 0
        self.checks_failed = 0
        self.health_history = []
    
    def check_git_status(self) -> bool:
        """Check if git repository is clean"""
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=5
            )
            is_clean = result.stdout.strip() == ""
            print(f"{'✅' if is_clean else '⚠️'} Git status: {'Clean' if is_clean else 'Uncommitted changes'}")
            return is_clean
        except Exception as e:
            print(f"❌ Git check failed: {e}")
            return False
    
    def check_python_syntax(self) -> bool:
        """Check Python syntax for all core modules"""
        try:
            py_files = list(Path("core").glob("**/*.py"))
            errors = 0
            
            for file in py_files:
                try:
                    compile(file.read_text(), str(file), 'exec')
                except SyntaxError as e:
                    print(f"   Syntax error in {file}: {e}")
                    errors += 1
            
            success = errors == 0
            print(f"{'✅' if success else '❌'} Python syntax: {len(py_files)} files, {errors} errors")
            return success
        except Exception as e:
            print(f"❌ Syntax check failed: {e}")
            return False
    
    def check_dependencies(self) -> bool:
        """Check if all critical dependencies are available"""
        critical = [
            "telegram", "google.generativeai", "groq", "fpdf", 
            "bs4", "aiohttp", "supabase"
        ]
        
        missing = []
        for package in critical:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)
        
        success = len(missing) == 0
        print(f"{'✅' if success else '❌'} Dependencies: {len(critical)} required, {len(missing)} missing")
        return success
    
    def check_file_structure(self) -> bool:
        """Check if critical files exist"""
        critical_files = [
            "run.py",
            "launch_sam.py",
            "core/main_bot.py",
            "core/telegram_dashboard.py",
            ".env.example",
            "requirements.txt"
        ]
        
        missing = [f for f in critical_files if not Path(f).exists()]
        success = len(missing) == 0
        
        print(f"{'✅' if success else '❌'} File structure: {len(critical_files)} critical files, {len(missing)} missing")
        if missing:
            for file in missing:
                print(f"   Missing: {file}")
        
        return success
    
    def check_documentation(self) -> bool:
        """Check if documentation is complete"""
        docs = [
            "README.md", "QUICK_START.md", "DEPLOYMENT_AND_VERIFICATION_GUIDE.md",
            "MONITORING_AND_OPERATIONS.md", "TROUBLESHOOTING_AND_FAQ.md"
        ]
        
        missing = [f for f in docs if not Path(f).exists()]
        success = len(missing) == 0
        
        print(f"{'✅' if success else '⚠️'} Documentation: {len(docs)} files, {len(missing)} missing")
        return success
    
    def check_code_quality(self) -> bool:
        """Check code quality metrics"""
        try:
            py_files = list(Path("core").glob("**/*.py"))
            total_lines = 0
            
            for file in py_files:
                total_lines += len(file.read_text().split("\n"))
            
            # Basic quality checks
            quality_ok = total_lines > 5000  # Should have reasonable amount of code
            print(f"{'✅' if quality_ok else '⚠️'} Code quality: {total_lines} lines of code")
            return quality_ok
        except Exception as e:
            print(f"❌ Code quality check failed: {e}")
            return False
    
    def check_configuration(self) -> bool:
        """Check if configuration is properly set up"""
        checks = []
        
        # Check .env.example
        checks.append(("env.example", Path(".env.example").exists()))
        
        # Check render.yaml
        checks.append(("render.yaml", Path("render.yaml").exists()))
        
        # Check GitHub workflows
        workflows = list(Path(".github/workflows").glob("*.yml")) if Path(".github/workflows").exists() else []
        checks.append(("workflows", len(workflows) >= 3))
        
        all_ok = all(ok for _, ok in checks)
        print(f"{'✅' if all_ok else '⚠️'} Configuration: {sum(1 for _, ok in checks if ok)}/{len(checks)} checks passed")
        
        return all_ok
    
    def get_health_score(self) -> int:
        """Calculate overall health score (0-100)"""
        total = self.checks_passed + self.checks_failed
        if total == 0:
            return 0
        return int((self.checks_passed / total) * 100)
    
    async def run_all_checks(self):
        """Run all health checks"""
        print("\n" + "="*60)
        print("PROJECT CHRONOS - HEALTH CHECK")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*60)
        
        self.checks_passed = 0
        self.checks_failed = 0
        
        checks = [
            ("Git Status", self.check_git_status),
            ("Python Syntax", self.check_python_syntax),
            ("Dependencies", self.check_dependencies),
            ("File Structure", self.check_file_structure),
            ("Documentation", self.check_documentation),
            ("Code Quality", self.check_code_quality),
            ("Configuration", self.check_configuration),
        ]
        
        print("\n🔍 Running health checks...")
        print("-" * 60)
        
        for name, check in checks:
            try:
                result = check()
                if result:
                    self.checks_passed += 1
                else:
                    self.checks_failed += 1
            except Exception as e:
                print(f"❌ {name} check error: {e}")
                self.checks_failed += 1
        
        # Summary
        print("\n" + "="*60)
        score = self.get_health_score()
        print(f"Health Score: {score}/100")
        print(f"Passed: {self.checks_passed} | Failed: {self.checks_failed}")
        
        if score >= 90:
            print("🟢 Status: EXCELLENT")
        elif score >= 70:
            print("🟡 Status: GOOD")
        else:
            print("🔴 Status: NEEDS ATTENTION")
        
        print("="*60)
        
        # Save history
        self.health_history.append({
            "timestamp": datetime.now().isoformat(),
            "score": score,
            "passed": self.checks_passed,
            "failed": self.checks_failed
        })
        
        return score >= 70
    
    async def continuous_monitoring(self, interval: int = 60):
        """Run health checks continuously"""
        print(f"\n🔄 Starting continuous monitoring (interval: {interval}s)")
        print("Press Ctrl+C to stop")
        
        try:
            while True:
                await self.run_all_checks()
                print(f"\n⏳ Next check in {interval} seconds...")
                await asyncio.sleep(interval)
        except KeyboardInterrupt:
            print("\n\n✅ Monitoring stopped")
            self.save_history()
    
    def save_history(self):
        """Save health check history"""
        if self.health_history:
            history_file = Path("health_check_history.json")
            history_file.write_text(json.dumps(self.health_history, indent=2))
            print(f"📊 History saved: {history_file}")

async def main():
    checker = HealthCheck()
    
    # Check command line arguments
    continuous = "--continuous" in sys.argv
    interval = 60
    
    if "--interval" in sys.argv:
        idx = sys.argv.index("--interval")
        if idx + 1 < len(sys.argv):
            try:
                interval = int(sys.argv[idx + 1])
            except ValueError:
                interval = 60
    
    if continuous:
        await checker.continuous_monitoring(interval)
    else:
        await checker.run_all_checks()
    
    return 0

if __name__ == "__main__":
    asyncio.run(main())
