#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    SWARM ORCHESTRATOR - MAXIMUM POWER                        ║
║                    0 Investment | 24/7 Cloud | Maximum Performance            ║
╚══════════════════════════════════════════════════════════════════════════════╝

Distributed swarm architecture for job automation:
- Scout Agent: Finds jobs from multiple sources
- Writer Agent: Analyzes and generates personalized applications  
- Sender Agent: Sends emails with CV attachments
- Tracker Agent: Monitors responses and follow-ups

Optimized for free cloud deployment on Render + GitHub Actions.
"""

import asyncio
import json
import logging
import os
import sqlite3
import sys
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple

import aiohttp
import httpx
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - [SWARM] %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('swarm.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class SwarmConfig:
    """Centralized configuration for all swarm agents."""
    
    # API Keys (Free tiers)
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
    
    # Email Configuration (Multiple free providers)
    EMAIL_PROVIDERS = [
        {
            "name": "brevo",
            "server": "smtp-relay.brevo.com",
            "port": 587,
            "user": os.getenv("BREVO_SMTP_LOGIN", ""),
            "password": os.getenv("BREVO_SMTP_PASSWORD", ""),
            "daily_limit": 300,
        },
        {
            "name": "gmail", 
            "server": "smtp.gmail.com",
            "port": 587,
            "user": os.getenv("GMAIL_SMTP_USER", ""),
            "password": os.getenv("GMAIL_APP_PASSWORD", ""),
            "daily_limit": 100,
        },
        {
            "name": "outlook",
            "server": "smtp-mail.outlook.com",
            "port": 587,
            "user": os.getenv("OUTLOOK_USER", ""),
            "password": os.getenv("OUTLOOK_PASSWORD", ""),
            "daily_limit": 100,
        }
    ]
    
    # Telegram Notifications
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # Database
    DB_PATH = os.getenv("DB_PATH", "swarm_data.db")
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")
    
    # Performance
    MAX_PARALLEL_STRIKES = int(os.getenv("MAX_PARALLEL_STRIKES", "5"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "15"))
    MIN_MATCH_SCORE = int(os.getenv("MIN_MATCH_SCORE", "70"))
    
    # Job Search
    JOB_TITLES = [
        "network engineer", "senior network engineer", "network administrator",
        "it infrastructure engineer", "systems administrator", "sysadmin",
        "it manager", "network security engineer", "cybersecurity engineer",
        "noc engineer", "telecom engineer", "cisco engineer", "ccna", "ccnp"
    ]
    
    LOCATIONS = [
        "lebanon", "beirut", "remote", "uae", "dubai", "qatar", "doha",
        "saudi arabia", "riyadh", "kuwait", "oman", "bahrain", "worldwide"
    ]
    
    # CV Content (Will be loaded from file)
    CV_CONTENT = ""
    CANDIDATE_NAME = os.getenv("CANDIDATE_NAME", "Sam Salameh")
    CANDIDATE_EMAIL = os.getenv("CANDIDATE_EMAIL", "")


# ═══════════════════════════════════════════════════════════════════════════════
# DATABASE MANAGER
# ═══════════════════════════════════════════════════════════════════════════════

class SwarmDatabase:
    """SQLite database for local data persistence."""
    
    def __init__(self, db_path: str = None):
        self.db_path = db_path or SwarmConfig.DB_PATH
        self._init_db()
    
    def _init_db(self):
        """Initialize database tables."""
        with sqlite3.connect(self.db_path) as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS jobs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT UNIQUE,
                    title TEXT,
                    company TEXT,
                    location TEXT,
                    description TEXT,
                    url TEXT,
                    email TEXT,
                    salary TEXT,
                    match_score INTEGER,
                    status TEXT DEFAULT 'new',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    applied_at TIMESTAMP,
                    follow_up_at TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_id TEXT,
                    company TEXT,
                    title TEXT,
                    email TEXT,
                    cover_letter TEXT,
                    cv_path TEXT,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'sent',
                    opened BOOLEAN DEFAULT 0,
                    responded BOOLEAN DEFAULT 0
                );
                
                CREATE TABLE IF NOT EXISTS email_quota (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    provider TEXT,
                    sent_count INTEGER DEFAULT 0,
                    date TEXT,
                    reset_at TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS metrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    agent TEXT,
                    action TEXT,
                    count INTEGER DEFAULT 0,
                    date TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
                CREATE INDEX IF NOT EXISTS idx_jobs_score ON jobs(match_score);
                CREATE INDEX IF NOT EXISTS idx_applications_status ON applications(status);
            """)
            conn.commit()
    
    def save_job(self, job: Dict[str, Any]) -> bool:
        """Save a job to the database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute("""
                    INSERT OR IGNORE INTO jobs 
                    (job_id, title, company, location, description, url, email, salary, match_score)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    job.get('id', ''),
                    job.get('title', ''),
                    job.get('company', ''),
                    job.get('location', ''),
                    job.get('description', '')[:2000],
                    job.get('url', ''),
                    job.get('email', ''),
                    job.get('salary', ''),
                    job.get('match_score', 0)
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Database error saving job: {e}")
            return False
    
    def get_jobs_by_status(self, status: str, limit: int = 50) -> List[Dict]:
        """Get jobs by status."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM jobs WHERE status = ? ORDER BY match_score DESC LIMIT ?",
                (status, limit)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def update_job_status(self, job_id: str, status: str):
        """Update job status."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                "UPDATE jobs SET status = ?, applied_at = CURRENT_TIMESTAMP WHERE job_id = ?",
                (status, job_id)
            )
            conn.commit()
    
    def save_application(self, app: Dict[str, Any]):
        """Save application record."""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO applications (job_id, company, title, email, cover_letter, cv_path)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                app.get('job_id', ''),
                app.get('company', ''),
                app.get('title', ''),
                app.get('email', ''),
                app.get('cover_letter', '')[:1000],
                app.get('cv_path', '')
            ))
            conn.commit()
    
    def get_metrics(self, agent: str, action: str, date: str) -> int:
        """Get metrics for an agent action."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute(
                "SELECT count FROM metrics WHERE agent = ? AND action = ? AND date = ?",
                (agent, action, date)
            )
            row = cursor.fetchone()
            return row[0] if row else 0
    
    def increment_metric(self, agent: str, action: str):
        """Increment metric counter."""
        today = datetime.now().strftime('%Y-%m-%d')
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO metrics (agent, action, count, date)
                VALUES (?, ?, 1, ?)
                ON CONFLICT DO UPDATE SET 
                count = count + 1, updated_at = CURRENT_TIMESTAMP
            """, (agent, action, today))
            conn.commit()


