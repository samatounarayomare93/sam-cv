import asyncio
import random
import logging
from bs4 import BeautifulSoup
from typing import List, Dict

async def fetch_daleel_page(page: int, db=None) -> List[Dict]:
    """[👑 FIX] Uses shared stealth fetch_page_async with proxy injection."""
    url = f"https://daleel-madani.org/jobs?page={page}"
    try:
        from core.scrapers.scraper import fetch_page_async
        from core.runtime_helpers import EvasionRouter
        
        from core.runtime_helpers import evasion
        headers = evasion.get_stealth_headers()
        headers['Referer'] = 'https://www.google.com/'
        
        resp = await fetch_page_async(url, headers=headers, timeout=20)
        if not resp or resp.status_code != 200:
            return []
        
        soup = BeautifulSoup(resp.text, 'html.parser')
        jobs = []
        rows = soup.select('.views-row')
        for row in rows:
            title_elem = row.select_one('.views-field-title a')
            if not title_elem: continue
            
            title = title_elem.get_text(strip=True)
            link = "https://daleel-madani.org" + title_elem['href']
            company = row.select_one('.views-field-field-employer-name').get_text(strip=True) if row.select_one('.views-field-field-employer-name') else "Unknown"
            
            jobs.append({
                "company_name": company,
                "job_title": title,
                "job_url": link,
                "platform": "daleel_madani",
                "priority_score": 75
            })
        return jobs
    except Exception as e:
        logging.error(f"Daleel Page {page} failed: {e}")
        return []

async def daleel_parallel_scan(db, pages: int = 5) -> List[Dict]:
    """[👑 FIX] Batched scan — 3 pages at a time with delays to avoid 403 floods."""
    batch_size = 3
    all_jobs = []
    page_list = list(range(pages))
    
    for i in range(0, len(page_list), batch_size):
        batch = page_list[i:i + batch_size]
        tasks = [fetch_daleel_page(p, db) for p in batch]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        for r in results:
            if isinstance(r, list):
                all_jobs.extend(r)
        # Delay between batches
        if i + batch_size < len(page_list):
            await asyncio.sleep(random.uniform(2, 5))
    
    return all_jobs
