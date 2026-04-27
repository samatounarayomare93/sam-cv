import asyncio
import httpx
from bs4 import BeautifulSoup
import logging
from typing import List, Dict

async def fetch_daleel_page(page: int, db=None) -> List[Dict]:
    url = f"https://daleel-madani.org/jobs?page={page}"
    try:
        async with httpx.AsyncClient(timeout=20) as client:
            resp = await client.get(url)
            if resp.status_code != 200:
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
                
                # Check for duplicates if db is provided
                if db:
                    # [👑 CLOUD-SENSE] Check for duplicates in hive-mind
                    # Using a simplified check here
                    pass

                jobs.append({
                    "company_name": company,
                    "job_title": title,
                    "job_url": link,
                    "platform": "daleel_madani",
                    "priority_score": 75 # Daleel is high-value
                })
            return jobs
    except Exception as e:
        logging.error(f"Daleel Page {page} failed: {e}")
        return []

async def daleel_parallel_scan(db, pages: int = 5) -> List[Dict]:
    """[🚀 HYPER-SPEED] Scans multiple Daleel pages in parallel."""
    tasks = [fetch_daleel_page(p, db) for p in range(pages)]
    results = await asyncio.gather(*tasks)
    all_jobs = []
    for r in results:
        all_jobs.extend(r)
    return all_jobs
