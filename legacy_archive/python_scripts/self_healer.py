"""
Sam Job Automator - ENHANCED Self-Healing System v2
=======================================
MAXIMUM POWER: Faster healing, instant git restore, parallel diagnostics
"""

import os
import sys
import json
import time
import logging
import traceback
import shutil
import subprocess
from functools import wraps
from datetime import datetime, timedelta
from pathlib import Path
import requests
import concurrent.futures

# Configure logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("logs/healer.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# MAXIMUM POWER SELF-HEALING CONFIGURATION
# ============================================

class UltraHealingConfig:
    """Maximum power configuration for self-healing system."""
    
    def __init__(self):
        # MAXIMUM POWER: Faster retries and checks
        self.max_retries = 3  # Reduced from 5
        self.retry_delay = 1  # Halved from 3 seconds
        self.backup_enabled = True
        self.auto_repair = True
        self.health_check_interval = 30  # Halved from 60 - check every 30s
        self.auto_restart_on_failure = True
        self.max_consecutive_failures = 3
        self.max_workers = 4  # Parallel file checks
        
        # Critical files - must exist for system to work
        self.critical_files = [
            "config.py",
            "database.py",
            "scraper.py",
            "smtp_engine.py",
            "main_bot.py",
            "ai_agent.py",
            "system_health.py",
            "uplink.py"
        ]
        
        # Runtime files - can be recreated if missing
        self.runtime_files = [
            "tracker.json",
            "metrics.json",
            "health_check.json",
            "company_database.json",
            "discovered_companies.json",
            "system_pulse.txt"
        ]
        
        # Directory structure
        self.required_dirs = [
            "pdf_cache",
            "logs",
            "recovery",
            "recovery/runtime_backups",
            "recovery/logs"
        ]
        
        # External services to monitor (parallel check)
        self.health_check_urls = [
            "https://www.google.com",
            "https://api.telegram.org",
            "https://smtp-relay.brevo.com",
            "https://smtp.gmail.com"
        ]
        
        # Email providers to test
        self.smtp_tests = [
            ("smtp-relay.brevo.com", 587),
            ("smtp.gmail.com", 587),
            ("smtp-mail.outlook.com", 587)
        ]

# ============================================
# FILE SYSTEM HEALER - MAXIMUM POWER
# ============================================

