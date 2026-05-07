#!/usr/bin/env python3
"""
🏥 ENHANCED HEALTH CHECK SYSTEM
═══════════════════════════════════════════════════════════════════════════════
Comprehensive system health monitoring for Project Chronos
Checks all components and provides detailed status report
═══════════════════════════════════════════════════════════════════════════════
"""

import os
import sys
import json
import sqlite3
import psutil
import logging
from datetime import datetime
from typing import Dict, List, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - [HEALTH-CHECK] %(levelname)s - %(message)s"
)

class HealthChecker:
    """Comprehensive health check system"""
    
    def __init__(self):
        self.results = {}
        self.score = 0
        self.max_score = 0
        
    def check_system_resources(self) -> Tuple[bool, str, Dict]:
        """Check CPU, Memory, and Disk usage"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('.')
            
            status = "OK"
            details = {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available_mb": memory.available / (1024 * 1024),
                "disk_percent": disk.percent,
                "disk_free_gb": disk.free / (1024 * 1024 * 1024)
            }
            
            # Check thresholds
            if cpu_percent > 90:
                status = "WARNING"
            if memory.percent > 85:
                status = "WARNING"
            if disk.percent > 90:
                status = "CRITICAL"
            
            message = f"CPU: {cpu_percent:.1f}%, Memory: {memory.percent:.1f}%, Disk: {disk.percent:.1f}%"
            
            return status == "OK", message, details
            
        except Exception as e:
            return False, f"Error: {e}", {}
    
    def check_files(self) -> Tuple[bool, str, Dict]:
        """Check critical files exist"""
        critical_files = [
            "run.py",
            "core/main_bot.py",
            "core/ai_agent.py",
            "core/smtp_engine.py",
            "core/db_client.py",
            "core/telegram_dashboard.py",
            ".env",
            "profile.json",
            "Sam_Salameh_CV.html",
            "requirements.txt",
        ]
        
        missing = []
        for file in critical_files:
            if not os.path.exists(file):
                missing.append(file)
        
        if missing:
            return False, f"Missing {len(missing)} files", {"missing": missing}
        
        return True, f"All {len(critical_files)} critical files present", {}
    
    def check_env_variables(self) -> Tuple[bool, str, Dict]:
        """Check required environment variables"""
        from dotenv import load_dotenv
        load_dotenv()
        
        required = [
            "TELEGRAM_BOT_TOKEN",
            "TELEGRAM_CHAT_ID",
            "GEMINI_API_KEY",
            "GROQ_API_KEY",
            "SUPABASE_URL",
            "SUPABASE_KEY",
        ]
        
        optional = [
            "GMAIL_SMTP_USER",
            "BREVO_SMTP_LOGIN",
            "ZOHO_SMTP_USER",
            "RESEND_API_KEY",
        ]
        
        missing_required = []
        missing_optional = []
        
        for var in required:
            if not os.getenv(var):
                missing_required.append(var)
        
        for var in optional:
            if not os.getenv(var):
                missing_optional.append(var)
        
        email_count = len(optional) - len(missing_optional)
        
        if missing_required:
            return False, f"Missing {len(missing_required)} required vars", {
                "missing_required": missing_required,
                "email_providers": email_count
            }
        
        if email_count == 0:
            return False, "No email providers configured", {"email_providers": 0}
        
        return True, f"All required vars set, {email_count} email providers", {
            "email_providers": email_count
        }
    
    def check_database(self) -> Tuple[bool, str, Dict]:
        """Check database connectivity"""
        details = {}
        
        # Check SQLite
        try:
            conn = sqlite3.connect("sam_ultimate.db")
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
            tables = cursor.fetchall()
            conn.close()
            
            details["sqlite"] = {
                "status": "OK",
                "tables": len(tables)
            }
        except Exception as e:
            details["sqlite"] = {
                "status": "ERROR",
                "error": str(e)
            }
        
        # Check Supabase
        from dotenv import load_dotenv
        load_dotenv()
        
        supabase_url = os.getenv("SUPABASE_URL", "")
        supabase_key = os.getenv("SUPABASE_KEY", "")
        
        if supabase_url and supabase_key and "your-project" not in supabase_url:
            try:
                import httpx
                response = httpx.get(
                    f"{supabase_url}/rest/v1/",
                    headers={"apikey": supabase_key},
                    timeout=5
                )
                
                details["supabase"] = {
                    "status": "OK" if response.status_code == 200 else "ERROR",
                    "status_code": response.status_code
                }
            except Exception as e:
                details["supabase"] = {
                    "status": "ERROR",
                    "error": str(e)
                }
        else:
            details["supabase"] = {
                "status": "NOT_CONFIGURED"
            }
        
        # Overall status
        sqlite_ok = details.get("sqlite", {}).get("status") == "OK"
        supabase_ok = details.get("supabase", {}).get("status") == "OK"
        
        if sqlite_ok and supabase_ok:
            return True, "Supabase + SQLite both working", details
        elif sqlite_ok:
            return True, "SQLite working (Supabase fallback)", details
        else:
            return False, "Database connection failed", details
    
    def check_email_providers(self) -> Tuple[bool, str, Dict]:
        """Check email provider configuration"""
        from dotenv import load_dotenv
        load_dotenv()
        
        providers = {
            "Gmail": ("GMAIL_SMTP_USER", "GMAIL_APP_PASSWORD"),
            "Brevo": ("BREVO_SMTP_LOGIN", "BREVO_SMTP_PASSWORD"),
            "Zoho": ("ZOHO_SMTP_USER", "ZOHO_APP_PASSWORD"),
            "Resend": ("RESEND_API_KEY",),
            "Yahoo": ("YAHOO_SMTP_USER", "YAHOO_APP_PASSWORD"),
            "Outlook": ("OUTLOOK_USER", "OUTLOOK_PASSWORD"),
        }
        
        configured = []
        details = {}
        
        for name, vars in providers.items():
            if all(os.getenv(var) for var in vars):
                configured.append(name)
                details[name] = "CONFIGURED"
            else:
                details[name] = "NOT_CONFIGURED"
        
        if len(configured) == 0:
            return False, "No email providers configured", details
        elif len(configured) < 2:
            return True, f"{len(configured)} provider (need 2+ for redundancy)", details
        else:
            return True, f"{len(configured)} providers configured", details
    
    def check_ai_engines(self) -> Tuple[bool, str, Dict]:
        """Check AI engine configuration"""
        from dotenv import load_dotenv
        load_dotenv()
        
        gemini_key = os.getenv("GEMINI_API_KEY", "")
        groq_key = os.getenv("GROQ_API_KEY", "")
        
        details = {
            "Gemini": "CONFIGURED" if gemini_key else "NOT_CONFIGURED",
            "Groq": "CONFIGURED" if groq_key else "NOT_CONFIGURED"
        }
        
        if gemini_key and groq_key:
            return True, "Gemini + Groq both configured", details
        elif gemini_key or groq_key:
            return True, "One AI engine configured (fallback available)", details
        else:
            return False, "No AI engines configured", details
    
    def check_telegram_bot(self) -> Tuple[bool, str, Dict]:
        """Check Telegram bot configuration"""
        from dotenv import load_dotenv
        load_dotenv()
        
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        chat_id = os.getenv("TELEGRAM_CHAT_ID", "")
        
        details = {
            "bot_token": "SET" if bot_token else "MISSING",
            "chat_id": "SET" if chat_id else "MISSING"
        }
        
        if bot_token and chat_id:
            return True, "Telegram bot configured", details
        else:
            return False, "Telegram bot not configured", details
    
    def check_scrapers(self) -> Tuple[bool, str, Dict]:
        """Check scraper modules"""
        scrapers = [
            "core.scrapers.scraper",
            "core.scrapers.omni_crawler",
            "core.scrapers.daleel_parallel",
        ]
        
        available = []
        details = {}
        
        for scraper in scrapers:
            try:
                __import__(scraper)
                available.append(scraper.split('.')[-1])
                details[scraper.split('.')[-1]] = "AVAILABLE"
            except ImportError:
                details[scraper.split('.')[-1]] = "NOT_AVAILABLE"
        
        if len(available) == 0:
            return False, "No scrapers available", details
        else:
            return True, f"{len(available)}/{len(scrapers)} scrapers available", details
    
    def run_all_checks(self) -> Dict:
        """Run all health checks"""
        print("\n" + "="*80)
        print("🏥 PROJECT CHRONOS - COMPREHENSIVE HEALTH CHECK")
        print("="*80 + "\n")
        
        checks = [
            ("System Resources", self.check_system_resources),
            ("Critical Files", self.check_files),
            ("Environment Variables", self.check_env_variables),
            ("Database", self.check_database),
            ("Email Providers", self.check_email_providers),
            ("AI Engines", self.check_ai_engines),
            ("Telegram Bot", self.check_telegram_bot),
            ("Scrapers", self.check_scrapers),
        ]
        
        results = {}
        total_score = 0
        max_score = len(checks) * 10
        
        for name, check_func in checks:
            try:
                success, message, details = check_func()
                
                status_icon = "✅" if success else "❌"
                score = 10 if success else 0
                total_score += score
                
                print(f"{status_icon} {name}: {message}")
                
                results[name] = {
                    "success": success,
                    "message": message,
                    "details": details,
                    "score": score
                }
                
            except Exception as e:
                print(f"❌ {name}: Error - {e}")
                results[name] = {
                    "success": False,
                    "message": f"Error: {e}",
                    "details": {},
                    "score": 0
                }
        
        # Calculate overall health score
        health_percentage = (total_score / max_score) * 100
        
        print("\n" + "="*80)
        print(f"Overall Health Score: {total_score}/{max_score} ({health_percentage:.1f}%)")
        
        if health_percentage >= 90:
            print("Status: 🟢 EXCELLENT - System is fully operational")
        elif health_percentage >= 70:
            print("Status: 🟡 GOOD - System is operational with minor issues")
        elif health_percentage >= 50:
            print("Status: 🟠 WARNING - System has significant issues")
        else:
            print("Status: 🔴 CRITICAL - System requires immediate attention")
        
        print("="*80 + "\n")
        
        # Save results to file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"health_check_{timestamp}.json"
        
        with open(report_file, 'w') as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_score": total_score,
                "max_score": max_score,
                "health_percentage": health_percentage,
                "results": results
            }, f, indent=2)
        
        print(f"📄 Detailed report saved to: {report_file}\n")
        
        return results


def main():
    """Main entry point"""
    checker = HealthChecker()
    results = checker.run_all_checks()
    
    # Exit with appropriate code
    all_critical_ok = all(
        results.get(check, {}).get("success", False)
        for check in ["Critical Files", "Environment Variables", "Database"]
    )
    
    sys.exit(0 if all_critical_ok else 1)


if __name__ == "__main__":
    main()
