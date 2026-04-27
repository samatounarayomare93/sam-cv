"""
SAM JOB AUTOMATOR - CORE UTILITIES
=================================
Shared utilities across all modules
"""

import re
import hashlib
from typing import Any, Optional
from datetime import datetime, timedelta, timezone


# ============================================================================
# EMAIL VALIDATION
# ============================================================================

EMAIL_PATTERN = re.compile(r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$')


def is_valid_email(email: str) -> bool:
    """
    Validate email format
    Returns True if email is valid, False otherwise
    """
    if not email:
        return False
    return bool(EMAIL_PATTERN.match(email.strip()))


def is_valid_email_advanced(email: str) -> bool:
    """
    Advanced email validation with domain check
    """
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
    # Basic pattern check
    if not EMAIL_PATTERN.match(email):
        return False
    
    # Extract domain
    domain = email.split('@')[1] if '@' in email else ''
    
    # Check for common invalid domains
    invalid_domains = [
        'example.com', 'test.com', 'sample.com', 'localhost',
        'domain.com', 'mail.com', 'email.com'
    ]
    if any(inv in domain.lower() for inv in invalid_domains):
        return False
    
    return True


# ============================================================================
# COMPANY NAME UTILITIES
# ============================================================================

def normalize_company_slug(company: str) -> str:
    """
    Normalize company name to URL-safe slug
    Removes all non-alphanumeric characters and converts to lowercase
    """
    if not company:
        return ''
    return re.sub(r'[^a-zA-Z0-9]', '', company).lower()


def build_fallback_email(company: str, prefix: str = 'careers') -> str:
    """
    Build fallback email for a company based on company name
    Example: 'Google Inc' -> 'careers@google.com'
    """
    slug = normalize_company_slug(company)
    if not slug:
        return ''
    
    # Common TLDs to try
    tlds = ['.com', '.org', '.net', '.co', '.io']
    
    for tld in tlds:
        candidate = f'{prefix}@{slug}{tld}'
        if is_valid_email(candidate):
            return candidate
    
    # Default to .com
    return f'{prefix}@{slug}.com'


def guess_company_domain(company: str) -> Optional[str]:
    """
    Guess company domain from company name
    """
    slug = normalize_company_slug(company)
    if not slug:
        return None
    
    # Common patterns
    domains = [
        f'{slug}.com',
        f'{slug}.org',
        f'{slug}.net',
        f'www.{slug}.com',
        f'{slug}inc.com',
        f'{slug}group.com',
        f'{slug}corporation.com',
    ]
    
    for domain in domains:
        if is_valid_email(f'test@{domain}'):
            return domain
    
    return f'{slug}.com'


# ============================================================================
# TEXT UTILITIES
# ============================================================================

def clean_html(html: str) -> str:
    """Remove HTML tags from text"""
    if not html:
        return ''
    return re.sub(r'<[^>]+>', '', html)


def truncate_text(text: str, max_length: int = 100, suffix: str = '...') -> str:
    """Truncate text to max length"""
    if not text:
        return ''
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace in text"""
    if not text:
        return ''
    return ' '.join(text.split())


# ============================================================================
# DATE/TIME UTILITIES
# ============================================================================

def format_timestamp(dt: datetime = None) -> str:
    """Format datetime as ISO string"""
    if dt is None:
        dt = datetime.now()
    return dt.strftime('%Y-%m-%d %H:%M:%S')


def is_recent(dt_str: str, hours: int = 24) -> bool:
    """Check if datetime string is within the last N hours"""
    if not dt_str:
        return False
    
    try:
        dt = datetime.fromisoformat(dt_str.replace('Z', '+00:00'))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        delta = now - dt.astimezone(timezone.utc)
        return delta.total_seconds() < (hours * 3600)
    except (ValueError, AttributeError, TypeError):
        return False


def get_date_range(days: int = 30) -> tuple:
    """Get date range tuple (start_date, end_date)"""
    end = datetime.now()
    start = end - timedelta(days=days)
    return start, end


# ============================================================================
# BREVO STATS UTILITIES
# ============================================================================

def compute_brevo_open_rate(payload: Any) -> float:
    """
    Compute email open rate from Brevo API response
    Handles both dict and list response formats
    """
    delivered = 0
    unique_opens = 0
    
    if isinstance(payload, dict):
        delivered = payload.get('delivered', 0) or 0
        unique_opens = payload.get('uniqueOpens', 0) or 0
    elif isinstance(payload, list):
        delivered = sum(x.get('delivered', 0) for x in payload if isinstance(x, dict))
        unique_opens = sum(x.get('uniqueOpens', 0) for x in payload if isinstance(x, dict))
    
    try:
        delivered = float(delivered)
        unique_opens = float(unique_opens)
    except (TypeError, ValueError):
        return 0.0
    
    if delivered <= 0:
        return 0.0
    
    return round((unique_opens / delivered) * 100, 1)


# ============================================================================
# COMMAND PARSING UTILITIES
# ============================================================================

def parse_prep_company(prompt: str) -> str:
    """
    Parse company name from PREP command
    Example: 'PREP Google' -> 'Google'
    """
    text = (prompt or '').strip()
    if not text.upper().startswith('PREP'):
        return ''
    return text[4:].strip(': ').strip()


def parse_command_args(text: str) -> tuple:
    """
    Parse command and arguments from text
    Example: '/start arg1 arg2' -> ('/start', ['arg1', 'arg2'])
    """
    if not text:
        return '', []
    
    parts = text.strip().split(None, 1)
    command = parts[0] if parts else ''
    args = parts[1].split() if len(parts) > 1 else []
    
    return command, args


# ============================================================================
# HASHING & SECURITY
# ============================================================================

def hash_email(email: str) -> str:
    """Create hash of email for privacy-safe storage"""
    if not email:
        return ''
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()[:16]


def mask_sensitive(text: str, visible_chars: int = 4) -> str:
    """Mask sensitive information showing only last N characters"""
    if not text or len(text) <= visible_chars:
        return '*' * len(text) if text else ''
    return '*' * (len(text) - visible_chars) + text[-visible_chars:]


# ============================================================================
# JOB TITLE UTILITIES
# ============================================================================

def is_relevant_title(title: str, keywords: list) -> bool:
    """Check if job title contains any relevant keywords"""
    if not title or not keywords:
        return False
    
    title_lower = title.lower()
    
    for keyword in keywords:
        if keyword.lower() in title_lower:
            return True
    
    return False


def is_banned_title(title: str, banned_keywords: list) -> bool:
    """Check if job title contains any banned keywords"""
    if not title or not banned_keywords:
        return False
    
    title_lower = title.lower()
    
    for keyword in banned_keywords:
        if keyword.lower() in title_lower:
            return True
    
    return False


# ============================================================================
# LOCATION UTILITIES
# ============================================================================

def is_valid_location(location: str, target_countries: list = None, 
                      excluded_locations: list = None) -> bool:
    """
    Check if location is valid for targeting
    """
    if not location:
        return False
    
    location_lower = location.lower()
    
    # Check excluded locations
    if excluded_locations:
        for excl in excluded_locations:
            if excl.lower() in location_lower:
                return False
    
    # Check target countries
    if target_countries:
        for country in target_countries:
            if country.lower() in location_lower:
                return True
        return False
    
    return True


# ============================================================================
# EXPORTED API
# ============================================================================

__all__ = [
    # Email
    'is_valid_email',
    'is_valid_email_advanced',
    'build_fallback_email',
    'guess_company_domain',
    
    # Company
    'normalize_company_slug',
    
    # Text
    'clean_html',
    'truncate_text',
    'normalize_whitespace',
    
    # Date/Time
    'format_timestamp',
    'is_recent',
    'get_date_range',
    
    # Brevo
    'compute_brevo_open_rate',
    
    # Commands
    'parse_prep_company',
    'parse_command_args',
    
    # Security
    'hash_email',
    'mask_sensitive',
    
    # Job
    'is_relevant_title',
    'is_banned_title',
    
    # Location
    'is_valid_location',
]
