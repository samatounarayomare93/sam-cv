"""
🚀 ZERO-COST EMAIL ROTATION SYSTEM
Maximizes free tier email limits across multiple providers
Target: 2,300+ emails/day (100% FREE)
"""

import logging
import os
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import json
from pathlib import Path

# Daily limits for each provider (FREE tier)
PROVIDER_LIMITS = {
    "resend": 100,     # Resend free tier (3000/month = ~100/day)
    "brevo": 300,      # Brevo free tier
    "zoho": 500,       # Zoho free tier
    "gmail_1": 500,    # Gmail account #1
    "gmail_2": 500,    # Gmail account #2 (if configured)
    "yahoo": 500,      # Yahoo free tier
    "outlook": 300,    # Outlook free tier
}

# Usage tracking file
USAGE_FILE = Path("cache/email_usage.json")
USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)


class EmailRotator:
    """Smart email provider rotation to maximize free tier usage."""
    
    def __init__(self):
        self.usage = self._load_usage()
        self.providers = self._get_available_providers()
        self._cleanup_old_usage()
    
    def _load_usage(self) -> Dict:
        """Load today's usage from file."""
        try:
            if USAGE_FILE.exists():
                with open(USAGE_FILE, 'r') as f:
                    data = json.load(f)
                
                # Check if data is from today
                saved_date = data.get("date")
                today = datetime.now().strftime("%Y-%m-%d")
                
                if saved_date == today:
                    return data.get("usage", {})
                else:
                    # New day, reset usage
                    return {}
            return {}
        except Exception as e:
            logging.warning(f"Failed to load email usage: {e}")
            return {}
    
    def _save_usage(self):
        """Save usage to file."""
        try:
            data = {
                "date": datetime.now().strftime("%Y-%m-%d"),
                "usage": self.usage,
                "last_updated": datetime.now().isoformat()
            }
            with open(USAGE_FILE, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to save email usage: {e}")
    
    def _cleanup_old_usage(self):
        """Reset usage if it's a new day."""
        today = datetime.now().strftime("%Y-%m-%d")
        
        for provider in list(self.usage.keys()):
            if self.usage[provider].get("date") != today:
                self.usage[provider] = {"count": 0, "date": today}
        
        self._save_usage()
    
    def _get_available_providers(self) -> List[Dict]:
        """Get list of configured email providers."""
        providers = []
        
        # Brevo
        if os.getenv("BREVO_SMTP_LOGIN") and os.getenv("BREVO_SMTP_PASSWORD"):
            providers.append({
                "name": "brevo",
                "display_name": "Brevo",
                "limit": PROVIDER_LIMITS["brevo"],
                "priority": 1
            })
        
        # Zoho
        if os.getenv("ZOHO_SMTP_USER") and os.getenv("ZOHO_APP_PASSWORD"):
            providers.append({
                "name": "zoho",
                "display_name": "Zoho",
                "limit": PROVIDER_LIMITS["zoho"],
                "priority": 2
            })
        
        # Gmail #1
        if os.getenv("GMAIL_SMTP_USER") and os.getenv("GMAIL_APP_PASSWORD"):
            providers.append({
                "name": "gmail_1",
                "display_name": "Gmail",
                "limit": PROVIDER_LIMITS["gmail_1"],
                "priority": 3
            })
        
        # Yahoo
        if os.getenv("YAHOO_SMTP_USER") and os.getenv("YAHOO_APP_PASSWORD"):
            providers.append({
                "name": "yahoo",
                "display_name": "Yahoo",
                "limit": PROVIDER_LIMITS["yahoo"],
                "priority": 4
            })
        
        # Outlook
        if os.getenv("OUTLOOK_USER") and os.getenv("OUTLOOK_PASSWORD"):
            providers.append({
                "name": "outlook",
                "display_name": "Outlook",
                "limit": PROVIDER_LIMITS["outlook"],
                "priority": 5
            })
        
        return sorted(providers, key=lambda x: x["priority"])
    
    def get_next_provider(self) -> Optional[Dict]:
        """
        Get next available provider based on daily limits.
        
        Returns:
            Provider dict or None if all limits reached
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        for provider in self.providers:
            provider_name = provider["name"]
            
            # Initialize usage if not exists
            if provider_name not in self.usage:
                self.usage[provider_name] = {"count": 0, "date": today}
            
            # Check if under limit
            current_usage = self.usage[provider_name].get("count", 0)
            limit = provider["limit"]
            
            if current_usage < limit:
                remaining = limit - current_usage
                logging.info(
                    f"📧 Selected provider: {provider['display_name']} "
                    f"({current_usage}/{limit} used, {remaining} remaining)"
                )
                return provider
        
        # All providers exhausted
        logging.error("❌ ALL EMAIL PROVIDERS EXHAUSTED FOR TODAY!")
        return None
    
    def record_sent(self, provider_name: str) -> bool:
        """
        Record that an email was sent via provider.
        
        Args:
            provider_name: Name of provider used
        
        Returns:
            True if recorded successfully
        """
        today = datetime.now().strftime("%Y-%m-%d")
        
        if provider_name not in self.usage:
            self.usage[provider_name] = {"count": 0, "date": today}
        
        self.usage[provider_name]["count"] += 1
        self.usage[provider_name]["date"] = today
        
        self._save_usage()
        return True
    
    def get_daily_stats(self) -> Dict:
        """
        Get today's usage statistics.
        
        Returns:
            Dict with usage stats per provider
        """
        today = datetime.now().strftime("%Y-%m-%d")
        stats = {
            "date": today,
            "providers": {},
            "total_sent": 0,
            "total_remaining": 0
        }
        
        for provider in self.providers:
            provider_name = provider["name"]
            limit = provider["limit"]
            
            if provider_name in self.usage:
                used = self.usage[provider_name].get("count", 0)
            else:
                used = 0
            
            remaining = limit - used
            
            stats["providers"][provider["display_name"]] = {
                "used": used,
                "limit": limit,
                "remaining": remaining,
                "percentage": round((used / limit) * 100, 1) if limit > 0 else 0
            }
            
            stats["total_sent"] += used
            stats["total_remaining"] += remaining
        
        return stats
    
    def can_send_more(self) -> bool:
        """Check if we can send more emails today."""
        return self.get_next_provider() is not None
    
    def get_total_daily_limit(self) -> int:
        """Get total daily limit across all providers."""
        return sum(p["limit"] for p in self.providers)
    
    def reset_usage(self):
        """Manually reset usage (for testing)."""
        self.usage = {}
        self._save_usage()
        logging.info("🔄 Email usage reset")


# Global instance
_rotator = None


def get_rotator() -> EmailRotator:
    """Get global email rotator instance."""
    global _rotator
    if _rotator is None:
        _rotator = EmailRotator()
    return _rotator


def get_next_email_provider() -> Optional[Dict]:
    """Get next available email provider."""
    return get_rotator().get_next_provider()


def record_email_sent(provider_name: str):
    """Record that an email was sent."""
    get_rotator().record_sent(provider_name)


def get_email_stats() -> Dict:
    """Get email usage statistics."""
    return get_rotator().get_daily_stats()


def can_send_email() -> bool:
    """Check if we can send more emails today."""
    return get_rotator().can_send_more()


# Example usage
if __name__ == "__main__":
    rotator = EmailRotator()
    
    print("📊 Email Rotation System Status")
    print("=" * 50)
    
    stats = rotator.get_daily_stats()
    print(f"\n📅 Date: {stats['date']}")
    print(f"📧 Total sent today: {stats['total_sent']}")
    print(f"📬 Total remaining: {stats['total_remaining']}")
    print(f"🎯 Total daily limit: {rotator.get_total_daily_limit()}")
    
    print("\n📊 Provider Breakdown:")
    for provider, data in stats['providers'].items():
        print(f"  {provider}: {data['used']}/{data['limit']} ({data['percentage']}%)")
    
    print("\n✅ Next provider:", rotator.get_next_provider())
