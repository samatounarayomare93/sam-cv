import asyncio
import logging
import os
import random
import time
import requests
from typing import Dict

import aiohttp
try:
    from core.scrapers.stealth_config import USER_AGENTS
except ImportError:
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
    ]


class TelegramNotifier:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.enabled = bool(self.token and self.chat_id)

    async def send_broadcast(self, message: str):
        if not self.enabled:
            return
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {"chat_id": self.chat_id, "text": message, "parse_mode": "HTML"}
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=payload, timeout=10) as resp:
                    if resp.status != 200:
                        logging.error(f"Telegram Broadcast Failed: {resp.status}")
        except Exception as e:
            logging.error(f"Telegram exception: {e}")


class HumanParityJitter:
    """Simulates organic cognitive delays between mission phases."""
    @staticmethod
    async def cognitive_delay(min_sec: int = 2, max_sec: int = 5):
        await asyncio.sleep(random.uniform(min_sec, max_sec))
    
    @staticmethod
    async def poisson_jitter(target_mean: int):
        """100% STEALTH: Mimics human jitter behavior using Poisson distribution."""
        import math
        
        # Simple Poisson-like distribution
        L = math.exp(-target_mean)
        k = 0
        p = 1
        while p > L:
            k = k + 1
            p = p * random.random()
        delay = k - 1
        
        # Add 20% variance
        final_delay = max(2, delay + random.uniform(-0.2, 0.2) * delay)
        await asyncio.sleep(final_delay)


class EvasionRouter:
    """Manages Proxy Routing and Anti-Cloudflare headers with enhanced stealth."""
    
    USER_AGENTS = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:125.0) Gecko/20100101 Firefox/125.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"
    ]
    
    # Accept-Language variations
    LANGUAGES = [
        "en-US,en;q=0.9",
        "en-US,en;q=0.9,ar;q=0.8",
        "en-GB,en;q=0.9",
        "en;q=0.9,en-US;q=0.8",
        "en-US,en;q=0.9,fr;q=0.7,de;q=0.6",
    ]
    
    def __init__(self):
        self.proxy = os.getenv("PROXY_URL")
        self._ua_index = random.randint(0, len(self.USER_AGENTS) - 1)

        
    def get_stealth_headers(self) -> Dict[str, str]:
        """Generate random stealth headers with modern Client-Hints."""
        ua = self.USER_AGENTS[self._ua_index]
        # Extract Chrome version for Client-Hints if applicable
        chrome_ver = "124"
        if "Chrome/" in ua:
            chrome_ver = ua.split("Chrome/")[1].split(".")[0]
            
        headers = {
            "User-Agent": ua,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Language": random.choice(self.LANGUAGES),
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Sec-Ch-Ua": f'"Not-A.Brand";v="99", "Chromium";v="{chrome_ver}", "Google Chrome";v="{chrome_ver}"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-User": "?1",
            "Upgrade-Insecure-Requests": "1",
            "Connection": "keep-alive",
            "Cache-Control": "max-age=0",
            "DNT": "1",
            "Priority": "u=0, i",
        }
        return headers
    
    def get_impersonation_mode(self) -> str:
        """Returns curl_cffi compatible impersonation string."""
        ua = self.USER_AGENTS[self._ua_index].lower()
        if "chrome" in ua: return "chrome"
        if "safari" in ua: return "safari"
        if "firefox" in ua: return "firefox"
        return "chrome"

    def rotate_identity(self):
        """Rotate both UA and request proxy mesh to cycle."""
        self.rotate_ua()
        logging.info(f"🔄 IDENTITY ROTATED: UA switched to {self.USER_AGENTS[self._ua_index][:30]}...")

    def rotate_ua(self):
        """Rotate to next user agent"""
        self._ua_index = (self._ua_index + 1) % len(self.USER_AGENTS)


class ProxyMesh:
    """The Shadow Grid: Rotational Proxy logic with Residential tier support."""
    def __init__(self):
        # [👑 RESIDENTIAL TIER]: Priority proxies from environment
        res_proxies = os.getenv("RESIDENTIAL_PROXIES", "").split(",") if os.getenv("RESIDENTIAL_PROXIES") else []
        self.residential = [p.strip() for p in res_proxies if p.strip()]
        
        self.proxies = [None] 
        self._index = 0
        self._res_index = 0
        self._last_refresh = 0
        self._refresh_interval = 1800 # 30 mins
        self._lock = asyncio.Lock()

    async def _refresh_proxies(self):
        """Scrapes free global proxies as a sovereign fallback grid with multi-source failover."""
        async with self._lock:
            if time.time() - self._last_refresh < self._refresh_interval and len(self.proxies) > 1: 
                return
            logging.info("🕸️ SHADOW GRID: Refreshing global proxy grid...")
            
            sources = [
                "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=5000&country=all&ssl=all&anonymity=all",
                "https://www.proxy-list.download/api/v1/get?type=http",
                "https://raw.githubusercontent.com/TheSpeedX/SOCKS-List/master/http.txt"
            ]
            
            new_proxies = []
            for url in sources:
                try:
                    res = requests.get(url, timeout=15)
                    if res.status_code == 200:
                        scraped = [p.strip() for p in res.text.split("\n") if p.strip()]
                        valid = [f"http://{p}" if "://" not in p else p for p in scraped if len(p) > 7]
                        new_proxies.extend(valid)
                        if len(new_proxies) > 50: break
                except Exception as e:
                    logging.warning(f"Shadow Grid Source Failed ({url[:30]}...): {e}")

            if new_proxies:
                # Keep direct connection (None) as the first option, then unique proxies
                self.proxies = [None] + list(set(new_proxies))[:100]
                self._last_refresh = time.time()
                logging.info(f"🕸️ SHADOW GRID: {len(self.proxies)} nodes active in the mesh.")
            else:
                logging.warning("Shadow Grid Refresh Failed: No proxies found from any source.")

    async def get_next(self):
        """[👑 PROXY-ROUTER]: Priority logic: Residential -> Shadow Grid -> Direct."""
        # 1. Try Residential if available (High Reputation)
        if self.residential:
            p = self.residential[self._res_index]
            self._res_index = (self._res_index + 1) % len(self.residential)
            return p if "://" in p else f"http://{p}"

        # 2. Fallback to Shadow Grid (Free rotation)
        await self._refresh_proxies()
        if not self.proxies: 
            return None
        p = self.proxies[self._index]
        self._index = (self._index + 1) % len(self.proxies)
        return p

    def get_next_sync(self):
        """Synchronous retrieval for legacy scraper components."""
        if not self.proxies or len(self.proxies) <= 1:
            return None
        p = self.proxies[self._index]
        self._index = (self._index + 1) % len(self.proxies)
        return p

    @property
    def active_nodes(self):
        """Telemetry for HUD reporting."""
        return len(self.proxies) if self.proxies else 0


# [👑 EXPORTED SINGLETONS]: For global system access
evasion = EvasionRouter()
proxy_mesh = ProxyMesh()

def get_evasion():
    return evasion

def get_proxy_mesh():
    return proxy_mesh

