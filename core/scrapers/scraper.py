"""
ENHANCED SCRAPER - MAXIMUM JOB SOURCES v2
======================================
Multiplied job sources for maximum job discovery
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import re
import os
import asyncio
import urllib.parse
from typing import Optional
from core import config
from tenacity import retry, stop_after_attempt, wait_exponential
# Removed legacy database import for Sovereign Data Layer
from core.db_manager import db_manager
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

try:
    from curl_cffi.requests import AsyncSession
    HAS_CURL_CFFI = True
except ImportError:
    HAS_CURL_CFFI = False

# Import EvasionRouter for user agents
try:
    from core.runtime_helpers import EvasionRouter
except ImportError:
    # Fallback if import fails
    class EvasionRouter:
        USER_AGENTS = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ]

TOTAL_DEEP_DIVES = 0
SCRAPE_COOLDOWN = 0

# [shield] BLOCKED DOMAIN TRACKER: Stop retrying domains that consistently return 403
# Maps domain -> consecutive 403 count. Once >= threshold, skip silently.
_blocked_domain_counts: dict = {}
_BLOCKED_DOMAIN_THRESHOLD = 3  # After 3 consecutive 403s, stop logging and skip

def _record_domain_block(url: str):
    """Track 403 hits per domain. Returns True if domain is now considered permanently blocked."""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
    except Exception:
        domain = url
    _blocked_domain_counts[domain] = _blocked_domain_counts.get(domain, 0) + 1
    return _blocked_domain_counts[domain] >= _BLOCKED_DOMAIN_THRESHOLD

def _is_domain_blocked(url: str) -> bool:
    """Returns True if this domain has been blocked too many times."""
    try:
        from urllib.parse import urlparse
        domain = urlparse(url).netloc
    except Exception:
        domain = url
    return _blocked_domain_counts.get(domain, 0) >= _BLOCKED_DOMAIN_THRESHOLD

def _get_deep_dive_count():
    return TOTAL_DEEP_DIVES

def _increment_deep_dive():
    global TOTAL_DEEP_DIVES
    TOTAL_DEEP_DIVES += 1
    return TOTAL_DEEP_DIVES

def _reset_deep_dive():
    """Reset counter at start of each scrape cycle"""
    global TOTAL_DEEP_DIVES
    TOTAL_DEEP_DIVES = 0

def create_session():
    """God-Tier Stealth: Sync session with Chrome impersonation"""
    pass  # Reserved for future sync session factory

from core.runtime_helpers import proxy_mesh as _proxy_mesh, evasion as _evasion

import httpx

_async_session: Optional[httpx.AsyncClient] = None

async def _get_proxy():
    """[[crown] SOVEREIGN PROXY]: Select the best available proxy from the shared mesh."""
    return await _proxy_mesh.get_next()

async def fetch_page_async(url, headers=None, timeout=15, retry_count=0):
    """[[crown] OMEGA FETCH]: Dual-Engine (curl_cffi + httpx) for absolute WAF penetration."""
    headers = headers or {}
    stealth_headers = _evasion.get_stealth_headers()
    stealth_headers.update(headers)
    
    proxy = await _get_proxy()
    
    # [[crown] ENGINE 1: curl_cffi] - Best for Cloudflare/TLS Fingerprinting
    if HAS_CURL_CFFI:
        try:
            impersonate = _evasion.get_impersonation_mode()
            async with AsyncSession(impersonate=impersonate, proxies={"http": proxy, "https": proxy} if proxy else None) as s:
                response = await s.get(url, headers=stealth_headers, timeout=timeout, follow_redirects=True)
                if response.status_code == 403 or response.status_code == 429:
                    permanently_blocked = _record_domain_block(url)
                    if not permanently_blocked:
                        logging.warning(f"âš ï¸ [CURL-CFFI] Blocked (HTTP {response.status_code}) on {url}")
                    _evasion.rotate_ua()
                    if retry_count < 2 and not permanently_blocked:
                        await asyncio.sleep(random.uniform(2, 5))
                        return await fetch_page_async(url, headers, timeout, retry_count + 1)
                return response
        except Exception as e:
            logging.debug(f"curl_cffi engine failed for {url}: {e}. Falling back to httpx.")
            # Continue to Engine 2

    # [[crown] ENGINE 2: httpx] - Secondary/Fallback Engine
    try:
        async with httpx.AsyncClient(
            timeout=timeout,
            follow_redirects=True,
            proxy=proxy
        ) as client:
            response = await client.get(url, headers=stealth_headers)
            if response.status_code == 403 or response.status_code == 429:
                permanently_blocked = _record_domain_block(url)
                if not permanently_blocked:
                    logging.warning(f"âš ï¸ [HTTPX] Blocked (HTTP {response.status_code}) on {url}")
                else:
                    logging.debug(f" [HTTPX] Domain persistently blocked, skipping silently: {url[:60]}")
                _evasion.rotate_ua()
                await asyncio.sleep(random.uniform(2, 5))
                if retry_count < 2 and not permanently_blocked:
                    return await fetch_page_async(url, headers, timeout, retry_count + 1)
            return response
    except Exception as e:
        logging.debug(f"Request failed for {url}: {e}")
        _evasion.rotate_ua()
        if retry_count < 1:
             await asyncio.sleep(random.uniform(1, 3))
             return await fetch_page_async(url, headers, timeout, retry_count + 1)
        return None

def fetch_page(url, headers, timeout=15, retry_count=0):
    """Legacy wrapper for synchronous calls"""
    return asyncio.run(fetch_page_async(url, headers, timeout, retry_count))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def extract_email(text):
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    # Filter out common non-career emails
    filtered = [e for e in emails if not any(b in e.lower() for b in 
        ['example.com', 'test.com', 'noreply', 'no-reply', 'donotreply', 'support@', 'admin@'])]
    return filtered[0] if filtered else None

def get_job_email_and_desc(job_url, headers):
    """Extract email and description from job detail page."""
    try:
        is_github = os.getenv('GITHUB_ACTIONS') == 'true'
        if is_github:
            time.sleep(random.uniform(0.5, 1.5))
        else:
            time.sleep(random.uniform(1.5, 3.0))

        response = fetch_page(job_url, headers=headers, timeout=20)
        if response.status_code != 200:
            return None, ""

        soup = BeautifulSoup(response.content, 'html.parser')

        # Try mailto link first
        mailto = soup.select_one('a[href^="mailto:"]')
        if mailto:
            email = mailto['href'].replace('mailto:', '').split('?')[0]
            return email, ""

        # Check for apply buttons
        apply_btn = soup.select_one('a[href*="apply"], button[data-action="apply"]')
        if apply_btn:
            href = apply_btn.get('href', '')
            if 'mailto:' in href:
                return href.split('mailto:')[1].split('?')[0], ""

        # Extract from page text
        all_text = soup.get_text()
        # Email extraction regex
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = list(set(re.findall(email_regex, all_text)))
        # Filter out common non-career emails
        bad_emails = ['example.com', 'test.com', 'noreply', 'no-reply', 'donotreply', 'support@', 'admin@']
        valid_emails = [e for e in emails if not any(b in e.lower() for b in bad_emails)]
        if valid_emails:
            email = valid_emails[0]
            clean_text = ' '.join(all_text.split())
            description_snippet = clean_text[:2000]
            return email, description_snippet

        return None, ""

    except Exception as e:
        logging.debug(f"Error extracting data: {e}")
        return None, ""

# ENHANCED: More pages, faster scraping
async def scrape_daleel_page(page, user_agents, base_url, site_patch):
    url = f"{base_url}?page={page}"
    headers = {
        'User-Agent': random.choice(user_agents),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-GB,en;q=0.9,en-US;q=0.8',
        'Referer': 'https://www.google.com/',
    }
    
    response = await fetch_page_async(url, headers=headers)
    if not response or response.status_code != 200:
        return []

    soup = BeautifulSoup(response.content, 'html.parser')
    job_cards = soup.select(site_patch.get("job_card", ".views-row")) or soup.select(".views-row")
    
    page_jobs = []
    if not job_cards:
        # Blind extraction fallback
        raw_text = response.text
        email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
        emails = list(set(re.findall(email_regex, raw_text)))
        bad_emails = ['example.com', 'test.com', 'noreply', 'no-reply', 'donotreply', 'support@', 'admin@', 'press@', 'login@', 'die@']
        valid_emails = [e for e in emails if not any(b in e.lower() for b in bad_emails)]
        for email in valid_emails:
            domain = email.split('@')[1].lower()
            if any(x in domain for x in ['twitter.com', 'facebook.com', 'linkedin.com', 'google.com']): continue
            page_jobs.append({
                "company_name": email.split('@')[1].split('.')[0].capitalize(),
                "email": email,
                "location": "Lebanon",
                "job_title": "Strategic Lead",
                "description": "Found via directory re-con.",
                "link": url,
                "source_board": "Daleel_Blind"
            })
        return page_jobs

    for card in job_cards:
        try:
            title_elem = card.select_one(".views-field-title a") or card.select_one("h2 a")
            if not title_elem: continue
            
            job_title = title_elem.get_text(strip=True)
            job_link = title_elem['href']
            if job_link.startswith('/'): job_link = "https://daleel-madani.org" + job_link
            
            company_elem = card.select_one(".views-field-field-job-employer a") or card.select_one(".views-field-field-organization")
            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
            
            # Deep dive for email (optional async)
            email, desc = await get_job_email_and_desc_async(job_link, headers)
            if email:
                page_jobs.append({
                    "company_name": company,
                    "email": email,
                    "location": "Lebanon",
                    "job_title": job_title,
                    "description": desc or "No description found.",
                    "link": job_link,
                    "source_board": "daleel-madani"
                })
        except: continue
    return page_jobs

async def get_job_email_and_desc_async(url, headers):
    resp = await fetch_page_async(url, headers)
    if not resp or resp.status_code != 200: return None, ""
    soup = BeautifulSoup(resp.content, 'html.parser')
    # Basic email extraction
    all_text = soup.get_text()
    emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', all_text)
    valid = [e for e in emails if not any(b in e.lower() for b in ['example', 'test', 'noreply'])]
    return (valid[0], all_text[:1000]) if valid else (None, "")

async def scrape_new_companies_async():
    """BYPASS MODE: Delegates to daleel_parallel_scan (search-engine queries).
    Direct HTTP to daleel-madani.org returns 403 on every request."""
    from core.scrapers.daleel_parallel import daleel_parallel_scan
    return await daleel_parallel_scan(db=None)

def scrape_new_companies():
    # [[shield] FIX]: Use get_event_loop() instead of asyncio.run() to avoid event loop conflicts
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # If loop is already running, create a task instead
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(asyncio.run, scrape_new_companies_async())
                return future.result()
        else:
            return loop.run_until_complete(scrape_new_companies_async())
    except RuntimeError:
        # Fallback: create new event loop
        return asyncio.run(scrape_new_companies_async())


# ============================================================================
# NEW: More job boards for maximum coverage
# ============================================================================

def scrape_glassdoor_jobs():
    """Scrape Glassdoor jobs"""
    jobs = []
    keywords = ["Network Engineer", "Senior Network Engineer", "IT Infrastructure Engineer", "Network Administrator"]
    locations = ["Lebanon", "Dubai", "UAE", "Qatar", "Saudi Arabia"]
    
    for kw in keywords:
        for loc in locations[:2]:
            try:
                headers = {
                    'User-Agent': random.choice([
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    ])
                }
                url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(kw)}&locT=C&locKeyword={urllib.parse.quote(loc)}"
                time.sleep(random.uniform(2.0, 4.0))
                response = fetch_page(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select("[class*='jobListing']")[:10]
                    
                    for card in cards:
                        try:
                            title_elem = card.select_one("[class*='title'], h2 a, h3 a")
                            company_elem = card.select_one("[class*='company'], span:has(a)")
                            
                            if title_elem:
                                job_title = title_elem.get_text(strip=True)
                                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                                
                                if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                    safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                                    jobs.append({
                                        "company_name": company,
                                        "email": "",
                                        "location": loc,
                                        "salary": "0",
                                        "job_title": job_title,
                                        "description": "",
                                        "link": "",
                                        "source_board": "glassdoor"
                                    })
                        except Exception:
                            continue
            except Exception as e:
                logging.debug(f"Glassdoor scrape failed: {e}")
    
    return jobs


def scrape_indeed_jobs(location="Lebanon"):
    """Scrape Indeed jobs"""
    jobs = []
    keywords = ["Network Engineer", "Senior Network Engineer", "IT Infrastructure", "Network Administrator", "Systems Administrator", "Network Security Engineer"]
    
    for kw in keywords:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            }
            url = f"https://www.indeed.com/jobs?q={urllib.parse.quote(kw)}&l={urllib.parse.quote(location)}"
            time.sleep(random.uniform(2.0, 4.0))
            response = fetch_page(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select(".job_seen_behind")[:15]
                
                for card in cards:
                    try:
                        title_elem = card.select_one("h2.jobTitle a, a.jobtitle")
                        company_elem = card.select_one("span.companyName, .company")
                        salary_elem = card.select_one(".salary-snippet, .estimated-salary")
                        
                        if title_elem:
                            job_title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            salary = salary_elem.get_text(strip=True) if salary_elem else "0"
                            job_link = title_elem.get('href', '')
                            if job_link and not job_link.startswith('http'):
                                job_link = "https://www.indeed.com" + job_link
                            
                            if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                                jobs.append({
                                    "company_name": company,
                                    "email": "",
                                    "location": location,
                                    "salary": salary.replace('$', '').replace(',', ''),
                                    "job_title": job_title,
                                    "description": "",
                                    "link": job_link,
                                    "source_board": "indeed"
                                })
                    except Exception:
                        continue
        except Exception as e:
            logging.debug(f"Indeed scrape failed: {e}")
    
    return jobs


def scrape_careerbuilder_jobs():
    """Scrape CareerBuilder jobs"""
    jobs = []
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        keywords = ["Network Engineer", "IT Infrastructure", "Network Administrator", "Systems Administrator"]
        
        for kw in keywords:
            url = f"https://www.careerbuilder.com/jobs/hr-in-lebanon?keywords={urllib.parse.quote(kw)}"
            time.sleep(random.uniform(2.0, 4.0))
            response = fetch_page(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select(".job-card")[:10]
                
                for card in cards:
                    try:
                        title_elem = card.select_one(".job-title a, h2 a")
                        company_elem = card.select_one(".company-name")
                        
                        if title_elem:
                            job_title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            
                            if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                                jobs.append({
                                    "company_name": company,
                                    "email": "",
                                    "location": "Lebanon",
                                    "salary": "0",
                                    "job_title": job_title,
                                    "description": "",
                                    "link": "",
                                    "source_board": "careerbuilder"
                                })
                    except Exception:
                        continue
    except Exception as e:
        logging.debug(f"CareerBuilder scrape failed: {e}")
    
    return jobs


# ENHANCED: More job boards
def scrape_jobportals():
    """Additional job boards for maximum coverage"""
    jobs = []
    
    # Job portals to scrape
    portals = [
        {
            "name": "Wazajobs",
            "url": "https://www.wazajobs.com/search?search=hr",
            "cards": ".job-card",
            "title": "h3 a",
            "company": ".company-name"
        },
        {
            "name": "CareerNext",
            "url": "https://www.careernext.ai/jobs?query=hr",
            "cards": ".job-listing",
            "title": ".job-title",
            "company": ".company"
        },
        {
            "name": "GulfTalent",
            "url": "https://www.gulftalent.com/jobs/hr",
            "cards": ".job-tile",
            "title": "h3",
            "company": ".company-name"
        },
        {
            "name": "Dubizzle",
            "url": "https://www.dubizzle.com.ae/jobs/hr/",
            "cards": ".listing-card",
            "title": ".title",
            "company": ".listing-user"
        },
        {
            "name": "NaukriGulf",
            "url": "https://www.naukrigulf.com/hr-jobs/",
            "cards": ".job-list-item",
            "title": ".job-heading a",
            "company": ".company-name"
        },
    ]
    
    for portal in portals:
        try:
            headers = {
                'User-Agent': random.choice([
                    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                ])
            }
            time.sleep(random.uniform(2.0, 4.0))
            response = fetch_page(portal["url"], headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select(portal["cards"])
                
                # BLIND EXTRACTION OVERRIDE
                if not cards:
                    logging.warning(f"âš ï¸ {portal['name']} HTML structure changed or blocked! Executing RAW BLIND EXTRACT...")
                    raw_text = response.text
                    # Email extraction regex
                    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                    emails = list(set(re.findall(email_regex, raw_text)))
                    # Filter out common non-career emails
                    bad_emails = ['example.com', 'test.com', 'noreply', 'no-reply', 'donotreply', 'support@', 'admin@']
                    valid_emails = [e for e in emails if not any(b in e.lower() for b in bad_emails)]

                    if not valid_emails:
                        domain = urllib.parse.urlparse(portal["url"]).netloc.replace("www.", "")
                        # Skip fake domain email - recon surge will find real contact

                    for email in valid_emails:
                        jobs.append({
                            "company_name": email.split('@')[1].split('.')[0].capitalize(),
                            "email": email,
                            "location": "Gulf Region",
                            "salary": "0",
                            "job_title": "Regional Role",
                            "description": "Blindly extracted lead.",
                            "link": portal["url"],
                            "platform": portal["name"] + "_Blind"
                        })
                    continue

                logging.info(f" {portal['name']}: {len(cards)} structured jobs")
                
                for card in cards[:15]:
                    try:
                        title_elem = card.select_one(portal["title"])
                        company_elem = card.select_one(portal["company"])
                        
                        if title_elem:
                            job_title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            
                            if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                                jobs.append({
                                    "company_name": company,
                                    "email": "",
                                    "location": "Gulf",
                                    "salary": "0",
                                    "job_title": job_title,
                                    "description": "",
                                    "link": "",
                                    "source_board": portal["name"].lower()
                                })
                    except Exception:
                        continue
        except Exception as e:
            logging.debug(f"{portal['name']} failed: {e}")
    
    return jobs


def get_latest_jobs():
    """Aggregates MAXIMUM jobs from all sources"""
    import gc
    global TOTAL_DEEP_DIVES
    _reset_deep_dive()  # Reset counter for new scrape cycle
    
    all_jobs = []

    # Primary Sources
    try:
        all_jobs += scrape_new_companies()
    except Exception as e:
        logging.error(f"Daleel Error: {e}")

    try:
        all_jobs += scrape_linkedin_jobs()
    except Exception as e:
        logging.error(f"LinkedIn Error: {e}")

    # [[shield] 403-FIX]: Bayt, Indeed, Glassdoor, and job portals consistently return HTTP 403.
    # They are already covered by OmniCrawler's search-engine bypass (site: queries via DDG).
    # Disabling direct HTTP scrapers to save memory and prevent wasted connections.
    logging.info("Skipping direct Bayt/Indeed/Glassdoor scrapers (covered by OmniCrawler DDG bypass)")

    try:
        all_jobs += scrape_monster_jobs()
    except Exception as e:
        logging.error(f"Monster Error: {e}")

    # [ OOM-FIX]: Force garbage collection after heavy scraping
    gc.collect()

    # Remove duplicates
    unique_jobs = []
    seen = set()
    for j in all_jobs:
        key = j.get('company_name', '') + j.get('job_title', '')
        if key and key not in seen:
            seen.add(key)
            unique_jobs.append(j)
            try:
                from core.db_manager import db_manager
                db_manager.sync_save_potential_lead(j, score=80)
            except Exception as e:
                logging.debug(f"Failed to persist lead: {e}")
            
    logging.info(f" Total unique jobs: {len(unique_jobs)} (Deep dives: {TOTAL_DEEP_DIVES})")
    gc.collect()  # Final cleanup
    return unique_jobs

def scrape_linkedin_jobs(location="Lebanon", keyword="HR"):
    """Enhanced LinkedIn scraper"""
    logging.info(f" LinkedIn: {keyword} in {location}")
    
    jobs = []
    keywords = ["HR", "Human Resources", "Operations Manager", "Admin", "Recruiter", "Office Manager"]
    locations = ["Lebanon", "Dubai", "Remote", "Saudi Arabia", "Gulf"]
    
    for kw in keywords:
        for loc in locations[:2]:  # Limit to avoid bans
            try:
                q_kw = urllib.parse.quote(kw)
                q_loc = urllib.parse.quote(loc)
                url = f"https://www.linkedin.com/jobs/search?keywords={q_kw}&location={q_loc}"
                
                headers = {
                    'User-Agent': random.choice([
                        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
                    ])
                }
                
                time.sleep(random.uniform(3.0, 5.0))
                response = fetch_page(url, headers=headers, timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select(".base-card")[:8]
                    
                    for card in cards:
                        try:
                            title_elem = card.select_one(".base-search-card__title")
                            company_elem = card.select_one(".base-search-card__subtitle")
                            link_elem = card.select_one("a.base-card__full-link")
                            
                            if title_elem and link_elem:
                                job_title = title_elem.get_text(strip=True)
                                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                                job_link = link_elem.get('href', '').split('?')[0]
                                
                                if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                    safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                                    jobs.append({
                                        "company_name": company,
                                        "email": "",
                                        "location": loc,
                                        "salary": "0",
                                        "job_title": job_title,
                                        "description": "",
                                        "link": job_link,
                                        "source_board": "linkedin"
                                    })
                        except Exception:
                            continue
            except Exception as e:
                continue
    
    return jobs

def scrape_hirelebanese_jobs():
    """Enhanced HireLebanese scraper"""
    logging.info(" HireLebanese...")
    jobs = []
    keywords = ["HR", "Human Resources", "Administration", "Operations", "Assistant", "Coordinator", "Manager"]
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for keyword in keywords:
        try:
            url = f"https://www.hirelebanese.com/searchresults.aspx?order=date&country=117&keywords={urllib.parse.quote(keyword)}"
            time.sleep(random.uniform(2.0, 4.0))
            response = fetch_page(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select(".panel.panel-default")[:15]
                
                for card in cards:
                    try:
                        title_elem = card.select_one("h4 a")
                        if title_elem:
                            job_title = title_elem.get_text(strip=True)
                            job_link = title_elem['href']
                            if not job_link.startswith("http"):
                                job_link = "https://www.hirelebanese.com/" + job_link
                            
                            card_text = card.get_text("|", strip=True).split("|")
                            company = card_text[1] if len(card_text) > 1 else "Unknown"
                            
                            if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                email, desc = get_job_email_and_desc(job_link, headers)
                                safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                                jobs.append({
                                    "company_name": company,
                                    "email": email or "",
                                    "location": "Lebanon",
                                    "salary": "0",
                                    "job_title": job_title,
                                    "description": desc,
                                    "link": job_link,
                                    "source_board": "hirelebanese"
                                })
                    except Exception:
                        continue
        except Exception as e:
            continue
    
    return jobs

def scrape_bayt_jobs(location="lebanon", keyword="hr"):
    """Enhanced Bayt scraper"""
    logging.info(f" Bayt: {keyword}")
    jobs = []
    
    keywords = ["hr", "human resources", "operations", "admin", "recruiter", "office manager"]
    
    headers = {
        'User-Agent': random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        ])
    }
    
    for kw in keywords:
        try:
            url = f"https://www.bayt.com/en/{location}/jobs/q/{kw}/"
            time.sleep(random.uniform(2.0, 4.0))
            response = fetch_page(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select("li.has-pointer-d")[:12]
                
                for card in cards:
                    try:
                        title_elem = card.select_one("h2.job-title a")
                        company_elem = card.select_one("b.job-company-name")
                        
                        if title_elem:
                            job_title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                            
                            if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                jobs.append({
                                    "company_name": company,
                                    "email": "",
                                    "location": location,
                                    "salary": "0",
                                    "job_title": job_title,
                                    "description": "",
                                    "link": "https://www.bayt.com" + title_elem['href'],
                                    "source_board": "bayt"
                                })
                    except Exception:
                        continue
        except Exception as e:
            continue
    
    return jobs

def scrape_monster_jobs(location="Lebanon", keyword="HR"):
    """Enhanced Monster scraper"""
    logging.info(f" Monster/Foundit...")
    jobs = []
    
    keywords = ["HR", "Operations", "Admin", "Recruiter"]
    
    for kw in keywords:
        try:
            url = f"https://www.founditgulf.com/srp/results?query={urllib.parse.quote(kw)}&locations={urllib.parse.quote(location)}"
            headers = random.choice([
                {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'},
                {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'}
            ])
            
            time.sleep(random.uniform(2.0, 4.0))
            response = fetch_page(url, headers=headers, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select(".srp-result-card")[:10]
                
                for card in cards:
                    try:
                        title_elem = card.select_one(".job-t") or card.select_one("h2")
                        company_elem = card.select_one(".company-name")
                        
                        if title_elem:
                            job_title = title_elem.get_text(strip=True)
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            safe_company = "".join(c for c in company if c.isalnum() or c in ' -').strip()
                            
                            if not db_manager.sync_is_duplicate(job_link or company + job_title):
                                jobs.append({
                                    "company_name": company,
                                    "email": "",
                                    "location": location,
                                    "salary": "0",
                                    "job_title": job_title,
                                    "description": "",
                                    "link": "",
                                    "source_board": "monster"
                                })
                    except Exception:
                        continue
        except Exception as e:
            continue
    
    return jobs

