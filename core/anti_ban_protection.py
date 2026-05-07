"""
🛡️ ANTI-BAN PROTECTION SYSTEM
Makes the bot look like a real human to avoid detection and bans
"""

import logging
import random
import asyncio
import re
from datetime import datetime, timedelta
from typing import Dict, List, Set
import hashlib

class AntiBanProtection:
    """
    🛡️ ANTI-BAN PROTECTION
    Protects the bot from being detected and banned by companies
    
    Features:
    - Human-like timing patterns
    - Rate limiting per company
    - Suspicious company detection
    - Honeypot detection
    - Application spacing
    - Domain reputation tracking
    """
    
    def __init__(self):
        # Track applications per company
        self.company_applications: Dict[str, List[datetime]] = {}
        
        # Blacklist of suspicious/honeypot companies
        self.suspicious_companies: Set[str] = set()
        
        # Track failed applications
        self.failed_applications: Dict[str, int] = {}
        
        # Honeypot indicators — use exact word patterns (checked with \b boundaries)
        self.honeypot_keywords = {
            'test', 'fake', 'honeypot', 'trap', 'automated',
            'spam', 'scam', 'phishing', 'verification', 'validate',
            'check', 'monitor', 'detect', 'crawler', 'scraper'
        }
        # Keywords that must match as whole words only (not substrings)
        self.honeypot_whole_word_keywords = {
            'bot',  # "bot" alone, not "bothell", "robot", etc.
        }
        
        # Suspicious patterns
        self.suspicious_patterns = {
            'too_good': ['$500k', '$1M', 'million dollar', 'instant hire', 'no experience needed'],
            'vague': ['various positions', 'multiple roles', 'any position', 'flexible role'],
            'urgent': ['urgent', 'immediate', 'asap', 'right now', 'today only'],
            'suspicious_email': ['noreply', 'no-reply', 'donotreply', 'test@', 'admin@']
        }
        
        # Rate limits (applications per company per time period)
        self.max_apps_per_company_per_day = 1  # Only 1 application per company per day
        self.max_apps_per_company_per_week = 2  # Max 2 per week (if they repost)
        self.max_apps_per_company_total = 5  # Max 5 total (if they keep reposting)
        
        # Timing constraints (look human)
        self.min_time_between_apps = 2    # 2 seconds minimum between applications (was 30 - too slow for parallel)
        self.max_apps_per_hour = 200      # 200 applications per hour
        self.max_apps_per_day = 5000      # 5000 per day (scaled up)
        
        # Last application time (global)
        self.last_application_time = None
        
        # Daily counter
        self.daily_applications = 0
        self.daily_reset_time = datetime.now()
    
    def _normalize_company_name(self, company_name: str) -> str:
        """Normalize company name for tracking"""
        return company_name.lower().strip().replace(' ', '_')
    
    def _is_honeypot(self, company_name: str, job_title: str, description: str, email: str) -> bool:
        """
        🛡️ HONEYPOT DETECTION
        Detects fake job postings designed to catch bots
        """
        company_lower = company_name.lower()
        title_lower = job_title.lower()
        desc_lower = description.lower() if description else ""
        email_lower = email.lower() if email else ""
        
        # Check for honeypot keywords
        for keyword in self.honeypot_keywords:
            if keyword in company_lower or keyword in title_lower:
                logging.warning(f"🚨 HONEYPOT DETECTED: Keyword '{keyword}' in {company_name}")
                return True

        # Check whole-word-only keywords (e.g. "bot" should not match "bothell")
        for keyword in self.honeypot_whole_word_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            if re.search(pattern, company_lower) or re.search(pattern, title_lower):
                logging.warning(f"🚨 HONEYPOT DETECTED: Keyword '{keyword}' in {company_name}")
                return True
        
        # Check for suspicious patterns
        for pattern_type, patterns in self.suspicious_patterns.items():
            for pattern in patterns:
                if pattern in desc_lower or pattern in title_lower:
                    logging.warning(f"🚨 SUSPICIOUS PATTERN: {pattern_type} - '{pattern}' in {company_name}")
                    # Don't immediately reject, but flag as suspicious
                    self.suspicious_companies.add(self._normalize_company_name(company_name))
        
        # Check for suspicious email
        for pattern in self.suspicious_patterns['suspicious_email']:
            if pattern in email_lower:
                logging.warning(f"🚨 SUSPICIOUS EMAIL: {email} for {company_name}")
                return True
        
        # Check if company name is too generic
        generic_names = ['company', 'corporation', 'inc', 'llc', 'test', 'example', 'sample']
        if any(name in company_lower for name in generic_names) and len(company_name) < 15:
            logging.warning(f"🚨 GENERIC COMPANY NAME: {company_name}")
            return True
        
        return False
    
    def _check_rate_limit(self, company_name: str) -> tuple[bool, str]:
        """
        🛡️ RATE LIMIT CHECK
        Ensures we don't apply too many times to the same company
        """
        normalized_name = self._normalize_company_name(company_name)
        now = datetime.now()
        
        # Initialize if first time
        if normalized_name not in self.company_applications:
            self.company_applications[normalized_name] = []
        
        # Get application history
        app_history = self.company_applications[normalized_name]
        
        # Remove old applications (older than 7 days)
        app_history = [app_time for app_time in app_history if now - app_time < timedelta(days=7)]
        self.company_applications[normalized_name] = app_history
        
        # Check total applications
        if len(app_history) >= self.max_apps_per_company_total:
            return False, f"Already applied {len(app_history)} times to {company_name} (max: {self.max_apps_per_company_total})"
        
        # Check applications in last 24 hours
        recent_apps = [app_time for app_time in app_history if now - app_time < timedelta(hours=24)]
        if len(recent_apps) >= self.max_apps_per_company_per_day:
            return False, f"Already applied to {company_name} today (max: {self.max_apps_per_company_per_day}/day)"
        
        # Check applications in last 7 days
        weekly_apps = [app_time for app_time in app_history if now - app_time < timedelta(days=7)]
        if len(weekly_apps) >= self.max_apps_per_company_per_week:
            return False, f"Already applied {len(weekly_apps)} times to {company_name} this week (max: {self.max_apps_per_company_per_week}/week)"
        
        return True, "OK"
    
    def _check_global_rate_limit(self) -> tuple[bool, str]:
        """
        🛡️ GLOBAL RATE LIMIT
        Ensures we don't send too many applications too quickly (look human)
        """
        now = datetime.now()
        
        # Reset daily counter if new day
        if now.date() > self.daily_reset_time.date():
            self.daily_applications = 0
            self.daily_reset_time = now
        
        # Check daily limit
        if self.daily_applications >= self.max_apps_per_day:
            return False, f"Daily limit reached ({self.max_apps_per_day} applications/day)"
        
        # Check time between applications
        if self.last_application_time:
            time_since_last = (now - self.last_application_time).total_seconds()
            if time_since_last < self.min_time_between_apps:
                wait_time = self.min_time_between_apps - time_since_last
                return False, f"Too fast! Wait {wait_time:.0f} seconds (human speed: {self.min_time_between_apps}s between apps)"
        
        return True, "OK"
    
    async def can_apply(self, company_name: str, job_title: str, description: str, email: str) -> tuple[bool, str]:
        """
        🛡️ MAIN PROTECTION CHECK
        Returns (can_apply, reason)
        """
        # 1. Check for honeypot
        if self._is_honeypot(company_name, job_title, description, email):
            return False, "🚨 HONEYPOT DETECTED - Skipping to protect bot"
        
        # 2. Check company rate limit
        can_apply_company, reason_company = self._check_rate_limit(company_name)
        if not can_apply_company:
            return False, f"🛡️ RATE LIMIT: {reason_company}"
        
        # 3. Check global rate limit
        can_apply_global, reason_global = self._check_global_rate_limit()
        if not can_apply_global:
            return False, f"🛡️ GLOBAL LIMIT: {reason_global}"
        
        # 4. Check if company is flagged as suspicious
        normalized_name = self._normalize_company_name(company_name)
        if normalized_name in self.suspicious_companies:
            # Allow but with extra caution
            logging.warning(f"⚠️ SUSPICIOUS COMPANY: {company_name} - Proceeding with caution")
        
        return True, "✅ Safe to apply"
    
    def record_application(self, company_name: str, success: bool):
        """
        📝 RECORD APPLICATION
        Track application for rate limiting
        """
        normalized_name = self._normalize_company_name(company_name)
        now = datetime.now()
        
        # Record application time
        if normalized_name not in self.company_applications:
            self.company_applications[normalized_name] = []
        self.company_applications[normalized_name].append(now)
        
        # Update global tracking
        self.last_application_time = now
        self.daily_applications += 1
        
        # Track failures
        if not success:
            if normalized_name not in self.failed_applications:
                self.failed_applications[normalized_name] = 0
            self.failed_applications[normalized_name] += 1
            
            # If too many failures, mark as suspicious
            if self.failed_applications[normalized_name] >= 3:
                logging.warning(f"🚨 MARKING AS SUSPICIOUS: {company_name} (3+ failures)")
                self.suspicious_companies.add(normalized_name)
        
        logging.info(f"📝 Recorded application to {company_name} (success: {success})")
        logging.info(f"📊 Stats: {self.daily_applications}/{self.max_apps_per_day} today, {len(self.company_applications[normalized_name])} to this company")
    
    async def get_human_delay(self) -> int:
        """
        ⏱️ HUMAN-LIKE DELAY
        Returns a random delay that looks human
        """
        # Base delay: 5-10 minutes between applications
        base_delay = random.randint(300, 600)
        
        # Add randomness to look more human
        # Sometimes humans take breaks
        if random.random() < 0.1:  # 10% chance of longer break
            base_delay += random.randint(600, 1800)  # 10-30 min break
            logging.info("☕ Taking a human-like break (10-30 minutes)")
        
        # Add small random jitter
        jitter = random.randint(-30, 30)
        
        return base_delay + jitter
    
    def get_protection_stats(self) -> Dict:
        """
        📊 GET PROTECTION STATS
        Returns statistics about protection system
        """
        return {
            'daily_applications': self.daily_applications,
            'max_daily': self.max_apps_per_day,
            'suspicious_companies': len(self.suspicious_companies),
            'tracked_companies': len(self.company_applications),
            'failed_applications': sum(self.failed_applications.values()),
            'last_application': self.last_application_time.isoformat() if self.last_application_time else None
        }
    
    def is_safe_to_continue(self) -> bool:
        """
        🛡️ SAFETY CHECK
        Returns True if it's safe to continue applying
        """
        # Check if we've hit daily limit
        if self.daily_applications >= self.max_apps_per_day:
            logging.warning(f"🛑 Daily limit reached: {self.daily_applications}/{self.max_apps_per_day}")
            return False
        
        # Check if too many suspicious companies
        if len(self.suspicious_companies) > 10:
            logging.warning(f"🚨 Too many suspicious companies detected: {len(self.suspicious_companies)}")
            # Don't stop, but be cautious
        
        return True

# Global instance
_protection_instance = None

def get_protection() -> AntiBanProtection:
    """Get the global protection instance"""
    global _protection_instance
    if _protection_instance is None:
        _protection_instance = AntiBanProtection()
    return _protection_instance
