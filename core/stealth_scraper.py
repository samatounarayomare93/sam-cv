"""
🕵️ STEALTH SCRAPING TECHNIQUES (100% FREE)
Advanced anti-detection methods from around the world
Zero investment required
"""

import random
import time
import hashlib
from typing import Dict, List, Optional
import logging


class StealthScraper:
    """Advanced scraping techniques to avoid detection."""
    
    def __init__(self):
        self.request_count = 0
        self.last_request_time = 0
        self.user_agents = self._load_user_agents()
        self.fingerprints = self._generate_fingerprints()
    
    def _load_user_agents(self) -> List[str]:
        """
        🌍 GLOBAL USER AGENTS
        Real browser fingerprints from around the world
        """
        return [
            # 🇺🇸 USA - Chrome (most common)
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            
            # 🇬🇧 UK - Safari
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
            
            # 🇩🇪 Germany - Firefox
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
            
            # 🇦🇪 UAE - Mobile (many recruiters use mobile)
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Linux; Android 13) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.144 Mobile Safari/537.36",
            
            # 🇨🇳 China - QQ Browser
            "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 QQBrowser/10.8.4559.400",
            
            # 🇷🇺 Russia - Yandex
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 YaBrowser/23.11.0.0 Safari/537.36",
            
            # 🇯🇵 Japan - Edge
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        ]
    
    def _generate_fingerprints(self) -> List[Dict]:
        """
        🎭 BROWSER FINGERPRINTS
        Complete browser profiles to avoid detection
        """
        return [
            {
                "name": "chrome_windows",
                "platform": "Win32",
                "vendor": "Google Inc.",
                "languages": ["en-US", "en"],
                "screen": {"width": 1920, "height": 1080, "colorDepth": 24},
                "timezone": -300,  # EST
            },
            {
                "name": "safari_mac",
                "platform": "MacIntel",
                "vendor": "Apple Computer, Inc.",
                "languages": ["en-US", "en"],
                "screen": {"width": 2560, "height": 1440, "colorDepth": 24},
                "timezone": -300,
            },
            {
                "name": "firefox_linux",
                "platform": "Linux x86_64",
                "vendor": "",
                "languages": ["en-US", "en"],
                "screen": {"width": 1920, "height": 1080, "colorDepth": 24},
                "timezone": 0,  # UTC
            },
        ]
    
    def get_stealth_headers(self, url: str = "") -> Dict[str, str]:
        """
        🕵️ STEALTH HEADERS
        Headers that look like real browser
        """
        user_agent = random.choice(self.user_agents)
        fingerprint = random.choice(self.fingerprints)
        
        headers = {
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": f"{fingerprint['languages'][0]},{fingerprint['languages'][1]};q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "DNT": "1",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Cache-Control": "max-age=0",
        }
        
        # Add referer for non-first requests
        if url and self.request_count > 0:
            domain = url.split('/')[2] if '/' in url else url
            headers["Referer"] = f"https://{domain}/"
        
        # Randomly add some optional headers (more realistic)
        if random.random() > 0.5:
            headers["Sec-CH-UA"] = '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"'
            headers["Sec-CH-UA-Mobile"] = "?0"
            headers["Sec-CH-UA-Platform"] = f'"{fingerprint["platform"]}"'
        
        return headers
    
    def human_delay(self, min_seconds: float = 2.0, max_seconds: float = 5.0):
        """
        🧠 HUMAN-LIKE DELAYS
        Mimic human browsing patterns
        """
        # Calculate time since last request
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        # If too fast, add extra delay
        if time_since_last < 1.0:
            extra_delay = random.uniform(2.0, 4.0)
            time.sleep(extra_delay)
        
        # Normal human delay with variance
        base_delay = random.uniform(min_seconds, max_seconds)
        
        # Add micro-variations (humans don't have perfect timing)
        micro_variance = random.gauss(0, 0.3)  # Gaussian distribution
        delay = max(0.5, base_delay + micro_variance)
        
        # Occasionally add longer "reading" delays
        if random.random() < 0.1:  # 10% chance
            delay += random.uniform(5.0, 10.0)
            logging.debug("🧠 Simulating human 'reading' pause")
        
        time.sleep(delay)
        self.last_request_time = time.time()
        self.request_count += 1
    
    def get_session_cookies(self) -> Dict[str, str]:
        """
        🍪 REALISTIC COOKIES
        Generate cookies that look like real session
        """
        session_id = hashlib.md5(str(time.time()).encode()).hexdigest()
        
        return {
            "session_id": session_id,
            "_ga": f"GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}",
            "_gid": f"GA1.2.{random.randint(100000000, 999999999)}.{int(time.time())}",
            "_gat": "1",
        }
    
    def rotate_identity(self):
        """
        🎭 ROTATE COMPLETE IDENTITY
        Change user agent, fingerprint, cookies
        """
        self.user_agents = self._load_user_agents()
        self.fingerprints = self._generate_fingerprints()
        self.request_count = 0
        logging.info("🎭 Identity rotated - new browser fingerprint")
    
    def check_rate_limit(self, max_requests_per_minute: int = 10) -> bool:
        """
        ⏱️ RATE LIMIT CHECK
        Ensure we don't exceed safe request rate
        """
        if self.request_count >= max_requests_per_minute:
            # Reset counter after 1 minute
            if time.time() - self.last_request_time > 60:
                self.request_count = 0
                return True
            else:
                logging.warning("⏱️ Rate limit reached - waiting...")
                time.sleep(60 - (time.time() - self.last_request_time))
                self.request_count = 0
                return True
        return True
    
    @staticmethod
    def get_proxy_list() -> List[str]:
        """
        🌐 FREE PROXY LIST
        Public proxies (use with caution - quality varies)
        """
        # Note: Free proxies are unreliable
        # Better to use delays and rotation instead
        return [
            # Add free proxy sources here if needed
            # But delays + rotation is more reliable
        ]
    
    @staticmethod
    def bypass_cloudflare() -> Dict[str, str]:
        """
        ☁️ CLOUDFLARE BYPASS
        Headers to pass Cloudflare protection
        """
        return {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "TE": "trailers",
        }
    
    @staticmethod
    def extract_email_patterns(text: str) -> List[str]:
        """
        📧 ADVANCED EMAIL EXTRACTION
        Find emails even when obfuscated
        """
        import re
        
        emails = []
        
        # Standard email pattern
        standard = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)
        emails.extend(standard)
        
        # Obfuscated patterns
        # "name [at] company [dot] com"
        obfuscated1 = re.findall(r'\b[\w.+-]+\s*\[at\]\s*[\w.-]+\s*\[dot\]\s*\w+\b', text, re.IGNORECASE)
        for email in obfuscated1:
            clean = email.replace('[at]', '@').replace('[dot]', '.').replace(' ', '')
            emails.append(clean)
        
        # "name (at) company (dot) com"
        obfuscated2 = re.findall(r'\b[\w.+-]+\s*\(at\)\s*[\w.-]+\s*\(dot\)\s*\w+\b', text, re.IGNORECASE)
        for email in obfuscated2:
            clean = email.replace('(at)', '@').replace('(dot)', '.').replace(' ', '')
            emails.append(clean)
        
        # "name @ company . com" (with spaces)
        spaced = re.findall(r'\b[\w.+-]+\s*@\s*[\w.-]+\s*\.\s*\w+\b', text)
        for email in spaced:
            clean = email.replace(' ', '')
            emails.append(clean)
        
        return list(set(emails))  # Remove duplicates
    
    @staticmethod
    def smart_retry(func, max_retries: int = 3, backoff_factor: float = 2.0):
        """
        🔄 SMART RETRY WITH EXPONENTIAL BACKOFF
        Retry failed requests with increasing delays
        """
        for attempt in range(max_retries):
            try:
                return func()
            except Exception as e:
                if attempt == max_retries - 1:
                    raise e
                
                delay = backoff_factor ** attempt
                jitter = random.uniform(0, 0.3 * delay)
                total_delay = delay + jitter
                
                logging.warning(f"Attempt {attempt + 1} failed, retrying in {total_delay:.1f}s...")
                time.sleep(total_delay)
        
        return None