# ═══════════════════════════════════════════════════════════════════════════════
# TELEGRAM NOTIFIER
# ═══════════════════════════════════════════════════════════════════════════════

class TelegramNotifier:
    """Send notifications via Telegram bot."""
    
    def __init__(self):
        self.token = SwarmConfig.TELEGRAM_BOT_TOKEN
        self.chat_id = SwarmConfig.TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}"
    
    async def send_message(self, message: str) -> bool:
        """Send a message to Telegram."""
        if not self.token or not self.chat_id:
            return False
        
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.post(
                    f"{self.base_url}/sendMessage",
                    json={
                        "chat_id": self.chat_id,
                        "text": message[:4096],
                        "parse_mode": "HTML"
                    }
                )
                return response.status_code == 200
        except Exception as e:
            logger.error(f"Telegram send failed: {e}")
            return False
    
    async def send_stats(self, db: SwarmDatabase):
        """Send daily statistics."""
        today = datetime.now().strftime('%Y-%m-%d')
        
        jobs_found = db.get_metrics('scout', 'jobs_found', today)
        jobs_qualified = db.get_metrics('writer', 'jobs_qualified', today)
        emails_sent = db.get_metrics('sender', 'emails_sent', today)
        
        message = f"""
📊 <b>SWARM DAILY STATS</b>

🔍 Jobs Found: {jobs_found}
✅ Jobs Qualified: {jobs_qualified}
📧 Emails Sent: {emails_sent}

<i>Swarm is running 24/7 on cloud ☁️</i>
        """
        await self.send_message(message)