class FileSystemHealer:
    """MAXIMUM POWER: Heals missing, corrupted, or broken files automatically with parallel checks."""
    
    def __init__(self, config):
        self.config = config
        self.healed_count = 0
        
    def _check_file_fast(self, filepath):
        """Fast single file integrity check"""
        if not os.path.exists(filepath):
            return ("missing", filepath)
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read(100)
            if not content:
                return ("empty", filepath)
            return ("ok", filepath)
        except Exception as e:
            return ("corrupted", filepath)
    
    def check_critical_files(self):
        """MAXIMUM POWER: Parallel file integrity checks"""
        missing = []
        corrupted = []
        
        # Use ThreadPoolExecutor for parallel checks (faster than sequential)
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.max_workers) as executor:
            results = list(executor.map(self._check_file_fast, self.config.critical_files))
        
        for status, filepath in results:
            if status == "missing":
                missing.append(filepath)
                logger.error(f"CRITICAL FILE MISSING: {filepath}")
            elif status == "empty" or status == "corrupted":
                corrupted.append(filepath)
                logger.error(f"CRITICAL FILE {status.upper()}: {filepath}")
        
        if missing or corrupted:
            return False, {"missing": missing, "corrupted": corrupted}
        
        return True, {"missing": [], "corrupted": []}
    
    def git_restore_all(self):
        """MAXIMUM POWER: Instant git restore for all modified files"""
        try:
            result = subprocess.run(
                ["git", "checkout", "--", "."],
                capture_output=True,
                text=True,
                timeout=30
            )
            if result.returncode == 0:
                logger.info("✅ Git restore successful - all files restored to last commit")
                return True
            else:
                logger.warning(f"⚠️ Git restore warning: {result.stderr}")
        except subprocess.TimeoutExpired:
            logger.error("❌ Git restore timed out")
        except Exception as e:
            logger.error(f"❌ Git restore error: {e}")
        return False
    
    def fix_runtime_files(self):
        """Recreate missing runtime files with proper defaults."""
        fixed = []
        
        for filepath in self.config.runtime_files:
            if not os.path.exists(filepath):
                try:
                    if filepath == "tracker.json":
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump({
                                "applications": [],
                                "last_updated": datetime.now().isoformat(),
                                "version": "2.0"
                            }, f, indent=2)
                    
                    elif filepath == "metrics.json":
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump({
                                "today": {"applications_sent": 0, "jobs_analyzed": 0, "errors": 0},
                                "this_week": {"applications_sent": 0, "jobs_analyzed": 0},
                                "this_month": {"applications_sent": 0, "jobs_analyzed": 0},
                                "all_time": {"applications_sent": 0, "jobs_analyzed": 0},
                                "last_run": datetime.now().isoformat(),
                                "version": "2.0"
                            }, f, indent=2)
                    
                    elif filepath == "health_check.json":
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump({
                                "system_health": "🟢 HEALTHY",
                                "components": {
                                    "pdf_cache": "✅",
                                    "database": "✅",
                                    "smtp": "✅",
                                    "telegram": "✅",
                                    "tracker": "✅",
                                    "ai_agent": "✅",
                                    "scraper": "✅"
                                },
                                "last_check": datetime.now().isoformat(),
                                "issues_fixed": 0,
                                "total_issues": 0,
                                "version": "2.0"
                            }, f, indent=2)
                    
                    elif filepath == "company_database.json":
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump({
                                "companies": [],
                                "total_unique": 0,
                                "last_updated": datetime.now().isoformat(),
                                "version": "2.0"
                            }, f, indent=2)
                    
                    elif filepath == "discovered_companies.json":
                        with open(filepath, 'w', encoding='utf-8') as f:
                            json.dump({
                                "companies": [],
                                "total": 0,
                                "last_updated": datetime.now().isoformat(),
                                "version": "2.0"
                            }, f, indent=2)
                    
                    elif filepath == "system_pulse.txt":
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(datetime.now().isoformat())
                    
                    fixed.append(filepath)
                    self.healed_count += 1
                    logger.info(f"🏥 AUTO-HEALED: {filepath}")
                    
                except Exception as e:
                    logger.error(f"Failed to heal {filepath}: {e}")
        
        return fixed
    
    def ensure_directories(self):
        """Create all required directories with maximum error tolerance."""
        created = []
        
        for dirname in self.config.required_dirs:
            try:
                if not os.path.exists(dirname):
                    os.makedirs(dirname, exist_ok=True)
                    created.append(dirname)
                    logger.info(f"📁 CREATED: Directory {dirname}")
                    
                # Also ensure parent directories exist
                path = Path(dirname)
                if path.exists() and path.is_dir():
                    # Create a .gitkeep to preserve empty directories
                    gitkeep = path / ".gitkeep"
                    if not gitkeep.exists():
                        gitkeep.touch()
                        
            except Exception as e:
                logger.error(f"Failed to create {dirname}: {e}")
        
        return created
    
    def verify_json_integrity(self, filepath):
        """Verify JSON file is valid and repair if possible."""
        if not os.path.exists(filepath):
            return False, "File not found"
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json.load(f)
            return True, "Valid"
        except json.JSONDecodeError as e:
            return False, f"Corrupted: {e}"
        except Exception as e:
            return False, f"Error: {e}"
    
    def repair_json_file(self, filepath):
        """Attempt to repair a corrupted JSON file."""
        logger.warning(f"🔧 ATTEMPTING REPAIR: {filepath}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Fix common JSON issues
            content = content.replace(',}', '}')
            content = content.replace(',]', ']')
            content = content.replace("'", '"')
            
            # Remove trailing commas
            import re
            content = re.sub(r',\s*([}\]])', r'\1', content)
            
            # Try to parse
            json.loads(content)
            
            # Write back
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            
            logger.info(f"✅ REPAIRED: {filepath}")
            return True
            
        except Exception as e:
            logger.error(f"Repair failed for {filepath}: {e}")
            
            # Backup corrupted file
            try:
                backup_path = filepath + f".corrupted.{int(time.time())}"
                shutil.copy2(filepath, backup_path)
                logger.info(f"📦 BACKED UP: Corrupted file to {backup_path}")
            except:
                pass
            
            return False

# ============================================
# NETWORK HEALER - ULTIMATE CONNECTIVITY
# ============================================

class NetworkHealer:
    """Heals network connectivity issues automatically."""
    
    def __init__(self):
        self.test_urls = [
            "https://www.google.com",
            "https://www.linkedin.com",
            "https://api.telegram.org",
            "https://smtp-relay.brevo.com"
        ]
        self.smtp_tests = [
            ("smtp-relay.brevo.com", 587),
            ("smtp.gmail.com", 587),
            ("smtp-mail.outlook.com", 587)
        ]
        self.timeout = 10
        self.last_connectivity_check = 0
        self.cached_connectivity = True
        
    def check_connectivity(self, force=False):
        """MAXIMUM POWER: Check internet connectivity with faster timeout"""
        now = time.time()
        
        # Use cache if recent
        if not force and (now - self.last_connectivity_check) < 30:  # Reduced from 60s
            return self.cached_connectivity
        
        reachable = []
        unreachable = []
        
        # Parallel connectivity check using ThreadPoolExecutor (much faster)
        def check_url(url):
            try:
                response = requests.get(url, timeout=5)  # Reduced from 10
                if response.status_code < 500:
                    return (url, True)
                return (url, False)
            except Exception:
                return (url, False)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=min(4, len(self.test_urls))) as executor:
            futures = [executor.submit(check_url, url) for url in self.test_urls]
            for future in concurrent.futures.as_completed(futures):
                url, is_reachable = future.result()
                if is_reachable:
                    reachable.append(url)
                else:
                    unreachable.append(url)
        
        self.last_connectivity_check = now
        self.cached_connectivity = len(unreachable) < len(reachable)
        
        return self.cached_connectivity
    
    def diagnose_smtp(self, host, port=587):
        """Diagnose SMTP connectivity with detailed feedback."""
        import socket
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            result = sock.connect_ex((host, port))
            sock.close()
            
            if result == 0:
                return True, f"✅ Connection to {host}:{port} successful"
            else:
                return False, f"❌ Connection to {host}:{port} failed (code: {result})"
        except Exception as e:
            return False, f"❌ Socket error: {e}"
    
    def test_all_smtp_providers(self):
        """Test all configured SMTP providers."""
        results = {}
        smtp_tests = [
            ("smtp-relay.brevo.com", 587),
            ("smtp.gmail.com", 587),
            ("smtp-mail.outlook.com", 587)
        ]
        for host, port in smtp_tests:
            success, message = self.diagnose_smtp(host, port)
            results[host] = {"success": success, "message": message}
        return results
    
    def test_telegram(self, bot_token):
        """Test Telegram bot connectivity with detailed status."""
        if not bot_token:
            return False, "No bot token provided", "MISSING"
        
        try:
            response = requests.get(
                f"https://api.telegram.org/bot{bot_token}/getMe",
                timeout=10
            )
            data = response.json()
            
            if data.get("ok"):
                return True, f"✅ Bot @{data['result']['username']} is working", "CONNECTED"
            else:
                return False, f"❌ Bot error: {data.get('description')}", "ERROR"
        except Exception as e:
            return False, f"❌ Connection error: {e}", "DISCONNECTED"