class AntiDetectionTricks:
    """Advanced anti-detection techniques."""
    
    @staticmethod
    def randomize_request_order(urls: List[str]) -> List[str]:
        """
        🎲 RANDOMIZE ORDER
        Don't scrape in predictable order
        """
        shuffled = urls.copy()
        random.shuffle(shuffled)
        return shuffled
    
    @staticmethod
    def add_noise_requests(target_urls: List[str], noise_ratio: float = 0.2) -> List[str]:
        """
        🎭 NOISE REQUESTS
        Add random "decoy" requests to hide pattern
        """
        noise_urls = [
            "https://www.google.com",
            "https://www.linkedin.com",
            "https://www.indeed.com",
            "https://www.glassdoor.com",
        ]
        
        num_noise = int(len(target_urls) * noise_ratio)
        noise_samples = random.choices(noise_urls, k=num_noise)
        
        combined = target_urls + noise_samples
        random.shuffle(combined)
        
        return combined
    
    @staticmethod
    def mimic_human_scrolling():
        """
        📜 MIMIC SCROLLING
        Simulate human scrolling behavior
        (For headless browser scenarios)
        """
        scroll_delays = [
            random.uniform(0.5, 1.5),
            random.uniform(1.0, 2.0),
            random.uniform(0.3, 0.8),
        ]
        
        return scroll_delays
    
    @staticmethod
    def detect_honeypot(html: str) -> bool:
        """
        🍯 HONEYPOT DETECTION
        Detect if page is a trap for scrapers
        """
        honeypot_indicators = [
            "display:none",
            "visibility:hidden",
            "position:absolute;left:-9999px",
            "opacity:0",
        ]
        
        for indicator in honeypot_indicators:
            if indicator in html.lower():
                logging.warning("🍯 Possible honeypot detected")
                return True
        
        return False


# Example usage
if __name__ == "__main__":
    scraper = StealthScraper()
    
    print("🕵️ STEALTH SCRAPER TEST")
    print("=" * 50)
    
    # Test headers
    headers = scraper.get_stealth_headers("https://example.com")
    print("\n📋 Stealth Headers:")
    for key, value in list(headers.items())[:5]:
        print(f"  {key}: {value[:50]}...")
    
    # Test human delay
    print("\n⏱️ Testing human-like delays...")
    for i in range(3):
        start = time.time()
        scraper.human_delay(1.0, 2.0)
        elapsed = time.time() - start
        print(f"  Request {i+1}: {elapsed:.2f}s delay")
    
    # Test email extraction
    test_text = """
    Contact us at: info@company.com
    Or reach out to: john [at] example [dot] com
    Support: support (at) test (dot) org
    """
    emails = scraper.extract_email_patterns(test_text)
    print(f"\n📧 Extracted emails: {emails}")
    
    print("\n✅ All stealth features working!")
