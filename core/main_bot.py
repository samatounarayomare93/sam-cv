import asyncio
import logging
import os
import sys
import random
import time
import traceback
from typing import List, Dict, Any, Optional
import httpx
from dotenv import load_dotenv
import aiohttp
import requests
# Zero-Cost Cloud Logic: msvcrt removed for Linux compatibility

# Ensure we can import modules from core and root
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import internal components with absolute certainty
try:
    from core.db_client import RealityShapingDB
    from core.interview_prep import InterviewPrepEngine
    from core.ai_agent import OmniIntelligence
    from core.smtp_engine import send_strike
    from core.pdf_generator import create_personalized_pdf, generate_triple_package as generate_ultimate_package
except ImportError as e:
    logging.critical(f"INTERNAL SYSTEM FAILURE: Missing Core Components - {e}")
    RealityShapingDB = None
    InterviewPrepEngine = None
    OmniIntelligence = None

# ✅ Import SmartRetry for intelligent retry logic (replaces raw asyncio.sleep)
try:
    from core.error_recovery import SmartRetry, with_retry, get_error_recovery
    _smart_retry = SmartRetry(max_retries=3, base_delay=2.0, max_delay=30.0)
except ImportError:
    _smart_retry = None
    logging.warning("⚠️ error_recovery module not found — using basic retry fallback")

# Load legacy scrapers from their new nested location
try:
    from core.scrapers import scraper
    from core.scrapers.omni_crawler import OmniCrawler
    from core.scrapers.daleel_parallel import daleel_parallel_scan
except ImportError as e:
    logging.warning(f"⚠️ Scraper Layer Fragmented: {e}")
    scraper = None
    OmniCrawler = None

load_dotenv()

logging.basicConfig(
    level=getattr(logging, os.getenv("DIVINE_LOG_LEVEL", "INFO")),
    format="%(asctime)s - [CHRONOS] %(levelname)s - %(message)s"
)

# ═══════════════════════════════════════════════════════════════════════════════
# [👑 OMEGA-SINGULARITY: CYBERPUNK AESTHETICS]
# ═══════════════════════════════════════════════════════════════════════════════

CYBER_HEADER = """
╔══════════════════════════════════════════════════╗
║  ███╗   ███╗██╗██╗██╗████████╗███████╗██╗ ██████╗ ║
║  ████╗ ████║██║██║██║╚══██╔══╝██╔════╝██║██╔═══██╗║
║  ██╔████╔██║██║██║██║   ██║   █████╗  ██║██║   ██║║
║  ██║╚██╔╝██║██║██║██║   ██║   ██╔══╝  ██║██║   ██║║
║  ██║ ╚═╝ ██║██║██║██║   ██║   ██║     ██║╚██████╔╝║
║  ╚═╝     ╚═╝╚═╝╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ║
╚══════════════════════════════════════════════════╝
"""

def cyber_box(content, border_color="cyan"):
    border_chars = {
        "cyan": ("╔", "╗", "╚", "╝", "║", "═"),
        "pink": ("╔", "╗", "╚", "╝", "║", "═"),
        "green": ("┌", "┐", "└", "┘", "│", "─"),
    }
    tl, tr, bl, br, v, h = border_chars.get(border_color, border_chars["cyan"])
    lines = content.split('\n')
    max_len = max(len(line) for line in lines)
    result = f"{tl}{h * (max_len + 2)}{tr}\n"
    for line in lines:
        padding = max_len - len(line)
        result += f"{v} {line}{' ' * padding} {v}\n"
    result += f"{bl}{h * (max_len + 2)}{br}"
    return result

# OMEGA-SYNC: telebot removed. Unification with core.telegram_dashboard.py
# Import consolidated helper classes from runtime_helpers
from core.runtime_helpers import HumanParityJitter, EvasionRouter, ProxyMesh

from core.follow_up_engine import FollowUpEngine

from core.ai_agent import OmniIntelligence
from core.linkedin_automator import NeuralLinkedIn

# ═══════════════════════════════════════════════════════════════════════════════
# 🛡️ CENTRALIZED JUNK FILTER CONSTANTS
# Single source of truth — used by process_single_lead() AND _perform_self_healing()
# ═══════════════════════════════════════════════════════════════════════════════
JUNK_COMPANY_NAMES: set = {
    'login', 'die', 'press', 'how', 'win', 'create', 'company', 'who',
    'what', 'the', 'info', 'contact', 'about', 'home', 'page', 'test',
    'admin', 'user', 'unternehmensstruktur', 'unknown', 'none', 'null',
    'undefined', 'error', 'help', 'support', 'search', 'index', 'api',
    'target node', 'automatic target', 'oracle lead',
    'microsoft word', 'cv template', 'example company', 'test job', 'placeholder',
    'careers at', 'hiring manager', 'recruitment team', 'hr department',
    'application', 'resume', 'cv', 'job opening', 'linkedin job',
    'youtube', 'wikipedia', 'google', 'microsoft', 'apple', 'amazon',
    'odoo dubai office', 'top startup investors', 'dubai office',
    'search result', 'index of', 'parent directory',
    'new', 'word', 'my', 'it', 'top', 'best', 'list', 'well', 'future',
    'common', 'venture', 'doing business', 'stack overflow', 'startup programs',
    'newest questions', 'windows', 'tech', 'automatically', 'when',
    'arizona', 'install', 'biggest companies to work for in chandler',
    'murray company mechanical contractors', 'hensley beverage company',
    'gulf digest', 'ex', 'linkedin recruiter', 'official travel',
    'strategic interview questions cheat sheet',
    'www', 'http', 'https', 'com', 'org', 'net', 'co', 'io',
    'indeed', 'linkedin', 'glassdoor', 'monster', 'ziprecruiter',
    'bayt', 'naukrigulf', 'gulftalent', 'dubizzle', 'daleel madani',
    'akhtaboot', 'wuzzuf', 'crunchbase', 'builtin', 'wellfound',
    'angel.co', 'lever', 'greenhouse', 'workable', 'bamboohr',
    'kaito', 'kaito radios', 'kaito voyager', 'travel', 'right',
    'understanding companies', 'gulf recruitment', 'welcome to windows',
    'periodic labs hiring', 'google hiring',
}

JUNK_URL_DOMAINS: list = [
    'stackoverflow.com', 'windows.com', 'zippia.com', 'glassdoor.com',
    'crunchbase.com', 'techcrunch.com', 'wikipedia.org',
]