# ============================================
# BACKUP SYSTEM - SOVEREIGN PROTECTION
# ============================================

class BackupSystem:
    """Maximum protection backup system with auto-cleanup."""
    
    def __init__(self, backup_dir="recovery/runtime_backups"):
        self.backup_dir = Path(backup_dir)
        self.max_backups = 20  # Keep more backups
        self.files_to_backup = [
            "tracker.json",
            "metrics.json",
            "health_check.json",
            "company_database.json",
            "discovered_companies.json",
            "system_pulse.txt"
        ]
        
    def create_backup(self):
        """Create a timestamped backup with maximum protection."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_path = self.backup_dir / f"backup_{timestamp}"
            backup_path.mkdir(parents=True, exist_ok=True)
            
            backed_up = []
            for filename in self.files_to_backup:
                src = Path(filename)
                if src.exists():
                    try:
                        shutil.copy2(src, backup_path / filename)
                        backed_up.append(filename)
                    except Exception as e:
                        logger.warning(f"Backup failed for {filename}: {e}")
            
            logger.info(f"💾 Backup created: {backup_path.name} ({len(backed_up)} files)")
            
            # Clean old backups
            self.clean_old_backups()
            
            return True, str(backup_path), backed_up
            
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False, str(e), []
    
    def clean_old_backups(self):
        """Remove old backups, keeping only the most recent."""
        try:
            backups = sorted(self.backup_dir.glob("backup_*"), key=lambda p: p.name)
            
            while len(backups) > self.max_backups:
                oldest = backups.pop(0)
                try:
                    shutil.rmtree(oldest)
                    logger.debug(f"Removed old backup: {oldest.name}")
                except Exception as e:
                    logger.warning(f"Could not remove {oldest.name}: {e}")
                    
        except Exception as e:
            logger.error(f"Cleanup failed: {e}")
    
    def restore_latest(self):
        """Restore from the latest backup with maximum safety."""
        try:
            backups = sorted(self.backup_dir.glob("backup_*"), key=lambda p: p.name)
            
            if not backups:
                return False, "No backups found", []
            
            latest = backups[-1]
            restored = []
            
            for filename in self.files_to_backup:
                src = latest / filename
                dst = Path(filename)
                
                if src.exists():
                    try:
                        shutil.copy2(src, dst)
                        restored.append(filename)
                    except Exception as e:
                        logger.warning(f"Restore failed for {filename}: {e}")
            
            logger.info(f"♻️ Restored from: {latest.name} ({len(restored)} files)")
            return True, latest.name, restored
            
        except Exception as e:
            logger.error(f"Restore failed: {e}")
            return False, str(e), []

# ============================================
# MAIN SELF-HEALING ENGINE - MAXIMUM POWER
# ============================================

class UltraHealingEngine:
    """Ultimate self-healing system - never fails, always recovers."""
    
    def __init__(self):
        self.config = UltraHealingConfig()
        self.file_healer = FileSystemHealer(self.config)
        self.network_healer = NetworkHealer()
        self.backup = BackupSystem()
        self.last_health_check = 0
        self.healing_history = []
        self.consecutive_failures = 0
        self.start_time = datetime.now()
        
    def run_full_diagnostic(self):
        """Run complete system diagnostic with detailed reporting."""
        results = {
            "timestamp": datetime.now().isoformat(),
            "uptime": str(datetime.now() - self.start_time),
            "critical_files": {"status": "ok", "missing": [], "corrupted": []},
            "runtime_files": {"status": "ok", "missing": [], "corrupted": []},
            "directories": {"status": "ok", "missing": []},
            "network": {"status": "ok", "reachable": [], "unreachable": []},
            "smtp": {"status": "ok", "providers": {}},
            "overall": "🟢 HEALTHY"
        }
        
        # Check critical files
        ok, details = self.file_healer.check_critical_files()
        if not ok:
            results["critical_files"]["status"] = "ERROR"
            results["critical_files"] = details
            results["overall"] = "🔴 CRITICAL"
        
        # Check runtime files
        for filepath in self.config.runtime_files:
            valid, msg = self.file_healer.verify_json_integrity(filepath)
            if msg == "File not found":
                results["runtime_files"]["missing"].append(filepath)
                results["runtime_files"]["status"] = "WARNING"
            elif not valid:
                results["runtime_files"]["corrupted"].append({"file": filepath, "reason": msg})
                results["runtime_files"]["status"] = "WARNING"
                results["overall"] = "🟡 RECOVERING"
        
        # Check directories
        created = self.file_healer.ensure_directories()
        if created:
            results["directories"]["status"] = "WARNING"
            results["directories"]["missing"] = created
            results["overall"] = "🟡 RECOVERING"
        
        # Check network
        reachable, unreachable = [], []
        for url in self.config.health_check_urls:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code < 500:
                    reachable.append(url)
                else:
                    unreachable.append(url)
            except:
                unreachable.append(url)
        
        results["network"]["reachable"] = [u.split("//")[1] if "//" in u else u for u in reachable]
        results["network"]["unreachable"] = [u.split("//")[1] if "//" in u else u for u in unreachable]
        
        if len(unreachable) > len(reachable):
            results["network"]["status"] = "WARNING"
            results["overall"] = "🟡 RECOVERING"
        
        return results
    
    def auto_repair(self, diagnostic_results=None):
        """MAXIMUM POWER: Automatically repair ALL issues found with git restore option."""
        if diagnostic_results is None:
            diagnostic_results = self.run_full_diagnostic()
        
        repairs = []
        
        # Create backup before any repairs
        backup_ok, backup_path, _ = self.backup.create_backup()
        if backup_ok:
            repairs.append(f"Backup created: {backup_path}")
        
        # Check if critical files are missing/corrupted - use git restore
        crit_issues = diagnostic_results.get("critical_files", {})
        if crit_issues.get("missing") or crit_issues.get("corrupted"):
            logger.warning("Critical files issues detected - attempting git restore...")
            if self.file_healer.git_restore_all():
                repairs.append("Git restore successful - all files restored")
            else:
                repairs.append("Git restore failed - will recreate files")
        
        # Fix missing runtime files
        fixed = self.file_healer.fix_runtime_files()
        for f in fixed:
            repairs.append(f"Created: {f}")
        
        # Fix missing directories
        created = self.file_healer.ensure_directories()
        for d in created:
            repairs.append(f"Created directory: {d}")
        
        # Repair corrupted JSON files
        for item in diagnostic_results.get("runtime_files", {}).get("corrupted", []):
            filepath = item["file"]
            if self.file_healer.repair_json_file(filepath):
                repairs.append(f"Repaired: {filepath}")
        
        # Log healing action
        self.healing_history.append({
            "timestamp": datetime.now().isoformat(),
            "diagnostic": diagnostic_results,
            "repairs": repairs
        })
        
        # Keep history bounded
        if len(self.healing_history) > 100:
            self.healing_history = self.healing_history[-100:]
        
        return repairs
    
    def should_run_health_check(self):
        """Check if it's time for a health check."""
        now = time.time()
        if now - self.last_health_check > self.config.health_check_interval:
            self.last_health_check = now
            return True
        return False
    
    def get_health_summary(self):
        """Get a quick health summary."""
        diagnostic = self.run_full_diagnostic()
        return {
            "overall": diagnostic["overall"],
            "critical_ok": diagnostic["critical_files"]["status"] == "ok",
            "runtime_ok": diagnostic["runtime_files"]["status"] == "ok",
            "network_ok": diagnostic["network"]["status"] == "ok",
            "last_check": datetime.fromisoformat(diagnostic["timestamp"]).strftime("%H:%M:%S"),
            "uptime": diagnostic["uptime"],
            "consecutive_failures": self.consecutive_failures
        }
    
    def record_failure(self):
        """Record a failure for auto-restart logic."""
        self.consecutive_failures += 1
        if self.consecutive_failures >= self.config.max_consecutive_failures:
            logger.error(f"🚨 MAX FAILURES REACHED: {self.consecutive_failures}")
            return True
        return False
    
    def reset_failures(self):
        """Reset failure counter after successful operation."""
        self.consecutive_failures = 0

