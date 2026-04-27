import asyncio
import logging
import os
from typing import Any, Dict, List, Optional

import aiohttp

from core.runtime_helpers import EvasionRouter

try:
    from core.scrapers import scraper
    from core.scrapers.omni_crawler import OmniCrawler
except ImportError:
    scraper = None
    OmniCrawler = None


class ScrapeService:
    def __init__(self, semaphore: asyncio.Semaphore, omni_crawler=None):
        self.semaphore = semaphore
        self.evasion = EvasionRouter()
        self.omni_crawler = omni_crawler
        self._session = None
        self._total_requests = 0
        self._failed_requests = 0

    @staticmethod
    def is_available() -> bool:
        return scraper is not None or OmniCrawler is not None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            connector = aiohttp.TCPConnector(limit=100, limit_per_host=20, ttl_dns_cache=300, ssl=False, enable_cleanup_closed=True)
            timeout = aiohttp.ClientTimeout(total=30, connect=10, sock_read=15)
            self._session = aiohttp.ClientSession(connector=connector, timeout=timeout)
        return self._session

    async def close(self):
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None

    async def stealth_scrape_target(self, target_url: str) -> Optional[str]:
        async with self.semaphore:
            headers = self.evasion.get_stealth_headers()
            for attempt in range(3):
                try:
                    session = await self._get_session()
                    async with session.get(target_url, headers=headers, proxy=self.evasion.proxy, allow_redirects=True, timeout=20) as response:
                        self._total_requests += 1
                        if response.status == 200:
                            content = await response.text()
                            return content if len(content) > 100 else None
                        if response.status in [403, 429]:
                            await asyncio.sleep((attempt + 1) * 5)
                            self.evasion.rotate_ua()
                        elif response.status in [500, 502, 503, 504]:
                            await asyncio.sleep(2 ** attempt)
                        else:
                            return None
                except asyncio.TimeoutError:
                    self._failed_requests += 1
                    await asyncio.sleep(2 ** attempt)
                except aiohttp.ClientError:
                    self._failed_requests += 1
                    await asyncio.sleep(1)
            self._failed_requests += 1
            return None

    async def collect_leads(self) -> List[Dict[str, Any]]:
        raw_leads = []
        if scraper:
            raw_leads.extend(await asyncio.to_thread(scraper.get_latest_jobs))
        if self.omni_crawler:
            raw_leads.extend(await asyncio.to_thread(self.omni_crawler.hunt_the_web))
        return raw_leads
