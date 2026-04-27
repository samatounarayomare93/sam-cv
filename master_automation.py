#!/usr/bin/env python
"""
master_automation.py - Master automation script for all project operations
Usage: python master_automation.py --help
"""

import sys
import subprocess
import argparse
from pathlib import Path
from datetime import datetime
import json

class MasterAutomation:
    """Master automation and orchestration script"""
    
    def __init__(self):
        self.log = []
    
    def log_action(self, action: str, status: str, message: str = ""):
        """Log an action"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": status,
            "message": message
        }
        self.log.append(entry)
        print(f"[{status}] {action} {message}")
    
    def run_command(self, cmd: list, description: str = "") -> bool:
        """Run a command safely"""
        try:
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                self.log_action(description or " ".join(cmd), "✅", "Success")
                return True
            else:
                self.log_action(description or " ".join(cmd), "❌", result.stderr[:100])
                return False
        except Exception as e:
            self.log_action(description or " ".join(cmd), "❌", str(e)[:100])
            return False
    
    def validate_project(self):
        """Validate entire project"""
        print("\n" + "="*60)
        print("VALIDATING PROJECT")
        print("="*60)
        
        self.run_command([sys.executable, "pre_deployment_suite.py"], "Pre-deployment validation")
    
    def run_health_check(self):
        """Run health check"""
        print("\n" + "="*60)
        print("RUNNING HEALTH CHECK")
        print("="*60)
        
        self.run_command([sys.executable, "health_check.py"], "Health check")
    
    def backup_all_data(self):
        """Backup all data"""
        print("\n" + "="*60)
        print("BACKING UP DATA")
        print("="*60)
        
        self.run_command([sys.executable, "database_manager.py", "--backup"], "Database backup")
        
        # Also backup configuration
        for config_file in [".env.example", "render.yaml", "requirements.txt"]:
            if Path(config_file).exists():
                backup_file = Path("backups") / f"{config_file}.backup"
                Path("backups").mkdir(exist_ok=True)
                backup_file.write_text(Path(config_file).read_text())
                self.log_action(f"Backup {config_file}", "✅")
    
    def analyze_performance(self):
        """Analyze performance"""
        print("\n" + "="*60)
        print("ANALYZING PERFORMANCE")
        print("="*60)
        
        self.run_command([sys.executable, "performance_analyzer.py"], "Performance analysis")
    
    def optimize_database(self):
        """Optimize database"""
        print("\n" + "="*60)
        print("OPTIMIZING DATABASE")
        print("="*60)
        
        self.run_command([sys.executable, "database_manager.py", "--optimize"], "Database optimization")
    
    def full_deployment_prep(self):
        """Full deployment preparation"""
        print("\n" + "="*60)
        print("FULL DEPLOYMENT PREPARATION")
        print("="*60)
        
        # Run all validations
        self.validate_project()
        self.run_health_check()
        self.backup_all_data()
        self.analyze_performance()
        self.optimize_database()
        
        # Final report
        print("\n" + "="*60)
        print("DEPLOYMENT PREPARATION COMPLETE")
        print("="*60)
        print(f"✅ {sum(1 for log in self.log if 'Success' in str(log))} successful operations")
        print(f"❌ {sum(1 for log in self.log if '✅' not in str(log))} issues found")
    
    def save_log(self):
        """Save operation log"""
        log_file = Path(f"automation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        log_file.write_text(json.dumps(self.log, indent=2))
        print(f"\n📊 Log saved: {log_file}")

def main():
    parser = argparse.ArgumentParser(
        description="Master Automation Script for Project Chronos"
    )
    parser.add_argument("--validate", action="store_true", help="Validate project")
    parser.add_argument("--health", action="store_true", help="Run health check")
    parser.add_argument("--backup", action="store_true", help="Backup all data")
    parser.add_argument("--performance", action="store_true", help="Analyze performance")
    parser.add_argument("--optimize", action="store_true", help="Optimize database")
    parser.add_argument("--full", action="store_true", help="Full deployment prep (all checks)")
    
    args = parser.parse_args()
    
    automation = MasterAutomation()
    
    if args.validate:
        automation.validate_project()
    elif args.health:
        automation.run_health_check()
    elif args.backup:
        automation.backup_all_data()
    elif args.performance:
        automation.analyze_performance()
    elif args.optimize:
        automation.optimize_database()
    elif args.full:
        automation.full_deployment_prep()
    else:
        print("Project Chronos Master Automation")
        print("\nUse --help for options")
        parser.print_help()
    
    automation.save_log()

if __name__ == "__main__":
    main()
