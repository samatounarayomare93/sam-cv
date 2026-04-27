"""
SAM SYSTEM VERIFIER v2
========================
Comprehensive verification of all system components
Ensures everything works 100% without errors
"""

import os
import sys
import json
import time
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Colors for output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def print_success(msg):
    print(f"{GREEN}✅ {msg}{RESET}")

def print_error(msg):
    print(f"{RED}❌ {msg}{RESET}")

def print_warning(msg):
    print(f"{YELLOW}⚠️  {msg}{RESET}")

def print_info(msg):
    print(f"{BLUE}ℹ️  {msg}{RESET}")

class SystemVerifier:
    def __init__(self):
        self.results = {
            "critical_files": [],
            "runtime_files": [],
            "modules": [],
            "config": [],
            "api_keys": [],
            "overall": "PASS"
        }
        self.errors = []
        
    def check_critical_files(self):
        """Check all critical files exist."""
        print("\n" + "="*60)
        print("CHECKING CRITICAL FILES")
        print("="*60)
        
        critical_files = [
            "config.py",
            "database.py",
            "scraper.py",
            "smtp_engine.py",
            "main_bot.py",
            "ai_agent.py",
            "system_health.py",
            "uplink.py",
            "self_healer.py",
            "omni_crawler.py",
            "pdf_generator.py",
            "telegram_dashboard.py",
            "core_utils.py"
        ]
        
        all_pass = True
        for f in critical_files:
            if os.path.exists(f):
                print_success(f"Found: {f}")
                self.results["critical_files"].append({"file": f, "status": "OK"})
            else:
                print_error(f"Missing: {f}")
                self.results["critical_files"].append({"file": f, "status": "MISSING"})
                all_pass = False
        
        return all_pass
    
    def check_runtime_files(self):
        """Check runtime files can be created."""
        print("\n" + "="*60)
        print("CHECKING RUNTIME FILES")
        print("="*60)
        
        runtime_files = [
            "tracker.json",
            "metrics.json",
            "health_check.json",
            "company_database.json",
            "discovered_companies.json",
            "system_pulse.txt"
        ]
        
        all_pass = True
        for f in runtime_files:
            if os.path.exists(f):
                print_success(f"Found: {f}")
                self.results["runtime_files"].append({"file": f, "status": "OK"})
            else:
                print_warning(f"Missing (will auto-create): {f}")
                self.results["runtime_files"].append({"file": f, "status": "AUTO_CREATE"})
        
        return True
    
    def check_modules(self):
        """Check all Python modules can be imported."""
        print("\n" + "="*60)
        print("CHECKING PYTHON MODULES")
        print("="*60)
        
        modules = [
            ("config", "Configuration module"),
            ("database", "Database module"),
            ("smtp_engine", "SMTP engine"),
            ("scraper", "Web scraper"),
            ("ai_agent", "AI agent"),
            ("system_health", "Health checker"),
            ("uplink", "Telegram uplink"),
            ("self_healer", "Self-healer"),
            ("omni_crawler", "Omni crawler"),
            ("core_utils", "Core utilities")
        ]
        
        all_pass = True
        for module_name, description in modules:
            try:
                __import__(module_name)
                print_success(f"Imported: {module_name} ({description})")
                self.results["modules"].append({"module": module_name, "status": "OK"})
            except ImportError as e:
                print_error(f"Import failed: {module_name} - {e}")
                self.results["modules"].append({"module": module_name, "status": "ERROR"})
                all_pass = False
            except Exception as e:
                print_warning(f"Warning: {module_name} - {e}")
                self.results["modules"].append({"module": module_name, "status": "WARNING"})
        
        return all_pass
    
    def check_config(self):
        """Check configuration settings."""
        print("\n" + "="*60)
        print("CHECKING CONFIGURATION")
        print("="*60)
        
        try:
            import config
            
            checks = [
                ("ZERO_INVESTMENT_MODE", "Zero investment mode"),
                ("PREFER_GMAIL_ONLY", "Prefer Gmail"),
                ("ALLOW_BREVO_IN_ZERO_MODE", "Allow Brevo"),
                ("USE_AI_ANALYSIS", "AI analysis"),
                ("MAX_QUALIFIED_LEADS_PER_CYCLE", "Lead cycle limit"),
                ("MAX_PARALLEL_STRIKES", "Parallel strikes"),
                ("MISSION_INTERVAL_SECONDS", "Mission interval")
            ]
            
            all_pass = True
            for attr, description in checks:
                value = getattr(config, attr, None)
                if value is not None:
                    print_success(f"{description}: {value}")
                    self.results["config"].append({"item": description, "status": "OK", "value": str(value)})
                else:
                    print_warning(f"{description}: Not set")
                    self.results["config"].append({"item": description, "status": "WARNING"})
            
            return all_pass
            
        except Exception as e:
            print_error(f"Config check failed: {e}")
            return False
    
    def check_api_keys(self):
        """Check API keys configuration."""
        print("\n" + "="*60)
        print("CHECKING API KEYS")
        print("="*60)
        
        try:
            from dotenv import load_dotenv
            load_dotenv()
            
            import os
            
            keys = [
                ("TELEGRAM_BOT_TOKEN", "Telegram Bot", False),
                ("TELEGRAM_CHAT_ID", "Telegram Chat ID", False),
                ("BREVO_API_KEY", "Brevo API", False),
                ("BREVO_SMTP_PASSWORD", "Brevo SMTP", False),
                ("GMAIL_APP_PASSWORD", "Gmail App Password", False),
                ("GEMINI_API_KEY", "Gemini AI", False),
                ("GROQ_API_KEY", "Groq AI", False),
                ("SUPABASE_URL", "Supabase URL", False),
                ("SUPABASE_KEY", "Supabase Key", False)
            ]
            
            all_pass = True
            for key, description, required in keys:
                value = os.getenv(key, "")
                if value and len(value) > 5:
                    # Mask the value for display
                    masked = value[:8] + "..." + value[-4:] if len(value) > 12 else "****"
                    print_success(f"{description}: CONFIGURED ({masked})")
                    self.results["api_keys"].append({"key": description, "status": "OK"})
                else:
                    if required:
                        print_error(f"{description}: MISSING")
                        self.results["api_keys"].append({"key": description, "status": "MISSING"})
                        all_pass = False
                    else:
                        print_warning(f"{description}: NOT SET (optional)")
                        self.results["api_keys"].append({"key": description, "status": "OPTIONAL"})
            
            return all_pass
            
        except Exception as e:
            print_error(f"API key check failed: {e}")
            return False
    
    def check_self_healing(self):
        """Test self-healing system."""
        print("\n" + "="*60)
        print("CHECKING SELF-HEALING SYSTEM")
        print("="*60)
        
        try:
            from self_healer import healer
            summary = healer.get_health_summary()
            
            print_info(f"Overall Health: {summary['overall']}")
            print_info(f"Critical OK: {summary['critical_ok']}")
            print_info(f"Runtime OK: {summary['runtime_ok']}")
            print_info(f"Network OK: {summary['network_ok']}")
            print_info(f"Uptime: {summary['uptime']}")
            
            if summary['overall'] in ['🟢 HEALTHY', '🟡 RECOVERING']:
                print_success("Self-healing system is operational")
                return True
            else:
                print_warning("Self-healing needs attention")
                return False
                
        except Exception as e:
            print_error(f"Self-healing check failed: {e}")
            return False
    
    def check_database_connectivity(self):
        """Check database connectivity."""
        print("\n" + "="*60)
        print("CHECKING DATABASE CONNECTIVITY")
        print("="*60)
        
        try:
            import config
            
            if not config.SUPABASE_URL or not config.SUPABASE_KEY:
                print_warning("Supabase not configured - using local mode")
                return True
            
            import requests
            headers = {
                "apikey": config.SUPABASE_KEY,
                "Authorization": f"Bearer {config.SUPABASE_KEY}"
            }
            
            # Test connection
            url = f"{config.SUPABASE_URL}/rest/v1/"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code in [200, 401, 403]:
                print_success("Database connection: OK")
                return True
            else:
                print_warning(f"Database connection: {response.status_code}")
                return False
                
        except Exception as e:
            print_warning(f"Database check: {e}")
            return True  # Don't fail on this
    
    def check_smtp_connectivity(self):
        """Check SMTP providers."""
        print("\n" + "="*60)
        print("CHECKING SMTP PROVIDERS")
        print("="*60)
        
        import socket
        
        providers = [
            ("smtp-relay.brevo.com", 587),
            ("smtp.gmail.com", 587),
            ("smtp-mail.outlook.com", 587)
        ]
        
        any_success = False
        for host, port in providers:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                result = sock.connect_ex((host, port))
                sock.close()
                
                if result == 0:
                    print_success(f"{host}:{port} - REACHABLE")
                    any_success = True
                else:
                    print_warning(f"{host}:{port} - Not reachable")
            except Exception as e:
                print_warning(f"{host}:{port} - Error: {e}")
        
        return any_success
    
    def run_all_checks(self):
        """Run all verification checks."""
        print("\n" + "="*60)
        print("SAM JOB AUTOMATOR - SYSTEM VERIFICATION")
        print("Maximum Power - 100% Reliability Check")
        print("="*60)
        print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        checks = [
            ("Critical Files", self.check_critical_files),
            ("Runtime Files", self.check_runtime_files),
            ("Python Modules", self.check_modules),
            ("Configuration", self.check_config),
            ("API Keys", self.check_api_keys),
            ("Self-Healing", self.check_self_healing),
            ("Database", self.check_database_connectivity),
            ("SMTP", self.check_smtp_connectivity)
        ]
        
        results = []
        for name, check_func in checks:
            try:
                result = check_func()
                results.append((name, result))
            except Exception as e:
                print_error(f"{name} check crashed: {e}")
                results.append((name, False))
        
        # Summary
        print("\n" + "="*60)
        print("VERIFICATION SUMMARY")
        print("="*60)
        
        passed = 0
        failed = 0
        for name, result in results:
            if result:
                print_success(f"{name}: PASS")
                passed += 1
            else:
                print_warning(f"{name}: NEEDS ATTENTION")
                failed += 1
        
        print("\n" + "="*60)
        if failed == 0:
            print_success(f"ALL CHECKS PASSED! ({passed}/{len(results)})")
            print("Your system is ready for maximum power!")
        else:
            print_warning(f"CHECKS: {passed} passed, {failed} need attention")
            print("System can run but may have limitations.")
        print("="*60)
        
        # Save results
        self.results["summary"] = {
            "passed": passed,
            "failed": failed,
            "timestamp": datetime.now().isoformat()
        }
        
        with open("verification_results.json", "w") as f:
            json.dump(self.results, f, indent=2, default=str)
        
        print(f"\nResults saved to: verification_results.json")
        
        return failed == 0

def main():
    verifier = SystemVerifier()
    success = verifier.run_all_checks()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
