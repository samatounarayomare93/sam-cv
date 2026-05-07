"""
🚀 ZERO-COST JOB SCRAPERS
8 free job sources - No API keys needed
Target: 400+ jobs/day (100% FREE)
"""

import logging
import random
import time
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import re

# User agents for rotation
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]


def get_random_headers() -> Dict[str, str]:
    """Get random headers for scraping."""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "DNT": "1",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }


def smart_delay():
    """Smart delay to avoid rate limiting."""
    delay = random.uniform(3, 7)
    time.sleep(delay)


class FreeScraper:
    """Base class for free job scrapers."""
    
    def __init__(self, name: str):
        self.name = name
        self.session = requests.Session()
        self.session.headers.update(get_random_headers())
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Override this method in subclasses."""
        raise NotImplementedError
    
    def _safe_get(self, url: str, timeout: int = 15) -> requests.Response:
        """Safe HTTP GET with error handling."""
        try:
            response = self.session.get(url, timeout=timeout)
            response.raise_for_status()
            return response
        except Exception as e:
            logging.error(f"[{self.name}] Failed to fetch {url}: {e}")
            return None


class DaleelMadaniScraper(FreeScraper):
    """Daleel Madani (Lebanon) - FREE, no limits."""
    
    def __init__(self):
        super().__init__("Daleel Madani")
        self.base_url = "https://daleel-madani.org/jobs"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape jobs from Daleel Madani."""
        jobs = []
        
        try:
            logging.info(f"[{self.name}] Starting scrape...")
            
            for page in range(1, 6):  # First 5 pages
                url = f"{self.base_url}?page={page}"
                response = self._safe_get(url)
                
                if not response:
                    break
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job-card')
                
                for card in job_cards:
                    try:
                        title_elem = card.find('h3')
                        company_elem = card.find('div', class_='company-name')
                        link_elem = card.find('a', href=True)
                        
                        if title_elem and company_elem:
                            jobs.append({
                                'job_title': title_elem.text.strip(),
                                'company_name': company_elem.text.strip(),
                                'job_url': f"https://daleel-madani.org{link_elem['href']}" if link_elem else "",
                                'location': 'Lebanon',
                                'source': self.name
                            })
                    except Exception as e:
                        logging.debug(f"[{self.name}] Failed to parse job card: {e}")
                        continue
                
                smart_delay()
            
            logging.info(f"[{self.name}] Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"[{self.name}] Scrape failed: {e}")
            return []


class BaytScraper(FreeScraper):
    """Bayt.com (GCC) - FREE browsing."""
    
    def __init__(self):
        super().__init__("Bayt.com")
        self.base_url = "https://www.bayt.com/en/uae/jobs"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape jobs from Bayt.com."""
        jobs = []
        
        try:
            logging.info(f"[{self.name}] Starting scrape...")
            
            # Search for Network Engineering jobs in UAE
            search_terms = ["network-engineer", "it-infrastructure-engineer", "systems-administrator"]
            
            for term in search_terms:
                url = f"{self.base_url}/{term}/"
                response = self._safe_get(url)
                
                if not response:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_listings = soup.find_all('li', class_='has-pointer-d')
                
                for listing in job_listings[:20]:  # First 20 per search
                    try:
                        title_elem = listing.find('h2')
                        company_elem = listing.find('b', class_='t-default')
                        link_elem = listing.find('a', href=True)
                        
                        if title_elem and company_elem:
                            jobs.append({
                                'job_title': title_elem.text.strip(),
                                'company_name': company_elem.text.strip(),
                                'job_url': f"https://www.bayt.com{link_elem['href']}" if link_elem else "",
                                'location': 'UAE',
                                'source': self.name
                            })
                    except Exception as e:
                        logging.debug(f"[{self.name}] Failed to parse listing: {e}")
                        continue
                
                smart_delay()
            
            logging.info(f"[{self.name}] Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"[{self.name}] Scrape failed: {e}")
            return []


class GulfTalentScraper(FreeScraper):
    """GulfTalent (GCC) - FREE browsing."""
    
    def __init__(self):
        super().__init__("GulfTalent")
        self.base_url = "https://www.gulftalent.com/jobs"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape jobs from GulfTalent."""
        jobs = []
        
        try:
            logging.info(f"[{self.name}] Starting scrape...")
            
            # Search for Network Engineering jobs
            keywords = ["network-engineer", "it-infrastructure"]
            
            for keyword in keywords:
                url = f"{self.base_url}/{keyword}"
                response = self._safe_get(url)
                
                if not response:
                    continue
                
                soup = BeautifulSoup(response.text, 'html.parser')
                job_cards = soup.find_all('div', class_='job-card')
                
                for card in job_cards[:15]:  # First 15 per search
                    try:
                        title_elem = card.find('h3')
                        company_elem = card.find('span', class_='company')
                        link_elem = card.find('a', href=True)
                        location_elem = card.find('span', class_='location')
                        
                        if title_elem and company_elem:
                            jobs.append({
                                'job_title': title_elem.text.strip(),
                                'company_name': company_elem.text.strip(),
                                'job_url': f"https://www.gulftalent.com{link_elem['href']}" if link_elem else "",
                                'location': location_elem.text.strip() if location_elem else 'GCC',
                                'source': self.name
                            })
                    except Exception as e:
                        logging.debug(f"[{self.name}] Failed to parse card: {e}")
                        continue
                
                smart_delay()
            
            logging.info(f"[{self.name}] Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"[{self.name}] Scrape failed: {e}")
            return []


class NaukrigulfScraper(FreeScraper):
    """Naukrigulf (GCC) - FREE browsing."""
    
    def __init__(self):
        super().__init__("Naukrigulf")
        self.base_url = "https://www.naukrigulf.com"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape jobs from Naukrigulf."""
        jobs = []
        
        try:
            logging.info(f"[{self.name}] Starting scrape...")
            
            # Search for Network Engineering jobs in UAE
            search_url = f"{self.base_url}/network-engineer-jobs-in-uae"
            response = self._safe_get(search_url)
            
            if not response:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = soup.find_all('article', class_='jobTuple')
            
            for listing in job_listings[:25]:  # First 25 jobs
                try:
                    title_elem = listing.find('a', class_='title')
                    company_elem = listing.find('a', class_='subTitle')
                    location_elem = listing.find('li', class_='location')
                    
                    if title_elem and company_elem:
                        jobs.append({
                            'job_title': title_elem.text.strip(),
                            'company_name': company_elem.text.strip(),
                            'job_url': f"{self.base_url}{title_elem['href']}" if title_elem.get('href') else "",
                            'location': location_elem.text.strip() if location_elem else 'UAE',
                            'source': self.name
                        })
                except Exception as e:
                    logging.debug(f"[{self.name}] Failed to parse listing: {e}")
                    continue
            
            logging.info(f"[{self.name}] Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"[{self.name}] Scrape failed: {e}")
            return []


class DubizzleScraper(FreeScraper):
    """Dubizzle Jobs (UAE) - FREE."""
    
    def __init__(self):
        super().__init__("Dubizzle")
        self.base_url = "https://dubai.dubizzle.com/jobs"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape jobs from Dubizzle."""
        jobs = []
        
        try:
            logging.info(f"[{self.name}] Starting scrape...")
            
            # HR & Admin category
            url = f"{self.base_url}/hr-admin/"
            response = self._safe_get(url)
            
            if not response:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            job_cards = soup.find_all('div', {'data-testid': 'listing-card'})
            
            for card in job_cards[:20]:  # First 20 jobs
                try:
                    title_elem = card.find('h2')
                    company_elem = card.find('span', text=re.compile('Company'))
                    link_elem = card.find('a', href=True)
                    
                    if title_elem:
                        jobs.append({
                            'job_title': title_elem.text.strip(),
                            'company_name': company_elem.text.strip() if company_elem else 'Company in Dubai',
                            'job_url': f"https://dubai.dubizzle.com{link_elem['href']}" if link_elem else "",
                            'location': 'Dubai, UAE',
                            'source': self.name
                        })
                except Exception as e:
                    logging.debug(f"[{self.name}] Failed to parse card: {e}")
                    continue
            
            logging.info(f"[{self.name}] Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"[{self.name}] Scrape failed: {e}")
            return []


class AkhtabootScraper(FreeScraper):
    """Akhtaboot (MENA) - FREE."""
    
    def __init__(self):
        super().__init__("Akhtaboot")
        self.base_url = "https://www.akhtaboot.com"
    
    def scrape(self) -> List[Dict[str, Any]]:
        """Scrape jobs from Akhtaboot."""
        jobs = []
        
        try:
            logging.info(f"[{self.name}] Starting scrape...")
            
            # Search for HR jobs
            search_url = f"{self.base_url}/en/uae/jobs/hr-manager"
            response = self._safe_get(search_url)
            
            if not response:
                return []
            
            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = soup.find_all('div', class_='job-listing')
            
            for listing in job_listings[:20]:  # First 20 jobs
                try:
                    title_elem = listing.find('h3')
                    company_elem = listing.find('span', class_='company-name')
                    link_elem = listing.find('a', href=True)
                    location_elem = listing.find('span', class_='location')
                    
                    if title_elem and company_elem:
                        jobs.append({
                            'job_title': title_elem.text.strip(),
                            'company_name': company_elem.text.strip(),
                            'job_url': f"{self.base_url}{link_elem['href']}" if link_elem else "",
                            'location': location_elem.text.strip() if location_elem else 'UAE',
                            'source': self.name
                        })
                except Exception as e:
                    logging.debug(f"[{self.name}] Failed to parse listing: {e}")
                    continue
            
            logging.info(f"[{self.name}] Found {len(jobs)} jobs")
            return jobs
            
        except Exception as e:
            logging.error(f"[{self.name}] Scrape failed: {e}")
            return []


def scrape_all_free_sources() -> List[Dict[str, Any]]:
    """
    Scrape all free job sources.
    
    Returns:
        List of job dictionaries
    """
    all_jobs = []
    
    scrapers = [
        DaleelMadaniScraper(),
        BaytScraper(),
        GulfTalentScraper(),
        NaukrigulfScraper(),
        DubizzleScraper(),
        AkhtabootScraper(),
    ]
    
    for scraper in scrapers:
        try:
            jobs = scraper.scrape()
            all_jobs.extend(jobs)
            logging.info(f"✅ {scraper.name}: {len(jobs)} jobs")
        except Exception as e:
            logging.error(f"❌ {scraper.name} failed: {e}")
        
        # Delay between scrapers
        smart_delay()
    
    # Remove duplicates based on job_url
    unique_jobs = []
    seen_urls = set()
    
    for job in all_jobs:
        url = job.get('job_url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique_jobs.append(job)
    
    logging.info(f"🎯 Total unique jobs: {len(unique_jobs)}")
    return unique_jobs


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Starting FREE job scraping...")
    print("=" * 50)
    
    jobs = scrape_all_free_sources()
    
    print(f"\n✅ Total jobs found: {len(jobs)}")
    print("\n📊 Breakdown by source:")
    
    sources = {}
    for job in jobs:
        source = job.get('source', 'Unknown')
        sources[source] = sources.get(source, 0) + 1
    
    for source, count in sources.items():
        print(f"  {source}: {count} jobs")
    
    print("\n📋 Sample jobs:")
    for job in jobs[:5]:
        print(f"  - {job['job_title']} at {job['company_name']} ({job['location']})")