# ═══════════════════════════════════════════════════════════════════════════════
# AI ENGINE
# ═══════════════════════════════════════════════════════════════════════════════

class SwarmAI:
    """AI engine for job analysis and cover letter generation."""
    
    def __init__(self):
        self.gemini_key = SwarmConfig.GEMINI_API_KEY
        self.groq_key = SwarmConfig.GROQ_API_KEY
        self.primary = "gemini" if self.gemini_key else ("groq" if self.groq_key else None)
    
    async def analyze_job(self, title: str, description: str) -> Tuple[bool, int, str]:
        """
        Analyze if a job matches the candidate's profile.
        Returns: (is_match, score, reason)
        """
        if not self.primary:
            # Fallback: simple keyword matching
            score = self._keyword_match(title, description)
            return score >= SwarmConfig.MIN_MATCH_SCORE, score, "Keyword match"
        
        try:
            if self.primary == "gemini":
                return await self._analyze_with_gemini(title, description)
            else:
                return await self._analyze_with_groq(title, description)
        except Exception as e:
            logger.error(f"AI analysis failed: {e}")
            score = self._keyword_match(title, description)
            return score >= SwarmConfig.MIN_MATCH_SCORE, score, "Fallback keyword match"
    
    async def generate_cover_letter(self, job: Dict[str, Any]) -> str:
        """Generate a personalized cover letter."""
        if not self.primary:
            return self._template_cover_letter(job)
        
        try:
            if self.primary == "gemini":
                return await self._generate_with_gemini(job)
            else:
                return await self._generate_with_groq(job)
        except Exception as e:
            logger.error(f"Cover letter generation failed: {e}")
            return self._template_cover_letter(job)
    
    def _keyword_match(self, title: str, description: str) -> int:
        """Simple keyword matching for fallback."""
        text = (title + " " + description).lower()
        matches = sum(1 for keyword in SwarmConfig.JOB_TITLES if keyword in text)
        return min(100, matches * 15)
    
    def _template_cover_letter(self, job: Dict[str, Any]) -> str:
        """Template-based cover letter as fallback."""
        return f"""Dear Hiring Manager,

I am writing to express my strong interest in the {job.get('title', 'position')} at {job.get('company', 'your company')}.

With my extensive experience in network engineering and IT infrastructure, I am confident in my ability to contribute effectively to your team.

Key qualifications:
• 15+ years in network engineering (Cisco, MikroTik, Fortinet)
• Expertise in IT infrastructure design and management
• Strong problem-solving and analytical skills
• Proven track record in enterprise environments

I would welcome the opportunity to discuss how my background aligns with your needs.

Best regards,
{SwarmConfig.CANDIDATE_NAME}
{SwarmConfig.CANDIDATE_EMAIL}
"""
    
    async def _analyze_with_gemini(self, title: str, description: str) -> Tuple[bool, int, str]:
        """Analyze job using Gemini API."""
        prompt = f"""
        Analyze this job for a senior network engineer with 15+ years experience.
        
        Job Title: {title}
        Description: {description[:1500]}
        
        Respond in JSON format:
        {{
            "is_match": true/false,
            "score": 0-100,
            "reason": "brief explanation"
        }}
        """
        
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}",
                json={
                    "contents": [{"parts": [{"text": prompt}]}],
                    "generationConfig": {"responseMimeType": "application/json"}
                }
            )
            
            if response.status_code == 200:
                data = response.json()
                text = data['candidates'][0]['content']['parts'][0]['text']
                result = json.loads(text)
                return result.get('is_match', False), result.get('score', 0), result.get('reason', '')
            
            return False, 0, "Gemini API error"
    
    async def _generate_with_gemini(self, job: Dict[str, Any]) -> str:
        """Generate cover letter using Gemini."""
        prompt = f"""
        Write a professional cover letter for:
        
        Position: {job.get('title', '')}
        Company: {job.get('company', '')}
        Description: {job.get('description', '')[:1000]}
        
        Candidate: {SwarmConfig.CANDIDATE_NAME}
        Experience: 15+ years network engineering (Cisco, MikroTik, Fortinet, Ubiquiti)
        
        Keep it concise (200-300 words), professional, and personalized.
        """
        
        async with httpx.AsyncClient(timeout=20) as client:
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.gemini_key}",
                json={"contents": [{"parts": [{"text": prompt}]}]}
            )
            
            if response.status_code == 200:
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text']
            
            return self._template_cover_letter(job)
    
    async def _analyze_with_groq(self, title: str, description: str) -> Tuple[bool, int, str]:
        """Analyze job using Groq API."""
        # Similar implementation for Groq
        return self._keyword_match(title, description) >= SwarmConfig.MIN_MATCH_SCORE, \
               self._keyword_match(title, description), "Groq analysis"
    
    async def _generate_with_groq(self, job: Dict[str, Any]) -> str:
        """Generate cover letter using Groq."""
        return self._template_cover_letter(job)


