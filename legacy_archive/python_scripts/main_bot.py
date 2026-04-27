import os
import json
import time
import random
import logging
import asyncio
import traceback
import atexit
import sys
import threading
import shutil
import re
import html
import socket
from pathlib import Path
from datetime import datetime
from types import SimpleNamespace

# Telegram Advanced Library
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.error import Conflict, RetryAfter, TimedOut, NetworkError, BadRequest
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# Project Chronos Modules
import config 
import database
import scraper
import ai_agent
import pdf_generator
import smtp_engine
from omni_crawler import OmniCrawler
from system_health import HealthCheck, CompanyDatabase, MetricsTracker
from telegram_dashboard import TelegramDashboard
from global_company_scraper import GlobalCompanyScraper
import uplink
import self_healer

# ==========================================
# 🛰️ SYSTEM CONFIGURATION & LOGGING
# ==========================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("bot.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)

# 🛠️ GLOBAL ENGINES (Module-level for proper async access)
ai_brain = None
crawler = None
health_check = None
company_db = None
metrics_tracker = None
company_scraper = None
dashboard = TelegramDashboard()

# MAXIMUM POWER: Optimized rate limiting for faster throughput
LAST_EMAIL_TIMES = []  # Track last email send times
MAX_EMAILS_PER_MINUTE = 20  # Increased from 10 for maximum power
EMAIL_RATE_LOCK = None
MISSION_LOCK = None
LAST_SUCCESSFUL_MISSION_TS = 0.0
SAFE_MODE_UNTIL_TS = 0.0
LAST_SAFE_MODE_ALERT_TS = 0.0
LAST_DAILY_REPORT_DATE = ""
EXPLAIN_CACHE = {}
EXPLAIN_ORDER = []
EXPLAIN_SEQ = 0
DELIVERY_PROBE = {"ts": 0.0, "status": "unknown", "detail": ""}

# MAXIMUM POWER: AI result cache to avoid re-analyzing same jobs
_AI_CACHE = {}
_AI_CACHE_TTL = 86400  # 24 hours

# MAXIMUM POWER: Higher parallel processing limits
MAX_PARALLEL_WORKERS = 8  # Increased for faster parallel execution
REQUEST_TIMEOUT = 10  # Reduced from higher values for faster timeout

RUNTIME_STATE_FILES = [
    "tracker.json",
    "metrics.json",
    "health_check.json",
    "company_database.json",
    "discovered_companies.json",
]


class SingleInstanceLock:
    """Simple lock-file guard to prevent multiple local bot instances."""

    def __init__(self, lock_path: str):
        self.lock_path = lock_path
        self._fh = None
        self._acquired = False

    def acquire(self) -> bool:
        if os.name == 'nt':
            try:
                import msvcrt

                # Remove stale lock file if it exists
                if os.path.exists(self.lock_path):
                    try:
                        # Try to read PID from lock file
                        with open(self.lock_path, 'r', encoding='utf-8') as f:
                            old_pid = f.read().strip()
                        # Check if old process is still running
                        try:
                            os.kill(int(old_pid), 0)
                            # Process is still running, fail to acquire
                            return False
                        except (ValueError, ProcessLookupError, OSError):
                            # Process not running, stale lock - delete it
                            try:
                                os.remove(self.lock_path)
                            except:
                                pass
                    except:
                        try:
                            os.remove(self.lock_path)
                        except:
                            pass

                self._fh = open(self.lock_path, 'a+', encoding='utf-8')
                self._fh.seek(0)
                msvcrt.locking(self._fh.fileno(), msvcrt.LK_NBLCK, 1)
                self._fh.seek(0)
                self._fh.truncate()
                self._fh.write(str(os.getpid()))
                self._fh.flush()
                self._acquired = True
                return True
            except OSError:
                return False
        else:
            # Best-effort fallback for non-Windows environments.
            try:
                self._fh = open(self.lock_path, 'x', encoding='utf-8')
                self._fh.write(str(os.getpid()))
                self._fh.flush()
                self._acquired = True
                return True
            except FileExistsError:
                return False

    def release(self):
        if not self._fh:
            return

        try:
            if os.name == 'nt' and self._acquired:
                import msvcrt

                self._fh.seek(0)
                msvcrt.locking(self._fh.fileno(), msvcrt.LK_UNLCK, 1)
        except Exception as exc:
            logging.debug(f"Lock release warning: {exc}")
        finally:
            try:
                self._fh.close()
            except Exception as exc:
                logging.debug(f"Lock file close warning: {exc}")
            self._fh = None
            self._acquired = False

            # Remove stale lock file if possible.
            try:
                if os.path.exists(self.lock_path):
                    os.remove(self.lock_path)
            except Exception as exc:
                logging.debug(f"Lock file cleanup warning: {exc}")

# ==========================================
# 🛡️ THE STRIKE FILTERS (CORE LOGIC)
# ==========================================

def is_valid_target(company_name, location, salary, phase, description=""):
    """Validates if a target meets the uncompromising Phase/God-Mode criteria."""
    loc_lower = str(location).lower().strip()
    desc_lower = str(description).lower()
    company_lower = str(company_name).lower()
    
    for exc in config.EXCLUDED_COMPANIES:
        if exc in company_lower:
            return False, f"Banned company: {exc}", 0, 0
            
    for exc in config.EXCLUDED_LOCATIONS:
        if exc in loc_lower:
            return False, f"Banned location: {exc}", 0, 0

    try:
        salary_val = float(str(salary).replace('$', '').replace(',', ''))
    except ValueError:
        salary_val = 0.0

    is_prime = any(city in loc_lower for city in config.PRIME_LEBANON_CITIES)
    is_lebanon = is_prime or "lebanon" in loc_lower or "lb" in loc_lower or "remote" in loc_lower or loc_lower == ""
    
    perk_count = sum(1 for kw in config.GLOBAL_SPONSOR_KEYWORDS if kw in desc_lower)
    has_perks = perk_count > 0
    
    # Validate phase is valid
    if phase not in ("lebanon", "global"):
        phase = "global"  # Default to global if unknown
    
    if phase == "lebanon":
        if not is_lebanon:
            if (salary_val >= 6000 or salary_val == 0) and has_perks:
                return True, "⚡ GOD-MODE: Lucrative Global Sponsorship", salary_val, perk_count
            return False, "Not Lebanon & no God-Mode override.", 0, 0
            
        if is_prime:
            if salary_val >= config.MIN_SALARY_LEBANON_PRIME or salary_val == 0:
                return True, "Valid Prime Lebanon target.", salary_val, 0
            return False, f"Prime Lebanon salary too low ({salary_val})", 0, 0
        if salary_val >= config.MIN_SALARY_LEBANON_OTHER or salary_val == 0:
            return True, "Valid Other Lebanon target.", salary_val, 0
        return False, f"Other Lebanon salary too low ({salary_val})", 0, 0
        
    elif phase == "global":
        if is_lebanon: return False, "Global phase, skipping Lebanon.", 0, 0
        loc_match = any(target.lower() in loc_lower for target in config.GOD_MODE_LOCATIONS)
        if (salary_val >= config.MIN_SALARY_GLOBAL or salary_val == 0) and (has_perks or loc_match):
            return True, "Valid Premium Global target.", salary_val, perk_count
        return False, "Global target skipped criteria.", 0, 0
        
    return False, "Unknown phase.", 0, 0

def is_relevant_to_cv(job_title, description=""):
    """AI-powered relevance check with 100% fallback mode if AI unavailable."""
    title_lower = str(job_title).lower().strip()
    if not title_lower:
        return True, "No title", "", "0"

    for banned in getattr(config, 'BANNED_TITLES', []):
        if banned.lower() in title_lower:
            return False, f"Banned title: {banned}", "", "0"

    # Check AI cache first
    cache_key = f"{title_lower}_{description[:200]}"
    if cache_key in _AI_CACHE:
        entry = _AI_CACHE[cache_key]
        if time.time() - entry['ts'] < _AI_CACHE_TTL:
            return entry['result']

    # Core target keywords
    target_keywords = ["hr", "operations", "admin", "assistant", "manager", "people", "coordinator", "officer", "recruitment", "talent"]
    is_relevant_keyword = any(k in title_lower for k in target_keywords)

    # AI analysis
    if is_relevant_keyword and ai_brain and hasattr(ai_brain, 'enabled') and ai_brain.enabled:
        try:
            result = ai_brain.analyze_job(job_title, description)
            # Cache result
            _AI_CACHE[cache_key] = {
                'result': result,
                'ts': time.time()
            }
            return result
        except Exception as e:
            logging.warning(f"AI analysis failed, using keyword match: {e}")

    # FALLBACK
    if is_relevant_keyword:
        fallback_body = getattr(config, 'EMAIL_BODY_TEMPLATE', '').strip() or (
            "Dear {company_name} Hiring Team,\n\n"
            f"I am applying for the {job_title} position and believe my HR/operations background can add value from day one.\n\n"
            "Best regards,\nSam Salameh"
        )
        result = (True, "Matched keywords (AI unavailable)", fallback_body, "0")
        # Cache fallback
        _AI_CACHE[cache_key] = {
            'result': result,
            'ts': time.time()
        }
        return result

    return False, "No relevant keywords.", "", "0"

# ==========================================
# 🪐 THE AUTONOMOUS MISSION LOOP
# ==========================================

