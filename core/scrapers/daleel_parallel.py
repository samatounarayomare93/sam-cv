"""
Daleel Madani Scraper — Search-Engine Bypass Mode
===================================================
daleel-madani.org blocks all direct HTTP scrapers (HTTP 403).
We use DuckDuckGo site: queries to discover job listings instead,
exactly the same strategy used for Bayt, Naukrigulf, GulfTalent, etc.
"""

import asyncio
import random
import logging
from typing import List, Dict
from urllib.parse import urlparse

DALEEL_DOMAIN = "www.daleel-madani.org"

# Search queries that surface Daleel Madani job listings via search engines.
# Varied by role type and region to maximise coverage.
DALEEL_QUERIES = [
    f'site:{DALEEL_DOMAIN} "HR" OR "Human Resources" Lebanon',
    f'site:{DALEEL_DOMAIN} "Operations" Lebanon',
    f'site:{DALEEL_DOMAIN} "Administrative" Lebanon',
    f'site:{DALEEL_DOMAIN} "Business" Lebanon hiring',
    f'site:{DALEEL_DOMAIN} "Manager" Beirut',
    f'site:{DALEEL_DOMAIN} "Recruiter" Lebanon',
    f'site:{DALEEL_DOMAIN} "Finance" Lebanon',
    f'site:{DALEEL_DOMAIN} "Marketing" Lebanon',
]


def _safe_ddgs_search(query: str, max_results: int = 10) -> list:
    """Thread-safe DDGS search with warning suppression."""
    import warnings
    warnings.filterwarnings('ignore')
    try:
        try:
            from ddgs import DDGS
        except ImportError:
            from duckduckgo_search import DDGS
        with DDGS(timeout=20) as ddgs:
            return list(ddgs.text(query, max_results=max_results, region='wt-wt'))
    except Exception as e:
        logging.debug(f"DDGS search failed for '{query[:50]}': {e}")
        return []


async def daleel_parallel_scan(db=None, pages: int = 5) -> List[Dict]:
    """
    [👑 BYPASS MODE] Discovers Daleel Madani jobs via search-engine site: queries.

    Direct HTTP scraping of daleel-madani.org returns HTTP 403 on every request.
    This function uses DuckDuckGo site: queries to surface the same listings
    without ever touching the origin server — identical to how the omni-crawler
    handles Bayt, Naukrigulf, GulfTalent, and Indeed Middle East.

    The `pages` parameter is kept for API compatibility but is unused.
    """
    logging.info("🌍 Initiating BATCHED Auto-Sourcing on Daleel Madani...")

    all_jobs: List[Dict] = []
    seen_urls: set = set()

    # Pick a random subset of queries each cycle to vary the search pattern
    queries_to_run = random.sample(DALEEL_QUERIES, min(len(DALEEL_QUERIES), 5))

    for i, query in enumerate(queries_to_run):
        try:
            results = await asyncio.to_thread(_safe_ddgs_search, query, 10)
        except Exception as e:
            logging.warning(f"⚠️ Daleel search query failed: {e}")
            results = []

        for r in results:
            url = r.get('href', '')
            title = r.get('title', '').strip()
            snippet = r.get('body', '').strip()

            # Only keep URLs that actually point to daleel-madani.org
            if DALEEL_DOMAIN not in url.lower():
                continue

            if url in seen_urls or not title:
                continue
            seen_urls.add(url)

            # Try to extract a company name from the snippet or title
            company = "Unknown"
            for sep in [' - ', ' | ', ' – ', ' at ']:
                if sep in title:
                    parts = title.split(sep)
                    if len(parts) >= 2:
                        # Heuristic: shorter part is usually the company
                        candidate = parts[-1].strip()
                        if 3 < len(candidate) < 60:
                            company = candidate
                            break

            all_jobs.append({
                "company_name": company,
                "job_title": title,
                "job_url": url,
                "snippet": snippet,
                "platform": "daleel_madani",
                "priority_score": 75,
            })

        logging.info(f"⏳ Daleel batch {i + 1} done ({len(all_jobs)} jobs so far).")

        # Polite delay between search queries to avoid rate-limiting
        if i < len(queries_to_run) - 1:
            await asyncio.sleep(random.uniform(3, 7))

    logging.info(f"🏁 Daleel Batched Finished: {len(all_jobs)} jobs found")
    return all_jobs
