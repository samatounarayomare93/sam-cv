import os
import time
import hashlib
import smtplib
import subprocess
import logging
import requests
import asyncio
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s - [HEALER] %(levelname)s - %(message)s")

class RegenerativeSentinel:
    """
    [🕵️ PHASE OMEGA: REGENERATIVE INTELLIGENCE]
    The system's cortical repair engine. Uses LLM-based structural analysis
    to bypass website layout changes and automatically repair scrapers.
    """
    def __init__(self, db, ai):
        self.db = db
        self.ai = ai

    async def attempt_selector_repair(self, domain: str, html_sample: str, failed_field: str) -> Optional[str]:
        """Uses Omni-Intelligence to find new selectors for a broken field."""
        logging.info(f"🔧 SENTINEL: Attempting regenerative repair for {domain} ({failed_field})...")
        
        prompt = f"""
        Role: Senior Web Automation Engineer (Playwright/Scrapy Expert).
        Task: Identify the CSS selector for the '{failed_field}' in the following HTML sample.
        Target Domain: {domain}
        
        HTML Sample:
        {html_sample[:10000]}
        
        Rules:
        1. Return ONLY a valid CSS selector string.
        2. Reply with strict JSON: {{"selector": "...", "confidence": 0.0}}
        """
        
        try:
            data = await self.ai.structural_query(prompt)
            new_selector = data.get("selector")
            if new_selector:
                logging.info(f"✨ SENTINEL: New selector deduced: {new_selector}")
                # Auto-patch the DB
                if self.db:
                    await self.db.save_site_patch(domain, {failed_field: new_selector})
                    logging.info("💾 SENTINEL: Site patch successfully synchronized to the Hive-Mind.")
                return new_selector
        except Exception as e:
            logging.error(f"Sentinel repair failed: {e}")
            
        return None