def fast_filter(lead, current_phase=None):
    """Quick pre-filter to skip obviously bad matches before expensive AI analysis."""
    try:
        # 1. Location pre-filter
        location = lead.get('location', '').lower()
        phase = (current_phase or 'global').lower()
        if phase == 'lebanon':
            required_locations = [
                'lebanon', 'lb', 'beirut', 'keserwan', 'kesrouane',
                'jbeil', 'byblos', 'metn', 'matn', 'maten',
                'jabal lebanon', 'mount lebanon', 'remote'
            ]
        else:
            required_locations = ['remote', 'worldwide', 'global', 'uae', 'dubai', 'qa', 'sa', 'gcc', 'gulf', 'middle east', 'lebanon', 'beirut', 'lb']

        if location and not any(loc in location for loc in required_locations):
            return False
        
        # 2. Salary pre-filter
        salary_str = lead.get('salary_min', '0')
        try:
            salary = int(salary_str) if isinstance(salary_str, str) else salary_str
            if phase == 'lebanon':
                min_allowed = int(getattr(config, 'MIN_SALARY_LEBANON_OTHER', 0) or 0)
            else:
                min_allowed = int(getattr(config, 'MIN_SALARY_GLOBAL', 0) or 0)
            if salary > 0 and salary < min_allowed:
                return False
        except:
            pass
        
        # 3. Keyword blacklist (skip internal candidates, interns, etc)
        title = lead.get('job_title', '').lower()
        bad_keywords = ['intern', 'junior', 'scholarship', 'volunteer', 'apprentice', 'trainee']
        if any(kw in title for kw in bad_keywords):
            return False
        
        return True  # Passes pre-filter
    except Exception as e:
        logging.debug(f"Pre-filter error: {e}")
        return True  # If error, let main filter decide

