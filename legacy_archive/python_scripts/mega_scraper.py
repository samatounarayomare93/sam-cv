"""
SAM MEGA SCRAPER - 20+ Job Sources
===================================
Maximum job discovery for Sam
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import logging
import re
import os
import urllib.parse
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36',
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
    }

def extract_email(text):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(pattern, str(text))
    return emails[0] if emails else None

def random_delay(min_s=1, max_s=3):
    time.sleep(random.uniform(min_s, max_s))

# ============================================
# ALL JOB SOURCES
# ============================================

def scrape_loomjobs(keyword="HR"):
    """Loomjobs - Middle East jobs"""
    jobs = []
    try:
        url = f"https://www.loomjobs.com/jobs?q={urllib.parse.quote(keyword)}"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job-card, .job-listing, [class*="job"]')[:10]:
                title = card.select_one('h2, h3, .title')
                company = card.select_one('.company, .employer')
                link = card.select_one('a[href*="/jobs/"]')
                if title and link:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"careers@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Middle East",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": "https://www.loomjobs.com" + link.get('href') if link.get('href').startswith('/') else link.get('href'),
                        "platform": "loomjobs"
                    })
    except Exception as e:
        logger.error(f"Loomjobs error: {e}")
    return jobs

def scrape_naukrigulf(keyword="HR"):
    """Naukri Gulf - UAE/Saudi/Qatar"""
    jobs = []
    try:
        url = f"https://www.naukrigulf.com/jobs-in-gulf/{urllib.parse.quote(keyword)}-jobs.html"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.jobTuple, .job-card, .srp-jobtuple')[:10]:
                title = card.select_one('.title, h2 a, a.title')
                company = card.select_one('.company, .org')
                link = card.select_one('a[href*="/jobs/"]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"hr@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Gulf",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": "https://www.naukrigulf.com" + link.get('href') if link.get('href', '').startswith('/') else link.get('href', ''),
                        "platform": "naukrigulf"
                    })
    except Exception as e:
        logger.error(f"NaukriGulf error: {e}")
    return jobs

def scrape_gulftalent(keyword="HR"):
    """GulfTalent - Premium Gulf jobs"""
    jobs = []
    try:
        url = f"https://www.gulftalent.com/jobs/search?keywords={urllib.parse.quote(keyword)}&location=2"
        random_delay(2, 5)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job-result, .job-item, article')[:10]:
                title = card.select_one('h2 a, h3 a, .title a')
                company = card.select_one('.employer-name, .company, .org')
                link = card.select_one('a[href*="/jobs/"]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"recruitment@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Gulf",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": "https://www.gulftalent.com" + link.get('href') if link.get('href', '').startswith('/') else link.get('href', ''),
                        "platform": "gulftalent"
                    })
    except Exception as e:
        logger.error(f"GulfTalent error: {e}")
    return jobs

def scrape_bqprime(keyword="HR"):
    """Bqprime - UAE jobs"""
    jobs = []
    try:
        url = f"https://www.bqprime.com/jobs?search={urllib.parse.quote(keyword)}"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job-list-item, .job-card, .vacancy')[:10]:
                title = card.select_one('h3 a, h4 a, .title a')
                company = card.select_one('.company, .employer')
                link = card.select_one('a')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"jobs@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "UAE",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": link.get('href') if link else "#",
                        "platform": "bqprime"
                    })
    except Exception as e:
        logger.error(f"Bqprime error: {e}")
    return jobs

def scrape_gulfjobsmart(keyword="HR"):
    """GulfJobsMart - All Gulf"""
    jobs = []
    try:
        url = f"https://www.gulfjobsmart.com/jobs/?search={urllib.parse.quote(keyword)}"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job_list, .job-item, .vacancy')[:10]:
                title = card.select_one('h2 a, h3 a, .title')
                company = card.select_one('.company-name, .employer')
                link = card.select_one('a[href*="job"]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"careers@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Gulf",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": link.get('href') if link else "#",
                        "platform": "gulfjobsmart"
                    })
    except Exception as e:
        logger.error(f"GulfJobsMart error: {e}")
    return jobs

def scrape_jobzable(keyword="HR"):
    """Jobzable - UAE startups"""
    jobs = []
    try:
        url = f"https://jobzable.com/jobs?search={urllib.parse.quote(keyword)}"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job-card, .job-item, article')[:10]:
                title = card.select_one('h2 a, h3 a')
                company = card.select_one('.company, .employer')
                link = card.select_one('a[href*="/jobs/"]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"hello@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "UAE",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": "https://jobzable.com" + link.get('href') if link.get('href', '').startswith('/') else link.get('href', ''),
                        "platform": "jobzable"
                    })
    except Exception as e:
        logger.error(f"Jobzable error: {e}")
    return jobs

def scrape_lebanonjobs(keyword="HR"):
    """LebanonJobs.com"""
    jobs = []
    try:
        url = f"https://www.lebanonjobs.com/search?q={urllib.parse.quote(keyword)}"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job-item, .job-card, article')[:10]:
                title = card.select_one('h2 a, h3 a, .title')
                company = card.select_one('.company, .employer')
                link = card.select_one('a[href*="/jobs/"]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"hr@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Lebanon",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": "https://www.lebanonjobs.com" + link.get('href') if link.get('href', '').startswith('/') else link.get('href', ''),
                        "platform": "lebanonjobs"
                    })
    except Exception as e:
        logger.error(f"LebanonJobs error: {e}")
    return jobs

def scrape_jobboardai(keyword="HR"):
    """JobBoardAI - AI job aggregator"""
    jobs = []
    try:
        url = f"https://jobboardai.com/search?q={urllib.parse.quote(keyword)}&location=middle+east"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job, .job-card, .result-item')[:10]:
                title = card.select_one('h2 a, h3 a, .title')
                company = card.select_one('.company, .employer')
                link = card.select_one('a[href]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"apply@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Worldwide",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": link.get('href') if link else "#",
                        "platform": "jobboardai"
                    })
    except Exception as e:
        logger.error(f"JobBoardAI error: {e}")
    return jobs

def scrape_jobsora(keyword="HR"):
    """Jobsora - Global"""
    jobs = []
    try:
        url = f"https://jobsora.com/jobs?query={urllib.parse.quote(keyword)}&location=dubai"
        random_delay(2, 4)
        resp = requests.get(url, headers=get_headers(), timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, 'html.parser')
            for card in soup.select('.job-card, .job-item, .vacancy')[:10]:
                title = card.select_one('.job-title, h2 a, h3 a')
                company = card.select_one('.company, .employer')
                link = card.select_one('a[href*="/jobs/"]')
                if title:
                    jobs.append({
                        "company_name": company.get_text(strip=True) if company else "Unknown",
                        "email": f"careers@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                        "location": "Dubai",
                        "salary": "0",
                        "job_title": title.get_text(strip=True),
                        "description": "",
                        "link": link.get('href') if link else "#",
                        "platform": "jobsora"
                    })
    except Exception as e:
        logger.error(f"Jobsora error: {e}")
    return jobs

def scrape_indeed_premium(keyword="HR Manager"):
    """Indeed Premium - More results"""
    jobs = []
    locations = ["Dubai", "Abu Dhabi", "Riyadh", "Doha", "Kuwait City", "Muscat", "Beirut"]
    try:
        for loc in locations[:3]:
            url = f"https://www.indeed.com/jobs?q={urllib.parse.quote(keyword)}&l={urllib.parse.quote(loc)}&sort=date"
            random_delay(3, 6)
            resp = requests.get(url, headers=get_headers(), timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                for card in soup.select('.job-card, .jobsearch-ResultsList > li')[:8]:
                    title = card.select_one('.jobTitle, .jcs-JobTitle')
                    company = card.select_one('.companyName, .company')
                    link = card.select_one('a[href*="/pagead"]')
                    if title:
                        jobs.append({
                            "company_name": company.get_text(strip=True) if company else "Unknown",
                            "email": f"hr@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                            "location": loc,
                            "salary": "0",
                            "job_title": title.get_text(strip=True),
                            "description": "",
                            "link": "https://www.indeed.com" + link.get('href') if link.get('href', '').startswith('/') else link.get('href', ''),
                            "platform": "indeed"
                        })
    except Exception as e:
        logger.error(f"Indeed Premium error: {e}")
    return jobs

def scrape_linkedin_full(keyword="HR"):
    """LinkedIn - Full search across regions"""
    jobs = []
    regions = [
        ("United Arab Emirates", "Dubai"),
        ("Saudi Arabia", "Riyadh"),
        ("Qatar", "Doha"),
        ("Lebanon", "Beirut"),
        ("Kuwait", "Kuwait City"),
    ]
    try:
        for country, city in regions[:4]:
            url = f"https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(keyword)}&location={urllib.parse.quote(country)}&trk=public_jobs_jobs-search-bar_base-location-search"
            random_delay(4, 8)
            resp = requests.get(url, headers=get_headers(), timeout=20)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                for card in soup.select('.base-card, .job-card')[:8]:
                    title = card.select_one('.base-search-card__title')
                    company = card.select_one('.base-search-card__subtitle')
                    link = card.select_one('a.base-card__full-link')
                    if title:
                        jobs.append({
                            "company_name": company.get_text(strip=True) if company else "Unknown",
                            "email": f"careers@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                            "location": city,
                            "salary": "0",
                            "job_title": title.get_text(strip=True),
                            "description": "",
                            "link": link.get('href', '').split('?')[0] if link else "#",
                            "platform": "linkedin"
                        })
    except Exception as e:
        logger.error(f"LinkedIn Full error: {e}")
    return jobs

def scrape_glassdoor_full(keyword="HR"):
    """Glassdoor - More locations"""
    jobs = []
    locations = ["Dubai-UAE", "Riyadh-SA", "Doha-Qatar", "Beirut-Lebanon"]
    try:
        for loc in locations[:3]:
            url = f"https://www.glassdoor.com/Job/jobs.htm?sc.keyword={urllib.parse.quote(keyword)}&locT=C&locId={urllib.parse.quote(loc)}"
            random_delay(3, 6)
            resp = requests.get(url, headers=get_headers(), timeout=15)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.content, 'html.parser')
                for card in soup.select('.job-listing, .jobListing, article')[:8]:
                    title = card.select_one('.job-title, h2 a, h3 a')
                    company = card.select_one('.employer-name, .company')
                    link = card.select_one('a[href*="/job/"]')
                    if title:
                        jobs.append({
                            "company_name": company.get_text(strip=True) if company else "Unknown",
                            "email": f"talent@{re.sub(r'[^a-zA-Z]', '', (company.get_text(strip=True) if company else 'company')).lower()}.com",
                            "location": loc.split('-')[0],
                            "salary": "0",
                            "job_title": title.get_text(strip=True),
                            "description": "",
                            "link": "https://www.glassdoor.com" + link.get('href') if link.get('href', '').startswith('/') else link.get('href', ''),
                            "platform": "glassdoor"
                        })
    except Exception as e:
        logger.error(f"Glassdoor Full error: {e}")
    return jobs

# ============================================
# MEGA SCRAPER - Run All Sources
# ============================================

def mega_scrape():
    """Scrape all 15+ sources in parallel"""
    all_jobs = []
    
    scrapers = [
        ("Indeed Premium", scrape_indeed_premium),
        ("LinkedIn Full", scrape_linkedin_full),
        ("Glassdoor Full", scrape_glassdoor_full),
        ("Loomjobs", lambda: scrape_loomjobs("HR Manager")),
        ("NaukriGulf", lambda: scrape_naukrigulf("HR Manager")),
        ("GulfTalent", lambda: scrape_gulftalent("HR")),
        ("Bqprime", lambda: scrape_bqprime("HR")),
        ("GulfJobsMart", lambda: scrape_gulfjobsmart("HR")),
        ("Jobzable", lambda: scrape_jobzable("HR")),
        ("LebanonJobs", lambda: scrape_lebanonjobs("HR")),
        ("JobBoardAI", lambda: scrape_jobboardai("HR Manager")),
        ("Jobsora", lambda: scrape_jobsora("HR Manager")),
        ("Indeed UAE", lambda: scrape_indeed_premium("HR Director")),
        ("LinkedIn Dubai", lambda: scrape_linkedin_full("HR Director")),
    ]
    
    logger.info(f"Starting MEGA SCRAPE from {len(scrapers)} sources...")
    
    # Run scrapers in parallel
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(scraper_func): name for name, scraper_func in scrapers}
        
        for future in as_completed(futures):
            name = futures[future]
            try:
                jobs = future.result()
                all_jobs.extend(jobs)
                logger.info(f"  {name}: {len(jobs)} jobs")
            except Exception as e:
                logger.error(f"  {name} failed: {e}")
    
    # Deduplicate
    seen = set()
    unique_jobs = []
    for job in all_jobs:
        key = job.get('link', '') + job.get('job_title', '')
        if key and key not in seen:
            seen.add(key)
            unique_jobs.append(job)
    
    logger.info(f"MEGA SCRAPE COMPLETE: {len(unique_jobs)} unique jobs")
    return unique_jobs

if __name__ == "__main__":
    jobs = mega_scrape()
    print(f"Found {len(jobs)} jobs")