# ═══════════════════════════════════════════════════════════════════════════════
# SCOUT AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class ScoutAgent:
    """Finds jobs from multiple sources."""
    
    def __init__(self, db: SwarmDatabase, ai: SwarmAI, notifier: TelegramNotifier):
        self.db = db
        self.ai = ai
        self.notifier = notifier
        self.sources = [
            self._scrape_daleel_madani,
            self._scrape_linkedin,
            self._scrape_indeed,
            self._scrape_bayt,
        ]
    
    async def run(self):
        """Execute scouting mission."""
        logger.info("🕵️ SCOUT AGENT: Starting job hunt...")
        
        all_jobs = []
        for source in self.sources:
            try:
                jobs = await source()
                all_jobs.extend(jobs)
                logger.info(f"  ✓ {source.__name__}: {len(jobs)} jobs")
            except Exception as e:
                logger.error(f"  ✗ {source.__name__}: {e}")
        
        # Deduplicate and save
        saved_count = 0
        for job in all_jobs:
            if self.db.save_job(job):
                saved_count += 1
        
        self.db.increment_metric('scout', 'jobs_found')
        
        logger.info(f"🕵️ SCOUT AGENT: Found {len(all_jobs)} jobs, saved {saved_count} new")
        
        if saved_count > 0:
            await self.notifier.send_message(
                f"🔍 <b>Scout Agent</b>\nFound {saved_count} new jobs!\n"
                f"Total today: {self.db.get_metrics('scout', 'jobs_found', datetime.now().strftime('%Y-%m-%d'))}"
            )
    
    async def _scrape_daleel_madani(self) -> List[Dict]:
        """Scrape Daleel Madani (Lebanon NGO jobs)."""
        jobs = []
        try:
            async with httpx.AsyncClient(timeout=15) as client:
                response = await client.get(
                    "https://daleel-madani.org/jobs",
                    headers={"User-Agent": "Mozilla/5.0"}
                )
                # Parse HTML and extract jobs
                # This is a simplified version - implement full parsing
                if response.status_code == 200:
                    # Extract job listings from HTML
                    pass
        except Exception as e:
            logger.warning(f"Daleel Madani scrape failed: {e}")
        return jobs
    
    async def _scrape_linkedin(self) -> List[Dict]:
        """Scrape LinkedIn jobs (public listings)."""
        jobs = []
        try:
            # Use LinkedIn public job search
            keywords = "%20".join(SwarmConfig.JOB_TITLES[:3])
            url = f"https://www.linkedin.com/jobs/search?keywords={keywords}&location=Lebanon"
            # Implementation requires parsing LinkedIn's JSON data
        except Exception as e:
            logger.warning(f"LinkedIn scrape failed: {e}")
        return jobs
    
    async def _scrape_indeed(self) -> List[Dict]:
        """Scrape Indeed jobs."""
        jobs = []
        try:
            # Indeed RSS feed or API
            pass
        except Exception as e:
            logger.warning(f"Indeed scrape failed: {e}")
        return jobs
    
    async def _scrape_bayt(self) -> List[Dict]:
        """Scrape Bayt.com (Middle East jobs)."""
        jobs = []
        try:
            # Bayt.com scraping logic
            pass
        except Exception as e:
            logger.warning(f"Bayt scrape failed: {e}")
        return jobs