def lead_priority_score(lead):
    """Rank leads so the best opportunities are processed first."""
    score = 0

    title = str(lead.get('job_title', '')).lower()
    description = str(lead.get('description', '')).lower()
    location = str(lead.get('location', '')).lower()

    # Role seniority/fit
    if any(k in title for k in ['manager', 'lead', 'director', 'head']):
        score += 20
    if any(k in title for k in ['hr', 'operations', 'admin', 'talent', 'recruit']):
        score += 15

    # Remote/global preferred for faster conversion
    if any(k in location for k in ['remote', 'worldwide', 'global']):
        score += 10

    # Sponsorship/relocation opportunities
    if any(k in description for k in ['visa', 'relocation', 'sponsorship']):
        score += 12

    # Salary signal
    salary_val = 0
    for key in ['salary_min', 'salary', 'estimated_salary']:
        raw = lead.get(key, 0)
        try:
            salary_val = max(salary_val, float(str(raw).replace('$', '').replace(',', '').strip() or 0))
        except Exception:
            continue
    score += min(int(salary_val // 500), 20)
    return score

    return score


def render_application_body(template_body, lead):
    """Render body placeholders safely with lead data."""
    body = template_body or ''
    company = str(lead.get('company_name', 'Hiring Team')).strip() or 'Hiring Team'
    title = str(lead.get('job_title', 'Professional Role')).strip() or 'Professional Role'

    try:
        return body.format(company_name=company, job_title=title)
    except Exception:
        # Fallback if braces in template are not format placeholders.
        return body.replace('{company_name}', company).replace('{job_title}', title)

async def apply_rate_limit():
    """MAXIMUM POWER: Apply rate limiting with optimized wait times"""
    global LAST_EMAIL_TIMES, EMAIL_RATE_LOCK
    if EMAIL_RATE_LOCK is None:
        EMAIL_RATE_LOCK = asyncio.Lock()

    async with EMAIL_RATE_LOCK:
        current_time = time.time()
        # Remove emails older than 60 seconds
        LAST_EMAIL_TIMES = [t for t in LAST_EMAIL_TIMES if current_time - t < 60]

        if len(LAST_EMAIL_TIMES) >= MAX_EMAILS_PER_MINUTE:
            wait_time = 60 - (current_time - LAST_EMAIL_TIMES[0])
            if wait_time > 0:
                logging.info(f"Rate limit hit. Waiting {wait_time:.1f}s...")
                await asyncio.sleep(wait_time)

        LAST_EMAIL_TIMES.append(time.time())

async def parallel_scrape_jobs():
    """MAXIMUM POWER: Scrape all job boards in parallel for 4-5x more jobs per cycle"""
    logging.info("Starting parallel job board scraping...")
    all_jobs = []
    
    try:
        # Prepare async scraping tasks
        tasks = []
        
        # Primary scraper
        primary_scraper = getattr(scraper, 'get_latest_jobs', None) or getattr(scraper, 'scrape_new_companies', None)
        if primary_scraper:
            tasks.append(asyncio.to_thread(primary_scraper))
        
        # OmniCrawler source
        if crawler:
            try:
                omni_method = getattr(crawler, 'hunt_the_web', None)
                if omni_method:
                    tasks.append(asyncio.to_thread(omni_method))
            except Exception:
                pass
        
        # Run all scraping tasks in parallel with timeout
        results = await asyncio.wait_for(
            asyncio.gather(*tasks, return_exceptions=True),
            timeout=45.0  # MAXIMUM POWER: Timeout after 45s to prevent hanging
        )
        
        # Combine results, handle exceptions gracefully
        for result in results:
            if result and not isinstance(result, Exception):
                if isinstance(result, list):
                    all_jobs.extend(result)
        
        # Remove duplicates by URL
        seen_urls = set()
        unique_jobs = []
        for job in all_jobs:
            if isinstance(job, dict):
                url = job.get('url', job.get('link', ''))
                if url and url not in seen_urls:
                    seen_urls.add(url)
                    unique_jobs.append(job)
        
        logging.info(f"Parallel scrape complete: {len(unique_jobs)} unique jobs")
        return unique_jobs
        
    except asyncio.TimeoutError:
        logging.warning("Parallel scraping timed out, using fallback")
    except Exception as e:
        logging.error(f"Parallel scraping error: {e}")
    
    # Fallback to sequential scraping with shorter timeout
    try:
        jobs = await asyncio.wait_for(
            asyncio.to_thread(scraper.scrape_new_companies),
            timeout=30.0
        )
        logging.info(f"Fallback scraping: {len(jobs) if jobs else 0} jobs")
        return jobs if jobs else []
    except Exception as e2:
        logging.error(f"Fallback scraping failed: {e2}")
        return []

def send_strike_with_fallover(lead, pdf_path):
    """Send email with Brevo, fallback to Gmail if Brevo fails."""
    prefer_gmail_only = bool(
        getattr(config, 'ZERO_INVESTMENT_MODE', False) or
        getattr(config, 'PREFER_GMAIL_ONLY', False)
    )
    allow_brevo_in_zero = bool(getattr(config, 'ALLOW_BREVO_IN_ZERO_MODE', False))
    allow_brevo_http = bool(getattr(config, 'USE_BREVO_HTTP_FALLBACK', True)) and (not prefer_gmail_only or allow_brevo_in_zero)

    # First try Brevo (primary)
    if not prefer_gmail_only:
        try:
            success = smtp_engine.send_strike(lead, pdf_path)
            if success:
                return True
        except Exception as e:
            logging.warning(f"Brevo SMTP failed, trying Gmail fallover: {e}")
    
    # Fallback to Gmail (primary in zero-investment mode).
    try:
        import smtplib
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        from email.mime.application import MIMEApplication
        
        email = lead.get('email')
        company = lead.get('company_name', 'Unknown Company')
        title = lead.get('job_title', 'Professional Role')
        custom_body = render_application_body(config.EMAIL_BODY_TEMPLATE, lead)
        
        if not email or "@" not in email:
            return False
        
        import re
        msg = MIMEMultipart('mixed')
        msg['From'] = f"Sam Salameh <{config.GMAIL_SMTP_USER}>"
        msg['To'] = email
        msg['Subject'] = f"{title} | Sam Salameh - HR & Operations | Available Immediately"
        msg['User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'

        body = custom_body if custom_body else f"Dear HR Team at {company},\n\nPlease find my application for the {title} position attached.\n\nBest regards,\nSam Salameh"
        is_html_body = '<' in body and '>' in body
        plain_body = re.sub(r'<[^>]+>', ' ', body)
        plain_body = re.sub(r'\s+', ' ', plain_body).strip() if plain_body else body

        alt = MIMEMultipart('alternative')
        alt.attach(MIMEText(plain_body or body, 'plain'))
        if is_html_body:
            alt.attach(MIMEText(body, 'html'))
        msg.attach(alt)
        
        # Attach PDF
        if pdf_path:
            try:
                with open(pdf_path, "rb") as f:
                    part = MIMEApplication(f.read(), Name=f"{company}_Sam_Cordahi.pdf")
                part['Content-Disposition'] = f'attachment; filename="{company}_Sam_Cordahi.pdf"'
                msg.attach(part)
            except Exception as e:
                logging.error(f"Failed to attach PDF for fallover: {e}")

        # Attach CV (HTML) when available, matching production packet style.
        try:
            cv_path = getattr(config, 'CV_FILE_PATH', '')
            if cv_path and os.path.exists(cv_path):
                with open(cv_path, 'rb') as f:
                    cv_part = MIMEApplication(f.read(), Name=os.path.basename(cv_path))
                cv_part['Content-Disposition'] = f'attachment; filename="{os.path.basename(cv_path)}"'
                msg.attach(cv_part)
        except Exception as e:
            logging.warning(f"CV attachment skipped in Gmail fallback: {e}")
        
        # Send via Gmail
        if not config.GMAIL_SMTP_USER or not config.GMAIL_APP_PASSWORD:
            logging.error("Gmail SMTP unavailable: missing Gmail credentials")
            if getattr(config, 'ZERO_INVESTMENT_MODE', False) and not getattr(config, 'ALLOW_BREVO_IN_ZERO_MODE', False):
                return False
            # Optional emergency fallback to Brevo only when explicitly allowed.
            try:
                return smtp_engine.send_strike(lead, pdf_path)
            except Exception as e:
                logging.error(f"Brevo emergency fallback failed: {e}")
                return False

        smtp_timeout = int(getattr(config, 'SMTP_CONNECT_TIMEOUT_SECONDS', 8) or 8)
        server = smtplib.SMTP(config.GMAIL_SMTP_SERVER, config.GMAIL_SMTP_PORT, timeout=smtp_timeout)
        server.starttls()
        server.login(config.GMAIL_SMTP_USER, config.GMAIL_APP_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        logging.info(f"✅ GMAIL FALLOVER SUCCESS: Sent to {email}")
        return True
        
    except Exception as e:
        logging.error(f"⚠️ Gmail delivery failed for {email}: {e}")

    # As a last resort, try Brevo HTTP (443) only when explicitly allowed.
    if allow_brevo_http:
        try:
            api_success = smtp_engine.send_email_via_brevo_http(
                to_email=lead.get('email'),
                company_name=lead.get('company_name', 'Unknown Company'),
                job_title=lead.get('job_title', 'Professional Role'),
                custom_body=render_application_body(config.EMAIL_BODY_TEMPLATE, lead),
                pdf_path=pdf_path,
            )
            if api_success:
                return True
        except Exception as e:
            logging.warning(f"Brevo HTTP fallback failed after Gmail failure: {e}")

    logging.error(f"💥 Delivery failed on all channels for {lead.get('email', 'unknown')}.")
    return False

async def process_strike_candidate(context: ContextTypes.DEFAULT_TYPE, chat_id, lead, current_phase):
    """Process one qualified lead through PDF generation and SMTP delivery."""
    company_name = lead.get('company_name', 'Unknown Company')
    email = lead.get('email', 'unknown')

    # Apply global rate limiting just before send attempt.
    await apply_rate_limit()
    await asyncio.sleep(random.uniform(0.2, 1.0))

    logging.info(f"⚔️ STRIKING: {company_name} - {lead.get('job_title', 'Unknown Role')}")

    # Render placeholders once before PDF/email sending.
    lead['custom_body'] = render_application_body(config.EMAIL_BODY_TEMPLATE, lead)

    pdf_path = await asyncio.to_thread(pdf_generator.create_personalized_pdf, lead)
    if not pdf_path:
        logging.warning(f"⏭️ SKIP: PDF generation failed for {company_name}")
        return False

    success = await asyncio.to_thread(send_strike_with_fallover, lead, pdf_path)
    if not success:
        await asyncio.to_thread(database.save_potential_lead, lead, priority_score=100)
        try:
            if metrics_tracker:
                metrics_tracker.record_error(autosave=False)
        except Exception as e:
            logging.error(f"Metrics error-record failed (non-blocking): {e}")
        return False

    await asyncio.to_thread(database.log_application, lead)

    try:
        if company_db:
            company_db.add_company(
                email=email,
                company_name=company_name,
                job_title=lead.get('job_title', 'Unknown'),
                location=lead.get('location', 'Unknown'),
                source=lead.get('source_board', 'unknown_board')
            )
            company_db.mark_application_sent(email, company_name, lead.get('job_title', 'Unknown'))
    except Exception as e:
        logging.error(f"Company DB error (non-blocking): {e}")

    try:
        if metrics_tracker:
            metrics_tracker.record_application(autosave=False)
    except Exception as e:
        logging.error(f"Metrics error (non-blocking): {e}")

    try:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🚀 <b>STRIKE SUCCESS</b>\n🏢 {company_name}\n💼 {lead.get('job_title', 'Unknown Role')}\n🎯 Phase: {current_phase.upper()}",
            parse_mode='HTML'
        )
    except Exception as e:
        logging.warning(f"Could not send Telegram update (not blocking mission): {e}")

    await asyncio.to_thread(database.update_heartbeat)
    return True

async def auto_strike_mission(context: ContextTypes.DEFAULT_TYPE):
    """The 24/7 Autonomous Scout & Strike Loop with company tracking & natural timing."""
    import random
    global MISSION_LOCK

    if MISSION_LOCK is None:
        MISSION_LOCK = asyncio.Lock()

    if MISSION_LOCK.locked():
        logging.warning("⏭️ Previous mission still running. Skipping this cycle to avoid overlap.")
        return

    async with MISSION_LOCK:
    
        job = context.job
        chat_id = job.chat_id
    
        # 🏥 EARLY EXIT: Kill switch check
        if database.check_system_flag("kill_switch", "true"):
            logging.info("🛑 LOOP SUPPRESSED: Kill Switch is ON.")
            return
    
        # 🏥 RUN HEALTH CHECK BEFORE MISSION (Auto-repair any issues)
        try:
            if health_check:
                await asyncio.to_thread(health_check.run_full_health_check)
                logging.info(f"🏥 Pre-mission health: {health_check.get_status()['system_health']}")
        except Exception as e:
            logging.error(f"Health check error (non-critical): {e}")
    
        # 🌍 DISCOVER NEW COMPANIES (Actually use the scraper!)
        try:
            if company_scraper:
                discovery_result = await asyncio.to_thread(company_scraper.discover_all_companies)
                discovered_count = 0
                if isinstance(discovery_result, dict):
                    discovered_count = int(discovery_result.get('new_companies', 0) or 0)
                elif isinstance(discovery_result, int):
                    discovered_count = discovery_result

                if discovered_count > 0:
                    logging.info(f"🌍 Discovered {discovered_count} new companies from global boards")
        except Exception as e:
            logging.debug(f"Company discovery optional (non-critical): {e}")

        # 1. SCOUTING PHASE (OPTIMIZED: Parallel scraping)
        logging.info("🛰️ Scouting Phase Started...")
        raw_leads = await parallel_scrape_jobs()  # ⚡ Now parallel instead of sequential
        if not raw_leads:
            try:
                fallback_leads = await asyncio.to_thread(database.get_oracle_leads)
                if fallback_leads:
                    raw_leads = fallback_leads
                    logging.warning(f"🛟 Scrapers returned 0 jobs. Using Oracle fallback leads: {len(raw_leads)}")
            except Exception as e:
                logging.error(f"Oracle fallback failed (non-blocking): {e}")
        new_strikes = 0
        analyzed_count = 0

        current_phase = await asyncio.to_thread(database.get_phase)

        # ⚡ OPTIMIZATION: Quick pre-filter to skip obvious rejects before expensive AI
        from data_validator import DataValidator
        validator = DataValidator()

        pre_filtered_leads = []
        for lead in raw_leads:
            # Clean data first
            lead = validator.clean_lead(lead)

            # Quick validation
            is_valid, errors = validator.validate_lead(lead)
            if not is_valid:
                logging.debug(f"Lead validation failed: {', '.join(errors)}")
                continue

            if fast_filter(lead, current_phase):
                pre_filtered_leads.append(lead)

        logging.info(f"⚡ Pre-filter: {len(raw_leads)} → {len(pre_filtered_leads)} jobs ({100*len(pre_filtered_leads)//max(len(raw_leads),1)}% pass)")

        # OPTIMIZATION: Parallel pre-processing (dedup + AI filter) for 3-4x speedup
        async def process_lead_parallel(lead):
            """Process a single lead with all checks in parallel"""
            # Check Deduplication (The Guardian) - run in thread pool
            lead_url = lead.get('url') or lead.get('link') or ''
            if lead_url:
                is_dup = await asyncio.to_thread(database.is_duplicate, lead_url)
                if is_dup:
                    return None, "url_duplicate"

            # Check Company Database for duplicates - parallel
            email = lead.get('email', 'unknown')
            company_name = lead.get('company_name', 'Unknown Company')
            if company_db and company_db.is_duplicate(email, company_name):
                logging.debug(f"📋 COMPANY DUPLICATE: {company_name}")
                return None, "company_duplicate"

            # AI Triage & Filtering - run in parallel with above checks
            is_rel, reason, body, est_salary = await asyncio.to_thread(
                is_relevant_to_cv,
                lead.get('job_title', ''),
                lead.get('description', '')
            )
            if not is_rel:
                return None, f"AI REJECT: {reason}"

            # Validation check
            is_valid, v_reason, s_val, p_count = await asyncio.to_thread(
                is_valid_target,
                company_name,
                lead.get('location', ''),
                est_salary,
                current_phase,
                lead.get('description', '')
            )
            if not is_valid:
                return None, f"FILTER REJECT: {v_reason}"

            # All checks passed - enrich lead
            lead['custom_body'] = body
            lead['mission_type'] = current_phase
            lead['priority_score'] = lead_priority_score(lead)
            return lead, "qualified"

        # Process all pre-filtered leads in parallel batches
        qualified_leads = []
        batch_size = 20  # Process in batches to avoid overwhelming
        for i in range(0, len(pre_filtered_leads), batch_size):
            batch = pre_filtered_leads[i:i+batch_size]
            results = await asyncio.gather(*[process_lead_parallel(lead) for lead in batch])

            for lead, status in results:
                if lead is not None and status == "qualified":
                    qualified_leads.append(lead)
                elif status != "url_duplicate":  # Don't log URL dups (expected)
                    logging.debug(f"Lead rejected: {status}")

        logging.info(f"⚡ Qualified: {len(qualified_leads)}/{len(pre_filtered_leads)} leads")

        # Highest-value targets first.
        qualified_leads.sort(key=lambda x: x.get('priority_score', 0), reverse=True)

        # MAXIMUM POWER: Cap per-cycle workload to maintain throughput
        max_candidates = max(1, int(getattr(config, 'MAX_QUALIFIED_LEADS_PER_CYCLE', 100)))
        # Hard safety cap: prevents very long locked cycles when SMTP is degraded
        max_candidates = min(max_candidates, 30)
        if len(qualified_leads) > max_candidates:
            logging.info(f"Candidate cap: {len(qualified_leads)} -> {max_candidates} (priority-trimmed)")
            qualified_leads = qualified_leads[:max_candidates]

        # 2. STRIKE PHASE (MAXIMUM POWER parallel execution)
        if qualified_leads:
            # MAXIMUM POWER: Increased parallel workers for faster throughput
            max_parallel = max(1, int(getattr(config, 'MAX_PARALLEL_STRIKES', 8)))
            # Keep system responsive with reasonable cap
            max_parallel = min(max_parallel, 6)
            logging.info(f"Strike queue: {len(qualified_leads)} qualified leads | parallel workers: {max_parallel}")

            semaphore = asyncio.Semaphore(max_parallel)

            async def _strike_worker(candidate):
                async with semaphore:
                    try:
                        return await process_strike_candidate(context, chat_id, candidate, current_phase)
                    except Exception as e:
                        logging.error(f"Strike worker error: {e}")
                        return False

            strike_results = await asyncio.gather(*[_strike_worker(lead) for lead in qualified_leads], return_exceptions=True)
            for result in strike_results:
                if isinstance(result, Exception):
                    logging.error(f"Strike worker error (non-blocking): {result}")
                elif result:
                    new_strikes += 1

        # **NEW**: Persist metrics after mission (so daily/weekly/monthly stats accumulate)
        try:
            if metrics_tracker:
                metrics_tracker.record_job_analyzed(count=len(pre_filtered_leads), autosave=False)
                await asyncio.to_thread(metrics_tracker.save_metrics)
        except Exception as e:
            logging.error(f"Metrics persistence error (non-blocking): {e}")

        if new_strikes == 0:
            logging.info("🔮 Mission finished. No new targets found.")
        else:
            logging.info(f"🎯 Mission Strike Count: {new_strikes} new applications sent")

        # Optional natural breaks. Disabled by default for max throughput.
        if new_strikes > 0 and getattr(config, 'ENABLE_NATURAL_BREAKS', False):
            break_probability = float(getattr(config, 'NATURAL_BREAK_PROBABILITY', 0.15))
            break_min = int(getattr(config, 'NATURAL_BREAK_MINUTES_MIN', 1))
            break_max = int(getattr(config, 'NATURAL_BREAK_MINUTES_MAX', 3))
            if random.random() < break_probability:
                break_duration = random.randint(max(1, break_min), max(break_min, break_max))
                logging.info(f"☕ Natural Break: {break_duration} minutes")
                await asyncio.sleep(break_duration * 60)

        # **NEW**: Log mission completion with metrics summary
        try:
            if metrics_tracker and hasattr(metrics_tracker, 'metrics'):
                today_apps = metrics_tracker.metrics.get('today', {}).get('applications_sent', 0)
                total_companies = company_db.get_statistics().get('total_unique_companies', 0) if company_db else 0
                logging.info(f"✅ Mission Complete: {new_strikes} strikes | Today: {today_apps} apps | Companies: {total_companies}")
        except Exception as e:
            logging.error(f"Mission summary error (non-critical): {e}")

async def mission_loop(application):
    """Built-in fallback scheduler when PTB JobQueue is unavailable."""
    global LAST_SUCCESSFUL_MISSION_TS
    startup_delay = int(getattr(config, 'MISSION_STARTUP_DELAY_SECONDS', 10))
    interval = int(getattr(config, 'MISSION_INTERVAL_SECONDS', 300))

    logging.info(f"🛰️ Mission loop armed. First run in {startup_delay}s, then every {interval}s")

    await asyncio.sleep(startup_delay)
    LAST_SUCCESSFUL_MISSION_TS = time.time()
    while True:
        try:
            if time.time() < SAFE_MODE_UNTIL_TS:
                remaining = int(SAFE_MODE_UNTIL_TS - time.time())
                logging.warning(f"🧯 Safe mode active. Skipping mission for {remaining}s")
                await asyncio.sleep(min(interval, max(10, remaining)))
                continue

            context = SimpleNamespace(
                job=SimpleNamespace(chat_id=config.TELEGRAM_CHAT_ID),
                bot=application.bot,
            )
            retry_attempts = max(1, int(getattr(config, 'MISSION_RETRY_ATTEMPTS', 2)))
            retry_delay = max(1, int(getattr(config, 'MISSION_RETRY_BASE_DELAY_SECONDS', 2)))
            await run_async_with_retries(
                lambda: auto_strike_mission(context),
                attempts=retry_attempts,
                base_delay=retry_delay,
                label='mission_loop'
            )
            await evaluate_safe_mode_guard(application)
            LAST_SUCCESSFUL_MISSION_TS = time.time()
        except Exception as e:
            logging.error(f"Mission loop error (non-blocking): {e}")
        await asyncio.sleep(interval)


async def supervisor_loop(application):
    """Self-heal supervisor: detects stalled missions and triggers recovery run."""
    global LAST_SUCCESSFUL_MISSION_TS, LAST_DAILY_REPORT_DATE

    interval = max(60, int(getattr(config, 'SUPERVISOR_CHECK_INTERVAL_SECONDS', 120)))
    mission_interval = max(60, int(getattr(config, 'MISSION_INTERVAL_SECONDS', 300)))
    stall_threshold = max(600, int(getattr(config, 'MISSION_STALL_THRESHOLD_SECONDS', mission_interval * 4)))

    logging.info(f"🛡️ Supervisor loop armed. Checking every {interval}s | stall threshold {stall_threshold}s")
    while True:
        try:
            report_hour = int(getattr(config, 'DAILY_REPORT_HOUR_LOCAL', 9))
            today_label = datetime.now().strftime('%Y-%m-%d')
            if datetime.now().hour >= report_hour and LAST_DAILY_REPORT_DATE != today_label:
                await send_system_message(application, build_health_snapshot_text())
                LAST_DAILY_REPORT_DATE = today_label

            now = time.time()
            stale_for = now - float(LAST_SUCCESSFUL_MISSION_TS or now)

            if stale_for >= stall_threshold:
                if MISSION_LOCK is not None and MISSION_LOCK.locked():
                    logging.info("🛡️ Supervisor: mission currently active, no intervention needed.")
                else:
                    kill_switch = await asyncio.to_thread(database.check_system_flag, "kill_switch", "true")
                    if kill_switch:
                        logging.info("🛡️ Supervisor: kill switch active, skipping recovery run.")
                    else:
                        logging.warning(f"🛡️ Supervisor detected mission stall ({int(stale_for)}s). Triggering recovery mission.")
                        context = SimpleNamespace(
                            job=SimpleNamespace(chat_id=config.TELEGRAM_CHAT_ID),
                            bot=application.bot,
                        )
                        await run_async_with_retries(
                            lambda: auto_strike_mission(context),
                            attempts=max(1, int(getattr(config, 'MISSION_RETRY_ATTEMPTS', 2))),
                            base_delay=max(1, int(getattr(config, 'MISSION_RETRY_BASE_DELAY_SECONDS', 2))),
                            label='supervisor_recovery'
                        )
                        await evaluate_safe_mode_guard(application)
                        LAST_SUCCESSFUL_MISSION_TS = time.time()
        except Exception as e:
            logging.error(f"Supervisor loop error (non-blocking): {e}")

        await asyncio.sleep(interval)


async def run_async_with_retries(coro_factory, attempts=2, base_delay=2, label='task'):
    """Run async work with bounded retries and exponential backoff."""
    max_attempts = max(1, int(attempts))
    delay_base = max(1, int(base_delay))
    last_error = None

    for attempt in range(1, max_attempts + 1):
        try:
            return await coro_factory()
        except Exception as e:
            last_error = e
            if attempt >= max_attempts:
                break
            wait_seconds = min(delay_base * (2 ** (attempt - 1)), 30)
            logging.warning(
                f"{label} failed (attempt {attempt}/{max_attempts}): {e}. Retrying in {wait_seconds}s"
            )
            await asyncio.sleep(wait_seconds)

    raise last_error


def configure_runtime_safety_hooks():
    """Install global exception hooks to improve observability of uncaught crashes."""

    def _sys_hook(exc_type, exc_value, exc_tb):
        logging.critical("Uncaught exception", exc_info=(exc_type, exc_value, exc_tb))

    def _thread_hook(args):
        logging.critical(
            f"Uncaught thread exception in {getattr(args, 'thread', None)}",
            exc_info=(args.exc_type, args.exc_value, args.exc_traceback),
        )

    sys.excepthook = _sys_hook
    if hasattr(threading, 'excepthook'):
        threading.excepthook = _thread_hook


def runtime_backup_root() -> Path:
    return Path(__file__).resolve().parent / "recovery" / "runtime_backups"


def create_runtime_backup() -> tuple[bool, str, list]:
    """Create a timestamped backup for key runtime state files."""
    base = runtime_backup_root()
    base.mkdir(parents=True, exist_ok=True)

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    target = base / f"backup_{stamp}"
    target.mkdir(parents=True, exist_ok=True)

    copied = []
    root = Path(__file__).resolve().parent
    for name in RUNTIME_STATE_FILES:
        src = root / name
        if src.exists():
            shutil.copy2(src, target / name)
            copied.append(name)

    if not copied:
        return False, "No runtime files found to backup.", []

    return True, str(target), copied


def restore_latest_runtime_backup() -> tuple[bool, str, list]:
    """Restore latest available runtime backup into project root."""
    base = runtime_backup_root()
    if not base.exists():
        return False, "No backup directory found.", []

    candidates = [p for p in base.iterdir() if p.is_dir() and p.name.startswith("backup_")]
    if not candidates:
        return False, "No backups available.", []

    latest = sorted(candidates)[-1]
    root = Path(__file__).resolve().parent
    restored = []

    for name in RUNTIME_STATE_FILES:
        src = latest / name
        if src.exists():
            shutil.copy2(src, root / name)
            restored.append(name)

    if not restored:
        return False, f"Backup exists but had no known runtime files: {latest.name}", []

    return True, latest.name, restored


def build_health_snapshot_text() -> str:
    """Build compact health report text for daily and on-demand report commands."""
    health = health_check.get_status() if health_check else {}
    health_state = health.get('system_health', '🟡 UNKNOWN') if isinstance(health, dict) else '🟡 UNKNOWN'

    today = {}
    if metrics_tracker and hasattr(metrics_tracker, 'metrics'):
        today = metrics_tracker.metrics.get('today', {})

    apps = int(today.get('applications_sent', 0) or 0)
    jobs = int(today.get('jobs_analyzed', 0) or 0)
    errors = int(today.get('errors', 0) or 0)
    success_rate = ((jobs - errors) / max(jobs, 1)) * 100 if jobs > 0 else 0
    kill_switch = database.check_system_flag("kill_switch", "true")
    safe_mode_left = max(0, int(SAFE_MODE_UNTIL_TS - time.time()))
    companies_total = company_db.get_statistics().get('total_unique_companies', 0) if company_db else 0

    return (
        "📬 <b>DAILY HEALTH REPORT</b>\n\n"
        f"🏥 System: {health_state}\n"
        f"📧 Applications Today: {apps}\n"
        f"🔎 Jobs Analyzed Today: {jobs}\n"
        f"⚠️ Errors Today: {errors}\n"
        f"✅ Success Rate: {success_rate:.1f}%\n"
        f"🏢 Companies Tracked: {companies_total}\n"
        f"🛑 Kill Switch: {'ON' if kill_switch else 'OFF'}\n"
        f"🧯 Safe Mode: {'ON' if safe_mode_left > 0 else 'OFF'}"
        + (f" ({safe_mode_left}s left)" if safe_mode_left > 0 else "")
    )


async def send_system_message(application, text: str):
    """Send a system message to owner chat with retry for transient Telegram issues."""
    chat_id = getattr(config, 'TELEGRAM_CHAT_ID', None)
    if not chat_id:
        return

    for attempt in range(1, 4):
        try:
            await application.bot.send_message(chat_id=chat_id, text=text, parse_mode='HTML')
            return
        except RetryAfter as e:
            wait_seconds = int(getattr(e, 'retry_after', 1) or 1)
            await asyncio.sleep(min(wait_seconds + 1, 20))
        except (TimedOut, NetworkError) as e:
            wait_seconds = min(2 ** attempt, 8)
            logging.warning(f"System message transient error: {e}. retry in {wait_seconds}s")
            await asyncio.sleep(wait_seconds)
        except Exception as e:
            logging.warning(f"System message failed: {e}")
            return


async def evaluate_safe_mode_guard(application):
    """Pause missions temporarily when error rate spikes above safety threshold."""
    global SAFE_MODE_UNTIL_TS, LAST_SAFE_MODE_ALERT_TS

    if not metrics_tracker or not hasattr(metrics_tracker, 'metrics'):
        return

    today = metrics_tracker.metrics.get('today', {})
    jobs = int(today.get('jobs_analyzed', 0) or 0)
    errors = int(today.get('errors', 0) or 0)

    min_jobs = max(1, int(getattr(config, 'SAFE_MODE_MIN_JOBS', 20)))
    threshold = float(getattr(config, 'SAFE_MODE_ERROR_RATE_THRESHOLD', 0.35))
    cooldown = max(60, int(getattr(config, 'SAFE_MODE_COOLDOWN_SECONDS', 1800)))

    if jobs < min_jobs:
        return

    error_rate = errors / max(jobs, 1)
    now = time.time()
    if error_rate >= threshold and now >= SAFE_MODE_UNTIL_TS:
        SAFE_MODE_UNTIL_TS = now + cooldown
        if now - LAST_SAFE_MODE_ALERT_TS > 120:
            LAST_SAFE_MODE_ALERT_TS = now
            await send_system_message(
                application,
                (
                    "🧯 <b>SAFE MODE ACTIVATED</b>\n\n"
                    f"High error rate detected: {error_rate*100:.1f}%\n"
                    f"Cooldown: {cooldown}s\n"
                    "Missions will pause temporarily to self-stabilize."
                )
            )


def mission_interval_label():
    """Human-readable mission interval based on config."""
    interval = max(60, int(getattr(config, 'MISSION_INTERVAL_SECONDS', 300)))
    minutes = interval // 60
    if minutes < 60:
        return f"every {minutes} minute{'s' if minutes != 1 else ''}"
    hours = minutes // 60
    return f"every {hours} hour{'s' if hours != 1 else ''}"


def normalize_user_command(cmd: str) -> str:
    """Normalize callback/button/free-text/slash command into one command key."""
    text = (cmd or '').strip().lower()
    if not text:
        return ''

    # Strip slash command syntax (/status@bot -> status)
    if text.startswith('/'):
        first = text.split()[0]
        text = first.split('@')[0].lstrip('/')

    alias_map = {
        'live status': 'status',
        'status': 'status',
        'dashboard_status': 'dashboard_status',
        'health': 'system_health',
        'system health': 'system_health',
        'system_health': 'system_health',
        'stats': 'today_stats',
        'today': 'today_stats',
        'today_stats': 'today_stats',
        'monthly': 'monthly_stats',
        'monthly_stats': 'monthly_stats',
        'companies': 'companies_db',
        'companies_db': 'companies_db',
        'recent': 'recent_apps',
        'recent_apps': 'recent_apps',
        'next': 'next_run',
        'next_run': 'next_run',
        'targets': 'targets',
        'settings': 'settings',
        'pulse': 'pulse',
        'prep': 'prep',
        'interview': 'prep',
        'runnow': 'scout',
        'run_now': 'scout',
        'run': 'scout',
        'scout': 'scout',
        'whatsapp sam': 'scout',
        'whatsapp': 'scout',
        'stop': 'kill_on',
        'resume': 'kill_off',
        'diag': 'diagnostics',
        'diagnostics': 'diagnostics',
        'report': 'report',
        'healthreport': 'report',
        'backup': 'backup',
        'restore': 'restore',
        'myid': 'myid',
        'simple': 'simple',
        'easy': 'simple',
        'help': 'help',
        'guide': 'help',
        # Reply keyboard text aliases
        '📊 status': 'status',
        '📊 live status': 'status',
        '🏥 health': 'system_health',
        '📈 stats': 'today_stats',
        '🏢 companies': 'companies_db',
        '⏰ next run': 'next_run',
        '🎯 targets': 'targets',
        '🧠 interview prep': 'prep',
        '🚨 emergency stop': 'kill_on',
        '⚡ run now': 'scout',
        '✅ resume': 'kill_off',
        '✨ simple': 'simple',
        '📬 report': 'report',
        '💾 backup': 'backup',
        '♻️ restore': 'restore',
    }

    return alias_map.get(text, text)


async def handle_quick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Route slash commands to shared command processor."""
    raw = update.message.text if update and update.message else ''
    success = await process_command(raw, update, context)
    if not success and update and update.message:
        await update.message.reply_text("⚠️ Unknown command. Use /start or /help.")


def get_update_chat_id(update: Update):
    """Extract chat ID from callback/message updates."""
    try:
        if update and update.effective_chat:
            return str(update.effective_chat.id)
    except Exception:
        return None
    return None


def is_authorized_update(update: Update) -> bool:
    """Allow only configured Telegram chat to execute sensitive controls."""
    expected = str(getattr(config, 'TELEGRAM_CHAT_ID', '') or '').strip()
    actual = str(get_update_chat_id(update) or '').strip()
    if not expected:
        return True
    return expected == actual


def spawn_background_task(coro, task_name: str):
    """Create a background task and log any unhandled exception."""
    task = asyncio.create_task(coro, name=task_name)

    def _done_callback(t):
        try:
            _ = t.result()
        except Exception as e:
            logging.error(f"Background task '{task_name}' failed: {e}")

    task.add_done_callback(_done_callback)
    return task


def _extract_explainable_lines(text: str):
    """Extract concise non-empty lines from a Telegram HTML message."""
    if not text:
        return []

    cleaned = re.sub(r'<[^>]+>', '', str(text))
    lines = []
    for raw in cleaned.splitlines():
        line = raw.strip()
        if not line:
            continue
        if set(line) <= set('-_=*#│└├┌┐┘┬┴┼═║╔╗╚╝ '):
            continue
        lines.append(line)
    return lines


def _register_explain_payload(text: str):
    """Store explain payload and return compact message key for callback data."""
    global EXPLAIN_SEQ
    EXPLAIN_SEQ += 1
    key = format(EXPLAIN_SEQ, 'x')

    payload = {
        'raw': str(text or ''),
        'lines': _extract_explainable_lines(text),
        'created_at': time.time(),
    }
    EXPLAIN_CACHE[key] = payload
    EXPLAIN_ORDER.append(key)

    # Keep cache bounded to avoid unbounded memory growth.
    max_items = 200
    while len(EXPLAIN_ORDER) > max_items:
        old = EXPLAIN_ORDER.pop(0)
        EXPLAIN_CACHE.pop(old, None)

    return key


def _build_explain_markup(text: str):
    """Build clean explain UX: inline markers + one explain button."""
    key = _register_explain_payload(text)
    lines = EXPLAIN_CACHE.get(key, {}).get('lines', [])
    if not lines:
        return None, text

    # Add lightweight inline markers in displayed text.
    marked_lines = []
    marker_idx = 0
    for raw in str(text).splitlines():
        line = raw.strip()
        if (
            marker_idx < len(lines)
            and line
            and not (set(line) <= set('-_=*#│└├┌┐┘┬┴┼═║╔╗╚╝ '))
        ):
            marker_idx += 1
            marked_lines.append(f"{raw} <i>[?{marker_idx}]</i>")
        else:
            marked_lines.append(raw)

    markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("❓ شرح هالرسالة", callback_data=f"explain_all:{key}")],
        [InlineKeyboardButton("🧹 إخفاء العلامات", callback_data=f"explain_hide:{key}")],
    ])
    return markup, "\n".join(marked_lines)


def _explain_line_meaning(line: str):
    """Return a user-friendly Arabic explanation for one status/command line."""
    low = line.lower()

    if 'scouted leads' in low:
        return "هيدا عدد الفرص اللي انجمعت وانفلترت كـ leads (مش يعني انبعت عليهم بعد)."
    if 'applications' in low:
        return "هيدا عدد التقديمات اللي انبعتت فعلياً بنجاح."
    if 'jobs analyzed' in low:
        return "هيدا عدد الوظائف اللي البوت قراها وحلّلها خلال اليوم."
    if 'errors today' in low:
        return "هيدا عدد الأخطاء اللي تسجّلت فعلياً اليوم داخل دورة التشغيل."
    if 'success rate' in low:
        return "نسبة النجاح محسوبة من الإرسالات الناجحة مقابل المحاولات."
    if 'companies tracked' in low:
        return "عدد الشركات المخزنة بقاعدة التتبع لمنع التكرار."
    if 'kill switch' in low:
        return "إذا ON يعني الإرسال متوقف إجبارياً. إذا OFF فالمهام مسموح تشتغل."
    if 'safe mode' in low:
        return "وضع حماية مؤقت عند أخطاء متكررة؛ بيخفّف/يوقف بعض العمليات لفترة قصيرة."
    if 'mission already running' in low:
        return "يعني في دورة شغّالة حالياً، والنظام مانع تشغيل دورة ثانية بنفس الوقت."
    if 'status' in low and ':' in line:
        return "هيدا سطر حالة مباشر للمكوّن الحالي (مؤشر عام للصحّة/النشاط)."

    if ':' in line:
        k, v = line.split(':', 1)
        return f"هيدا الحقل '{k.strip()}' وقيمته الحالية هي '{v.strip()}'."

    return "هيدا سطر معلومات من ملخص التشغيل الحالي للبوت."


def _probe_delivery_channel(ttl_seconds: int = 300):
    """Best-effort delivery channel probe with TTL cache to keep /status responsive."""
    now = time.time()
    if (now - float(DELIVERY_PROBE.get("ts", 0) or 0)) < ttl_seconds:
        return DELIVERY_PROBE.get("status", "unknown"), DELIVERY_PROBE.get("detail", "")

    brevo_api = (getattr(config, 'BREVO_API_KEY', '') or '').strip()
    if brevo_api:
        DELIVERY_PROBE.update({
            "ts": now,
            "status": "ready",
            "detail": "Brevo HTTP key configured",
        })
        return DELIVERY_PROBE["status"], DELIVERY_PROBE["detail"]

    smtp_targets = [
        (getattr(config, 'GMAIL_SMTP_SERVER', 'smtp.gmail.com'), int(getattr(config, 'GMAIL_SMTP_PORT', 587) or 587)),
        (getattr(config, 'BREVO_SMTP_SERVER', 'smtp-relay.brevo.com'), int(getattr(config, 'BREVO_SMTP_PORT', 587) or 587)),
    ]

    for host, port in smtp_targets:
        try:
            with socket.create_connection((host, port), timeout=2):
                DELIVERY_PROBE.update({
                    "ts": now,
                    "status": "ready",
                    "detail": f"SMTP reachable on {host}:{port}",
                })
                return DELIVERY_PROBE["status"], DELIVERY_PROBE["detail"]
        except Exception:
            continue

    DELIVERY_PROBE.update({
        "ts": now,
        "status": "blocked",
        "detail": "SMTP ports unreachable and Brevo API key missing",
    })
    return DELIVERY_PROBE["status"], DELIVERY_PROBE["detail"]


async def send_ui_response(update: Update, text: str, include_explain: bool = True):
    """Safely send UI response for callback or message contexts."""
    rendered_text = text
    explain_markup = None
    if include_explain:
        explain_markup, rendered_text = _build_explain_markup(text)

    async def _send_with_retry(send_coro_factory, tag: str):
        for attempt in range(1, 4):
            try:
                return await send_coro_factory()
            except RetryAfter as e:
                wait_seconds = int(getattr(e, 'retry_after', 1) or 1)
                await asyncio.sleep(min(wait_seconds + 1, 15))
            except (TimedOut, NetworkError) as e:
                wait_seconds = min(2 ** attempt, 8)
                logging.warning(f"Telegram transient error on {tag}: {e}. retry in {wait_seconds}s")
                await asyncio.sleep(wait_seconds)
            except BadRequest as e:
                logging.warning(f"Telegram bad request on {tag}: {e}")
                raise

    if update.callback_query:
        try:
            await _send_with_retry(
                lambda: update.callback_query.edit_message_text(rendered_text, parse_mode='HTML', reply_markup=explain_markup),
                'callback_edit'
            )
            return
        except Exception as e:
            logging.warning(f"Callback edit failed, falling back to chat message: {e}")
            await _send_with_retry(
                lambda: update.callback_query.message.reply_text(rendered_text, parse_mode='HTML', reply_markup=explain_markup),
                'callback_reply'
            )
            return

    if update.message:
        await _send_with_retry(
            lambda: update.message.reply_text(rendered_text, parse_mode='HTML', reply_markup=explain_markup),
            'message_reply'
        )
        return

# ==========================================
# ⌨️ TELEGRAM UI HANDLERS
# ==========================================

async def track_update(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Verbose Signature Logging: Prints EVERY incoming signal to the terminal."""
    u_id = update.update_id
    u_type = "UNKNOWN"
    if update.message: u_type = "MESSAGE"
    elif update.callback_query: u_type = f"CALLBACK ({update.callback_query.data})"
    
    print(f"🛰️ SIGNAL DETECTED: [Update ID: {u_id}] [Type: {u_type}]")
    logging.info(f"🛰️ Update Received: {u_id} | Type: {u_type}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for the Enhanced Command Center with full dashboard."""
    # 🗄️ BOTTOM KEYBOARD (Reply Keyboard) - For high-visibility persistence
    from telegram import ReplyKeyboardMarkup
    reply_kb = [
        ["📊 Status", "🏥 Health"],
        ["📈 Stats", "🏢 Companies"],
        ["⏰ Next Run", "🎯 Targets"],
        ["⚡ Run Now", "✅ Resume"],
        ["🧠 Interview Prep", "🚨 Emergency Stop"]
    ]
    reply_markup_kb = ReplyKeyboardMarkup(reply_kb, resize_keyboard=True)
    
    # 🖱️ INLINE BUTTONS (Using new enhanced dashboard)
    inline_markup = dashboard.get_main_keyboard()
    
    # Get system status for welcome message
    health_status_value = ""
    if health_check and hasattr(health_check, 'status') and isinstance(health_check.status, dict):
        health_status_value = str(health_check.status.get("system_health", ""))
    health_msg = "🟢 HEALTHY" if health_status_value == "🟢 HEALTHY" else "🟡 OK"
    apps_today = metrics_tracker.metrics.get("today", {}).get("applications_sent", 0) if metrics_tracker else 0
    companies_total = company_db.get_statistics().get("total_unique_companies", 0) if company_db else 0
    
    await update.message.reply_text(
        f"""🤖 <b>SAM JOB AUTOMATOR - COMMAND CENTER</b>

🟢 Status: {health_msg}
✅ Fully Autonomous & Self-Healing
🏥 Auto-Repair: ACTIVE

📊 CURRENT METRICS:
├─ Today: {apps_today} applications sent
├─ Companies Tracked: {companies_total}
└─ Next Run: {mission_interval_label()} (automated)

🎯 AVAILABLE COMMANDS:
Click buttons below to:
✅ Monitor live status
✅ Check system health
✅ View statistics
✅ Track companies
✅ Get interview prep
✅ Emergency controls

🛡️ All operations autonomous - zero human intervention needed!""",
        reply_markup=reply_markup_kb,
        parse_mode='HTML'
    )
    
    # Also send the inline version for maximum compatibility
    await update.message.reply_text(
        "🖱️ <i><b>Enhanced Dashboard Controls:</b></i>\n\nClick any button to see detailed information:",
        reply_markup=inline_markup,
        parse_mode='HTML'
    )

    # Super-simple quick panel with only the most important controls.
    await update.message.reply_text(
        dashboard.format_simple_help(getattr(config, 'MISSION_INTERVAL_SECONDS', 300)),
        reply_markup=dashboard.get_simple_keyboard(),
        parse_mode='HTML'
    )

async def process_command(cmd: str, update: Update, context: ContextTypes.DEFAULT_TYPE):
    """The Shared Logic Core: Ensures consistent behavior for buttons and text."""
    # Normalize command strings (handles both callback data and keyboard text)
    cmd = normalize_user_command(cmd)
    
    # Target Mapping: Syncing labels to logic
    if cmd in {"status", "dashboard_status"}:
        apps = 0
        analyzed = 0
        leads = 0

        try:
            if metrics_tracker and hasattr(metrics_tracker, 'metrics'):
                today = metrics_tracker.metrics.get('today', {})
                apps = int(today.get('applications_sent', 0) or 0)
                analyzed = int(today.get('jobs_analyzed', 0) or 0)
        except Exception as e:
            logging.debug(f"Status metrics read warning: {e}")

        try:
            data = await asyncio.to_thread(database.load_discovered_companies)
            if isinstance(data, dict):
                leads = int(data.get('total', 0) or 0)
                if leads == 0:
                    companies = data.get('companies', []) or []
                    leads = len(companies)
        except Exception as e:
            logging.debug(f"Status discovered-companies read warning: {e}")

        # Fallback to analyzed count when source lead cache was reset this cycle.
        if leads == 0 and analyzed > 0:
            leads = analyzed

        delivery_status, delivery_detail = _probe_delivery_channel()
        delivery_label = "✅ READY" if delivery_status == "ready" else ("⛔ BLOCKED" if delivery_status == "blocked" else "❔ UNKNOWN")

        text = (f"📊 <b>LIVE INTELLIGENCE</b>\n\n"
            f"📍 Scouted Leads: {leads}\n"
            f"🚀 Applications: {apps}\n"
            f"📤 Delivery Channel: {delivery_label}\n"
            f"📝 Delivery Detail: {delivery_detail}\n\n"
                f"<i>Verified 24/7 Autonomy.</i>")
    elif cmd == "pulse":
        mins, last_seen = await asyncio.to_thread(database.get_last_heartbeat)
        status = "🟢 ACTIVE" if mins < 60 else "🔴 OFFLINE"
        text = f"💓 <b>SYSTEM PULSE</b>\nStatus: {status}\nLast Active: {last_seen}"
    elif cmd == "vault":
        text = "🛡️ <b>VAULT ACCESS REQUIRED</b>\nPlease use terminal for credential updates."
    elif cmd == "prep":
        text = "🧠 <b>INTEL GATHERING: Interview Prep</b>\nPlease type the Company Name to generate a dossier."
        context.user_data['awaiting_prep'] = True
    elif cmd == "help":
        text = (
            "📚 <b>COMMAND GUIDE</b>\n\n"
            "Quick commands:\n"
            "/status, /health, /stats, /companies\n"
            "/targets, /next, /pulse\n"
            "/runnow, /stop, /resume, /prep, /diag\n\n"
            "Tip: Use /simple for the easiest emoji control panel."
        )
    elif cmd == "simple":
        text = dashboard.format_simple_help(getattr(config, 'MISSION_INTERVAL_SECONDS', 300))
    elif cmd == "myid":
        chat_id = get_update_chat_id(update)
        text = f"🆔 <b>Your Chat ID</b>\n{chat_id if chat_id else 'Unknown'}"
    elif cmd == "report":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        text = build_health_snapshot_text()
    elif cmd == "backup":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        ok, where, files = await asyncio.to_thread(create_runtime_backup)
        if ok:
            text = (
                "💾 <b>Backup Created</b>\n\n"
                f"Path: <code>{where}</code>\n"
                f"Files: {', '.join(files)}"
            )
        else:
            text = f"⚠️ <b>Backup Failed</b>\n{where}"
    elif cmd == "restore":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        ok, source, files = await asyncio.to_thread(restore_latest_runtime_backup)
        if ok:
            text = (
                "♻️ <b>Restore Complete</b>\n\n"
                f"Source: <code>{source}</code>\n"
                f"Files: {', '.join(files)}"
            )
        else:
            text = f"⚠️ <b>Restore Failed</b>\n{source}"
    elif cmd == "kill_on":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        await asyncio.to_thread(database.set_system_flag, "kill_switch", "true")
        text = "🛑 <b>KILL SWITCH ACTIVATED</b>\nEngine outreach frozen."
    elif cmd == "kill_off":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        await asyncio.to_thread(database.set_system_flag, "kill_switch", "false")
        text = "🟢 <b>ENGINE RESUMED</b>\nSovereign mode restored."
    elif cmd == "scout":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        if MISSION_LOCK is not None and MISSION_LOCK.locked():
            mins, last_seen = await asyncio.to_thread(database.get_last_heartbeat)
            text = (
                "⏳ <b>Mission already running</b>\n"
                "Engine is actively scouting/sending now.\n"
                f"Last heartbeat: {last_seen} ({mins} min ago).\n"
                "Try again in 1-2 minutes."
            )
        else:
            text = "🛰️ <b>Manual Reconnaissance initiated...</b>"
            spawn_background_task(auto_strike_mission(context), "manual_reconnaissance")
    elif cmd == "diagnostics":
        if not is_authorized_update(update):
            text = "⛔ <b>Unauthorized</b>\nThis control is owner-only."
            await send_ui_response(update, text)
            return True
        interval = int(getattr(config, 'MISSION_INTERVAL_SECONDS', 300))
        kill_switch = await asyncio.to_thread(database.check_system_flag, "kill_switch", "true")
        health = health_check.get_status() if health_check else {}
        health_state = health.get('system_health', '🟡 UNKNOWN') if isinstance(health, dict) else '🟡 UNKNOWN'
        text = (
            "🧪 <b>DIAGNOSTICS SNAPSHOT</b>\n\n"
            f"System Health: {health_state}\n"
            f"Mission Interval: {max(60, interval)} sec\n"
            f"Kill Switch: {'ON' if kill_switch else 'OFF'}\n"
            f"Mission Running: {'YES' if (MISSION_LOCK and MISSION_LOCK.locked()) else 'NO'}\n"
            f"AI Engine: {'ON' if ai_brain else 'OFF'}\n"
            f"Crawler: {'ON' if crawler else 'OFF'}\n\n"
            "If all above looks good, system is healthy."
        )
    elif cmd == "system_health":
        # System health report
        text = dashboard.format_health_status(health_check.get_status() if health_check else {})
    elif cmd == "today_stats":
        # Today's statistics
        text = dashboard.format_today_stats(metrics_tracker.metrics if metrics_tracker else {})
    elif cmd == "monthly_stats":
        # Monthly statistics
        stats = metrics_tracker.metrics if metrics_tracker else {}
        month_apps = stats.get("this_month", {}).get("applications_sent", 0)
        month_jobs = stats.get("this_month", {}).get("jobs_analyzed", 0)
        text = f"📅 <b>MONTHLY STATISTICS</b>\n\n📧 Applications: <b>{month_apps}</b>\n🔍 Jobs Analyzed: <b>{month_jobs}</b>\n\n🎯 Projected: ~{month_apps * 27} apps this month"
    elif cmd == "companies_db":
        # Companies database info
        text = dashboard.format_companies_db(company_db)
    elif cmd == "recent_apps":
        # Recent applications
        text = dashboard.format_recent_applications()
    elif cmd == "next_run":
        # Next run schedule
        text = dashboard.format_next_run(int(getattr(config, 'MISSION_INTERVAL_SECONDS', 300)))
    elif cmd == "targets":
        # Target information
        phase = await asyncio.to_thread(database.get_phase)
        text = f"🎯 <b>CURRENT TARGETS</b>\n\nPhase: <b>{phase.upper()}</b>\n\n📍 Scanning for {phase} opportunities\n💼 Matching role requirements\n🌍 Monitoring global market"
    elif cmd == "settings":
        # System settings
        text = "⚙️ <b>SYSTEM SETTINGS</b>\n\n✅ Auto-repair: ENABLED\n✅ Duplicate prevention: ENABLED\n✅ Company tracking: ENABLED\n✅ Metrics: REAL-TIME\n\nAll systems optimized for autonomous operation"
    elif cmd == "emergency_stop":
        # Emergency stop
        await asyncio.to_thread(database.set_system_flag, "kill_switch", "true")
        text = "🚨 <b>EMERGENCY STOP ACTIVATED</b>\n\nAll operations halted immediately.\n⏰ Auto-resume in 1 hour.\n\nUse /start to manually resume."
    else:
        return None # Command not recognized

    # Send Response
    await send_ui_response(update, text)
    return True

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Universal Callback Handler for Inline Buttons."""
    query = update.callback_query
    await query.answer()
    print(f"📡 UI CALLBACK Received: {query.data}")

    if str(query.data).startswith("explain_hide:"):
        try:
            _, key = str(query.data).split(':', 1)
            payload = EXPLAIN_CACHE.get(key, {})
            raw_text = payload.get('raw', '')
            if not raw_text:
                await query.answer("ما لقيت النص الأصلي لهالرسالة.", show_alert=True)
                return

            compact_markup = InlineKeyboardMarkup([
                [InlineKeyboardButton("❓ شرح هالرسالة", callback_data=f"explain_all:{key}")]
            ])
            await query.edit_message_text(raw_text, parse_mode='HTML', reply_markup=compact_markup)
            return
        except Exception as e:
            logging.warning(f"Explain-hide callback failed: {e}")
            await query.answer("صار خطأ أثناء إخفاء العلامات.", show_alert=True)
            return

    if str(query.data).startswith("explain_all:"):
        try:
            _, key = str(query.data).split(':', 1)
            payload = EXPLAIN_CACHE.get(key, {})
            lines = payload.get('lines', [])

            if not lines:
                await query.answer("الشرح مش متوفر لهالرسالة.", show_alert=True)
                return

            blocks = ["🔎 <b>شرح سريع لكل سطر</b>"]
            max_lines = min(len(lines), 10)
            for idx, line in enumerate(lines[:max_lines], start=1):
                meaning = _explain_line_meaning(line)
                blocks.append(
                    f"\n<b>؟{idx}</b> {html.escape(line)}\n"
                    f"↳ {html.escape(meaning)}"
                )

            if len(lines) > max_lines:
                blocks.append(f"\n<i>... وفي {len(lines) - max_lines} سطور إضافية.</i>")

            explain_text = "\n".join(blocks)
            await send_ui_response(update, explain_text, include_explain=False)
            return
        except Exception as e:
            logging.warning(f"Explain callback failed: {e}")
            await query.answer("صار خطأ أثناء عرض الشرح.", show_alert=True)
            return
    
    try:
        success = await process_command(query.data, update, context)
        if not success:
            print(f"⚠️ UNKNOWN CALLBACK: {query.data}")
            await query.answer(f"Unknown command: {query.data}", show_alert=True)
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"💥 CALLBACK CRASH:\n{error_trace}")
        await send_ui_response(update, f"⚠️ <b>Engine Error</b>\n{str(e)}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Message Handler for Text commands (Reply Keyboard clicks)."""
    text = update.message.text
    print(f"📡 UI MESSAGE Received: {text}")
    
    # Check if we are waiting for a specific input (e.g., Interview Prep Company)
    if context.user_data.get('awaiting_prep'):
        context.user_data['awaiting_prep'] = False
        await update.message.reply_text(f"🔍 <b>Analyzing {text}...</b> Generating Strategic Dossier.", parse_mode='HTML')

        if ai_brain and hasattr(ai_brain, 'generate_interview_prep'):
            try:
                prep_html = await asyncio.to_thread(ai_brain.generate_interview_prep, text)
                await update.message.reply_text(prep_html, parse_mode='HTML')
            except Exception as e:
                logging.warning(f"Interview prep AI failed, using fallback template: {e}")
                fallback = (
                    f"🧠 <b>Interview Prep (Fallback)</b>\n\n"
                    f"Company: <b>{text}</b>\n\n"
                    "1. Why this company? (mission, growth, values)\n"
                    "2. 3 achievements with numbers\n"
                    "3. HR/Operations case you solved\n"
                    "4. 30-60-90 day plan\n"
                    "5. Salary expectation range + flexibility\n\n"
                    "Tip: Re-run later after enabling AI for full dossier mode."
                )
                await update.message.reply_text(fallback, parse_mode='HTML')
        else:
            fallback = (
                f"🧠 <b>Interview Prep (Fallback)</b>\n\n"
                f"Company: <b>{text}</b>\n\n"
                "1. Why this company? (mission, growth, values)\n"
                "2. 3 achievements with numbers\n"
                "3. HR/Operations case you solved\n"
                "4. 30-60-90 day plan\n"
                "5. Salary expectation range + flexibility\n\n"
                "Tip: Re-run later after enabling AI for full dossier mode."
            )
            await update.message.reply_text(fallback, parse_mode='HTML')
        return

    try:
        success = await process_command(text, update, context)
        if not success:
            await update.message.reply_text(
                "⚠️ Unknown command. Use /help or press /start to open the control panel."
            )
    except Exception as e:
        print(f"💥 MESSAGE HANDLER CRASH:\n{traceback.format_exc()}")
        await update.message.reply_text(f"⚠️ <b>Internal logic error.</b>")

async def handle_telegram_error(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Reduce polling-noise when Telegram sees a duplicate bot instance."""
    if isinstance(context.error, Conflict):
        logging.warning("⚠️ Telegram token conflict: another bot instance is polling. Stop other instance and relaunch.")
        return
    logging.error(f"Telegram runtime error: {context.error}\n{traceback.format_exc()}")

# ==========================================
# 🖥️ CONSOLE MODE (No Telegram needed)
# ==========================================

async def console_scout_and_apply():
    """Console mode: scout and apply without Telegram."""
    global crawler, health_check, company_db, metrics_tracker, company_scraper

    print("\n" + "="*50)
    print("SAM CONSOLE MODE - AUTO SCOUT & APPLY")
    print("="*50 + "\n")

    try:
        # Health check
        if health_check:
            snapshot = health_check.take_snapshot()
            print(f"[HEALTH] {snapshot['overall']}")

        # Run mission cycle manually
        print("[SCOUT] Starting job search...")
        if crawler:
            jobs = await crawler.crawl()
            print(f"[FOUND] {len(jobs)} jobs")

        # Filter and rank
        print("[FILTER] Filtering for qualified leads...")
        leads = []
        for job in jobs:
            # Default to 'global' phase for console mode to accept all valid targets
            if is_valid_target(
                job.get('company_name', ''),
                job.get('location', ''),
                job.get('salary', '0'),
                'global',  # Use global phase for console mode
                job.get('description', '')
            ):
                leads.append(job)

        print(f"[QUALIFIED] {len(leads)} qualified leads")

        # Apply to top leads
        print("[APPLY] Sending applications...")
        applied = 0
        if getattr(config, 'TEST_MODE', False):
            print("[TEST] TEST_MODE enabled - sending one safe test email only.")
            try:
                test_result = smtp_engine.send_test_email(pdf_path=None)
                if test_result:
                    applied += 1
                    print("[TEST] Safe test email sent to sam.dev1@hotmail.com")
                else:
                    print("[TEST] Safe test email failed to send")
            except Exception as e:
                print(f"[ERROR] Test email failed: {e}")
        else:
            for lead in leads[:config.MAX_QUALIFIED_LEADS_PER_CYCLE]:
                try:
                    result = send_strike_with_fallover(lead, None)
                    if result:
                        applied += 1
                    await asyncio.sleep(random.uniform(
                        config.DELAY_BETWEEN_EMAILS_MIN,
                        config.DELAY_BETWEEN_EMAILS_MAX
                    ))
                except Exception as e:
                    print(f"[ERROR] Failed to apply: {e}")

        print(f"\n[DONE] Applied to {applied} companies")

        # Update metrics
        if metrics_tracker:
            metrics_tracker.increment_today('applications_sent', applied)

    except Exception as e:
        print(f"[ERROR] Console mode error: {e}")

def run_console_mode():
    """Run Sam in console mode without Telegram."""
    print("\n" + "="*50)
    print("SAM JOB AUTOMATOR - CONSOLE MODE")
    print("="*50)

    # Initialize components
    global crawler, health_check, company_db, metrics_tracker, company_scraper

    try:
        from system_health import HealthCheck, CompanyDatabase, MetricsTracker
        from global_company_scraper import GlobalCompanyScraper

        health_check = HealthCheck()
        company_db = CompanyDatabase()
        metrics_tracker = MetricsTracker()
        company_scraper = GlobalCompanyScraper()

        print("[OK] Components initialized")
        print("\nCommands:")
        print("  'scout' - Search for jobs")
        print("  'apply' - Apply to found jobs")
        print("  'status' - Show current status")
        print("  'stats' - Show statistics")
        print("  'quit' - Exit")
        print("\nRunning in auto-pilot mode...")

        # Run auto-pilot loop
        while True:
            print("\n[CYCLE] Starting new application cycle...")
            try:
                asyncio.run(console_scout_and_apply())
            except Exception as e:
                print(f"[ERROR] Cycle failed: {e}")

            print("\n[SLEEP] Next cycle in 30 minutes...")
            time.sleep(1800)  # 30 minutes

    except KeyboardInterrupt:
        print("\n[STOP] Bot stopped by user")
    except Exception as e:
        print(f"[ERROR] Console mode failed: {e}")

# ==========================================
# 🚀 MAIN ENTRY POINT
# ==========================================

def main():
    print("[STARTUP] Starting Project Chronos Autonomous Engine...")
    configure_runtime_safety_hooks()

    instance_lock = SingleInstanceLock(os.path.join(os.path.dirname(__file__), '.main_bot.lock'))
    if not instance_lock.acquire():
        print("[WARNING] Another bot instance is already running. Exiting to avoid Telegram conflict.")
        return
    atexit.register(instance_lock.release)
    
    # 🛡️ CONFLICT SHIELD: Local Priority Detection
    is_github = os.environ.get("GITHUB_ACTIONS") == "true"
    if is_github:
        print("[CLOUD] CLOUD NODE DETECTED: Checking for Local Overrides...")
        if database.check_system_flag("LOCAL_SESSION_ACTIVE", "true"):
            print("[BLOCKED] CONFLICT SHIELD: Local session is active. Cloud instance Hibernating.")
            return # Exit to save GitHub minutes and prevent update theft
    else:
        print("[LOCAL] LOCAL NODE DETECTED: Activating Priority Shield.")
        database.set_system_flag("LOCAL_SESSION_ACTIVE", "true")

    # 🧠 LAZY ENGINE LOADING (Prevents blocking the event loop on startup)
    global ai_brain, crawler, health_check, company_db, metrics_tracker, company_scraper
    print("[INIT] Initializing AI Brain & Omni-Crawler...")
    
    # 🛡️ AI Brain with fallback mode
    if getattr(config, 'ZERO_INVESTMENT_MODE', False) or not getattr(config, 'USE_AI_ANALYSIS', False):
        print("[ZERO] ZERO-INVESTMENT MODE: Paid AI disabled, using keyword-based engine")
        ai_brain = None
    else:
        try:
            ai_brain = ai_agent.GeminiAgent(config.GEMINI_API_KEY)
            if hasattr(ai_brain, 'enabled') and ai_brain.enabled:
                print("[OK] AI Brain initialized successfully")
            else:
                print("[WARN] AI Brain disabled, using keyword-based mode")
        except Exception as e:
            print(f"[WARN] AI Brain failed to initialize, using keyword-based fallback: {e}")
            ai_brain = None
    
    # 🌐 Omni-Crawler with AI fallback
    try:
        if getattr(config, 'ZERO_INVESTMENT_MODE', False):
            crawler = None
            print("[ZERO] ZERO-INVESTMENT MODE: Omni-Crawler disabled to avoid paid/blocked paths")
        else:
            crawler = OmniCrawler(ai_agent=ai_brain)
            print("[OK] Omni-Crawler initialized")
    except Exception as e:
        print(f"[WARN] Omni-Crawler failed: {e}")
        crawler = None
    
    # 📡 Initialize Uplink for Telegram communication
    try:
        uplink_instance = None  # Will be set after app is built
        print("[OK] Uplink module loaded")
    except Exception as e:
        print(f"[WARN] Uplink initialization failed: {e}")
    
    # 🏥 HEALTH CHECK & AUTO-REPAIR
    try:
        health_check = HealthCheck()
        health_check.run_full_health_check()
        print(f"[HEALTH] System Health: {health_check.get_status()['system_health']}")
    except Exception as e:
        print(f"[WARN] Health check failed: {e}")
    
    # 📊 COMPANY DATABASE & DEDUPLICATION
    try:
        company_db = CompanyDatabase()
        print(f"[DATABASE] Company database loaded: {company_db.get_statistics()['total_unique_companies']} companies")
    except Exception as e:
        print(f"[WARN] Company database failed: {e}")
    
    # 📈 REAL-TIME METRICS
    try:
        metrics_tracker = MetricsTracker()
        print("[METRICS] Metrics tracker initialized")
    except Exception as e:
        print(f"[WARN] Metrics tracker failed: {e}")
    
    # 🌍 GLOBAL COMPANY SCRAPER
    try:
        company_scraper = GlobalCompanyScraper()
        print("[SCRAPER] Global company scraper initialized")
    except Exception as e:
        print(f"[WARN] Company scraper failed: {e}")

    async def _post_init(application):
        loop = asyncio.get_running_loop()

        def _loop_exception_handler(_loop, context):
            msg = context.get('message', 'Async loop exception')
            err = context.get('exception')
            logging.error(f"Async loop error: {msg} | {err}")

        loop.set_exception_handler(_loop_exception_handler)
        
        # Set up uplink with bot instance
        uplink.set_bot(application.bot)
        print("[OK] Uplink connected to Telegram bot")
        
        # Run initial system health check
        try:
            if health_check:
                health_check.run_full_health_check()
                print(f"[HEALTH] Initial health check: {health_check.get_status()['system_health']}")
        except Exception as e:
            print(f"[WARN] Initial health check failed: {e}")
        
        spawn_background_task(mission_loop(application), "mission_loop")
        spawn_background_task(supervisor_loop(application), "supervisor_loop")

    # Check if Telegram token is properly configured (not placeholder)
    token = config.TELEGRAM_BOT_TOKEN or ""
    if not token or token in ["", "your-telegram-bot-token", "YOUR_BOT_TOKEN"]:
        print("[WARN] Telegram token not configured. Running in CONSOLE MODE...")
        print("[INFO] Bot will still scrape and apply, but without Telegram control.")
        return run_console_mode()

    app = ApplicationBuilder().token(config.TELEGRAM_BOT_TOKEN).post_init(_post_init).build()
    
    # Handlers
    from telegram.ext import TypeHandler
    app.add_handler(TypeHandler(Update, track_update), group=-1) # Group -1 ensures it runs first
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler(["menu", "simple", "easy", "myid", "report", "healthreport", "backup", "restore", "status", "health", "stats", "companies", "targets", "next", "pulse", "runnow", "scout", "stop", "resume", "help", "prep", "diag", "diagnostics"], handle_quick_command))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(handle_telegram_error)
    
    # 🚀 24/7 Mission Loop - always use the built-in asyncio scheduler.
    print("[OK] Using built-in asyncio mission loop (no PTB JobQueue dependency)")
    
    print("[READY] Uplink established. Monitoring for instructions...")
    try:
        app.run_polling(drop_pending_updates=True)
    except KeyboardInterrupt:
        logging.info("Bot interrupted by user")
    finally:
        instance_lock.release()
        if not is_github:
            try:
                print("🏠 Local Node shutting down. Releasing Priority Shield.")
                database.set_system_flag("LOCAL_SESSION_ACTIVE", "false")
            except Exception as e:
                logging.error(f"Error cleaning up session flag: {e}")

if __name__ == '__main__':
    main()
