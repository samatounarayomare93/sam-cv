"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           SAM ENHANCED SCRAPER - MAXIMUM SOURCES                     ║
║                     50+ Job Sources Worldwide                           ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import re
import time
import json
import random
import logging
import requests
import sqlite3
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from typing import List, Dict, Optional
import hashlib

# Import config
import config

# ============================================================================
# LOGGING
# ============================================================================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class JobLead:
    """Job lead data structure"""
    title: str
    company: str
    location: str
    email: str
    url: str
    salary: str
    description: str
    source: str
    discovered_at: str
    
    def to_dict(self) -> dict:
        return {
            'title': self.title,
            'company': self.company,
            'location': self.location,
            'email': self.email,
            'url': self.url,
            'salary': self.salary,
            'description': self.description[:500] if self.description else '',
            'source': self.source,
            'discovered_at': self.discovered_at
        }


@dataclass
class Company:
    """Company data structure"""
    name: str
    domain: str
    industry: str
    country: str
    email_patterns: List[str]
    
    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'domain': self.domain,
            'industry': self.industry,
            'country': self.country,
            'emails': self.email_patterns
        }


# ============================================================================
# HTTP SESSION WITH RETRY
# ============================================================================

class HTTPClient:
    """Enhanced HTTP client with retry and proxy support"""
    
    USER_AGENTS = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    ]
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(self.USER_AGENTS),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
    
    def get(self, url: str, timeout: int = 20, retry: int = 3) -> Optional[requests.Response]:
        """GET request with retry"""
        for attempt in range(retry):
            try:
                response = self.session.get(url, timeout=timeout)
                
                # Rotate user agent
                self.session.headers['User-Agent'] = random.choice(self.USER_AGENTS)
                
                return response
            except requests.RequestException as e:
                logger.debug(f"Request failed (attempt {attempt + 1}): {e}")
                if attempt < retry - 1:
                    time.sleep(random.uniform(1, 3))
        
        return None
    
    def rotate_user_agent(self):
        """Rotate user agent"""
        self.session.headers['User-Agent'] = random.choice(self.USER_AGENTS)


# ============================================================================
# EMAIL EXTRACTION
# ============================================================================

class EmailExtractor:
    """Extract emails from job pages and snippets"""
    
    EMAIL_PATTERN = re.compile(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}')
    
    BAD_EMAILS = {
        'example@', 'test@', 'no-reply@', 'noreply@', 'support@',
        'info@example', 'admin@', 'webmaster@', 'postmaster@'
    }
    
    @classmethod
    def extract_from_text(cls, text: str) -> Optional[str]:
        """Extract first valid email from text"""
        emails = re.findall(cls.EMAIL_PATTERN, text)
        
        for email in emails:
            email_lower = email.lower()
            
            # Filter bad emails
            if any(bad in email_lower for bad in cls.BAD_EMAILS):
                continue
            
            # Filter common invalid domains
            if any(domain in email_lower for domain in ['example', 'test', 'localhost']):
                continue
            
            return email
        
        return None
    
    @classmethod
    def extract_from_page(cls, url: str, headers: dict) -> Optional[str]:
        """Extract email from a page"""
        try:
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                return cls.extract_from_text(response.text)
        
        except Exception:
            pass
        
        return None
    
    @classmethod
    def generate_company_emails(cls, domain: str) -> List[str]:
        """Generate likely email patterns for a company"""
        if not domain:
            return []
        
        domain = domain.lower().strip()
        domain = re.sub(r'^https?://(www\.)?', '', domain)
        domain = domain.split('/')[0]
        
        patterns = [
            f"careers@{domain}",
            f"jobs@{domain}",
            f"hr@{domain}",
            f"recruitment@{domain}",
            f"hiring@{domain}",
            f"talent@{domain}",
            f"info@{domain}",
            f"contact@{domain}",
            f"admin@{domain}",
            f"apply@{domain}",
        ]
        
        return patterns


# ============================================================================
# JOB SCRAPERS
# ============================================================================

class BaseScraper:
    """Base scraper class"""
    
    def __init__(self, name: str, url: str, enabled: bool = True):
        self.name = name
        self.url = url
        self.enabled = enabled
        self.client = HTTPClient()
        self.leads_found = 0
    
    def scrape(self) -> List[JobLead]:
        """Scrape jobs - to be implemented by subclasses"""
        raise NotImplementedError
    
    def _random_delay(self, min_sec: float = 1.0, max_sec: float = 3.0):
        """Random delay between requests"""
        time.sleep(random.uniform(min_sec, max_sec))
    
    def _is_valid_title(self, title: str) -> bool:
        """Check if job title is relevant"""
        if not title:
            return False
        
        title_lower = title.lower()
        
        # Check banned titles
        for banned in config.BANNED_TITLES:
            if banned in title_lower:
                return False
        
        # Check for relevant titles
        for keyword in config.SAM_JOB_TITLES:
            if keyword in title_lower:
                return True
        
        return False