# ── Module-level constants used by _is_fake_domain ──────────────────────────
_FAKE_DOMAIN_GENERIC_WORDS: frozenset = frozenset({
    'new', 'my', 'it', 'top', 'word', 'list', 'well', 'future', 'common',
    'venture', 'best', 'homepage', 'home', 'startup', 'company', 'business',
    'office', 'work', 'job', 'jobs', 'career', 'careers', 'hire', 'hiring',
    'recruit', 'talent', 'people', 'team', 'staff', 'hr', 'human', 'resources',
    'global', 'world', 'international', 'group', 'corp', 'inc', 'llc', 'ltd',
    'the', 'a', 'an', 'and', 'or', 'of', 'in', 'at', 'by', 'for', 'with',
    'wight', 'airedale', 'heimdal', 'rhodeisland', 'doingbusiness',
    'stravavaluationpowersupto', 'newofficelondon', 'dubaiinternationalfinancialcentreattracts',
})
_FAKE_EXACT_EMAILS: frozenset = frozenset({
    'hr@new.com', 'hr@my.com', 'hr@it.com', 'hr@top.com',
    'hr@word.com', 'hr@list.com', 'hr@well.com', 'hr@future.com',
    'hr@common.com', 'hr@venture.com', 'hr@best.com',
    'hr@homepage.com', 'hr@home.com', 'hr@wight.com',
    'hr@airedale.com', 'hr@heimdal.com', 'hr@rhodeisland.com',
    'hr@doingbusiness.com', 'hr@stackoverflow.com',
    'hr@windows.com', 'hr@newestquestions.com',
    'hr@tech.com', 'hr@automatically.com', 'hr@when.com',
    'hr@arizona.com', 'hr@install.com', 'hr@gulpdigest.com',
    'careers@confidential.com', 'careers@ahiringcompany.com',
})
_NON_HIRING_DOMAINS: frozenset = frozenset({
    'stackoverflow.com', 'windows.com', 'microsoft.com', 'google.com',
    'apple.com', 'amazon.com', 'youtube.com', 'wikipedia.org',
    'facebook.com', 'twitter.com', 'instagram.com', 'tiktok.com',
    'reddit.com', 'github.com', 'zippia.com',
    'linkedin.com', 'lv.linkedin.com', 'ae.linkedin.com', 'uk.linkedin.com',
    'glassdoor.com', 'indeed.com', 'uk.indeed.com', 'ae.indeed.com',
    'monster.com', 'ziprecruiter.com', 'simplyhired.com',
    'bayt.com', 'naukrigulf.com', 'gulftalent.com', 'naukri.com',
    'dubizzle.com', 'daleel-madani.org', 'akhtaboot.com',
    'wuzzuf.net', 'forasna.com', 'tanqeeb.com',
    'crunchbase.com', 'techcrunch.com', 'builtin.com',
    'wellfound.com', 'angel.co', 'lever.co', 'greenhouse.io',
    'workable.com', 'bamboohr.com', 'smartrecruiters.com',
    'jobvite.com', 'icims.com', 'taleo.net',
})


def _is_fake_domain(email_addr: str) -> bool:
    """
    Module-level function (defined once, not per-call) that detects AI-generated
    fake email domains. Returns True if the email should be rejected.
    """
    if not email_addr or '@' not in email_addr:
        return True
    domain = email_addr.split('@')[-1].lower()

    if len(domain) > 35:
        return True

    base = domain.replace('.com', '').replace('.org', '').replace('.net', '').replace('.co', '').replace('-', '')
    if len(base) > 28:
        return True

    domain_root = domain.split('.')[0]
    if domain_root in _FAKE_DOMAIN_GENERIC_WORDS:
        return True

    if email_addr.lower() in _FAKE_EXACT_EMAILS:
        return True

    if domain in _NON_HIRING_DOMAINS:
        return True

    return False


async def _async_dns_check(domain: str, timeout: float = 3.0) -> bool:
    """
    Non-blocking async DNS check. Runs socket.getaddrinfo in a thread pool
    so it never blocks the event loop. Returns True if domain resolves.
    """
    import socket
    try:
        await asyncio.wait_for(
            asyncio.to_thread(socket.getaddrinfo, domain, None, socket.AF_INET, socket.SOCK_STREAM),
            timeout=timeout
        )
        return True
    except (asyncio.TimeoutError, socket.gaierror, OSError):
        return False


