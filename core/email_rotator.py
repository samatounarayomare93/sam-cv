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
    "brevo":     300,   # Brevo free
    "mailjet":   200,   # Mailjet free (6000/month)
    "sendpulse": 400,   # SendPulse free (12000/month)
    "zoho_1":    500,   # Zoho #1 free
    "zoho_2":    500,   # Zoho #2 free
    "zoho_3":    500,   # Zoho #3 free
    "gmail":     500,   # Gmail free
    "yahoo":     500,   # Yahoo free
    "outlook":   300,   # Outlook free
}
# TOTAL with all providers: ~4,000/day FREE
# Each extra Zoho account adds 500/day
# 20 Zoho accounts = 10,000/day total

USAGE_FILE = Path("cache/email_usage.json")
USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)


class EmailRotator:
    def __init__(self):
        self.usage = self._load_usage()
        self.providers = self._get_available_providers()
        self._cleanup_old_usage()

    def _load_usage(self) -> Dict:
        try:
            if USAGE_FILE.exists():
                with open(USAGE_FILE, 'r') as f:
                    data = json.load(f)
                if data.get("date") == datetime.now().strftime("%Y-%m-%d"):
                    return data.get("usage", {})
            return {}
        except:
            return {}

    def _save_usage(self):
        try:
            data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "usage": self.usage,
                "last_updated": datetime.now().isoformat()
            }
            with open(USAGE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except:
            pass

    def _cleanup_old_usage(self):
        today = datetime.now().strftime("%Y-%m-%d")
        for provider in list(self.usage.keys()):
            if self.usage[provider].get("date") != today:
                self.usage[provider] = {"count": 0, "date": today}
        self._save_usage()

    def _get_available_providers(self) -> List[Dict]:
        providers = []
        is_render = bool(os.getenv("RENDER"))
        resend_from = os.getenv("RESEND_FROM_EMAIL", "").strip()

        # Resend: only include if RESEND_FROM_EMAIL is set (verified domain required)
        if resend_from:
            if os.getenv("RESEND_API_KEY"):
                providers.append({"name": "resend_1", "display_name": "Resend #1",
                                   "limit": PROVIDER_LIMITS["resend_1"], "priority": 1})
            if os.getenv("RESEND_API_KEY_2"):
                providers.append({"name": "resend_2", "display_name": "Resend #2",
                                   "limit": PROVIDER_LIMITS["resend_2"], "priority": 2})
            if os.getenv("RESEND_API_KEY_3"):
                providers.append({"name": "resend_3", "display_name": "Resend #3",
                                   "limit": PROVIDER_LIMITS["resend_3"], "priority": 3})

        # Brevo HTTP API — works on Render (no SMTP port needed), always first HTTP provider
        if os.getenv("BREVO_API_KEY"):
            providers.append({"name": "brevo", "display_name": "Brevo",
                               "limit": PROVIDER_LIMITS["brevo"], "priority": 4})

        # Zoho Transactional API — works on Render when ZOHO_API_KEY is set
        if os.getenv("ZOHO_API_KEY") and os.getenv("ZOHO_SMTP_USER"):
            providers.append({"name": "zoho_1", "display_name": "Zoho API",
                               "limit": PROVIDER_LIMITS.get("zoho_1", 500), "priority": 5})

        # Mailjet HTTP API — works on Render
        if os.getenv("MAILJET_API_KEY") and os.getenv("MAILJET_SECRET_KEY"):
            providers.append({"name": "mailjet", "display_name": "Mailjet",
                               "limit": PROVIDER_LIMITS["mailjet"], "priority": 5})

        # SendPulse HTTP API — works on Render
        if os.getenv("SENDPULSE_CLIENT_ID") and os.getenv("SENDPULSE_CLIENT_SECRET"):
            providers.append({"name": "sendpulse", "display_name": "SendPulse",
                               "limit": PROVIDER_LIMITS["sendpulse"], "priority": 6})

        # SMTP providers — Render blocks outbound SMTP ports (465/587), skip on cloud
        if not is_render:
            if os.getenv("ZOHO_SMTP_USER") and os.getenv("ZOHO_APP_PASSWORD"):
                providers.append({"name": "zoho_1", "display_name": "Zoho #1",
                                   "limit": PROVIDER_LIMITS["zoho_1"], "priority": 7})
            if os.getenv("ZOHO_SMTP_USER_2") and os.getenv("ZOHO_APP_PASSWORD_2"):
                providers.append({"name": "zoho_2", "display_name": "Zoho #2",
                                   "limit": PROVIDER_LIMITS["zoho_2"], "priority": 8})
            if os.getenv("GMAIL_SMTP_USER") and os.getenv("GMAIL_APP_PASSWORD"):
                providers.append({"name": "gmail", "display_name": "Gmail",
                                   "limit": PROVIDER_LIMITS["gmail"], "priority": 9})
            if os.getenv("YAHOO_SMTP_USER") and os.getenv("YAHOO_APP_PASSWORD"):
                providers.append({"name": "yahoo", "display_name": "Yahoo",
                                   "limit": PROVIDER_LIMITS["yahoo"], "priority": 10})
            if os.getenv("OUTLOOK_USER") and os.getenv("OUTLOOK_PASSWORD"):
                providers.append({"name": "outlook", "display_name": "Outlook",
                                   "limit": PROVIDER_LIMITS["outlook"], "priority": 11})
        else:
            # On Render: Gmail API (OAuth, not SMTP) still works
            if os.getenv("GMAIL_SMTP_USER") and os.getenv("GMAIL_APP_PASSWORD"):
                providers.append({"name": "gmail", "display_name": "Gmail",
                                   "limit": PROVIDER_LIMITS["gmail"], "priority": 9})

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