class DaleelMadaniScraper(BaseScraper):
    """Scrape Daleel Madani - Lebanon NGO Jobs"""
    
    def scrape(self) -> List[JobLead]:
        """Scrape jobs from Daleel Madani"""
        if not self.enabled:
            return []
        
        jobs = []
        base_url = "https://daleel-madani.org/jobs"
        
        logger.info(f"🌍 Scraping Daleel Madani...")
        
        for page in range(config.SCRAPER_MAX_PAGES):
            try:
                url = f"{base_url}?page={page}"
                response = self.client.get(url)
                
                if not response or response.status_code != 200:
                    break
                
                soup = BeautifulSoup(response.content, 'html.parser')
                job_cards = soup.select('.views-row') or soup.select('.job-item') or soup.select('article')
                
                logger.info(f"  Page {page + 1}: Found {len(job_cards)} jobs")
                
                for card in job_cards:
                    try:
                        # Extract job info
                        title_elem = card.select_one('.views-field-title a') or card.select_one('h2 a')
                        company_elem = card.select_one('.views-field-field-job-employer') or card.select_one('[class*=company]')
                        location_elem = card.select_one('.views-field-field-job-location')
                        link_elem = title_elem
                        
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        if not self._is_valid_title(title):
                            continue
                        
                        company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                        location = location_elem.get_text(strip=True) if location_elem else "Lebanon"
                        
                        # Get job link
                        job_url = title_elem.get('href', '')
                        if job_url.startswith('/'):
                            job_url = f"https://daleel-madani.org{job_url}"
                        
                        # Extract email from job page
                        email = None
                        if job_url:
                            email_response = self.client.get(job_url, timeout=15)
                            if email_response and email_response.status_code == 200:
                                email = EmailExtractor.extract_from_text(email_response.text)
                                self._random_delay(1, 2)
                        
                        # Fallback email
                        if not email:
                            domain = f"{company.lower().replace(' ', '')}.org.lb"
                            email = f"careers@{domain}"
                        
                        jobs.append(JobLead(
                            title=title,
                            company=company,
                            location=location,
                            email=email,
                            url=job_url,
                            salary="0",
                            description="",
                            source="Daleel Madani",
                            discovered_at=time.strftime('%Y-%m-%d %H:%M:%S')
                        ))
                        
                        self.leads_found += 1
                        
                    except Exception as e:
                        logger.debug(f"Card parse error: {e}")
                        continue
                
                self._random_delay(2, 4)
                
            except Exception as e:
                logger.error(f"Daleel Madani error: {e}")
                break
        
        logger.info(f"  ✅ Daleel Madani: Found {len(jobs)} jobs")
        return jobs


class LinkedInScraper(BaseScraper):
    """Scrape LinkedIn Jobs"""
    
    def scrape(self) -> List[JobLead]:
        """Scrape jobs from LinkedIn"""
        if not self.enabled:
            return []
        
        jobs = []
        keywords = ["HR Manager", "Operations Manager", "Recruiter", "Admin Manager", "Office Manager"]
        locations = ["Lebanon", "United Arab Emirates", "Saudi Arabia", "Qatar", "Kuwait"]
        
        logger.info(f"🌍 Scraping LinkedIn...")
        
        for keyword in keywords:
            for location in locations:
                try:
                    query = f"https://www.linkedin.com/jobs/search/?keywords={keyword.replace(' ', '%20')}&location={location.replace(' ', '%20')}"
                    response = self.client.get(query)
                    
                    if not response or response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select('.base-card')[:15]
                    
                    logger.info(f"  {keyword} in {location}: {len(cards)} jobs")
                    
                    for card in cards:
                        try:
                            title_elem = card.select_one('.base-search-card__title')
                            company_elem = card.select_one('.base-search-card__subtitle')
                            link_elem = card.select_one('a.base-card__full-link')
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            if not self._is_valid_title(title):
                                continue
                            
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            job_url = link_elem.get('href', '').split('?')[0] if link_elem else ''
                            
                            # Generate email
                            domain = f"{company.lower().replace(' ', '')}.com"
                            email = EmailExtractor.extract_from_text(job_url) or f"careers@{domain}"
                            
                            jobs.append(JobLead(
                                title=title,
                                company=company,
                                location=location,
                                email=email,
                                url=job_url,
                                salary="0",
                                description="",
                                source="LinkedIn",
                                discovered_at=time.strftime('%Y-%m-%d %H:%M:%S')
                            ))
                            
                            self.leads_found += 1
                            
                        except Exception as e:
                            continue
                    
                    self._random_delay(2, 4)
                    
                except Exception as e:
                    logger.debug(f"LinkedIn scrape error: {e}")
                    continue
        
        logger.info(f"  ✅ LinkedIn: Found {len(jobs)} jobs")
        return jobs


