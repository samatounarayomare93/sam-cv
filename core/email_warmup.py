"""
📧 EMAIL WARM-UP STRATEGY (100% FREE)
Gradually increase sending volume to avoid spam filters

Strategy:
- Day 1: 10 emails
- Day 2: 20 emails
- Day 3: 30 emails
- Day 4: 50 emails
- Day 5+: Full capacity (300+)

Prevents new email accounts from being flagged as spam
"""

import logging
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional

# Warmup schedule (day: max_emails)
WARMUP_SCHEDULE = {
    1: 10,
    2: 20,
    3: 30,
    4: 50,
    5: 100,
    6: 200,
    7: 300,  # Full capacity after 1 week
}

# Warmup tracking file
WARMUP_FILE = Path("cache/email_warmup.json")
WARMUP_FILE.parent.mkdir(parents=True, exist_ok=True)

# Enable/disable warmup
WARMUP_ENABLED = os.getenv("EMAIL_WARMUP_ENABLED", "true").lower() == "true"


class EmailWarmup:
    """Manage email warm-up process for new accounts."""
    
    def __init__(self):
        self.warmup_data = self._load_warmup_data()
    
    def _load_warmup_data(self) -> Dict:
        """Load warmup data from file."""
        try:
            if WARMUP_FILE.exists():
                with open(WARMUP_FILE, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.warning(f"Failed to load warmup data: {e}")
            return {}
    
    def _save_warmup_data(self):
        """Save warmup data to file."""
        try:
            with open(WARMUP_FILE, 'w') as f:
                json.dump(self.warmup_data, f, indent=2)
        except Exception as e:
            logging.warning(f"Failed to save warmup data: {e}")
    
    def start_warmup(self, provider_name: str, start_date: str = None):
        """
        Start warmup process for a provider.
        
        Args:
            provider_name: Name of email provider (e.g., "zoho", "gmail")
            start_date: Start date (YYYY-MM-DD), defaults to today
        """
        if start_date is None:
            start_date = datetime.now().strftime("%Y-%m-%d")
        
        self.warmup_data[provider_name] = {
            "start_date": start_date,
            "status": "warming_up",
            "daily_sent": {}
        }
        
        self._save_warmup_data()
        logging.info(f"🔥 Started warmup for {provider_name} on {start_date}")
    
    def get_daily_limit(self, provider_name: str, default_limit: int = 300) -> int:
        """
        Get current daily limit for provider based on warmup schedule.
        
        Args:
            provider_name: Name of email provider
            default_limit: Default limit if not warming up
        
        Returns:
            Maximum emails allowed today
        """
        if not WARMUP_ENABLED:
            return default_limit
        
        # Check if provider is in warmup
        if provider_name not in self.warmup_data:
            return default_limit
        
        warmup_info = self.warmup_data[provider_name]
        
        # Check if warmup is complete
        if warmup_info.get("status") == "complete":
            return default_limit
        
        # Calculate warmup day
        start_date = datetime.strptime(warmup_info["start_date"], "%Y-%m-%d")
        today = datetime.now()
        days_since_start = (today - start_date).days + 1
        
        # Get limit from schedule
        if days_since_start >= max(WARMUP_SCHEDULE.keys()):
            # Warmup complete
            self.warmup_data[provider_name]["status"] = "complete"
            self._save_warmup_data()
            logging.info(f"✅ Warmup complete for {provider_name}")
            return default_limit
        
        # Get current day's limit
        limit = WARMUP_SCHEDULE.get(days_since_start, default_limit)
        
        logging.info(
            f"🔥 Warmup Day {days_since_start} for {provider_name}: "
            f"Limit = {limit} emails"
        )
        
        return limit
    
    def record_sent(self, provider_name: str, count: int = 1):
        """
        Record emails sent for provider.
        
        Args:
            provider_name: Name of email provider
            count: Number of emails sent
        """
        if provider_name not in self.warmup_data:
            return
        
        today = datetime.now().strftime("%Y-%m-%d")
        daily_sent = self.warmup_data[provider_name].get("daily_sent", {})
        daily_sent[today] = daily_sent.get(today, 0) + count
        
        self.warmup_data[provider_name]["daily_sent"] = daily_sent
        self._save_warmup_data()
    
    def get_warmup_status(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """
        Get warmup status for provider.
        
        Returns:
            Dict with warmup info or None if not warming up
        """
        if provider_name not in self.warmup_data:
            return None
        
        warmup_info = self.warmup_data[provider_name]
        start_date = datetime.strptime(warmup_info["start_date"], "%Y-%m-%d")
        today = datetime.now()
        days_since_start = (today - start_date).days + 1
        
        total_days = max(WARMUP_SCHEDULE.keys())
        progress = min(100, int((days_since_start / total_days) * 100))
        
        today_str = today.strftime("%Y-%m-%d")
        sent_today = warmup_info.get("daily_sent", {}).get(today_str, 0)
        limit_today = self.get_daily_limit(provider_name)
        
        return {
            "provider": provider_name,
            "status": warmup_info["status"],
            "start_date": warmup_info["start_date"],
            "day": days_since_start,
            "total_days": total_days,
            "progress": progress,
            "sent_today": sent_today,
            "limit_today": limit_today,
            "remaining_today": limit_today - sent_today
        }
    
    def get_all_warmup_status(self) -> Dict[str, Any]:
        """Get warmup status for all providers."""
        status = {}
        
        for provider_name in self.warmup_data.keys():
            status[provider_name] = self.get_warmup_status(provider_name)
        
        return status
    
    def is_warming_up(self, provider_name: str) -> bool:
        """Check if provider is currently warming up."""
        if provider_name not in self.warmup_data:
            return False
        
        return self.warmup_data[provider_name].get("status") == "warming_up"
    
    def reset_warmup(self, provider_name: str):
        """Reset warmup for provider (start over)."""
        if provider_name in self.warmup_data:
            del self.warmup_data[provider_name]
            self._save_warmup_data()
            logging.info(f"🔄 Reset warmup for {provider_name}")


# Global instance
_warmup = None


def get_warmup() -> EmailWarmup:
    """Get global email warmup instance."""
    global _warmup
    if _warmup is None:
        _warmup = EmailWarmup()
    return _warmup


def get_warmup_limit(provider_name: str, default_limit: int = 300) -> int:
    """Get daily limit for provider considering warmup."""
    return get_warmup().get_daily_limit(provider_name, default_limit)


def start_provider_warmup(provider_name: str):
    """Start warmup for a provider."""
    get_warmup().start_warmup(provider_name)


def record_warmup_sent(provider_name: str, count: int = 1):
    """Record emails sent during warmup."""
    get_warmup().record_sent(provider_name, count)


def get_warmup_status(provider_name: str = None) -> Dict[str, Any]:
    """Get warmup status."""
    if provider_name:
        return get_warmup().get_warmup_status(provider_name)
    return get_warmup().get_all_warmup_status()


# Example usage
if __name__ == "__main__":
    warmup = EmailWarmup()
    
    print("🔥 Email Warmup System")
    print("=" * 50)
    
    # Start warmup for test provider
    test_provider = "zoho"
    warmup.start_warmup(test_provider)
    
    # Show status
    status = warmup.get_warmup_status(test_provider)
    if status:
        print(f"\n📊 Warmup Status for {test_provider}:")
        print(f"  Day: {status['day']}/{status['total_days']}")
        print(f"  Progress: {status['progress']}%")
        print(f"  Today's limit: {status['limit_today']} emails")
        print(f"  Sent today: {status['sent_today']}")
        print(f"  Remaining: {status['remaining_today']}")
    
    # Show schedule
    print("\n📅 Warmup Schedule:")
    for day, limit in sorted(WARMUP_SCHEDULE.items()):
        print(f"  Day {day}: {limit} emails")
