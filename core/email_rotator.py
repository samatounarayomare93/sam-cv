"""
🚀 SCALED EMAIL ROTATION SYSTEM
Target: 10,000+ emails/day (100% FREE)
Providers: Resend x3 + Brevo + Zoho + Gmail
"""

import logging
import os
import time
from datetime import datetime
from typing import Dict, List, Optional
import json
from pathlib import Path

# ============================================================
# DAILY LIMITS PER PROVIDER (FREE TIER)
# ============================================================
PROVIDER_LIMITS = {
    "resend_1":  100,   # Resend #1 (3000/month free)
    "resend_2":  100,   # Resend #2
    "resend_3":  100,   # Resend #3
    "resend":    100,   # Resend alias (used by smtp_engine record_email_sent)
    "brevo":     300,   # Brevo free (300/day)
    "mailjet":   200,   # Mailjet free (6000/month)
    "sendpulse": 400,   # SendPulse free (12000/month)
    "zoho_1":    500,   # Zoho #1 (500/day)
    "zoho_2":    500,   # Zoho #2 (500/day)
    "zoho_3":    500,   # Zoho #3 (500/day)
    "gmail":     500,   # Gmail (500/day)
    "yahoo":     500,   # Yahoo (500/day)
    "outlook":   300,   # Outlook (300/day)
}
# TOTAL with all configured providers: ~2200/day
# brevo(300) + zoho_1(500) + zoho_2(500) + outlook(300) + gmail(500) + resend(100) = 2200

USAGE_FILE = Path("cache/email_usage.json")

def _ensure_cache_dir():
    """Create cache dir safely — works on both local and Render."""
    try:
        # On Render, /tmp is writable; local 'cache/' is fine too
        cache_dir = Path("/tmp/cache") if os.getenv("RENDER") else Path("cache")
        cache_dir.mkdir(parents=True, exist_ok=True)
        return cache_dir / "email_usage.json"
    except Exception:
        return Path("/tmp/email_usage.json")


