"""Compatibility utilities used by tests and legacy scripts."""

import re
from datetime import datetime, timezone


def normalize_company_slug(company: str) -> str:
    """Normalize company name to a lowercase alphanumeric slug."""
    if not company:
        return ""
    return re.sub(r"[^a-zA-Z0-9]", "", company).lower()


def build_fallback_email(company: str, prefix: str = "careers") -> str:
    """Build a fallback company email from the normalized slug."""
    slug = normalize_company_slug(company)
    if not slug:
        return ""
    return f"{prefix}@{slug}.com"


def is_recent(dt_str: str, hours: int = 24) -> bool:
    """Return True if timestamp is within the last N hours."""
    if not dt_str:
        return False
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        return (now - dt.astimezone(timezone.utc)).total_seconds() < (hours * 3600)
    except (ValueError, TypeError, AttributeError):
        return False