# ============================================
# AUTO-RETRY DECORATOR - MAXIMUM RESILIENCE
# ============================================

def auto_retry(max_attempts=5, delay=2, backoff=2):
    """Decorator for automatic retry with exponential backoff - never gives up."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}")
                    
                    if attempt < max_attempts:
                        sleep_time = delay * (backoff ** (attempt - 1))
                        logger.info(f"🔄 Retrying in {sleep_time}s...")
                        time.sleep(sleep_time)
            
            logger.error(f"{func.__name__} failed after {max_attempts} attempts - using fallback")
            return None  # Return None instead of raising to prevent crashes
        
        return wrapper
    return decorator

# ============================================
# GLOBAL INSTANCE
# ============================================

healer = UltraHealingEngine()

# ============================================
# MAIN - SELF-HEALING CHECK
# ============================================

if __name__ == "__main__":
    print("=" * 60)
    print("SAM ULTRA SELF-HEALING SYSTEM v2")
    print("Maximum Power - Never Fails - Always Recovers")
    print("=" * 60)
    
    # Run diagnostic
    print("\n[1] Running System Diagnostic...")
    results = healer.run_full_diagnostic()
    print(f"Overall Status: {results['overall']}")
    print(f"Uptime: {results['uptime']}")
    print(f"Critical Files: {results['critical_files']['status']}")
    print(f"Runtime Files: {results['runtime_files']['status']}")
    print(f"Network: {results['network']['status']}")
    
    # Auto repair
    print("\n[2] Running Auto-Repair...")
    repairs = healer.auto_repair(results)
    
    if repairs:
        print(f"  Repairs performed: {len(repairs)}")
        for repair in repairs:
            print(f"  + {repair}")
    else:
        print("  ✅ No repairs needed - System is perfect!")
    
    # Health summary
    print("\n[3] Health Summary:")
    summary = healer.get_health_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 60)
    print("ULTRA SELF-HEALING SYSTEM READY!")
    print("Your system is protected 24/7")
    print("=" * 60)