class EmailRotator:
    def __init__(self):
        self.usage_file = _ensure_cache_dir()
        self.usage = self._load_usage()
        self.providers = self._get_available_providers()
        self._cleanup_old_usage()

    def _load_usage(self) -> Dict:
        try:
            if self.usage_file.exists():
                with open(self.usage_file, 'r') as f:
                    data = json.load(f)
                if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                    return data.get("usage", {})
            return {}
        except Exception:
            return {}

    def _save_usage(self):
        try:
            data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "usage": self.usage,
                "last_updated": datetime.now().isoformat()
            }
            with open(self.usage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception:
            pass

    def _cleanup_old_usage(self):
        today = datetime.now().strftime("%Y-%m-%d")
        for provider in list(self.usage.keys()):
            if self.usage[provider].get("date") != today:
                self.usage[provider] = {"count": 0, "date": today}
        self._save_usage()

    def _get_available_providers(self) -> List[Dict]:
        providers = []
        is_render = bool(os.getenv("RENDER") or os.getenv("RENDER_SERVICE_ID") or
                         os.getenv("RENDER_EXTERNAL_URL"))

        # ── Resend: only useful with verified custom domain ──────────────────
        resend_from = os.getenv("RESEND_FROM_EMAIL", "")
        _free_domains = {'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'live.com', 'icloud.com'}
        _resend_domain = resend_from.split('@')[-1].lower() if '@' in resend_from else ''
        _resend_has_domain = resend_from and _resend_domain not in _free_domains

        if os.getenv("RESEND_API_KEY") and _resend_has_domain:
            providers.append({"name": "resend_1", "display_name": "Resend #1",
                               "limit": PROVIDER_LIMITS["resend_1"], "priority": 1})
        if os.getenv("RESEND_API_KEY_2") and _resend_has_domain:
            providers.append({"name": "resend_2", "display_name": "Resend #2",
                               "limit": PROVIDER_LIMITS["resend_2"], "priority": 2})
        if os.getenv("RESEND_API_KEY_3") and _resend_has_domain:
            providers.append({"name": "resend_3", "display_name": "Resend #3",
                               "limit": PROVIDER_LIMITS["resend_3"], "priority": 3})

        # ── Brevo HTTP API — only if credits > 0 ──────────────────────────────
        if os.getenv("BREVO_API_KEY"):
            # Quick credit check (cached — only check once per session)
            brevo_ok = getattr(EmailRotator, '_brevo_credits_ok', None)
            if brevo_ok is None:
                try:
                    import requests as _req
                    r = _req.get("https://api.brevo.com/v3/account",
                                 headers={"api-key": os.getenv("BREVO_API_KEY","")},
                                 timeout=5)
                    credits = next((p.get("credits",0) for p in r.json().get("plan",[])
                                    if p.get("type")=="free"), 0)
                    brevo_ok = credits > 0
                    EmailRotator._brevo_credits_ok = brevo_ok
                    if not brevo_ok:
                        logging.warning("⚠️ [ROTATOR] Brevo credits=0 — skipping Brevo")
                except Exception:
                    brevo_ok = True  # assume OK if check fails
                    EmailRotator._brevo_credits_ok = True
            if brevo_ok:
                providers.append({"name": "brevo", "display_name": "Brevo",
                                   "limit": PROVIDER_LIMITS["brevo"], "priority": 4})

        # ── Mailjet HTTP API ───────────────────────────────────────────────────
        if os.getenv("MAILJET_API_KEY") and os.getenv("MAILJET_SECRET_KEY"):
            providers.append({"name": "mailjet", "display_name": "Mailjet",
                               "limit": PROVIDER_LIMITS["mailjet"], "priority": 5})

        # ── Zoho SMTP — works on Render via port 465 SSL ──────────────────────
        if os.getenv("ZOHO_SMTP_USER") and os.getenv("ZOHO_APP_PASSWORD"):
            providers.append({"name": "zoho_1", "display_name": "Zoho #1",
                               "limit": PROVIDER_LIMITS["zoho_1"], "priority": 6})
        if os.getenv("ZOHO_SMTP_USER_2") and os.getenv("ZOHO_APP_PASSWORD_2"):
            providers.append({"name": "zoho_2", "display_name": "Zoho #2",
                               "limit": PROVIDER_LIMITS["zoho_2"], "priority": 7})
        if os.getenv("ZOHO_SMTP_USER_3") and os.getenv("ZOHO_APP_PASSWORD_3"):
            providers.append({"name": "zoho_3", "display_name": "Zoho #3",
                               "limit": PROVIDER_LIMITS.get("zoho_3", 500), "priority": 8})

        # ── Gmail SMTP port 465 — works on Render ─────────────────────────────
        if os.getenv("GMAIL_SMTP_USER") and os.getenv("GMAIL_APP_PASSWORD"):
            providers.append({"name": "gmail", "display_name": "Gmail",
                               "limit": PROVIDER_LIMITS["gmail"], "priority": 9})

        # ── Yahoo / Outlook — local only ──────────────────────────────────────
        if not is_render:
            if os.getenv("YAHOO_SMTP_USER") and os.getenv("YAHOO_APP_PASSWORD"):
                providers.append({"name": "yahoo", "display_name": "Yahoo",
                                   "limit": PROVIDER_LIMITS["yahoo"], "priority": 10})
            if os.getenv("OUTLOOK_USER") and os.getenv("OUTLOOK_PASSWORD"):
                providers.append({"name": "outlook", "display_name": "Outlook",
                                   "limit": PROVIDER_LIMITS["outlook"], "priority": 11})

        return sorted(providers, key=lambda x: x["priority"])

    def get_next_provider(self) -> Optional[Dict]:
        today = datetime.now().strftime("%Y-%m-%d")
        for provider in self.providers:
            name = provider["name"]
            if name not in self.usage:
                self.usage[name] = {"count": 0, "date": today}
            used = self.usage[name].get("count", 0)
            limit = provider["limit"]
            if used < limit:
                remaining = limit - used
                logging.info(f"📧 Selected provider: {provider['display_name']} ({used}/{limit} used, {remaining} remaining)")
                return provider
        logging.error("❌ ALL EMAIL PROVIDERS EXHAUSTED FOR TODAY!")
        return None

    def record_sent(self, provider_name: str):
        today = datetime.now().strftime("%Y-%m-%d")
        if provider_name not in self.usage:
            self.usage[provider_name] = {"count": 0, "date": today}
        self.usage[provider_name]["count"] += 1
        self.usage[provider_name]["date"] = today
        self._save_usage()

    def get_daily_stats(self) -> Dict:
        today = datetime.now().strftime("%Y-%m-%d")
        stats = {"date": today, "providers": {}, "total_sent": 0, "total_remaining": 0}
        for provider in self.providers:
            name = provider["name"]
            limit = provider["limit"]
            used = self.usage.get(name, {}).get("count", 0)
            remaining = limit - used
            stats["providers"][provider["display_name"]] = {
                "used": used, "limit": limit, "remaining": remaining,
                "percentage": round((used / limit) * 100, 1) if limit > 0 else 0
            }
            stats["total_sent"] += used
            stats["total_remaining"] += remaining
        return stats

    def can_send_more(self) -> bool:
        return self.get_next_provider() is not None

    def get_current_provider(self) -> str:
        """Return the display name of the next available provider (used by /status)."""
        provider = self.get_next_provider()
        return provider["display_name"] if provider else "None (exhausted)"

    def get_provider_stats(self) -> Dict:
        """Return per-provider stats dict compatible with /audit command."""
        today = datetime.now().strftime("%Y-%m-%d")
        result = {}
        for provider in self.providers:
            name = provider["name"]
            limit = provider["limit"]
            used = self.usage.get(name, {}).get("count", 0)
            result[provider["display_name"]] = {
                "sent_today": used,
                "daily_limit": limit,
                "available": used < limit,
                "remaining": limit - used,
            }
        return result

    def get_total_daily_limit(self) -> int:
        return sum(p["limit"] for p in self.providers)

    def reset_usage(self):
        self.usage = {}
        self._save_usage()


_rotator = None

def get_rotator() -> EmailRotator:
    global _rotator
    if _rotator is None:
        _rotator = EmailRotator()
    return _rotator

def get_next_email_provider() -> Optional[Dict]:
    return get_rotator().get_next_provider()

def record_email_sent(provider_name: str):
    get_rotator().record_sent(provider_name)

def get_email_stats() -> Dict:
    return get_rotator().get_daily_stats()

def can_send_email() -> bool:
    return get_rotator().can_send_more()