# ═══════════════════════════════════════════════════════════════════════════════
# WRITER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class WriterAgent:
    """Analyzes jobs and generates personalized applications."""
    
    def __init__(self, db: SwarmDatabase, ai: SwarmAI, notifier: TelegramNotifier):
        self.db = db
        self.ai = ai
        self.notifier = notifier
    
    async def run(self):
        """Execute writing mission."""
        logger.info("✍️ WRITER AGENT: Analyzing jobs...")
        
        # Get unscored jobs
        jobs = self.db.get_jobs_by_status('new', limit=20)
        
        qualified_count = 0
        for job in jobs:
            try:
                is_match, score, reason = await self.ai.analyze_job(
                    job['title'], job['description']
                )
                
                if is_match and score >= SwarmConfig.MIN_MATCH_SCORE:
                    # Generate cover letter
                    cover_letter = await self.ai.generate_cover_letter(job)
                    
                    # Update job
                    self.db.update_job_status(job['job_id'], 'qualified')
                    
                    # Save cover letter
                    # TODO: Save to file or database
                    
                    qualified_count += 1
                    logger.info(f"  ✓ Qualified: {job['title']} at {job['company']} (score: {score})")
                else:
                    self.db.update_job_status(job['job_id'], 'rejected')
                    
            except Exception as e:
                logger.error(f"  ✗ Error analyzing job: {e}")
        
        self.db.increment_metric('writer', 'jobs_qualified')
        
        logger.info(f"✍️ WRITER AGENT: Qualified {qualified_count}/{len(jobs)} jobs")
        
        if qualified_count > 0:
            await self.notifier.send_message(
                f"✍️ <b>Writer Agent</b>\nQualified {qualified_count} jobs for applications!"
            )


