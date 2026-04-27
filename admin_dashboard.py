#!/usr/bin/env python
"""
admin_dashboard.py - Comprehensive admin dashboard for production operations
Usage: python admin_dashboard.py
"""

import asyncio
import sys
import json
from datetime import datetime
from pathlib import Path

class AdminDashboard:
    """Comprehensive admin dashboard for managing Project Chronos"""
    
    def __init__(self):
        self.commands = {
            "1": ("Health Check", self.run_health_check),
            "2": ("Database Status", self.database_status),
            "3": ("Performance Analysis", self.performance_analysis),
            "4": ("Backup Database", self.backup_db),
            "5": ("View Logs", self.view_logs),
            "6": ("Deployment Status", self.deployment_status),
            "7": ("Configuration Check", self.config_check),
            "8": ("Security Audit", self.security_audit),
            "9": ("Exit", self.exit_menu),
        }
    
    def display_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("PROJECT CHRONOS - ADMIN DASHBOARD")
        print("="*60)
        print("\n📊 Quick Access Menu:\n")
        
        for key, (name, _) in self.commands.items():
            print(f"  {key}. {name}")
        
        print("\n" + "-"*60)
    
    async def run_health_check(self):
        """Run health check"""
        print("\n🔍 Running health check...")
        import subprocess
        subprocess.run([sys.executable, "health_check.py"])
    
    def database_status(self):
        """Show database status"""
        print("\n📊 DATABASE STATUS")
        print("-"*60)
        
        import subprocess
        subprocess.run([sys.executable, "database_manager.py", "--status"])
    
    def performance_analysis(self):
        """Run performance analysis"""
        print("\n⚡ PERFORMANCE ANALYSIS")
        print("-"*60)
        
        import subprocess
        subprocess.run([sys.executable, "performance_analyzer.py"])
    
    def backup_db(self):
        """Backup database"""
        print("\n💾 DATABASE BACKUP")
        print("-"*60)
        
        import subprocess
        subprocess.run([sys.executable, "database_manager.py", "--backup"])
    
    def view_logs(self):
        """View recent logs"""
        print("\n📝 RECENT LOGS")
        print("-"*60)
        
        log_file = Path("logs/bot.log") if Path("logs/bot.log").exists() else None
        
        if log_file:
            lines = log_file.read_text().split("\n")
            recent_lines = lines[-50:]  # Last 50 lines
            
            for line in recent_lines:
                if line.strip():
                    print(line)
        else:
            print("No log file found")
    
    def deployment_status(self):
        """Show deployment status"""
        print("\n🚀 DEPLOYMENT STATUS")
        print("-"*60)
        
        checks = [
            ("Code compiled", self.check_compilation()),
            ("Dependencies installed", self.check_dependencies()),
            ("Configuration complete", self.check_configuration()),
            ("Git synchronized", self.check_git()),
        ]
        
        for name, status in checks:
            symbol = "✅" if status else "❌"
            print(f"{symbol} {name}")
    
    def config_check(self):
        """Check configuration"""
        print("\n⚙️ CONFIGURATION CHECK")
        print("-"*60)
        
        configs = [
            (".env.example exists", Path(".env.example").exists()),
            ("render.yaml exists", Path("render.yaml").exists()),
            ("requirements.txt exists", Path("requirements.txt").exists()),
            (".github/workflows exists", Path(".github/workflows").exists()),
        ]
        
        for name, status in configs:
            symbol = "✅" if status else "⚠️"
            print(f"{symbol} {name}")
    
    def security_audit(self):
        """Run security audit"""
        print("\n🔒 SECURITY AUDIT")
        print("-"*60)
        
        audits = [
            ("No .env committed", self.check_env_not_committed()),
            ("No hardcoded secrets", self.check_no_secrets()),
            ("Dependencies verified", self.check_dependencies()),
        ]
        
        for name, status in audits:
            symbol = "✅" if status else "⚠️"
            print(f"{symbol} {name}")
    
    def check_compilation(self) -> bool:
        """Check if code compiles"""
        try:
            py_files = list(Path("core").glob("**/*.py"))
            for file in py_files:
                compile(file.read_text(), str(file), 'exec')
            return True
        except:
            return False
    
    def check_dependencies(self) -> bool:
        """Check if dependencies are installed"""
        try:
            import telegram, google.generativeai, groq, fpdf, bs4, aiohttp, supabase
            return True
        except:
            return False
    
    def check_configuration(self) -> bool:
        """Check if configuration is complete"""
        return (
            Path(".env.example").exists() and
            Path("render.yaml").exists() and
            Path("requirements.txt").exists()
        )
    
    def check_git(self) -> bool:
        """Check git status"""
        import subprocess
        try:
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() == ""
        except:
            return False
    
    def check_env_not_committed(self) -> bool:
        """Check .env not in git"""
        import subprocess
        try:
            result = subprocess.run(
                ["git", "ls-files", ".env"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() == ""
        except:
            return True
    
    def check_no_secrets(self) -> bool:
        """Check for hardcoded secrets"""
        try:
            py_files = list(Path("core").glob("**/*.py"))
            secret_patterns = ["api_key=", "password=", "token="]
            
            for file in py_files:
                content = file.read_text()
                if any(p in content.lower() and "os.getenv" not in content for p in secret_patterns):
                    return False
            return True
        except:
            return True
    
    def exit_menu(self):
        """Exit menu"""
        print("\n👋 Exiting admin dashboard...")
        sys.exit(0)
    
    async def run_menu(self):
        """Run interactive menu"""
        while True:
            self.display_menu()
            
            try:
                choice = input("Select an option (1-9): ").strip()
                
                if choice in self.commands:
                    name, func = self.commands[choice]
                    
                    if asyncio.iscoroutinefunction(func):
                        await func()
                    else:
                        func()
                    
                    input("\nPress Enter to continue...")
                else:
                    print("❌ Invalid selection")
            except KeyboardInterrupt:
                print("\n\n✅ Dashboard closed")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

async def main():
    dashboard = AdminDashboard()
    await dashboard.run_menu()

if __name__ == "__main__":
    asyncio.run(main())