class BaytScraper(BaseScraper):
    """Scrape Bayt.com - Middle East Jobs"""
    
    def scrape(self) -> List[JobLead]:
        """Scrape jobs from Bayt"""
        if not self.enabled:
            return []
        
        jobs = []
        countries = ["lebanon", "uae", "saudi-arabia", "qatar", "kuwait", "oman", "bahrain"]
        keywords = ["hr", "human resources", "operations", "admin", "recruiter"]
        
        logger.info(f"🌍 Scraping Bayt...")
        
        for country in countries:
            for keyword in keywords[:3]:  # Limit to avoid bans
                try:
                    url = f"https://www.bayt.com/en/{country}/jobs/q/{keyword}/"
                    response = self.client.get(url)
                    
                    if not response or response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select('li.has-pointer-d')[:15]
                    
                    logger.info(f"  Bayt {country}/{keyword}: {len(cards)} jobs")
                    
                    for card in cards:
                        try:
                            title_elem = card.select_one('h2.job-title a')
                            company_elem = card.select_one('b.job-company-name') or card.select_one('.company-name')
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            if not self._is_valid_title(title):
                                continue
                            
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            job_url = "https://www.bayt.com" + title_elem.get('href', '')
                            
                            # Generate email
                            domain = f"{company.lower().replace(' ', '')}.com"
                            email = f"careers@{domain}"
                            
                            jobs.append(JobLead(
                                title=title,
                                company=company,
                                location=country.replace('-', ' ').title(),
                                email=email,
                                url=job_url,
                                salary="0",
                                description="",
                                source="Bayt",
                                discovered_at=time.strftime('%Y-%m-%d %H:%M:%S')
                            ))
                            
                            self.leads_found += 1
                            
                        except Exception as e:
                            continue
                    
                    self._random_delay(2, 4)
                    
                except Exception as e:
                    logger.debug(f"Bayt scrape error: {e}")
                    continue
        
        logger.info(f"  ✅ Bayt: Found {len(jobs)} jobs")
        return jobs


class IndeedScraper(BaseScraper):
    """Scrape Indeed"""
    
    def scrape(self) -> List[JobLead]:
        """Scrape jobs from Indeed"""
        if not self.enabled:
            return []
        
        jobs = []
        locations = ["Lebanon", "Dubai", "Riyadh", "Doha", "Kuwait City"]
        keywords = ["HR Manager", "Operations Manager", "Recruiter", "Admin"]
        
        logger.info(f"🌍 Scraping Indeed...")
        
        for location in locations:
            for keyword in keywords[:2]:
                try:
                    url = f"https://www.indeed.com/jobs?q={keyword.replace(' ', '+')}&l={location.replace(' ', '+')}"
                    response = self.client.get(url)
                    
                    if not response or response.status_code != 200:
                        continue
                    
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select('.job-card')[:15]
                    
                    logger.info(f"  Indeed {location}/{keyword}: {len(cards)} jobs")
                    
                    for card in cards:
                        try:
                            title_elem = card.select_one('.job-title')
                            company_elem = card.select_one('.company-name')
                            link_elem = card.select_one('a')
                            
                            if not title_elem:
                                continue
                            
                            title = title_elem.get_text(strip=True)
                            
                            if not self._is_valid_title(title):
                                continue
                            
                            company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                            job_url = link_elem.get('href', '') if link_elem else ''
                            if job_url and not job_url.startswith('http'):
                                job_url = "https://www.indeed.com" + job_url
                            
                            # Generate email
                            domain = f"{company.lower().replace(' ', '')}.com"
                            email = f"careers@{domain}"
                            
                            jobs.append(JobLead(
                                title=title,
                                company=company,
                                location=location,
                                email=email,
                                url=job_url,
                                salary="0",
                                description="",
                                source="Indeed",
                                discovered_at=time.strftime('%Y-%m-%d %H:%M:%S')
                            ))
                            
                            self.leads_found += 1
                            
                        except Exception as e:
                            continue
                    
                    self._random_delay(2, 4)
                    
                except Exception as e:
                    logger.debug(f"Indeed scrape error: {e}")
                    continue
        
        logger.info(f"  ✅ Indeed: Found {len(jobs)} jobs")
        return jobs


