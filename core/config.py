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
MAX_PARALLEL_STRIKES = 5
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
    "HR Manager Dubai visa sponsorship relocation",
    "HR Business Partner Abu Dhabi housing allowance",
    "Senior HR Specialist Saudi Arabia relocation package",
    "Operations Manager Qatar employment visa",
    "Chief of Staff UAE family visa sponsorship",
    "HR Director Kuwait relocation housing",
    "Recruitment Lead Dubai employment package",
    "Talent Acquisition Manager Saudi Arabia visa",
    "Office Manager Oman relocation benefits",
    "HRBP Bahrain employment sponsorship",
    "HR Manager UK skilled worker visa sponsorship",
    "HR Director USA H1B visa transfer",
    "Operations Manager Canada LMIA work permit",
    "HR Business Partner Germany EU Blue Card",
    "Senior HR Specialist Australia457 visa sponsorship",
    "HR Manager New Zealand resident visa",
    "HR Director Netherlands highly skilled migrant",
    "Operations Manager Ireland critical skills employment",
    "Executive Assistant Dubai visa relocation",
    "Personal Secretary Saudi Arabia employment package",
    "Chief Operations Officer Qatar investment visa",
    "HR Generalist Malta employment permit",
    "Office Administrator Cyprus golden visa",
    "HR Coordinator Spain digital nomad visa",
]

SAM_JOB_TITLES = [
    "hr manager", "human resources manager", "hr director", "hr head",
    "hr business partner", "hrbp", "hr specialist", "hr generalist",
    "recruitment manager", "talent acquisition", "talent manager",
    "compensation manager", "benefits manager", "payroll manager",
    "operations manager", "operations director", "operations lead",
    "chief of staff", "office manager", "admin manager",
    "administrative manager", "facilities manager",
    "customer service manager", "customer success manager", "support manager",
    "client services manager", "service delivery manager",
    "executive assistant", "personal assistant", "secretary",
    "receptionist", "front desk", "office coordinator",
    "administrative assistant", "admin assistant",
    "hr assistant", "hr coordinator", "hr officer",
    "recruitment coordinator", "recruitment officer",
    "data entry clerk", "office clerk", "clerical",
    "training manager", "learning development", "l&d",
    "employee relations", "labor relations",
]

BANNED_TITLES = [
    "software", "developer", "engineer", "programmer", "coder",
    "data scientist", "data analyst", "IT", "tech",
    "nurse", "doctor", "physician", "medical", "healthcare assistant",
    "driver", "delivery", "warehouse", "laborer", "construction",
    "cleaner", "janitor", "maid", "housekeeping",
    "chef", "cook", "waiter", "waitress", "bartender", "food",
    "security guard", "security officer", "bouncer",
    "cashier", "retail", "store", "sales associate",
    "accountant", "lawyer", "teacher", "instructor",
]

EXCLUDED_COMPANIES = [
    "idm", "i.d.m", "idm lebanon", "interpublic", "ipg",
]