class TemporalHealer:
    """The system's immune system. Monitors file integrity, process health, and communication vitality."""
    
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        self.critical_files: Dict[str, str] = {
            "core/main_bot.py": "",
            "core/ai_agent.py": "",
            "core/db_client.py": "",
            "core/smtp_engine.py": "",
            "core/pdf_generator.py": "",
            "config.py": "",
            ".env": ""
        }

        self.repair_script = os.path.join(self.base_dir, "scripts", "CHRONOS_REPAIR.bat")
        self.tg_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.tg_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self._generate_baseline_hashes()
        
        # Phase Omega: Strike Surveillance
        try:
            from core.db_client import get_db
            from core.ai_agent import OmniIntelligence
            self.db = get_db()
            self.ai = OmniIntelligence()
            self.sentinel = RegenerativeSentinel(self.db, self.ai)
        except Exception:
            self.db = None
            self.ai = None
            self.sentinel = None
        
        # Track state to prevent false positives
        self._last_integrity_check = 0
        self._consecutive_failures = 0
        self._max_consecutive_failures = 3

    def _hash_file(self, filepath: str) -> str:
        """SHA256 hash with error handling and chunked reading."""
        if not os.path.exists(filepath):
            return ""
        hasher = hashlib.sha256()
        try:
            with open(filepath, 'rb') as f:
                while chunk := f.read(65536):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception as e:
            logging.error(f"Hash error for {filepath}: {e}")
            return ""

    def _generate_baseline_hashes(self):
        """Generate baseline hashes for all critical files"""
        for f in list(self.critical_files.keys()):
            path = os.path.join(self.base_dir, f)
            if os.path.exists(path):
                self.critical_files[f] = self._hash_file(path)
                logging.info(f"📋 Baseline registered: {f}")

    def check_file_integrity(self) -> bool:
        """Verifies if core files were altered, corrupted, or deleted."""
        anomaly_detected = False
        for f, original_hash in self.critical_files.items():
            path = os.path.join(self.base_dir, f)
            current_hash = self._hash_file(path)
            
            if not current_hash:
                logging.error(f"❌ CRITICAL FILE MISSING: {f}")
                anomaly_detected = True
                continue
                
            if original_hash and current_hash != original_hash:
                logging.warning(f"⚠️ INTEGRITY BREACH DETECTED: {f} has been modified.")
                # Update hash to prevent infinite repair loop if user intended change
                self.critical_files[f] = current_hash
                anomaly_detected = True
                
        return not anomaly_detected

    def test_smtp_fallback(self) -> str:
        """Verifies SMTP providers with smart fallback logic and Telegram alerting."""
        providers = []
        
        # Gmail
        gmail_user = os.getenv("GMAIL_SMTP_USER", "").strip()
        gmail_pass = os.getenv("GMAIL_APP_PASSWORD", "").strip()
        if gmail_user and gmail_pass:
            providers.append(("Gmail", os.getenv("GMAIL_SMTP_SERVER", "smtp.gmail.com"), os.getenv("GMAIL_SMTP_PORT", 587), gmail_user, gmail_pass))
        
        # Brevo
        brevo_user = os.getenv("BREVO_SMTP_LOGIN", "").strip()
        brevo_pass = os.getenv("BREVO_SMTP_PASSWORD", "").strip()
        if brevo_user and brevo_pass:
            providers.append(("Brevo", os.getenv("BREVO_SMTP_SERVER", "smtp-relay.brevo.com"), os.getenv("BREVO_SMTP_PORT", 587), brevo_user, brevo_pass))
        
        if not providers:
            logging.critical("🚨 NO SMTP PROVIDERS CONFIGURED!")
            return "NONE"

        for name, host, port, user, pwd in providers:
            try:
                server = smtplib.SMTP(host, int(port), timeout=10)
                server.starttls()
                server.login(user, pwd)
                server.quit()
                logging.info(f"✅ Communications Pulse: {name} is alive.")
                self._consecutive_failures = 0
                return name
            except Exception as e:
                logging.error(f"❌ SMTP ERROR [{name}]: {str(e)[:100]}")
        
        self._consecutive_failures += 1
        if self._consecutive_failures >= self._max_consecutive_failures:
            logging.critical(f"🚨 ALL SMTP CHANNELS DEAD ({self._consecutive_failures} consecutive failures)")
        
        return "NONE"

    def send_tg_alert(self, message: str):
        """Sends an emergency alert to the owner via Telegram."""
        if not (self.tg_token and self.tg_chat_id): return
        url = f"https://api.telegram.org/bot{self.tg_token}/sendMessage"
        try:
            requests.post(url, json={"chat_id": self.tg_chat_id, "text": message, "parse_mode": "HTML"}, timeout=10)
        except Exception as e:
            logging.error(f"Failed to send TG alert: {e}")

    def is_bot_running(self) -> bool:
        """Checks if the main bot process is alive (Cross-Platform)."""
        if os.name == 'nt':
            try:
                output = subprocess.check_output('tasklist /FI "IMAGENAME eq python.exe" /FO CSV', shell=True).decode()
                return "python.exe" in output
            except: return False
        else:
            # Linux/Render check
            try:
                # Use pgrep to find any python process running launch_sam or main_bot
                output = subprocess.check_output(['pgrep', '-f', 'python']).decode()
                return len(output.strip()) > 0
            except: return False

    def execute_repair_sequence(self):
        """Triggers the automated recovery protocol."""
        logging.critical("🔧 ANOMALY DETECTED. EXECUTING DIVINE REPAIR...")
        self.send_tg_alert("🔧 <b>TEMPORAL HEALER ALERT</b>\nIntegrity breach detected. Executing Divine Repair sequence...")
        
        if os.path.exists(self.repair_script):
            try:
                subprocess.Popen([self.repair_script], creationflags=subprocess.CREATE_NEW_CONSOLE, shell=True, cwd=self.base_dir)
            except Exception as e:
                logging.error(f"Failed to ignite repair sequence: {e}")
        else:
            logging.error("FATAL: Repair Script missing from filesystem.")

    async def check_strike_vitality(self) -> bool:
        """WATCHDOG: Verifies if the bot is actually striking or just hanging."""
        if not self.db: return True
        
        try:
            last_strike_str = await self.db.get_last_strike_timestamp()
            if not last_strike_str: return True # System might be new
            
            # Simple ISO parse (Supabase format: 2024-04-15T10:00:00...)
            last_strike = datetime.fromisoformat(last_strike_str.replace('Z', '+00:00'))
            staleness = datetime.now(last_strike.tzinfo) - last_strike
            
            # If stall > 4h during business hours (8-18)
            hour = datetime.now().hour
            if staleness > timedelta(hours=4) and (8 <= hour <= 18):
                logging.critical(f"🚨 DEAD-MAN SWITCH TRIGGERED: Bot stalled for {staleness.total_seconds()/3600:.1f} hours.")
                return False
        except Exception as e:
            logging.error(f"Strike vitality check failed: {e}")
            
        return True

    async def run_immortal_loop(self):
        """Infinite surveillance loop with Phase Omega Watchdog."""
        logging.info("👑 Immortal Surveillance active. Watching over Project Chronos.")
        
        while True:
            try:
                # 1. Check file integrity
                if not self.check_file_integrity():
                    logging.warning("🔄 Attempting git pull restore...")
                    if not self.execute_git_pull():
                        self.execute_repair_sequence()
                
                # 2. Check Process Health
                if not self.is_bot_running():
                    logging.warning("⚠️ Main Bot process not found. Attempting restart.")
                    self.send_tg_alert("⚠️ <b>VITALITY ALERT</b>\nMain Bot process is offline. Restarting...")
                    self.execute_repair_sequence()
                
                # 3. Phase Omega: Check Strike Vitality
                is_vital = await self.check_strike_vitality()
                if not is_vital:
                    self.send_tg_alert("🚨 <b>DEAD-MAN SWITCH</b>\nBot has stalled for > 4 hours during mission time. Triggering rescue...")
                    self.execute_repair_sequence()

                # 4. Check SMTP status periodically
                if (int(time.time()) - self._last_integrity_check) % 900 < 600:
                    health = self.test_smtp_fallback()
                    if health == "NONE":
                        self.send_tg_alert("🚨 <b>COMMUNICATIONS BLACKOUT</b>\nAll SMTP channels are offline.")
                
                self._last_integrity_check = int(time.time())
                await asyncio.sleep(600) # 10 minute heartbeat
                
            except Exception as e:
                logging.error(f"Healer loop anomaly: {e}")
                await asyncio.sleep(60)

if __name__ == "__main__":
    healer = TemporalHealer()
    asyncio.run(healer.run_immortal_loop())