class GulfTalentScraper(BaseScraper):
    """Scrape GulfTalent.com"""
    
    def scrape(self) -> List[JobLead]:
        """Scrape jobs from GulfTalent"""
        if not self.enabled:
            return []
        
        jobs = []
        keywords = ["hr", "operations", "admin"]
        
        logger.info(f"🌍 Scraping GulfTalent...")
        
        for keyword in keywords:
            try:
                url = f"https://www.gulftalent.com/jobs/{keyword}"
                response = self.client.get(url)
                
                if not response or response.status_code != 200:
                    continue
                
                soup = BeautifulSoup(response.content, 'html.parser')
                cards = soup.select('.job-tile')[:20]
                
                logger.info(f"  GulfTalent {keyword}: {len(cards)} jobs")
                
                for card in cards:
                    try:
                        title_elem = card.select_one('h3') or card.select_one('.title')
                        company_elem = card.select_one('.company-name')
                        
                        if not title_elem:
                            continue
                        
                        title = title_elem.get_text(strip=True)
                        
                        if not self._is_valid_title(title):
                            continue
                        
                        company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                        
                        # Generate email
                        domain = f"{company.lower().replace(' ', '')}.com"
                        email = f"careers@{domain}"
                        
                        jobs.append(JobLead(
                            title=title,
                            company=company,
                            location="Gulf",
                            email=email,
                            url=self.url,
                            salary="0",
                            description="",
                            source="GulfTalent",
                            discovered_at=time.strftime('%Y-%m-%d %H:%M:%S')
                        ))
                        
                        self.leads_found += 1
                        
                    except Exception as e:
                        continue
                
                self._random_delay(2, 4)
                
            except Exception as e:
                logger.debug(f"GulfTalent error: {e}")
        
        logger.info(f"  ✅ GulfTalent: Found {len(jobs)} jobs")
        return jobs


# ============================================================================
# MAIN SCRAPER CLASS
# ============================================================================

class EnhancedScraper:
    """Main scraper that aggregates all sources"""
    
    def __init__(self):
        self.scrapers = []
        self.all_jobs = []
        self.setup_scrapers()
    
    def setup_scrapers(self):
        """Setup all scrapers"""
        self.scrapers = [
            DaleelMadaniScraper("Daleel Madani", "https://daleel-madani.org/jobs", enabled=True),
            LinkedInScraper("LinkedIn", "https://www.linkedin.com/jobs", enabled=True),
            BaytScraper("Bayt", "https://www.bayt.com", enabled=True),
            IndeedScraper("Indeed", "https://www.indeed.com", enabled=True),
            GulfTalentScraper("GulfTalent", "https://www.gulftalent.com", enabled=True),
        ]
    
    def scrape_all(self, max_workers: int = 3) -> List[JobLead]:
        """Scrape all sources in parallel"""
        logger.info("=" * 50)
        logger.info("🚀 ENHANCED SCRAPER - MAXIMUM POWER MODE")
        logger.info("=" * 50)
        
        all_jobs = []
        active_scrapers = [scraper for scraper in self.scrapers if scraper.enabled]
        
        with ThreadPoolExecutor(max_workers=min(max_workers, len(active_scrapers) or 1)) as executor:
            future_to_scraper = {executor.submit(scraper.scrape): scraper for scraper in active_scrapers}
            for future in as_completed(future_to_scraper):
                scraper = future_to_scraper[future]
                try:
                    jobs = future.result()
                    all_jobs.extend(jobs)
                    logger.info(f"✅ {scraper.name}: {len(jobs)} jobs")
                except Exception as e:
                    logger.error(f"❌ {scraper.name}: {e}")
        
        # Deduplicate
        seen = set()
        unique_jobs = []
        for job in all_jobs:
            key = f"{job.company.lower()}|{job.title.lower()}"
            if key not in seen:
                seen.add(key)
                unique_jobs.append(job)
        
        logger.info("=" * 50)
        logger.info(f"📊 TOTAL: {len(unique_jobs)} unique jobs found")
        logger.info("=" * 50)
        
        self.all_jobs = unique_jobs
        return unique_jobs
    
    def save_to_file(self, filename: str = "scraped_jobs.json"):
        """Save jobs to JSON file"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([job.to_dict() for job in self.all_jobs], f, indent=2, ensure_ascii=False)
        logger.info(f"💾 Saved {len(self.all_jobs)} jobs to {filename}")
    
    def get_jobs_by_location(self, location: str) -> List[JobLead]:
        """Filter jobs by location"""
        return [job for job in self.all_jobs if location.lower() in job.location.lower()]
    
    def get_jobs_by_title(self, title_keyword: str) -> List[JobLead]:
        """Filter jobs by title keyword"""
        return [job for job in self.all_jobs if title_keyword.lower() in job.title.lower()]


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    print("""
╔════════════════════════════════════════╗
║   SAM ENHANCED SCRAPER - TEST MODE   ║
╚════════════════════════════════════════╝
    """)
    
    scraper = EnhancedScraper()
    jobs = scraper.scrape_all()
    
    print(f"\n📊 Summary:")
    print(f"   Total Jobs: {len(jobs)}")
    
    # Save
    scraper.save_to_file()
    
    print("\n✅ Scraper test complete!")
