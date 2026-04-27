# Sam Job Automator - Performance Optimizer
# ============================================
# Optimizes scraping, email delivery, and system performance
# No new accounts required!

import os
import time
import random
import logging
from datetime import datetime, timedelta
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================
# SMART SCHEDULER - Best Times for Email Delivery
# ============================================

def get_optimal_send_times():
    """
    Returns optimal times to send emails for maximum open rate.
    Based on email marketing research for MENA region.
    """
    return [
        # Morning slots (GCC timezone - 9-11 AM is prime time)
        (9, 0), (9, 30), (10, 0), (10, 30), (11, 0),
        # Afternoon slots (2-4 PM)
        (14, 0), (14, 30), (15, 0), (15, 30), (16, 0),
        # Evening slots (7-9 PM)
        (19, 0), (19, 30), (20, 0), (20, 30), (21, 0),
    ]

def should_send_now():
    """
    Determines if we should send emails right now based on:
    - Time of day (avoid late night, early morning)
    - Day of week (avoid weekends for B2B)
    - Current load
    """
    now = datetime.now()
    hour = now.hour
    
    # Weekend check (B2B emails less effective)
    if now.weekday() >= 5:  # Saturday = 5, Sunday = 6
        # Still send on weekends but fewer
        if hour < 10 or hour > 20:
            return False
        return random.random() < 0.3  # 30% chance during weekend
    
    # Weekday hours
    # Peak hours: 9-11 AM, 2-4 PM, 7-9 PM
    peak_hours = list(range(9, 12)) + list(range(14, 17)) + list(range(19, 22))
    
    # Slow hours: 12 AM - 8 AM, 12 PM - 1 PM, 10 PM - 11 PM
    slow_hours = list(range(0, 9)) + list(range(12, 14)) + [22, 23]
    
    if hour in peak_hours:
        return True  # Always send during peak
    elif hour in slow_hours:
        return False  # Never send during slow hours
    else:
        return random.random() < 0.5  # Random chance during shoulder hours

def get_delay_until_next_slot():
    """
    Returns seconds to wait until the next optimal email slot.
    """
    now = datetime.now()
    optimal_times = get_optimal_send_times()
    
    for hour, minute in optimal_times:
        next_slot = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if next_slot > now:
            return (next_slot - now).seconds
    
    # If no slots today, return time until first slot tomorrow
    tomorrow = now + timedelta(days=1)
    first_slot = tomorrow.replace(hour=9, minute=0, second=0, microsecond=0)
    return (first_slot - now).seconds

# ============================================
# RATE LIMITER - Intelligent Throttling
# ============================================

class SmartRateLimiter:
    """
    Intelligent rate limiter that adapts based on:
    - Success rate
    - Server responses
    - Time of day
    """
    
    def __init__(self):
        self.base_delay = 2.0  # seconds
        self.min_delay = 0.5
        self.max_delay = 30.0
        self.success_count = 0
        self.fail_count = 0
        self.consecutive_successes = 0
        self.consecutive_failures = 0
        self.last_request_time = 0
        
    def get_current_delay(self):
        """Calculate dynamic delay based on recent performance."""
        # If failing, increase delay
        if self.consecutive_failures > 0:
            delay = self.base_delay * (2 ** min(self.consecutive_failures, 5))
            return min(delay, self.max_delay)
        
        # If succeeding, gradually reduce delay
        if self.consecutive_successes > 5:
            delay = self.base_delay / (1.5 ** min(self.consecutive_successes - 5, 3))
            return max(delay, self.min_delay)
        
        return self.base_delay
    
    def record_success(self):
        """Record a successful request."""
        self.success_count += 1
        self.consecutive_successes += 1
        self.consecutive_failures = 0
        
    def record_failure(self):
        """Record a failed request."""
        self.fail_count += 1
        self.consecutive_failures += 1
        self.consecutive_successes = 0
        
    def wait_if_needed(self):
        """Wait appropriate time before next request."""
        delay = self.get_current_delay()
        
        # Add randomness to seem more human
        actual_delay = delay * random.uniform(0.8, 1.2)
        
        # Respect minimum interval between requests
        elapsed = time.time() - self.last_request_time
        if elapsed < actual_delay:
            time.sleep(actual_delay - elapsed)
        
        self.last_request_time = time.time()
        return actual_delay
    
    def get_stats(self):
        """Return current rate limiter statistics."""
        total = self.success_count + self.fail_count
        success_rate = self.success_count / total if total > 0 else 0
        
        return {
            'success_count': self.success_count,
            'fail_count': self.fail_count,
            'success_rate': success_rate,
            'current_delay': self.get_current_delay(),
            'consecutive_successes': self.consecutive_successes,
            'consecutive_failures': self.consecutive_failures
        }

# ============================================
# EMAIL DELIVERY OPTIMIZER
# ============================================