class AlphaOrchestrator:
    """Core orchestration engine with memory-efficient async scraping."""
    
    _instance = None
    _session: Optional[httpx.AsyncClient] = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self, concurrency_limit: int = int(os.getenv("MAX_PARALLEL_STRIKES", "5")), db=None, ai=None):
        if hasattr(self, '_initialized'):
            return
        self._initialized = True
        
        self.concurrency_limit = concurrency_limit
        self.semaphore = None  # [FIX] Lazy-init: must be created inside running event loop
        self.rate_limit_lock = None  # [FIX] Lazy-init: must be created inside running event loop
        self.orchestrator = self
        self.start_time = time.time()
        self.paused = False
        from core.runtime_helpers import get_evasion, get_proxy_mesh
        self.evasion = get_evasion()
        self.jitter = HumanParityJitter()
        self.proxy_mesh = get_proxy_mesh()
        self.is_running = True
        self.variant_weights = self.load_initial_weights()
        self._session = None
        self._total_requests = 0
        self._failed_requests = 0
        self.db = db if db else (RealityShapingDB() if RealityShapingDB else None)
        self.ai = ai if ai else (OmniIntelligence() if OmniIntelligence else None)
        # 🛡️ IN-MEMORY DEDUP: Prevents same lead being processed twice in same session
        self._processed_this_session = set()
        # 🛡️ PERMANENT DEDUP: company+email pairs that were successfully sent this run
        # (never reset — survives cycle resets to prevent duplicate sends)
        self._sent_company_email: set = set()
        # 🔒 ATOMIC DEDUP LOCK: Prevents race condition when parallel tasks check dedup simultaneously
        self._dedup_lock = None  # Lazy-init inside event loop
        self.follow_up = FollowUpEngine(self.db, self.ai)
        self.omni_crawler = OmniCrawler(self.ai) if OmniCrawler else None
        self.linkedin = NeuralLinkedIn(self.ai) if NeuralLinkedIn and self.ai else None
        self.decoy_count = int(os.getenv("DECOY_FLEET_SIZE", "2"))
        self.emergency_strike_requested = False

    @property
    def _semaphore(self):
        """Lazy-initialize Semaphore so it binds to the correct running event loop."""
        if self.semaphore is None:
            self.semaphore = asyncio.Semaphore(self.concurrency_limit)
        return self.semaphore

    @property
    def _rate_lock(self):
        """Lazy-initialize Lock so it binds to the correct running event loop."""
        if self.rate_limit_lock is None:
            self.rate_limit_lock = asyncio.Lock()
        return self.rate_limit_lock

    @property
    def _dedup_guard(self):
        """Lazy-initialize dedup Lock so it binds to the correct running event loop."""
        if self._dedup_lock is None:
            self._dedup_lock = asyncio.Lock()
        return self._dedup_lock

    async def poisson_jitter(self, target_mean: int):
        """100% STEALTH: Mimics human jitter behavior using Poisson distribution."""
        import random
        import math
        
        # Simple Poisson-like distribution
        L = math.exp(-target_mean)
        k = 0
        p = 1
        while p > L:
            k = k + 1
            p = p * random.random()
        delay = k - 1
        
        # Add 20% variance
        final_delay = max(2, delay + random.uniform(-0.2, 0.2) * delay)
        # Apply circadian multiplier
        final_delay /= self.get_circadian_intensity()
        
        await self.telemetry_stream("INFO", f"💓 Heartbeat: Mimicking human pulse... Delaying {final_delay:.1f}s")
        await asyncio.sleep(final_delay)

    async def telemetry_stream(self, level: str, message: str):
        """Broadcasts a signal to both local logging and the Global Hive-Mind terminal."""
        log_map = {"INFO": logging.info, "ERROR": logging.error, "WARNING": logging.warning, "CRITICAL": logging.critical}
        log_map.get(level, logging.info)(message)
        if self.db:
            try:
                asyncio.create_task(self.db.stream_log(level, message))
            except RuntimeError:
                pass

    def get_circadian_intensity(self) -> float:
        """Determines strike intensity based on day of week and hour."""
        from datetime import datetime
        now = datetime.now()
        day = now.weekday() # 0 = Monday, 6 = Sunday
        hour = now.hour
        
        # Higher intensity on Mon-Wed (0-2)
        multiplier = 1.0
        if day in [0, 1, 2]: multiplier = 1.3
        elif day in [5, 6]: multiplier = 0.5 # Weekend cooling
        
        # Peak business hours (8-11 and 14-16)
        if (8 <= hour <= 12) or (14 <= hour <= 17):
            multiplier *= 1.2
            
        return multiplier
        
    async def _get_session(self, target_location: str = "Global"):
        """
        [🌏 MULTIVERSE READY]
        Returns a stealth session with Latency-Matched IP Tunneling and TLS/JA3 Jitter.
        """
        if self._session is None:
            proxies = os.getenv("RESIDENTIAL_PROXIES", "").split(",") if os.getenv("RESIDENTIAL_PROXIES") else []
            
            # 📡 MULTIVERSE: Latency-Matched IP Tunneling (Geo-Cloning)
            # Attempt to find a proxy matching the target's geography
            proxy = random.choice(proxies) if proxies else None
            
            # Regional IP Tunneling Logic (Global -> Local)
            # If city-level proxy provider is used (format: 'user-zone-CITY:pass@provider:port')
            if proxy and target_location != "Global":
                loc_lower = target_location.lower()
                city_tags = {
                    "dubai": "dubai", "uae": "ae", "riyadh": "riyadh", "ksa": "sa",
                    "london": "london", "uk": "gb", "new york": "newyork", "ny": "us",
                    "california": "ca", "us": "us", "lebanon": "be", "beirut": "beirut"
                }
                for key, tag in city_tags.items():
                    if key in loc_lower:
                        # Inject regional tag into the proxy string (assuming standard provider logic)
                        if "customer-" in proxy and "zone-" in proxy:
                            proxy = proxy.replace("zone-", f"zone-{tag}-")
                        elif ":port_" in proxy:
                            proxy = proxy.split("_")[0] + "_" + tag
                        logging.info(f"📡 GEO-TUNNELING: Strike routed through proximal IP: {tag.upper()}")
                        break

            proxy_dict = {"http": proxy, "https": proxy} if proxy else None
            
            # 🕸️ OMNISCIENT: High-Entropy Impersonation
            # Rotate fingerprints to mimic a diverse human fleet
            fingerprints = ["chrome124", "safari17", "firefox120", "chrome110", "edge101"]
            impersonate_choice = random.choice(fingerprints)
            logging.info(f"🕸️ NETWORK MAPPING: Selected host fingerprint: {impersonate_choice}")

            # 🛡️ MULTIVERSE: Advanced TLS Fingerprint Jitter (JA3 Bypass)
            # Inject randomized TLS ALPN and Cipher strings to bypass enterprise security.
            tls_variants = ["chrome110", "chrome116", "safari15_5", "firefox102", "edge101"]
            tls_fingerprint = random.choice(tls_variants)
            
            self._session = httpx.AsyncClient(
                timeout=30,
                follow_redirects=True
            )
            # 🌌 TRANSCENDENCE: Session TTL Jitter
            self._session_created_at = time.time()
            self._session_ttl = random.randint(300, 900) # 5-15 mins
        
        # Check for session expiration
        if time.time() - getattr(self, '_session_created_at', 0) > getattr(self, '_session_ttl', 0):
            logging.info("🌌 NETWORK GHOST: Session expired. Refreshing host identity...")
            try:
                await self._session.aclose()
            except Exception:
                pass
            self._session = None
            return await self._get_session(target_location)
            
        return self._session
    
    async def close(self):
        """Graceful cleanup"""
        if self._session and not self._session.is_closed:
            await self._session.aclose()
        self._session = None

    async def check_kill_switch(self) -> bool:
        """Reads global environment AND live DB flag for instantaneous halt."""
        # Check env var first (fast)
        kill_switch = os.getenv("KILL_SWITCH_ACTIVE", "False").lower() == "true"
        
        # Also check DB kill switch (so /kill Telegram command actually works)
        if not kill_switch and self.db:
            try:
                success, data = await self.db._request_with_retry(
                    "GET",
                    f"{self.db.url}/rest/v1/system_settings?key=eq.kill_switch&select=value&limit=1"
                )
                if success and isinstance(data, list) and data:
                    db_kill = str(data[0].get("value", "false")).lower() == "true"
                    if db_kill:
                        kill_switch = True
            except Exception:
                pass  # If DB check fails, don't halt
        
        if kill_switch:
            logging.critical("🛑 KILL SWITCH ENGAGED. HALTING ALL OPERATIONS.")
            self.is_running = False
        return kill_switch

    async def _stealth_scrape_target(self, target_url: str) -> Optional[str]:
        """Execute stealth request with retry logic."""
        async with self._semaphore:
            headers = self.evasion.get_stealth_headers()
            max_retries = 3
            
            for attempt in range(max_retries):
                try:
                    session = await self._get_session()
                    response = await session.get(
                        target_url,
                        headers=headers,
                        follow_redirects=True
                    )
                    # 🔐 FIX #1: Thread-safe counter increment
                    async with self._rate_lock:
                        self._total_requests += 1
                        
                    if response.status_code == 200:
                        content = response.text
                        # Validate content
                        if len(content) > 100:
                            logging.info(f"⚡ Acquired: {target_url[:60]}...")
                            return content
                        else:
                            logging.warning(f"⚠️ Thin response from {target_url}")
                            return None
                            
                    elif response.status_code in [403, 429]:
                        wait_time = (attempt + 1) * 7 + random.uniform(2, 5)
                        logging.warning(f"🛡️ Blocked ({response.status_code}) - Force-rotating identity and waiting {wait_time:.1f}s...")
                        
                        # 🛡️ OMNISCIENT: Report block to Hive-Mind
                        if self.db:
                            domain = target_url.split("//")[-1].split("/")[0]
                            await self.db.report_blacklisted_domain(domain, f"HTTP {response.status_code}")
                        
                        # FORCE IDENTITY ROTATION
                        self.evasion.rotate_identity()
                        if self._session:
                            try:
                                await self._session.aclose()
                            except Exception:
                                pass
                            self._session = None # Force new session/proxy on retry
                            
                        await asyncio.sleep(wait_time)
                        
                    elif response.status_code in [500, 502, 503, 504]:
                        await asyncio.sleep(2 ** attempt)
                        
                    else:
                        logging.error(f"⚠️ HTTP {response.status_code} on {target_url[:50]}...")
                        return None
                            
                except asyncio.TimeoutError:
                    # 🔐 FIX #1: Thread-safe counter increment
                    async with self._rate_lock:
                        self._failed_requests += 1
                    logging.warning(f"⏳ Timeout on {target_url[:50]} (attempt {attempt + 1})")
                    await asyncio.sleep(2 ** attempt)
                    
                except Exception as e:
                    # 🔐 FIX #1: Thread-safe counter increment
                    async with self._rate_lock:
                        self._failed_requests += 1
                    logging.error(f"💥 Connection error {target_url[:50]}: {str(e)[:50]}")
                    await asyncio.sleep(1)
                    
            # 🔐 FIX #1: Thread-safe counter increment
            async with self._rate_lock:
                self._failed_requests += 1
            return None

    def is_business_hours(self, location: str = "Global") -> bool:
        """
        [🌏 MULTIVERSE READY]
        Sovereign timing: Checks if current time is optimal in the TARGET'S REALITY.
        Ensures strikes occur when the recruiter is likely active.
        """
        from datetime import datetime, timedelta
        import pytz # Standard in most advanced envs
        
        # Default to UTC (System)
        now_utc = datetime.now(pytz.UTC)
        
        # Timezone Mapping (Heuristic)
        tz_map = {
            "dubai": "Asia/Dubai", "uae": "Asia/Dubai", "emirates": "Asia/Dubai",
            "riyadh": "Asia/Riyadh", "ksa": "Asia/Riyadh", "saudi": "Asia/Riyadh",
            "london": "Europe/London", "uk": "Europe/London", "bsamin": "Europe/London",
            "new york": "America/New_York", "ny": "America/New_York", "usa": "America/New_York",
            "california": "America/Los_Angeles", "ca": "America/Los_Angeles",
            "lebanon": "Asia/Beirut", "beirut": "Asia/Beirut"
        }
        
        target_tz_name = "Asia/Beirut" # Default to Sam's primary region
        loc_lower = (location or "Global").lower()
        for key, tz in tz_map.items():
            if key in loc_lower:
                target_tz_name = tz
                break
        
        try:
            target_tz = pytz.timezone(target_tz_name)
            local_now = now_utc.astimezone(target_tz)
            hour = local_now.hour
            
            # Optimal recruiter visibility: 9AM - 5PM
            # Weekend Check (Fri/Sat in Middle East, Sat globally)
            # [👑 ABSOULTE-STRIKE]: Overriding all circadian checks for 1000% mission readiness.
            return True
        except Exception:
            return True

    def load_initial_weights(self) -> Dict[str, float]:
        """[🧬 PHASE EVOLUTION] Load analytical weights with reinforcement potential."""
        return {
            "EMPATHETIC": 0.25,
            "AGGRESSIVE": 0.25,
            "ANALYTICAL": 0.25,
            "VISIONARY": 0.25
        }

    async def sync_evolutionary_weights(self):
        """Fetches latest performance-based weights from the Hive-Mind."""
        if not self.db: return
        if _smart_retry:
            try:
                new_weights = await _smart_retry.retry_async(self.db.get_variant_weights)
                if new_weights:
                    self.variant_weights = new_weights
                    logging.info(f"🧬 EVOLUTION: Swarm weights synchronized: {self.variant_weights}")
            except Exception as e:
                logging.error(f"Evolution sync failure after retries: {e}")
        else:
            try:
                new_weights = await self.db.get_variant_weights()
                if new_weights:
                    self.variant_weights = new_weights
                    logging.info(f"🧬 EVOLUTION: Swarm weights synchronized: {self.variant_weights}")
            except Exception as e:
                logging.error(f"Evolution sync failure: {e}")

    async def process_single_lead(self, lead: Dict[str, Any], variant_weights: Dict[str, float] = None):
        """Runs the complete AI analysis and database verification on a single job lead."""
        # [👑 SOVEREIGN NORMALIZATION]: Ensure consistent keys regardless of source (Local vs Cloud)
        company_name = lead.get("company_name") or lead.get("company", "Unknown Company")
        job_title = lead.get("job_title") or lead.get("title", "Professional Role")
        job_url = lead.get("job_url") or lead.get("url") or lead.get("link", "")
        email = lead.get("email", "")
        description = lead.get("description", "")
        is_recon = lead.get("is_guessed", False)
        
        # Back-fill lead dict for downstream components
        lead["job_url"] = job_url
        lead["company_name"] = company_name
        lead["job_title"] = job_title

        # 🛡️ IN-MEMORY DEDUP: Prevent same lead being processed twice in same session
        session_key = f"{company_name}_{email}_{job_url}"
        # Also dedup by company+email alone to prevent parallel tasks hitting same target
        company_email_key = f"{company_name.lower().strip()}_{(email or '').lower().strip()}"

        # 🔒 ATOMIC CHECK-AND-ADD: Lock prevents race condition where two parallel tasks
        # both pass the check before either adds to the set (would cause duplicate sends)
        async with self._dedup_guard:
            if session_key in self._processed_this_session or company_email_key in self._processed_this_session:
                logging.info(f"⏭️ [SESSION-DEDUP] Already processed this session: {company_name}. Skipping.")
                return
            if company_email_key in self._sent_company_email:
                logging.info(f"⏭️ [PERM-DEDUP] Already sent to {company_name} this run. Skipping.")
                return
            # Add atomically inside the lock — no other task can slip through
            self._processed_this_session.add(session_key)
            self._processed_this_session.add(company_email_key)

        # Keep set size manageable (clear oldest entries if > 10000)
        if len(self._processed_this_session) > 10000:
            self._processed_this_session = set(list(self._processed_this_session)[-5000:])

        # 🛡️ ANTI-BAN PROTECTION: Check before processing
        from core.anti_ban_protection import get_protection
        protection = get_protection()
        
        can_apply, reason = await protection.can_apply(company_name, job_title, description, email)
        if not can_apply:
            logging.info(f"🛡️ PROTECTION: {reason} - Skipping {company_name}")
            if self.db and job_url:
                await self.db.update_lead_status(job_url, 'rate_limited')
            return

        # [🛡️ JUNK FILTER]: Reject garbage leads from blind extraction
        # Uses centralized JUNK_COMPANY_NAMES constant (defined at module level)
        
        # [🛡️ FAKE DOMAIN FILTER]: Uses module-level _is_fake_domain() — defined once, not per-call
        
        if company_name.lower().strip() in JUNK_COMPANY_NAMES or len(company_name.strip()) < 2:
            logging.info(f"🗑️ JUNK FILTER: Rejected garbage lead '{company_name}'. Skipping.")
            # Also mark it as processed in the cloud to stop it from reappearing
            if self.db and job_url:
                await self.db.update_lead_status(job_url, "rejected")
            return
        
        # Check for fake/AI-generated email domains
        if email and _is_fake_domain(email):
            logging.info(f"🗑️ FAKE DOMAIN FILTER: Rejected fake email '{email}' for '{company_name}'. Skipping.")
            if self.db and job_url:
                await self.db.update_lead_status(job_url, "rejected")
            return

        # 🛡️ MX RECORD CHECK: Verify domain actually accepts emails (prevents bounces)
        # Uses non-blocking async DNS check — never blocks the event loop
        if email and '@' in email:
            domain = email.split('@')[-1].lower()
            dns_ok = await _async_dns_check(domain)
            if not dns_ok:
                logging.info(f"🗑️ DNS FAIL: Domain '{domain}' doesn't resolve — rejecting '{email}'")
                if self.db and job_url:
                    await self.db.update_lead_status(job_url, "rejected")
                return
        
        # ✅ FIX: Early email check — no point running AI analysis on leads with no contact
        if not email:
            logging.info(f"📭 NO EMAIL: Lead '{company_name}' has no contact info. Marking skipped.")
            if self.db and job_url:
                await self.db.update_lead_status(job_url, "no_contact")
            return

        identifier = job_url if job_url else email
        
        # 1. Global DB Deduplication Check
        if self.db and identifier:
            is_dup = await self.db.is_duplicate(identifier)
            if is_dup:
                logging.info(f"⏭️ Skipping duplicate target: {company_name}")
                return

            # 🛡️ PRE-CLAIM: Mark as 'processing' immediately to prevent parallel tasks
            # from sending duplicate emails to the same company
            try:
                await self.db.update_lead_status(identifier, 'processing')
            except Exception:
                pass

        # ── Wrap the rest in try/finally so lead never stays stuck as 'processing' ──
        _marked_processing = bool(self.db and identifier)
        
        # 🛡️ OMNISCIENT: Global Blacklist Check
        domain = identifier.split("@")[-1] if "@" in identifier else ""
        if domain and self.db and await self.db.is_globally_blacklisted(domain):
            logging.warning(f"🛡️ HIVE-MIND BLOCK: {company_name} is under network-wide cooling. Aborting.")
            return
        if not description and job_url:
            logging.info(f"🔍 Deep Scraping Target Description: {job_url}")
            description = await self._stealth_scrape_target(job_url)

        # 3. AI Analysis & RAG Pipeline
        try:
          if self.ai:
            from core.cv_tailor import get_tailored_cv_path
            from core.scrapers.omni_crawler import MarketOracle
            from core.ultimate_failover import get_failover
            
            logging.info(f"🧠 Beaming target to Omni-Intelligence: {company_name}")
            
            # 🛡️ ULTIMATE FAILOVER: Try AI, fallback to templates if it fails
            try:
                # 🏹 OMNISCIENT: Swarm Intelligence Integration
                # Check the Hive-Mind first to see if another node has already sniped this target.
                hiring_mgr = lead.get("hiring_manager")
                recruiter_data = await self.db.get_global_recon(company_name) if self.db else None
                
                if recruiter_data:
                    logging.info(f"👑 HIVE-MIND SYNC: Recruiter already sniped: {recruiter_data['name']}")
                    hiring_mgr = recruiter_data["name"]
                else:
                    # Sniper Recon (LinkedIn Sniper)
                    if not hiring_mgr or hiring_mgr == "Unknown" or hiring_mgr == "Hiring Manager":
                        try:
                            recruiter_data = await MarketOracle.get_recruiter_info(company_name, job_title)
                            hiring_mgr = recruiter_data["name"]
                            # Report success to the swarm
                            if self.db: await self.db.report_recon_success(company_name, hiring_mgr, recruiter_data.get("url", ""))
                        except Exception as e:
                            logging.warning(f"⚠️ LinkedIn recon failed: {e}")
                            hiring_mgr = "Hiring Manager"
                
                # Record Nudge Task for the Sniped Recruiter
                try:
                    await self.record_linkedin_nudge_task(company_name, job_title, recruiter_data)
                except Exception as e:
                    logging.warning(f"⚠️ LinkedIn nudge task failed: {e}")
                
                # 📰 APEX DEITY: News-Pulse Recon (Oracle Pulse)
                try:
                    news_headline = await MarketOracle.get_latest_news(company_name)
                    oracle_pulse = await MarketOracle.get_news_pulse(company_name)
                    logging.info(f"🔮 ORACLE PULSE: Sentiment: {oracle_pulse['sentiment']} | Event: {oracle_pulse['event']}")
                except Exception as e:
                    logging.warning(f"⚠️ News pulse failed: {e}")
                    news_headline = ""
                    oracle_pulse = {"sentiment": "neutral", "event": "none"}
                
                # 🧬 OMNISCIENT: Total Narrative Recon
                try:
                    company_values = await MarketOracle.get_culture_values(company_name)
                    competitor_fail = await MarketOracle.get_competitor_disruption(company_name)
                except Exception as e:
                    logging.warning(f"⚠️ Company recon failed: {e}")
                    company_values = []
                    competitor_fail = ""
                
                # 🌌 TRANSCENDENCE: Social Infiltration Recon
                try:
                    internal_lingo = await MarketOracle.get_internal_lingo(company_name)
                    executive_names = await MarketOracle.get_leadership_team(company_name)
                except Exception as e:
                    logging.warning(f"⚠️ Social recon failed: {e}")
                    internal_lingo = []
                    executive_names = []
                
                # Fetch latest evolutionary weights before analysis
                await self.sync_evolutionary_weights()
                current_weights = variant_weights or self.variant_weights

                location = lead.get("location") or "Global"
                
                # 🛡️ TRY AI ANALYSIS
                try:
                    is_relevant, reason, cover_letter, salary, score, advantage, keywords, persona, psych_variant, archetype, highlights = await self.ai.analyze_job(
                        job_title, 
                        description[:3000] if description else "Professional role",
                        variant_weights=current_weights,
                        person_name=hiring_mgr,
                        location=location,
                        news_headline=news_headline,
                        company_values=company_values,
                        competitor_fail=competitor_fail,
                        internal_lingo=internal_lingo,
                        executive_names=executive_names,
                        oracle_pulse=oracle_pulse
                    )
                except Exception as ai_error:
                    # 🛡️ ULTIMATE FAILOVER: AI failed, use fallback templates
                    logging.error(f"❌ AI ANALYSIS FAILED: {ai_error}")
                    logging.info("🛡️ ACTIVATING FAILOVER: Using pre-written templates")
                    
                    failover = get_failover()
                    fallback_result = failover._fallback_analysis(job_title, description, company_name)
                    
                    is_relevant = fallback_result['is_relevant']
                    reason = fallback_result['reason']
                    cover_letter = fallback_result['cover_letter']
                    salary = fallback_result['salary']
                    score = fallback_result['score']
                    advantage = fallback_result['advantage']
                    keywords = fallback_result['keywords']
                    persona = fallback_result['persona']
                    psych_variant = fallback_result['psych_variant']
                    archetype = fallback_result['archetype']
                    highlights = fallback_result['highlights']
                    
                    logging.info(f"✅ FAILOVER SUCCESS: Generated application using template (score: {score})")
            
            except Exception as e:
                # 🛡️ ULTIMATE FAILOVER: Even if everything fails, use basic template
                logging.error(f"❌ COMPLETE ANALYSIS FAILURE: {e}")
                logging.info("🛡️ ULTIMATE FAILOVER: Using basic template")
                
                failover = get_failover()
                fallback_result = failover._fallback_analysis(job_title, description or "", company_name)
                
                is_relevant = True  # Always try to apply
                reason = "Failover mode - applying with template"
                cover_letter = fallback_result['cover_letter']
                salary = "Competitive"
                score = 70  # Default score
                advantage = "Strong technical background"
                keywords = ["network", "engineer", "infrastructure"]
                persona = "Professional"
                psych_variant = "ANALYTICAL"
                archetype = "Technical Expert"
                highlights = fallback_result['highlights']
            
            # ELITE SCORE THRESHOLD: 70 minimum for quality applications
            # Jitter prevents "Hard Blocking" on close matches
            jitter = random.randint(-3, 3)
            strike_threshold = (75 if lead.get("mission_type") == "Founding_Strike" else 70) + jitter
            
            if not is_relevant or score < strike_threshold:
                logging.info(f"❌ Target Denied by Intelligence: {company_name} | Score: {score}/{strike_threshold} | Reason: {reason[:100]}...")
                if self.db and job_url: await self.db.update_lead_status(job_url, 'rejected')
                return
            
            # RECON SURGE: Self-Healing Logic for High-Value Leads
            if not email and (score >= 75 or lead.get("mission_type") == "Founding_Strike"):
                logging.info(f"🧬 COSMIC RECON SURGE: High-value target {company_name} lacks contact. Deep-diving...")
                emails = await self.omni_crawler.recon_surge(company_name)
                if emails:
                    email = emails[0]
                    logging.info(f"✅ RECON SUCCESS: Found {email} for {company_name}")
            
            if not email:
                logging.warning(f"⚠️ No contact info for {company_name}. Strike Aborted.")
                if self.db and job_url: await self.db.update_lead_status(job_url, 'no_contact')
                return

            # CIRCADIAN TIMING
            if not self.is_business_hours(location):
                logging.info(f"⏳ CIRCADIAN HOLD: Holding strike for {company_name} until business hours.")
                if self.db and job_url: await self.db.update_lead_status(job_url, 'circadian_hold')
                return
            
            mission_display = lead.get("mission_type", "Evolutionary_Apex_Strike")
            logging.info(f"✅ Target Locked [{score}%]: {company_name} | Archetype: {archetype} | Variant: {psych_variant}")
            await self.telemetry_stream("INFO", f"🎯 SINGULARITY STRIKE LOCKED ({score}%) - {company_name}")
            
            # 4. Global CV Personalization (with ATS Bypass)
            logging.info(f"🎭 Masking Identity: Tailoring CV for {persona} culture.")
            tailored_html_path = await asyncio.to_thread(get_tailored_cv_path, company_name.replace(" ", "_"), job_title, advantage, keywords)
            
            # 🕵️ APEX DEITY: Shadow Tracking ID (NSA-Style)
            # Embed an invisible, forensic ID into the cover letter body.
            strike_id = f"{company_name[:4]}-{random.randint(1000, 9999)}"
            cover_letter = self.ai.encode_shadow_id(cover_letter, strike_id)
            
            # 5. Execute Strike Package (PDF + Email)
            lead_update = {
                "custom_body": cover_letter,
                "mission_type": mission_display,
                "tailored_cv_path": tailored_html_path,
                "culture_persona": persona,
                "personality_archetype": archetype,
                "psychological_variant": psych_variant,
                "email": email, # Update if recon surge found it
                "score": score,
                "strike_id": strike_id,
                "highlights": highlights
            }
            lead.update(lead_update)
            
            await self.poisson_jitter(5)
            # 👑 [ABSOLUTE VMAX: TWO-FILE PACKAGE]
            # Attaching PDF Cover Letter (Byblos Standard) + HTML VMAX CV.
            package = await asyncio.to_thread(generate_ultimate_package, lead)
            
            final_attachments = []
            if package.get("cv"): final_attachments.append(package["cv"])
            if package.get("cl"): final_attachments.append(package["cl"])
            
            if final_attachments:
                await self.poisson_jitter(10)
                success = await asyncio.to_thread(send_strike, lead, final_attachments)
                
                # [🧹 100-YEAR STABILITY]: Disk Cleanup to prevent memory/storage leaks over time
                try:
                    if isinstance(final_attachments, str) and os.path.exists(final_attachments):
                        os.remove(final_attachments)
                    elif isinstance(final_attachments, list):
                        for f in final_attachments:
                            if f and os.path.exists(f): os.remove(f)
                except Exception as e:
                    logging.warning(f"🧹 Cleanup failed for {company_name}: {e}")
                
                if success:
                    logging.info(f"🚀 STRIKE SUCCESS: Application beamed to {company_name}")
                    await self.telemetry_stream("SUCCESS", f"✅ STRIKE SUCCESS - {company_name}")
                    
                    # 🛡️ ANTI-BAN: Record successful application
                    from core.anti_ban_protection import get_protection
                    protection = get_protection()
                    protection.record_application(company_name, success=True)

                    # 🛡️ PERMANENT DEDUP: Mark company+email as sent so no duplicate in future cycles
                    self._sent_company_email.add(company_email_key)
                    
                    # 🧬 GHOST HUB: Pre-generate tactical cheat sheet for zero-latency prep
                    if score >= 85:
                        logging.info(f"👻 GHOST HUB: Generating tactical cheat sheet for {company_name}...")
                        cheat_sheet = await self.ai.generate_cheat_sheet(company_name, job_title)
                        lead['cheat_sheet'] = cheat_sheet
                    
                    if self.db:
                        # Log enriched data including variant for learning
                        await self.db.log_application(lead)
                        if job_url: await self.db.update_lead_status(job_url, 'processed')
                    
                    # 🇷🇺 THE MOSCOW TRICK: Launch Decoy Fleet
                    if score >= 85:
                        logging.info(f"🇷🇺 DECOY FLEET: Deploying support fleet for {company_name} strike...")
                        asyncio.create_task(self.deploy_decoy_fleet(lead, hiring_mgr))
                else:
                    logging.error(f"❌ STRIKE FAILED: {company_name}")
                    
                    # 🛡️ ANTI-BAN: Record failed application
                    from core.anti_ban_protection import get_protection
                    protection = get_protection()
                    protection.record_application(company_name, success=False)
                    
                    if self.db and job_url: await self.db.update_lead_status(job_url, 'failed')
            else:
                logging.error(f"❌ STRIKE FAILED: PDF Synthesis error for {company_name}")
                if self.db and job_url: await self.db.update_lead_status(job_url, 'pdf_error')

        # 🛡️ SAFETY NET: If an unhandled exception occurs, ensure lead doesn't stay stuck as 'processing'
        except Exception as _lead_err:
            logging.error(f"💥 [PROCESS-LEAD] Unhandled error for '{company_name}': {type(_lead_err).__name__}: {_lead_err}")
            if _marked_processing and self.db and identifier:
                try:
                    await self.db.update_lead_status(identifier, 'error')
                except Exception:
                    pass

    async def record_linkedin_nudge_task(self, company: str, role: str, recruiter: Dict[str, str]):
        """Records a task to manually connect with the sniped recruiter on LinkedIn."""
        if not recruiter.get("url") or not self.linkedin or not self.db:
            return
            
        # 🧠 Generate actual message via Neural engine
        nudge_message = await self.linkedin.generate_nudge(recruiter['name'], company, role)
        
        await self.telemetry_stream("INFO", f"🎯 RECRUITER SNIPED: {recruiter['name']} @ {company}")
        
        # 💾 Persist to Hive-Mind for Dashboard
        await self.linkedin.record_nudge_task(self.db, recruiter['name'], nudge_message, recruiter['url'])
        logging.info(f"🎯 NUDGE TASK RECORDED: {recruiter['name']} @ {company}")

    async def deploy_decoy_fleet(self, primary_lead: Dict[str, Any], hiring_mgr: str):
        """
        🇷🇺 DECOY FLEET: Deploys fake applicants to shift the recruiter's baseline.
        This makes Sam look like the only logical choice.
        """
        company = primary_lead.get("company_name")
        job_title = primary_lead.get("job_title")
        email = primary_lead.get("email")
        
        for i in range(self.decoy_count):
            try:
                # 1. Generate Persona
                persona = await self.ai.generate_decoy_persona(job_title, company)
                # 2. Generate Letter
                letter = await self.ai.generate_decoy_letter(persona, job_title, company)
                
                # 3. Create Decoy Lead
                decoy_lead = primary_lead.copy()
                decoy_lead.update({
                    "custom_body": letter,
                    "mission_type": "DECOY_STRIKE",
                    "hiring_manager": hiring_mgr,
                    "culture_persona": "Decoy"
                })
                
                # Wait for primary strike to land first
                await asyncio.sleep(60 * (i + 1) * random.uniform(1, 2))
                
                # 4. Generate Forensic PDF
                pdf_path = await asyncio.to_thread(create_personalized_pdf, decoy_lead)
                
                if pdf_path and os.path.exists(pdf_path):
                    # 5. Strike
                    success = await asyncio.to_thread(send_strike, decoy_lead, pdf_path, sender_name=persona['name'])
                    
                    # [🧹 100-YEAR STABILITY]: Disk Cleanup
                    try:
                        os.remove(pdf_path)
                    except OSError as _rm_err:
                        logging.debug(f"⚠️ [CLEANUP] Could not remove temp PDF {pdf_path}: {_rm_err}")
                    
                    if success:
                        logging.info(f"🇷🇺 DECOY SUCCESS: {persona['name']} deployed against {company}.")
            except Exception as e:
                logging.error(f"🇷🇺 DECOY FAILURE: {e}")

    async def _leadership_watchdog(self):
        """[👑 SOVEREIGN WATCHDOG]: Continuously monitors leadership to prevent 409 conflicts."""
        while self.is_running:
            try:
                if self.db:
                    is_leader = await self.db.claim_bot_leadership()
                    is_render = os.getenv("RENDER") is not None
                    
                    if not is_leader and not is_render:
                        # Check if a cloud node is actually active (not just stale)
                        # The db_client already handles staleness logic in claim_bot_leadership,
                        # but we want to be extra careful here.
                        logging.critical("🏰 SOVEREIGN OVERRIDE: Cloud Node is active. Shutting down local instance.")
                        import sys
                        sys.exit(0)
            except Exception as e:
                logging.debug(f"Leadership watchdog error: {e}")
            await asyncio.sleep(30)

    async def _perform_self_healing(self):
        """
        [🛡️ SOVEREIGN SELF-HEALING]
        Automatically detects queue jams, stale leads, and junk data blocks.
        """
        if not self.db: return
        
        try:
            # 1. PURGE JUNK LEADS: Mass-reject known garbage strings in the DB
            # Uses centralized JUNK_COMPANY_NAMES constant (defined at module level)
            for pattern in JUNK_COMPANY_NAMES:
                await self.db._request_with_retry('PATCH',
                    f"{self.db.url}/rest/v1/leads?company_name=eq.{pattern}&status=eq.pending",
                    payload={"status": "rejected"})

            # Also purge by junk job URLs (non-hiring domains)
            for domain in JUNK_URL_DOMAINS:
                try:
                    await self.db._request_with_retry('PATCH',
                        f"{self.db.url}/rest/v1/leads?job_url=like.*{domain}*&status=eq.pending",
                        payload={"status": "rejected"})
                except Exception as _purge_err:
                    logging.debug(f"⚠️ [SELF-HEAL] Could not purge junk domain {domain}: {_purge_err}")
            
            # 2. STAGNATION PREVENTION: Mark leads older than 7 days as expired (was 48h - too aggressive)
            from datetime import datetime, timedelta
            stale_threshold = (datetime.now() - timedelta(hours=168)).isoformat()  # 7 days
            await self.db._request_with_retry('PATCH', 
                f"{self.db.url}/rest/v1/leads?status=eq.pending&created_at=lt.{stale_threshold}", 
                payload={"status": "stale_expired"})
            
            logging.info("🛡️ SELF-HEALING: Hive-Mind scrubbed. Junk purged. Stale leads archived.")
        except Exception as e:
            logging.error(f"⚠️ SELF-HEALING FAILURE: {e}")

    async def execute_divine_loop(self):
        """Main execution loop with adaptive timing and Alpha-Centauri Swarm features."""
        logging.info("🌞 CHRONOS: Divine Loop Initialized. [VERSION: 10^20% PERFECTION] Absolute Dominance Protocol Active.")
        
        # Start background watchdog
        asyncio.create_task(self._leadership_watchdog())
        
        # [🛡️ SOVEREIGN MODE DETECTION]
        health = self.db.get_system_health() if self.db else {"mode": "standalone"}
        mode_msg = f"🛰️ SWARM MODE: {health['mode']} Protocol Active."
        logging.info(mode_msg)
        await self.telemetry_stream("INFO", mode_msg)
            
        if self.db:
            await self.db.register_node()
            
        logging.info("👑 Alpha Orchestrator Initialized. Beginning eternal cycle.")
        await self.telemetry_stream("INFO", "👑 PROJECT CHRONOS: OMEGA-SUPREMACY - Sovereign Intelligence Swarm Active.")
        
        strike_counter = 0
        while self.is_running:
            try:
                await self.check_kill_switch()
                if not self.is_running:
                    break
                
                # ALPHA-CENTAURI: Swarm Heartbeat
                if self.db: 
                    try:
                        # [🛡️ SELF-HEALING]: Run auto-recovery before starting the cycle
                        await self._perform_self_healing()
                        
                        logging.info("🔥 [LOOP-START] Checking heartbeat...")
                        await self.db.send_heartbeat()
                        logging.info("🔥 [LOOP-START] Checking leadership...")
                        is_leader = await self.db.claim_bot_leadership()
                        logging.info(f"🔥 [LOOP-START] Leadership status: {is_leader}")
                        
                        if is_leader:
                            logging.info("🔥 [LOOP-START] we are leader! Syncing cloud...")
                            # [🔥 FIX]: Only fetch leads ONCE per cycle (was fetched twice causing double API calls)
                            # Leads will be fetched again below in the main processing block
                            logging.info("📡 [LOOP-START] Leadership confirmed. Proceeding to main processing...")
                        else:
                            logging.info("💤 STANDBY: This node is currently an Auxiliary Node.")
                            # [🔥 FIX]: Don't exit on standby - just wait and retry leadership
                            logging.info("🔄 Retrying leadership in next cycle...")
                    except Exception as e:
                        logging.error(f"❌ CLOUD SYNC FAILURE: {e}")

                # SCALED MODE: No fatigue breaks - run continuously
                strike_counter += 1
                if strike_counter % 100 == 0:
                    logging.info(f"🚀 STRIKE COUNTER: {strike_counter} applications sent this session!")
                await self.check_kill_switch()
                if not self.is_running:
                    break
                
                logging.info("🧬 EVOLUTION: Fetching variant performance stats...")
                weights = await self.db.get_variant_weights() if self.db else None
                
                # [🔥 FIX]: Single lead fetch per cycle (removed duplicate fetch above)
                try:
                    logging.info("🧠 CLOUD SYNC: Checking for pending strikes in the Hive-Mind...")
                    cloud_leads = await self.db.get_pending_leads(limit=int(os.getenv("MAX_QUALIFIED_LEADS_PER_CYCLE", 300)))
                    if cloud_leads:
                        logging.info(f"🚀 MISSION READY: Found {len(cloud_leads)} pending strikes. Igniting Strikes...")
                        tasks = [self.process_single_lead(lead, variant_weights=weights) for lead in cloud_leads]
                        results = await asyncio.gather(*tasks, return_exceptions=True)
                        for i, res in enumerate(results):
                            if isinstance(res, Exception):
                                logging.error(f"❌ CRITICAL STRIKE FAILURE for lead {i}: {res}")
                                traceback.print_exception(type(res), res, res.__traceback__)
                    else:
                        logging.info("📡 CLOUD SYNC: No pending strikes found. Proceeding to scouting...")
                except Exception as e:
                    logging.error(f"❌ CLOUD SYNC FAILURE: {e}")

                await self.poisson_jitter(5)
                
                logging.info("🌍 Launching Vanguard Scraps...")
                raw_leads = []
                try:
                    scrape_tasks = []
                    if scraper:
                        scrape_tasks.append(asyncio.to_thread(scraper.get_latest_jobs))
                    if self.omni_crawler:
                        await self.telemetry_stream("INFO", "🕵️‍♂️ OMNI-CRAWLER: Engaging deep web re-connaissance...")
                        scrape_tasks.append(daleel_parallel_scan(self.db, pages=1))

                    if self.omni_crawler:
                        logging.info("🛰️ SOVEREIGN HUNT: Scanning registered custom platforms...")
                        platform_leads = await self.omni_crawler.hunt_registered_platforms()
                        raw_leads.extend(platform_leads)
                        
                        # [👑 OMEGA-STRIKE]: Every 3 cycles, perform a massive web-wide discovery
                        if strike_counter % 3 == 0:
                            await self.telemetry_stream("INFO", "🕵️‍♂️ OMNI-CRAWLER MAX: Initiating web-wide deep discovery...")
                            web_leads = await self.omni_crawler.hunt_the_web()
                            raw_leads.extend(web_leads)

                    if scrape_tasks:
                        results = await asyncio.gather(*scrape_tasks, return_exceptions=True)
                        for res in results:
                            if isinstance(res, list):
                                raw_leads.extend(res)
                            elif isinstance(res, Exception):
                                logging.error(f"Scraper Sub-node Failure: {res}")

                except Exception as e:
                    logging.error(f"Vanguard Scrape failed: {e}")

                # 👑 INFINITY: Sovereign Priority Sorting
                if raw_leads:
                    # Sort by priority_score (Descending) to ensure high-value strikes happen first
                    raw_leads.sort(key=lambda x: x.get("priority_score", 0), reverse=True)
                    
                    # 🛡️ PRE-SAVE FILTER: Remove junk before persisting to DB
                    JUNK_COMPANY_NAMES = {
                        'unknown', 'none', 'null', 'target node', 'automatic target',
                        'oracle lead', 'undefined', 'error', 'test', 'example',
                        'linkedin', 'indeed', 'glassdoor', 'bayt', 'naukrigulf',
                        'monster', 'gulftalent', 'dubizzle', 'daleel madani',
                    }
                    clean_leads = [
                        l for l in raw_leads
                        if l.get('company_name', '').lower().strip() not in JUNK_COMPANY_NAMES
                        and len(l.get('company_name', '').strip()) >= 3
                        and l.get('email', '') != ''  # Only save leads with real emails
                    ]
                    logging.info(f"📥 PERSISTENCE: Archiving {len(clean_leads)}/{len(raw_leads)} clean leads to the Hive-Mind...")
                    save_tasks = [self.db.save_potential_lead(l, score=l.get('priority_score', 80)) for l in clean_leads]
                    await asyncio.gather(*save_tasks, return_exceptions=True)
                    
                    # Limit to top 15 most valuable to prevent API burn, but prioritize Ghost Jobs
                    tasks = [self.process_single_lead(lead, variant_weights=weights) for lead in raw_leads[:15]]
                    await asyncio.gather(*tasks, return_exceptions=True)

                logging.info("💤 Cycle concluded. Entering 100% Heartbeat cooldown.")
                
                # 🔄 FOLLOW-UP ENGINE: Send second strikes to companies that didn't reply in 7 days
                try:
                    due_followups = await self.follow_up.get_due_follow_ups()
                    if due_followups:
                        logging.info(f"📬 FOLLOW-UP: {len(due_followups)} companies due for second strike")
                        for lead in due_followups[:5]:  # Max 5 follow-ups per cycle
                            try:
                                await self.follow_up.execute_second_strike(lead)
                            except Exception as fe:
                                logging.warning(f"⚠️ Follow-up failed for {lead.get('company_name')}: {fe}")
                except Exception as e:
                    logging.warning(f"⚠️ Follow-up engine error: {e}")
                
                # 🔄 RESET SESSION DEDUP: Clear processed set each cycle
                # This allows leads to be retried in the next cycle if they failed
                old_size = len(self._processed_this_session)
                self._processed_this_session = set()
                if old_size > 0:
                    logging.info(f"🔄 Session dedup reset: cleared {old_size} entries for next cycle")
                
                # 100% SOVEREIGN STEALTH: Adaptive Heartbeat
                pending_count = await self.db.get_pending_leads_count() if self.db else 0
                
                if pending_count > 0 and not self.emergency_strike_requested:
                    logging.info(f"⚡ FAST-TRACK: {pending_count} leads remaining. Skipping deep sleep.")
                    await self.poisson_jitter(30)
                elif not self.emergency_strike_requested:
                    await self.poisson_jitter(300)
                else:
                    self.emergency_strike_requested = False
                    logging.info("⚡ EMERGENCY STRIKE: Bypassing heartbeat cycle.")

            except Exception as e:
                logging.error(f"Divine loop cycle failed: {e}")
                await self.poisson_jitter(60)


