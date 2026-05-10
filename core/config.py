"""
╔══════════════════════════════════════════════════════════════════════════════╗
║               SAM JOB AUTOMATOR - MAXIMUM POWER v2                        ║
║                        ULTIMATE CONFIGURATION                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

ENHANCED FEATURES:
✓ Telegram Dashboard - Full inline keyboard control
✓ Email Engine - Multiple SMTP providers with fallback
✓ Scraper - 50+ sources, 195 countries
✓ AI Filter - Intelligent job matching
✓ Auto-Retry - Self-healing on failures
✓ Rate Limiting - Anti-ban protection
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# ============================================================================
# 🔑 HARDCODED FALLBACKS — used when env vars are missing (e.g. Render free plan)
# These are the actual credentials. Env vars take priority if set.
# ============================================================================
_DEFAULTS = {
    "SUPABASE_URL":          "https://lckiazbadymeikmxesit.supabase.co",
    "SUPABASE_KEY":          "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxja2lhemJhZHltZWlrbXhlc2l0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNzE1NSwiZXhwIjoyMDkyODkzMTU1fQ.NWdt3IcKs60M-6T_syPLQU4m22msqugqGA7wZpCXNbg",
    "SUPABASE_SERVICE_ROLE_KEY": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imxja2lhemJhZHltZWlrbXhlc2l0Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3NzMxNzE1NSwiZXhwIjoyMDkyODkzMTU1fQ.NWdt3IcKs60M-6T_syPLQU4m22msqugqGA7wZpCXNbg",
    "BREVO_API_KEY":          "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",
    "BREVO_SMTP_LOGIN":       "a974ef001@smtp-brevo.com",
    "BREVO_SMTP_PASSWORD":    "xsmtpsib-4ffec113189337d3602362d9b18e53d9462bdf499ee7ac27a1778f66a478bb7c-7rFR8WTs1UMRNoyw",
    "BREVO_ACCOUNT_EMAIL":    "samatou683@gmail.com",
    "BREVO_SENDER_EMAIL":     "samatou683@gmail.com",
    "GMAIL_SMTP_USER":        "samsalameh.cv@gmail.com",
    "GMAIL_APP_PASSWORD":     "oimuanudzzngklnf",
    "ZOHO_SMTP_USER":         "samsalameh.cv@zohomail.com",
    "ZOHO_APP_PASSWORD":      "R0R6dqr5qL1g",
    "ZOHO_SMTP_USER_2":       "samsalameh@zohomail.com",
    "ZOHO_APP_PASSWORD_2":    "EGDUw41ADNmM",
    "TELEGRAM_BOT_TOKEN":     "8630175054:AAGuMqlmCJAizvDlFUrsg-UletxSdOcsvn0",
    "TELEGRAM_CHAT_ID":       "6639482672",
    "GROQ_API_KEY":           "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",
    "GEMINI_API_KEY":         "AIzaSyBFNxUyS-WXIcaBCxrlMuaZ6l1f0c4KCZs",
    "SENDER_EMAIL":           "samsalameh.cv@gmail.com",
    "SENDER_NAME":            "Sam Salameh",
    "CANDIDATE_PHONE":        "+961 70 841 1009",
    "LINKEDIN_URL":           "https://www.linkedin.com/in/sam-salameh",
    "CANDIDATE_PROFESSION":   "Senior Network Engineer",
    "TEST_RECEIVER_EMAIL":    "samsalameh.cv@gmail.com",
    "KILL_SWITCH_ACTIVE":     "false",
    "MAX_PARALLEL_STRIKES":   "3",
    "MAX_QUALIFIED_LEADS_PER_CYCLE": "100",
    "MIN_MATCH_SCORE":        "45",
}

def _get(key: str, default: str = "") -> str:
    """Get env var, falling back to hardcoded defaults if not set."""
    val = os.getenv(key, "")
    if val:
        return val
    return _DEFAULTS.get(key, default)

# Apply defaults for missing env vars
for _k, _v in _DEFAULTS.items():
    if not os.getenv(_k):
        os.environ[_k] = _v


def _env_flag(name: str, default: bool = False) -> bool:
    return os.getenv(name, str(default)).lower() == "true"


# ============================================================================
# 🔴 KILL SWITCH - Emergency Stop
# ============================================================================
KILL_SWITCH = _env_flag("KILL_SWITCH", False)
KILL_SWITCH_ACTIVE = _env_flag("KILL_SWITCH_ACTIVE", False)

# ============================================================================
# ☁️ SUPABASE DATABASE
# ============================================================================
SUPABASE_URL = os.getenv("SUPABASE_URL", "").rstrip('/')
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# ============================================================================
# 📧 EMAIL CONFIGURATION - MULTI-PROVIDER
# ============================================================================

# Primary: Brevo (Free 300/day)
BREVO_SMTP_SERVER = "smtp-relay.brevo.com"
BREVO_SMTP_PORT = 587
BREVO_SMTP_LOGIN = os.getenv("BREVO_SMTP_LOGIN", "")
BREVO_SMTP_PASSWORD = os.getenv("BREVO_SMTP_PASSWORD", "")
BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
USE_BREVO_HTTP_FALLBACK = _env_flag("USE_BREVO_HTTP_FALLBACK", True)

# Resend (Best Gmail deliverability - FREE)
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")

# Secondary: Gmail
GMAIL_SMTP_SERVER = "smtp.gmail.com"
GMAIL_SMTP_PORT = 587
GMAIL_SMTP_USER = os.getenv("GMAIL_SMTP_USER", "")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")

# PRIMARY: Zoho Mail (DMARC-aligned, Inbox delivery)
ZOHO_SMTP_SERVER = "smtp.zoho.com"
ZOHO_SMTP_PORT = 587
ZOHO_SMTP_USER = os.getenv("ZOHO_SMTP_USER", "")
ZOHO_APP_PASSWORD = os.getenv("ZOHO_APP_PASSWORD", "")

# BACKUP: Yahoo Mail (DMARC-aligned, needs 24-48h for new accounts)
YAHOO_SMTP_SERVER = "smtp.mail.yahoo.com"
YAHOO_SMTP_PORT = 587
YAHOO_SMTP_USER = os.getenv("YAHOO_SMTP_USER", "")
YAHOO_APP_PASSWORD = os.getenv("YAHOO_APP_PASSWORD", "")

# Tertiary: Outlook/Hotmail
OUTLOOK_SMTP_SERVER = "smtp-mail.outlook.com"
OUTLOOK_SMTP_PORT = 587
OUTLOOK_USER = os.getenv("OUTLOOK_USER", "")
OUTLOOK_PASSWORD = os.getenv("OUTLOOK_PASSWORD", "")

# SMTP Behavior
SMTP_CONNECT_TIMEOUT_SECONDS = int(os.getenv("SMTP_CONNECT_TIMEOUT_SECONDS", "20"))
SMTP_PRE_SEND_DELAY_MIN_SECONDS = float(os.getenv("SMTP_PRE_SEND_DELAY_MIN_SECONDS", "0.2"))
SMTP_PRE_SEND_DELAY_MAX_SECONDS = float(os.getenv("SMTP_PRE_SEND_DELAY_MAX_SECONDS", "0.8"))

# Email Settings
# IMPORTANT: TEST_RECEIVER_EMAIL must be explicitly set in TEST_MODE; no hardcoded default in production.
TEST_RECEIVER_EMAIL = os.getenv("TEST_RECEIVER_EMAIL", "")
SENDER_NAME = "Sam Salameh"
SENDER_EMAIL = os.getenv("SENDER_EMAIL", "sam.dev1@outlook.com")
# TEST_MODE defaults to False for production safety. Set TEST_MODE=true only in development/CI test phases.
TEST_MODE = _env_flag("TEST_MODE", False)

# ============================================================================
# 🤖 AI CONFIGURATION
# ============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
USE_AI_ANALYSIS = _env_flag("USE_AI_ANALYSIS", False) and bool(GEMINI_API_KEY or GROQ_API_KEY)

# ============================================================================
# 📱 TELEGRAM CONFIGURATION
# ============================================================================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
USE_TELEGRAM = _env_flag("USE_TELEGRAM", False) and bool(TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID)

# ============================================================================
# 🛟 OFFLINE / FALLBACK MODE
# ============================================================================
OFFLINE_SAFE_MODE = not any([
    GEMINI_API_KEY,
    GROQ_API_KEY,
    SUPABASE_URL,
    SUPABASE_KEY,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    BREVO_SMTP_PASSWORD,
    BREVO_API_KEY,
    GMAIL_SMTP_USER,
    GMAIL_APP_PASSWORD,
    OUTLOOK_USER,
    OUTLOOK_PASSWORD,
])

ENABLE_LOCAL_FALLBACKS = _env_flag("ENABLE_LOCAL_FALLBACKS", True)

# ============================================================================
# ⚡ MAXIMUM POWER SETTINGS
# ============================================================================

# Scraper Settings
DALEEL_MADANI_BASE_URL = "https://daleel-madani.org/jobs"
SCRAPER_MAX_PAGES = 50
MAX_DEEP_SCRAPES_PER_RUN = 500

# Email Settings
MAX_EMAILS_PER_RUN = 50
DELAY_BETWEEN_EMAILS_MIN = 1
DELAY_BETWEEN_EMAILS_MAX = 3
MAX_EMAILS_PER_MINUTE = 20

# Parallel Processing
MAX_PARALLEL_STRIKES = 3
MAX_QUALIFIED_LEADS_PER_CYCLE = 100

# Performance
REQUEST_TIMEOUT = 15

# ============================================================================
# 🎯 JOB TARGET RULES
# ============================================================================

MIN_SALARY_LEBANON_PRIME = 1500
MIN_SALARY_LEBANON_OTHER = 1000
MIN_SALARY_GLOBAL = 6000

PRIME_LEBANON_CITIES = [
    "beirut", "keserwan", "kesrouane", "jbeil", "byblos",
    "metn", "matn", "maten", "jabal lebanon", "mount lebanon"
]

GOD_MODE_LOCATIONS = [
    "uae", "dubai", "abu dhabi", "sharjah", "ajman", "ras al khaimah",
    "qatar", "doha", "doha, qatar",
    "saudi arabia", "riyadh", "jeddah", "mecca", "medina",
    "kuwait", "kuwait city",
    "oman", "muscat",
    "bahrain", "manama",
    "gcc", "gulf", "middle east", "mena",
    "worldwide", "remote", "anywhere", "visa sponsorship", "relocation",
    "United Arab Emirates", "UAE", "KSA"
]

GOD_MODE_QUERIES = [
    # ── UAE / GULF ─────────────────────────────────────────────────────────────
    "Senior Network Engineer Dubai visa sponsorship relocation",
    "Network Administrator Abu Dhabi housing allowance",
    "IT Infrastructure Engineer Saudi Arabia relocation package",
    "Network Security Engineer Qatar employment visa",
    "IT Manager UAE family visa sponsorship",
    "NOC Engineer Kuwait relocation housing",
    "Systems Administrator Dubai employment package",
    "Network Consultant Saudi Arabia visa",
    "Telecom Engineer Oman relocation benefits",
    "IT Operations Manager Bahrain employment sponsorship",
    # ── EUROPE / WORLDWIDE ─────────────────────────────────────────────────────
    "Network Engineer UK skilled worker visa sponsorship",
    "IT Infrastructure Manager USA H1B visa transfer",
    "Senior Network Engineer Canada LMIA work permit",
    "Network Security Engineer Germany EU Blue Card",
    "Systems Administrator Australia visa sponsorship",
    "Network Engineer New Zealand resident visa",
    "IT Manager Netherlands highly skilled migrant",
    "Network Administrator Ireland critical skills employment",
    "Cisco Network Engineer Dubai visa relocation",
    "MikroTik Network Engineer Saudi Arabia employment package",
    "Fortinet Security Engineer Qatar investment visa",
    "Network Engineer Malta employment permit",
    "IT Infrastructure Cyprus golden visa",
    "Network Consultant Spain digital nomad visa",
]

SAM_JOB_TITLES = [
    # ── CORE NETWORK ENGINEERING ───────────────────────────────────────────────
    "network engineer", "senior network engineer", "network administrator",
    "network specialist", "network consultant", "network architect",
    "network infrastructure engineer", "network support engineer",
    "network technician", "network analyst",
    # ── IT INFRASTRUCTURE ──────────────────────────────────────────────────────
    "it infrastructure engineer", "it infrastructure manager",
    "systems administrator", "system administrator", "sysadmin",
    "it administrator", "it manager", "it director", "it specialist",
    "it support engineer", "it support manager", "it operations",
    "it operations manager", "infrastructure manager",
    # ── SECURITY ──────────────────────────────────────────────────────────────
    "network security engineer", "security engineer", "cybersecurity engineer",
    "firewall engineer", "security administrator", "security analyst",
    "information security", "noc engineer", "noc manager",
    # ── TELECOM ───────────────────────────────────────────────────────────────
    "telecom engineer", "telecommunications engineer", "isp engineer",
    "fiber optic technician", "fiber optic engineer", "cabling technician",
    # ── VENDOR SPECIFIC ───────────────────────────────────────────────────────
    "cisco engineer", "cisco network engineer", "ccna", "ccnp",
    "mikrotik engineer", "ubiquiti engineer", "fortinet engineer",
    "fortigate engineer", "juniper engineer",
    # ── MANAGEMENT ────────────────────────────────────────────────────────────
    "it manager", "network manager", "infrastructure manager",
    "technical manager", "technology manager", "head of it",
    "it director", "chief technology officer", "cto",
    "pre-sales engineer", "solutions engineer", "technical consultant",
]

BANNED_TITLES = [
    "hr manager", "human resources", "recruitment", "talent acquisition",
    "payroll", "compensation", "benefits manager",
    "nurse", "doctor", "physician", "medical", "healthcare assistant",
    "driver", "delivery", "warehouse", "laborer", "construction",
    "cleaner", "janitor", "maid", "housekeeping",
    "chef", "cook", "waiter", "waitress", "bartender", "food",
    "security guard", "security officer", "bouncer",
    "cashier", "retail", "store", "sales associate",
    "accountant", "lawyer", "teacher", "instructor",
    "software developer", "programmer", "coder", "web developer",
    "data scientist", "machine learning", "ai engineer",
]

EXCLUDED_COMPANIES = [
    "idm", "i.d.m", "idm lebanon", "interpublic", "ipg",
]

# ============================================================================
# ✅ CONFIGURATION VALIDATOR
# ============================================================================

def validate_config() -> dict:
    """
    Validates that critical environment variables are set at startup.
    Returns a dict with 'warnings' and 'errors' lists.
    Call this once at bot startup to catch misconfigurations early.
    """
    errors = []
    warnings = []

    # --- Critical: at least one email provider must be configured ---
    has_email_provider = any([
        BREVO_API_KEY,
        BREVO_SMTP_LOGIN and BREVO_SMTP_PASSWORD,
        GMAIL_SMTP_USER and GMAIL_APP_PASSWORD,
        ZOHO_SMTP_USER and ZOHO_APP_PASSWORD,
        OUTLOOK_USER and OUTLOOK_PASSWORD,
        os.getenv("RESEND_API_KEY", ""),
        os.getenv("SENDPULSE_API_KEY", "") or (os.getenv("SENDPULSE_CLIENT_ID", "") and os.getenv("SENDPULSE_CLIENT_SECRET", "")),
        os.getenv("MAILJET_API_KEY", "") and os.getenv("MAILJET_API_SECRET", ""),
    ])
    if not has_email_provider:
        errors.append("❌ No email provider configured! Set at least one of: BREVO_API_KEY, GMAIL_SMTP_USER+GMAIL_APP_PASSWORD, ZOHO_SMTP_USER+ZOHO_APP_PASSWORD, RESEND_API_KEY, etc.")

    # --- Sender identity ---
    if not SENDER_EMAIL:
        errors.append("❌ SENDER_EMAIL is not set.")

    # --- TEST_MODE safety check ---
    if TEST_MODE and not TEST_RECEIVER_EMAIL:
        errors.append("❌ TEST_MODE=true but TEST_RECEIVER_EMAIL is not set. All test emails will fail.")

    # --- Telegram (optional but warn if partially configured) ---
    if TELEGRAM_BOT_TOKEN and not TELEGRAM_CHAT_ID:
        warnings.append("⚠️ TELEGRAM_BOT_TOKEN is set but TELEGRAM_CHAT_ID is missing.")
    if TELEGRAM_CHAT_ID and not TELEGRAM_BOT_TOKEN:
        warnings.append("⚠️ TELEGRAM_CHAT_ID is set but TELEGRAM_BOT_TOKEN is missing.")

    # --- AI (optional but warn if USE_AI_ANALYSIS is forced on without keys) ---
    if os.getenv("USE_AI_ANALYSIS", "").lower() == "true" and not (GEMINI_API_KEY or GROQ_API_KEY):
        warnings.append("⚠️ USE_AI_ANALYSIS=true but neither GEMINI_API_KEY nor GROQ_API_KEY is set. AI analysis will be disabled.")

    # --- Supabase (optional but warn if partially configured) ---
    if SUPABASE_URL and not SUPABASE_KEY:
        warnings.append("⚠️ SUPABASE_URL is set but SUPABASE_KEY is missing. Database will fall back to SQLite.")
    if SUPABASE_KEY and not SUPABASE_URL:
        warnings.append("⚠️ SUPABASE_KEY is set but SUPABASE_URL is missing. Database will fall back to SQLite.")

    # --- Log results ---
    if errors:
        for e in errors:
            import logging as _log
            _log.error(f"[CONFIG] {e}")
    if warnings:
        for w in warnings:
            import logging as _log
            _log.warning(f"[CONFIG] {w}")
    if not errors and not warnings:
        import logging as _log
        _log.info("✅ [CONFIG] All configuration checks passed.")

    return {"errors": errors, "warnings": warnings, "ok": len(errors) == 0}