class EmailDeliveryOptimizer:
    """
    Optimizes email delivery for maximum inbox rate.
    """
    
    def __init__(self):
        self.sent_today = 0
        self.daily_limit = 50  # Safe limit per day
        self.hourly_limit = 10  # Max per hour
        self.hourly_sent = {}
        self._last_day = datetime.now().date()
        
    def _reset_if_new_day(self):
        """Reset daily counters when the calendar day changes."""
        today = datetime.now().date()
        if today != self._last_day:
            self.sent_today = 0
            self.hourly_sent = {}
            self._last_day = today
        
    def can_send_email(self):
        """Check if we should send an email now."""
        self._reset_if_new_day()
        now = datetime.now()
        current_hour = now.hour
        
        # Check daily limit
        if self.sent_today >= self.daily_limit:
            logger.info(f"Daily email limit reached ({self.daily_limit})")
            return False
        
        # Check hourly limit
        if self.hourly_sent.get(current_hour, 0) >= self.hourly_limit:
            logger.info(f"Hourly email limit reached ({self.hourly_limit}/hour)")
            return False
        
        # Check if it's a good time
        if not should_send_now():
            return False
        
        return True
    
    def record_send(self):
        """Record an email send."""
        self._reset_if_new_day()
        now = datetime.now()
        self.sent_today += 1
        self.hourly_sent[now.hour] = self.hourly_sent.get(now.hour, 0) + 1
        
    def get_remaining_quota(self):
        """Get remaining email quota for today."""
        self._reset_if_new_day()
        return self.daily_limit - self.sent_today
    
    def reset_daily_count(self):
        """Reset daily counter (called at midnight)."""
        self.sent_today = 0
        self.hourly_sent = {}
        self._last_day = datetime.now().date()

# ============================================
# SCRAPING PERFORMANCE OPTIMIZER
# ============================================

class ScrapingOptimizer:
    """
    Optimizes web scraping for maximum efficiency.
    """
    
    def __init__(self):
        self.session_pool = {}
        self.last_scrape_time = {}
        self.min_scrape_interval = 300  # 5 minutes minimum between scrapes
        self.cache = {}
        self.cache_ttl = 600  # 10 minutes cache TTL
        
    def should_scrape_source(self, source_name, force=False):
        """Check if we should scrape a source."""
        if force:
            return True
        
        now = time.time()
        
        # Check cache first
        cache_key = f"scrape_{source_name}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if now - cached_time < self.cache_ttl:
                logger.info(f"Using cached data for {source_name}")
                return False
        
        # Check rate limiting
        if source_name in self.last_scrape_time:
            elapsed = now - self.last_scrape_time[source_name]
            if elapsed < self.min_scrape_interval:
                logger.info(f"Rate limited for {source_name}: {self.min_scrape_interval - elapsed:.0f}s remaining")
                return False
        
        return True
    
    def record_scrape(self, source_name, data=None):
        """Record a scrape operation."""
        now = time.time()
        self.last_scrape_time[source_name] = now
        
        if data:
            self.cache[f"scrape_{source_name}"] = (now, data)
    
    def get_cached_data(self, source_name):
        """Get cached data for a source."""
        cache_key = f"scrape_{source_name}"
        if cache_key in self.cache:
            cached_time, cached_data = self.cache[cache_key]
            if time.time() - cached_time < self.cache_ttl:
                return cached_data
        return None

# ============================================
# GLOBAL INSTANCES
# ============================================

rate_limiter = SmartRateLimiter()
email_optimizer = EmailDeliveryOptimizer()
scraping_optimizer = ScrapingOptimizer()

# ============================================
# HELPER FUNCTIONS
# ============================================

def adaptive_sleep(min_seconds=1, max_seconds=3, activity='request'):
    """
    Human-like sleep that adapts based on activity type.
    """
    if activity == 'scrape':
        # Longer delays for scraping (more risky)
        base_delay = random.uniform(2.0, 5.0)
    elif activity == 'email':
        # Medium delays between emails
        base_delay = random.uniform(1.0, 3.0)
    else:
        # Short delays for simple operations
        base_delay = random.uniform(min_seconds, max_seconds)
    
    # Add randomness
    actual_delay = base_delay * random.uniform(0.7, 1.3)
    
    time.sleep(actual_delay)
    return actual_delay

def get_optimal_batch_size():
    """
    Calculate optimal batch size based on time of day.
    """
    now = datetime.now()
    hour = now.hour
    
    # Peak hours - larger batches
    if hour in range(9, 12) or hour in range(14, 17):
        return 15
    
    # Shoulder hours - medium batches
    if hour in range(7, 9) or hour in range(17, 20):
        return 10
    
    # Off hours - small batches
    return 5

# ============================================
# MAIN ENTRY POINT
# ============================================

if __name__ == "__main__":
    print("=" * 50)
    print("SAM PERFORMANCE OPTIMIZER")
    print("=" * 50)
    
    # Test rate limiter
    print("\n[1] Testing Rate Limiter...")
    for i in range(5):
        delay = rate_limiter.get_current_delay()
        print(f"    Request {i+1}: delay={delay:.2f}s")
        rate_limiter.wait_if_needed()
        rate_limiter.record_success()
    
    print(f"    Stats: {rate_limiter.get_stats()}")
    
    # Test email optimizer
    print("\n[2] Testing Email Optimizer...")
    print(f"    Can send: {email_optimizer.can_send_email()}")
    print(f"    Remaining quota: {email_optimizer.get_remaining_quota()}")
    for i in range(3):
        if email_optimizer.can_send_email():
            email_optimizer.record_send()
            print(f"    Sent email {i+1}")
    
    # Test optimal times
    print("\n[3] Optimal Send Times:")
    times = get_optimal_send_times()
    for hour, minute in times[:5]:
        print(f"    {hour:02d}:{minute:02d}")
    print(f"    ... and {len(times)-5} more slots")
    
    print("\n" + "=" * 50)
    print("Optimizer ready!")
    print("=" * 50)
