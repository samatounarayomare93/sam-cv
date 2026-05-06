import os
import requests
from bs4 import BeautifulSoup
import logging
import json
from datetime import datetime
import hashlib
from concurrent.futures import ThreadPoolExecutor, as_completed

# ==========================================
# 🌍 GLOBAL COMPANY DISCOVERY SYSTEM - MAXIMUM POWER
# ==========================================

class GlobalCompanyScraper:
    """
    MAXIMUM POWER: Discovers company names globally with parallel execution.
    Prevents duplicates and tracks all found companies.
    """
    
    def __init__(self):
        self.scraped_companies = set()
        self.company_file = "discovered_companies.json"
        self.load_discovered()
    
    def load_discovered(self):
        """Load previously discovered companies."""
        try:
            if os.path.exists(self.company_file):
                with open(self.company_file, 'r') as f:
                    data = json.load(f)
                    self.scraped_companies = set(data.get("companies", []))
                    logging.info(f"Loaded {len(self.scraped_companies)} previously discovered companies")
        except Exception as e:
            logging.warning(f"Could not load discovered companies: {e}")
    
    def save_discovered(self):
        """Save newly discovered companies."""
        try:
            data = {
                "companies": list(self.scraped_companies),
                "total": len(self.scraped_companies),
                "last_updated": datetime.now().isoformat()
            }
            with open(self.company_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logging.error(f"Could not save discovered companies: {e}")
    
    def scrape_linkedin_companies(self):
        """Scrape companies from LinkedIn public data."""
        logging.info("🌍 Scraping LinkedIn companies...")
        try:
            # This is a simplified version - in production would use LinkedIn API or scraping
            new_companies = []
            # Add companies from various sources
            sources = [
                "https://www.linkedin.com/jobs/search?keywords=HR",
                "https://www.linkedin.com/jobs/search?keywords=Operations",
            ]
            return new_companies
        except Exception as e:
            logging.warning(f"LinkedIn scrape failed: {e}")
            return []
    
    def scrape_bayt_companies(self):
        """Scrape companies from Bayt.com (Middle East job board)."""
        logging.info("🌍 Scraping Bayt.com companies...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            companies = set()
            
            categories = ['hr', 'operations', 'admin']
            for category in categories:
                try:
                    url = f"https://www.bayt.com/en/jobs/{category}/"
                    response = requests.get(url, headers=headers, timeout=10)
                    if response.status_code != 200:
                        continue
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract company names from job listings
                    for job in soup.find_all('div', class_='job-list-item'):
                        company = job.find('a', class_='company-link')
                        if company and company.get_text():
                            companies.add(company.get_text().strip())
                except Exception:
                    continue
            
            logging.info(f"🌍 Found {len(companies)} companies on Bayt")
            return list(companies)
        except Exception as e:
            logging.warning(f"Bayt scrape failed: {e}")
            return []
    
    def scrape_gulf_companies(self):
        """Scrape companies from Gulf job boards."""
        logging.info("🌍 Scraping Gulf companies...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            companies = set()
            
            # Top Gulf job sites
            urls = [
                "https://www.dubizzle.com/jobs/hr/",
                "https://gulftalent.com/jobs/hr",
            ]
            
            for url in urls:
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract company names
                    # This is a template - specific selectors vary by site
                except Exception:
                    continue
            
            logging.info(f"🌍 Found {len(companies)} companies on Gulf boards")
            return list(companies)
        except Exception as e:
            logging.warning(f"Gulf scrape failed: {e}")
            return []
    
    def scrape_indeed_companies(self):
        """Scrape companies from Indeed."""
        logging.info("🌍 Scraping Indeed companies...")
        try:
            headers = {'User-Agent': 'Mozilla/5.0'}
            companies = set()
            
            keywords = ['HR', 'Operations', 'Administrative']
            for keyword in keywords:
                try:
                    url = f"https://www.indeed.com/jobs?q={keyword}"
                    response = requests.get(url, headers=headers, timeout=10)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    for item in soup.find_all('span', class_='companyName'):
                        company = item.get_text().strip()
                        if company:
                            companies.add(company)
                except Exception:
                    continue
            
            logging.info(f"🌍 Found {len(companies)} companies on Indeed")
            return list(companies)
        except Exception as e:
            logging.warning(f"Indeed scrape failed: {e}")
            return []
    
    def discover_all_companies(self):
        """MAXIMUM POWER: Run all scrapers in parallel for faster company discovery."""
        logging.info("MAXIMUM POWER: Starting global company discovery in parallel...")
        
        # Define all scrapers
        scrapers = [
            ("Bayt", self.scrape_bayt_companies),
            ("Gulf", self.scrape_gulf_companies),
            ("Indeed", self.scrape_indeed_companies),
            ("LinkedIn", self.scrape_linkedin_companies),
        ]
        
        # MAXIMUM POWER: Run scrapers in parallel
        max_workers = min(4, len(scrapers))
        discovered = set()
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_scraper = {
                executor.submit(scraper_func): name
                for name, scraper_func in scrapers
            }
            
            for future in as_completed(future_to_scraper):
                name = future_to_scraper[future]
                try:
                    companies = future.result(timeout=30)  # 30s timeout per scraper
                    if companies:
                        discovered.update(companies)
                        logging.info(f"SUCCESS {name}: {len(companies)} companies")
                except Exception as e:
                    logging.warning(f"FAILED {name}: {e}")
        
        # Add to global list (avoid duplicates)
        before_count = len(self.scraped_companies)
        self.scraped_companies.update(discovered)
        new_companies = len(self.scraped_companies) - before_count
        
        logging.info(f"MAXIMUM POWER COMPLETE: {new_companies} new companies found")
        logging.info(f"TOTAL unique companies in database: {len(self.scraped_companies)}")
        
        self.save_discovered()
        
        return {
            "new_companies": new_companies,
            "total_companies": len(self.scraped_companies),
            "date": datetime.now().isoformat()
        }
    
    def get_statistics(self):
        """Get discovery statistics."""
        return {
            "total_discovered": len(self.scraped_companies),
            "database_file": self.company_file,
            "last_updated": datetime.now().isoformat()
        }


if __name__ == "__main__":
    scraper = GlobalCompanyScraper()
    results = scraper.discover_all_companies()
    print(f"Discovery results: {json.dumps(results, indent=2)}")
    print(f"Statistics: {json.dumps(scraper.get_statistics(), indent=2)}")