async def run_orchestrator():
    """[👑 APEX PHOENIX]: Infinite survival wrapper with AI-powered diagnostics."""
    # ✅ Validate configuration at startup — catch misconfigs before they cause silent failures
    from core.config import validate_config
    cfg_result = validate_config()
    if not cfg_result["ok"]:
        logging.critical("🚨 [STARTUP] Configuration errors detected! Bot may not function correctly.")
        logging.critical(f"🚨 [STARTUP] Errors: {cfg_result['errors']}")
        # Don't exit — try to run with whatever is configured

    restart_count = 0
    last_restart = 0
    
    while True:
        bot = None
        try:
            logging.info("🔥 PHOENIX: Igniting Alpha Orchestrator Core...")
            bot = AlphaOrchestrator()
            await bot.execute_divine_loop()
        except Exception as e:
            now = time.time()
            if now - last_restart < 3600: restart_count += 1
            else: restart_count = 1
            last_restart = now
            
            error_trace = traceback.format_exc()
            logging.critical(f"💀 CORE COLLAPSE: {e}")
            
            # [🧠 AI DIAGNOSIS]: Ask Gemini what happened and how to fix it
            try:
                from core.ai_agent import OmniIntelligence
                ai = OmniIntelligence()
                diagnosis = await ai.structural_query(f"The bot crashed with this error: {error_trace}. Explain the cause in simple terms for the user and suggest a fix. Keep it brief.")
                msg = f"🚨 <b>CORE CRASH DETECTED</b>\n\n<b>Diagnosis:</b> {diagnosis.get('answer', str(e))}\n\n<i>Phoenix restart initiated ({restart_count}/hr)</i>"
                
                from core.db_client import get_db
                db = get_db()
                await db.stream_log("CRITICAL", f"AI_DIAGNOSIS: {msg}")
                # We can't easily import dashboard here without circular issues, so we use a DB task for notification
                await db.sync_add_task(task_type="broadcast_notification", target="ALL_USERS", meta=msg)
            except Exception as _diag_err:
                logging.warning(f"⚠️ [PHOENIX] AI diagnosis/notification failed: {_diag_err}")
            
            await asyncio.sleep(30)
        finally:
            if bot:
                try: await bot.close()
                except Exception as _close_err:
                    logging.debug(f"⚠️ [PHOENIX] Bot close error: {_close_err}")

if __name__ == "__main__":
    try:
        asyncio.run(run_orchestrator())
    except KeyboardInterrupt:
        logging.info("Shutting down Alpha Orchestrator.")