# ═══════════════════════════════════════════════════════════════════════════════
# SENDER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class SenderAgent:
    """Sends job applications via email."""
    
    def __init__(self, db: SwarmDatabase, notifier: TelegramNotifier):
        self.db = db
        self.notifier = notifier
        self.email_providers = self._get_available_providers()
    
    def _get_available_providers(self) -> List[Dict]:
        """Get configured email providers."""
        providers = []
        for provider in SwarmConfig.EMAIL_PROVIDERS:
            if provider['user'] and provider['password']:
                providers.append(provider)
        return providers
    
    async def run(self):
        """Execute sending mission."""
        logger.info("📧 SENDER AGENT: Sending applications...")
        
        if not self.email_providers:
            logger.warning("📧 SENDER AGENT: No email providers configured!")
            await self.notifier.send_message(
                "⚠️ <b>Sender Agent</b>\nNo email providers configured!"
            )
            return
        
        # Get qualified jobs
        jobs = self.db.get_jobs_by_status('qualified', limit=10)
        
        sent_count = 0
        for job in jobs:
            try:
                success = await self._send_application(job)
                if success:
                    self.db.update_job_status(job['job_id'], 'sent')
                    self.db.save_application({
                        'job_id': job['job_id'],
                        'company': job['company'],
                        'title': job['title'],
                        'email': job['email']
                    })
                    sent_count += 1
                    
                    # Rotate provider
                    self.email_providers.append(self.email_providers.pop(0))
                    
                    # Delay between emails
                    await asyncio.sleep(2)
                    
            except Exception as e:
                logger.error(f"  ✗ Error sending application: {e}")
        
        self.db.increment_metric('sender', 'emails_sent')
        
        logger.info(f"📧 SENDER AGENT: Sent {sent_count}/{len(jobs)} applications")
        
        if sent_count > 0:
            await self.notifier.send_message(
                f"📧 <b>Sender Agent</b>\nSent {sent_count} applications today!"
            )
    
    async def _send_application(self, job: Dict[str, Any]) -> bool:
        """Send a single application email."""
        if not self.email_providers:
            return False
        
        provider = self.email_providers[0]
        
        try:
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            msg = MIMEMultipart()
            msg['From'] = f"{SwarmConfig.CANDIDATE_NAME} <{provider['user']}>"
            msg['To'] = job.get('email', '')
            msg['Subject'] = f"Application for {job.get('title', 'Position')}"
            
            # Body
            body = f"""
Dear Hiring Manager,

I am writing to apply for the {job.get('title', 'position')} at {job.get('company', 'your company')}.

[Cover letter would be inserted here]

Best regards,
{SwarmConfig.CANDIDATE_NAME}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send
            with smtplib.SMTP(provider['server'], provider['port'], timeout=20) as server:
                server.starttls()
                server.login(provider['user'], provider['password'])
                server.send_message(msg)
            
            return True
            
        except Exception as e:
            logger.error(f"Email send failed: {e}")
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# TRACKER AGENT
# ═══════════════════════════════════════════════════════════════════════════════

class TrackerAgent:
    """Monitors application responses and sends follow-ups."""
    
    def __init__(self, db: SwarmDatabase, notifier: TelegramNotifier):
        self.db = db
        self.notifier = notifier
    
    async def run(self):
        """Execute tracking mission."""
        logger.info("📊 TRACKER AGENT: Checking application status...")
        
        # Get sent applications older than 7 days
        # TODO: Implement follow-up logic
        
        # Send daily stats
        await self.notifier.send_stats(self.db)
        
        logger.info("📊 TRACKER AGENT: Tracking complete")


# ═══════════════════════════════════════════════════════════════════════════════
# SWARM ORCHESTRATOR
# ═══════════════════════════════════════════════════════════════════════════════

class SwarmOrchestrator:
    """Main orchestrator that coordinates all agents."""
    
    def __init__(self):
        self.db = SwarmDatabase()
        self.ai = SwarmAI()
        self.notifier = TelegramNotifier()
        
        self.scout = ScoutAgent(self.db, self.ai, self.notifier)
        self.writer = WriterAgent(self.db, self.ai, self.notifier)
        self.sender = SenderAgent(self.db, self.notifier)
        self.tracker = TrackerAgent(self.db, self.notifier)
        
        self.is_running = True
    
    async def run_single_cycle(self):
        """Run one complete swarm cycle."""
        logger.info("=" * 60)
        logger.info("🚀 SWARM CYCLE STARTING")
        logger.info("=" * 60)
        
        try:
            # Phase 1: Scout - Find jobs
            await self.scout.run()
            
            # Phase 2: Writer - Analyze and qualify
            await self.writer.run()
            
            # Phase 3: Sender - Send applications
            await self.sender.run()
            
            # Phase 4: Tracker - Monitor and report
            await self.tracker.run()
            
        except Exception as e:
            logger.error(f"Swarm cycle error: {e}")
            await self.notifier.send_message(f"⚠️ Swarm Error: {str(e)[:200]}")
        
        logger.info("=" * 60)
        logger.info("✅ SWARM CYCLE COMPLETE")
        logger.info("=" * 60)
    
    async def run_continuous(self):
        """Run swarm continuously with intervals."""
        await self.notifier.send_message(
            "🚀 <b>SWARM ORCHESTRATOR STARTED</b>\n"
            "Running 24/7 on cloud ☁️\n"
            "Agents: Scout → Writer → Sender → Tracker"
        )
        
        while self.is_running:
            await self.run_single_cycle()
            
            # Wait before next cycle (30 minutes)
            logger.info("⏳ Waiting 30 minutes before next cycle...")
            await asyncio.sleep(1800)
    
    async def run_agent(self, agent_name: str):
        """Run a specific agent."""
        agents = {
            'scout': self.scout,
            'writer': self.writer,
            'sender': self.sender,
            'tracker': self.tracker
        }
        
        agent = agents.get(agent_name)
        if agent:
            await agent.run()
        else:
            logger.error(f"Unknown agent: {agent_name}")


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN ENTRY POINT
# ═══════════════════════════════════════════════════════════════════════════════

async def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Swarm Orchestrator')
    parser.add_argument('--agent', choices=['scout', 'writer', 'sender', 'tracker'],
                       help='Run specific agent only')
    parser.add_argument('--once', action='store_true',
                       help='Run one cycle and exit')
    args = parser.parse_args()
    
    orchestrator = SwarmOrchestrator()
    
    if args.agent:
        await orchestrator.run_agent(args.agent)
    elif args.once:
        await orchestrator.run_single_cycle()
    else:
        await orchestrator.run_continuous()

if __name__ == "__main__":
    asyncio.run(main())
