"""
╔══════════════════════════════════════════════════════════════════════════════╗
║           SAM ULTIMATE WORLDWIDE JOB AUTOMATOR - ENGINE                ║
║                    ALL COUNTRIES • ALL PLATFORMS • MAXIMUM               ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import time
import random
import json
import re
import hashlib
import base64
import sqlite3
import threading
import asyncio
import logging
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
try:
    from duckduckgo_search import DDGS
except Exception:
    DDGS = None

# Import Ultimate Configuration
from ultimate_config import ULTIMATE_CONFIG, UltimateConfig

# ============================================================================
# LOGGING SETUP
# ============================================================================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("ultimate_engine.log", encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================================================
# ULTIMATE DATABASE
# ============================================================================
class UltimateDatabase:
    """SQLite database for tracking everything"""
    
    def __init__(self, db_path="ultimate_sam.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Accounts created
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                platform TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                country TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                status TEXT DEFAULT 'active',
                applications_sent INTEGER DEFAULT 0
            )
        """)
        
        # Applications sent
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                company_name TEXT NOT NULL,
                email TEXT NOT NULL,
                job_title TEXT,
                platform TEXT,
                country TEXT,
                status TEXT DEFAULT 'sent',
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_received BOOLEAN DEFAULT 0
            )
        """)
        
        # Email tracking
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                to_email TEXT NOT NULL,
                company_name TEXT,
                subject TEXT,
                status TEXT DEFAULT 'sent',
                sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                opened BOOLEAN DEFAULT 0
            )
        """)
        
        # Company intelligence
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                domain TEXT,
                industry TEXT,
                country TEXT,
                size TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                emails_found TEXT,
                jobs_posted INTEGER DEFAULT 0
            )
        """)
        
        # Job leads
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS job_leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                company TEXT NOT NULL,
                location TEXT,
                url TEXT,
                email TEXT,
                salary TEXT,
                discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                applied BOOLEAN DEFAULT 0,
                platform TEXT
            )
        """)
        
        # Statistics
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS statistics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date DATE UNIQUE NOT NULL,
                applications_sent INTEGER DEFAULT 0,
                emails_sent INTEGER DEFAULT 0,
                accounts_created INTEGER DEFAULT 0,
                jobs_scraped INTEGER DEFAULT 0,
                responses_received INTEGER DEFAULT 0
            )
        """)
        
        self.conn.commit()
    
    def save_application(self, company, email, job_title, platform, country):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO applications 
            (company_name, email, job_title, platform, country)
            VALUES (?, ?, ?, ?, ?)
        """, (company, email, job_title, platform, country))
        self.conn.commit()
    
    def save_job_lead(self, title, company, location, url, email, salary, platform):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO job_leads 
            (title, company, location, url, email, salary, platform)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (title, company, location, url, email, salary, platform))
        self.conn.commit()
    
    def save_company(self, name, domain, industry, country, emails):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT OR IGNORE INTO companies 
            (name, domain, industry, country, emails_found)
            VALUES (?, ?, ?, ?, ?)
        """, (name, domain, industry, country, json.dumps(emails)))
        self.conn.commit()
    
    def get_statistics(self, days=30):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT SUM(applications_sent), SUM(emails_sent), SUM(accounts_created),
                   SUM(jobs_scraped), SUM(responses_received)
            FROM statistics
            WHERE date >= date('now', '-' || ? || ' days')
        """, (days,))
        result = cursor.fetchone()
        return {
            'applications': result[0] or 0,
            'emails': result[1] or 0,
            'accounts': result[2] or 0,
            'jobs_scraped': result[3] or 0,
            'responses': result[4] or 0
        }
    
    def update_daily_stats(self):
        cursor = self.conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d')
        
        # Count today's stats
        cursor.execute("SELECT COUNT(*) FROM applications WHERE date(sent_at) = ?", (today,))
        apps = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM emails WHERE date(sent_at) = ?", (today,))
        emails = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM accounts WHERE date(created_at) = ?", (today,))
        accounts = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM job_leads WHERE date(discovered_at) = ?", (today,))
        jobs = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM applications WHERE date(sent_at) = ? AND response_received = 1", (today,))
        responses = cursor.fetchone()[0]
        
        # Upsert stats
        cursor.execute("""
            INSERT INTO statistics (date, applications_sent, emails_sent, accounts_created, jobs_scraped, responses_received)
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(date) DO UPDATE SET
                applications_sent = excluded.applications_sent,
                emails_sent = excluded.emails_sent,
                accounts_created = excluded.accounts_created,
                jobs_scraped = excluded.jobs_scraped,
                responses_received = excluded.responses_received
        """, (today, apps, emails, accounts, jobs, responses))
        
        self.conn.commit()
    
    def close(self):
        self.conn.close()


# ============================================================================
# ULTIMATE SMTP ENGINE
# ============================================================================
class UltimateSMTPEngine:
    """Multi-provider SMTP engine for maximum email delivery"""
    
    def __init__(self, db: UltimateDatabase):
        self.db = db
        self.current_provider_index = 0
        self.providers = ULTIMATE_CONFIG.SMTP_PROVIDERS
        self.session = requests.Session()
    
    def _get_next_provider(self):
        """Rotate through SMTP providers"""
        provider = self.providers[self.current_provider_index]
        self.current_provider_index = (self.current_provider_index + 1) % len(self.providers)
        return provider
    
    def send_email(self, to_email, subject, html_body, from_email=None, from_name="Sam Salameh"):
        """Send email with automatic provider rotation"""
        if not self.providers:
            logger.error("No SMTP providers configured.")
            return False
        max_retries = len(self.providers)
        
        for attempt in range(max_retries):
            provider = self._get_next_provider()
            
            if not provider.get('user') or not provider.get('pass'):
                continue
            
            try:
                msg = MIMEMultipart('mixed')
                msg['From'] = f'"{from_name}" <{from_email or provider["user"]}>'
                msg['To'] = to_email
                msg['Subject'] = subject
                msg['Date'] = datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')
                msg['Message-ID'] = f'<{hashlib.md5(str(time.time()).encode()).hexdigest()}@ SamBot>'
                
                # Plain text fallback
                plain_text = re.sub(r'<[^>]+>', ' ', html_body)
                plain_text = re.sub(r'\s+', ' ', plain_text).strip()
                
                alt = MIMEMultipart('alternative')
                alt.attach(MIMEText(plain_text, 'plain', 'utf-8'))
                alt.attach(MIMEText(html_body, 'html', 'utf-8'))
                msg.attach(alt)
                
                # Attach CV
                cv_path = "Sam_Cordahi_CV.html"
                if os.path.exists(cv_path):
                    with open(cv_path, 'rb') as f:
                        cv_part = MIMEApplication(f.read(), _subtype='html')
                        cv_part['Content-Disposition'] = 'attachment; filename="Sam_Cordahi_CV.html"'
                        msg.attach(cv_part)
                
                # Connect and send
                server = smtplib.SMTP(provider['host'], provider['port'], timeout=30)
                server.ehlo()
                server.starttls()
                server.login(provider['user'], provider['pass'])
                server.send_message(msg)
                server.quit()
                
                logger.info(f"✅ Email sent via {provider['name']}: {to_email}")
                
                # Track email
                self.db.save_application(
                    company_name=to_email.split('@')[1] if '@' in to_email else 'Unknown',
                    email=to_email,
                    job_title=subject,
                    platform=provider['name'],
                    country='WORLDWIDE'
                )
                
                return True
                
            except Exception as e:
                logger.warning(f"⚠️ {provider['name']} failed: {e}")
                continue
        
        logger.error(f"❌ All SMTP providers failed for {to_email}")
        return False


# ============================================================================
# ULTIMATE SCRAPER ENGINE
# ============================================================================
class UltimateScraperEngine:
    """Scrape jobs from ALL countries and platforms"""
    
    def __init__(self, db: UltimateDatabase):
        self.db = db
        self.session = requests.Session()
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
        ]
    
    def _get_headers(self):
        return {
            'User-Agent': random.choice(self.user_agents),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
    
    def scrape_indeed_worldwide(self, country_code="com", keywords=None):
        """Scrape Indeed for any country"""
        if keywords is None:
            keywords = ["HR", "Human Resources", "Operations Manager", "Admin", "Recruiter"]
        
        jobs = []
        country_domains = {
            "US": "indeed.com", "UK": "indeed.co.uk", "CA": "indeed.ca",
            "AU": "indeed.com.au", "DE": "indeed.de", "FR": "indeed.fr",
            "IN": "indeed.co.in", "CN": "indeed.com.hk", "JP": "indeed.co.jp",
            "BR": "indeed.com.br", "MX": "indeed.com.mx", "ES": "indeed.es",
            "IT": "indeed.it", "NL": "indeed.nl", "PL": "indeed.pl",
            "AE": "indeed.ae", "SA": "indeed.com.sa", "QA": "indeed.qa",
            "NZ": "indeed.co.nz", "SG": "indeed.com.sg", "MY": "indeed.my",
            "PH": "indeed.ph", "ID": "indeed.co.id", "TH": "indeed.co.th",
            "VN": "indeed.vn", "RU": "indeed.ru", "UA": "indeed.ua",
            "EG": "indeed.com.eg", "ZA": "indeed.co.za", "NG": "indeed.com.ng",
            "KE": "indeed.co.ke", "GH": "indeed.com.gh", "IE": "indeed.ie",
            "AT": "indeed.at", "CH": "indeed.ch", "BE": "indeed.be",
            "SE": "indeed.se", "NO": "indeed.no", "DK": "indeed.dk",
            "FI": "indeed.fi", "CZ": "indeed.cz", "HU": "indeed.hu",
            "RO": "indeed.ro", "BG": "indeed.bg", "HR": "indeed.hr",
            "SK": "indeed.sk", "SI": "indeed.si", "LT": "indeed.lt",
            "LV": "indeed.lv", "EE": "indeed.ee", "GR": "indeed.gr",
            "PT": "indeed.pt", "TR": "indeed.com.tr", "IL": "indeed.co.il",
        }
        
        domain = country_domains.get(country_code, "indeed.com")
        
        for keyword in keywords:
            try:
                import urllib.parse
                query = urllib.parse.quote(keyword)
                url = f"https://www.{domain}/jobs?q={query}"
                
                response = self.session.get(url, headers=self._get_headers(), timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    job_cards = soup.select('.jobsearch-ResultsList > li') or soup.select('.job_card')
                    
                    for card in job_cards[:20]:
                        try:
                            title_elem = card.select_one('.jobTitle a') or card.select_one('h2 a')
                            company_elem = card.select_one('.companyName') or card.select_one('.company')
                            loc_elem = card.select_one('.companyLocation') or card.select_one('.location')
                            link_elem = card.select_one('a[href*="/jobs/viewjob"]')
                            
                            if title_elem:
                                job_title = title_elem.get_text(strip=True)
                                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                                location = loc_elem.get_text(strip=True) if loc_elem else country_code
                                
                                job_url = link_elem['href'] if link_elem else ''
                                if job_url and not job_url.startswith('http'):
                                    job_url = f"https://www.{domain}{job_url}"
                                
                                self.db.save_job_lead(
                                    title=job_title,
                                    company=company,
                                    location=location,
                                    url=job_url,
                                    email='',
                                    salary='0',
                                    platform=f'Indeed {country_code}'
                                )
                                jobs.append({
                                    'title': job_title,
                                    'company': company,
                                    'location': location,
                                    'url': job_url
                                })
                        except:
                            continue
                
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                logger.debug(f"Indeed {country_code} error: {e}")
                continue
        
        return jobs
    
    def scrape_linkedin_worldwide(self, location="Worldwide", keywords=None):
        """Scrape LinkedIn jobs"""
        if keywords is None:
            keywords = ["HR Manager", "Operations", "Admin", "Recruiter", "Office Manager"]
        
        jobs = []
        
        for keyword in keywords:
            try:
                import urllib.parse
                q_keyword = urllib.parse.quote(keyword)
                q_location = urllib.parse.quote(location)
                url = f"https://www.linkedin.com/jobs/search?keywords={q_keyword}&location={q_location}"
                
                response = self.session.get(url, headers=self._get_headers(), timeout=15)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    cards = soup.select('.base-card')[:15]
                    
                    for card in cards:
                        try:
                            title_elem = card.select_one('.base-search-card__title')
                            company_elem = card.select_one('.base-search-card__subtitle')
                            link_elem = card.select_one('a.base-card__full-link')
                            
                            if title_elem and link_elem:
                                job_title = title_elem.get_text(strip=True)
                                company = company_elem.get_text(strip=True) if company_elem else "Unknown"
                                
                                self.db.save_job_lead(
                                    title=job_title,
                                    company=company,
                                    location=location,
                                    url=link_elem.get('href', ''),
                                    email='',
                                    salary='0',
                                    platform='LinkedIn'
                                )
                                jobs.append({
                                    'title': job_title,
                                    'company': company,
                                    'location': location
                                })
                        except:
                            continue
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logger.debug(f"LinkedIn error: {e}")
                continue
        
        return jobs
    
    def scrape_duckduckgo_worldwide(self, queries=None):
        """Scrape using DuckDuckGo for all countries"""
        if DDGS is None:
            logger.warning("DuckDuckGo search unavailable; skipping DDG scraping.")
            return []
        if queries is None:
            queries = [
                '"HR Manager" "apply" "email" "Dubai"',
                '"Operations Manager" "visa sponsorship" "relocation" "UAE"',
                '"HR Business Partner" "relocation package" "Qatar"',
                '"Recruiter" "sponsorship" "Kuwait"',
                '"Admin Manager" "relocation" "Saudi Arabia"',
                '"HR Director" "housing allowance" "Dubai"',
                '"Office Manager" "expat package" "Oman"',
                '"Human Resources" "relocation" "Singapore"',
                '"HR Specialist" "sponsorship" "Australia"',
                '"Operations Lead" "visa" "Canada"',
                '"HR Coordinator" "relocation package" "UK"',
                '"Talent Manager" "sponsorship" "USA"',
                '"People Operations" "relocation" "Germany"',
                '"HR Generalist" "visa sponsorship" "France"',
                '"HR Manager" "relocation" "Netherlands"',
                '"HR Officer" "sponsorship" "Ireland"',
                '"Employee Relations" "relocation" "Spain"',
                '"HR Assistant" "visa" "Italy"',
                '"Recruitment Lead" "sponsorship" "Portugal"',
                '"HR Consultant" "relocation" "Switzerland"',
                '"HR Manager" "relocation" "Japan"',
                '"Operations Manager" "visa" "South Korea"',
                '"HR Manager" "sponsorship" "New Zealand"',
                '"Office Administrator" "relocation" "Malaysia"',
                '"HR Business Partner" "visa" "Thailand"',
                '"HR Specialist" "sponsorship" "India"',
                '"Talent Acquisition" "relocation" "Philippines"',
                '"HR Director" "visa sponsorship" "Brazil"',
                '"Operations Manager" "relocation" "Mexico"',
                '"HR Manager" "sponsorship" "South Africa"',
            ]
        
        jobs = []
        
        try:
            with DDGS(timeout=30) as ddgs:
                for query in queries[:30]:
                    try:
                        logger.info(f"🔍 DDG: {query[:60]}...")
                        
                        results = [r for r in ddgs.text(query, max_results=15)]
                        
                        for res in results:
                            url = res.get('href', '')
                            title = res.get('title', '')
                            snippet = res.get('body', '')
                            
                            if not url or not title:
                                continue
                            
                            # Extract emails from snippet
                            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', snippet)
                            email = emails[0] if emails else None
                            
                            # Try to extract company name
                            company = "Unknown"
                            if ' - ' in title:
                                company = title.split(' - ')[0].strip()
                            elif '|' in title:
                                company = title.split('|')[0].strip()
                            
                            self.db.save_job_lead(
                                title=title,
                                company=company,
                                location="Worldwide",
                                url=url,
                                email=email or '',
                                salary='0',
                                platform='DuckDuckGo'
                            )
                            
                            jobs.append({
                                'title': title,
                                'company': company,
                                'email': email,
                                'url': url
                            })
                        
                        time.sleep(random.uniform(1, 2))
                        
                    except Exception as e:
                        logger.debug(f"DDG query error: {e}")
                        continue
                        
        except Exception as e:
            logger.error(f"DDG Error: {e}")
        
        return jobs
    
    def scrape_company_directories(self):
        """Scrape company directories for email patterns"""
        directories = [
            "https://www.hubspot.com/customer-stories",
            "https://www.g2.com/categories/hr",
            "https://www.crunchbase.com/organizations",
        ]
        
        companies = []
        
        for directory in directories:
            try:
                response = self.session.get(directory, headers=self._get_headers(), timeout=20)
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    # Extract company names
                    links = soup.select('a[href*="/organization/"]')[:50]
                    
                    for link in links:
                        name = link.get_text(strip=True)
                        if name and len(name) > 2:
                            domain = f"{name.lower().replace(' ', '')}.com"
                            self.db.save_company(
                                name=name,
                                domain=domain,
                                industry="Various",
                                country="Worldwide",
                                emails=self._generate_email_patterns(domain)
                            )
                            companies.append({'name': name, 'domain': domain})
                
                time.sleep(random.uniform(2, 4))
                
            except Exception as e:
                logger.debug(f"Directory scrape error: {e}")
                continue
        
        return companies
    
    def _generate_email_patterns(self, domain):
        """Generate likely email patterns for a domain"""
        patterns = [
            f"careers@{domain}",
            f"jobs@{domain}",
            f"hr@{domain}",
            f"recruitment@{domain}",
            f"hiring@{domain}",
            f"info@{domain}",
            f"contact@{domain}",
            f"admin@{domain}",
        ]
        return patterns


# ============================================================================
# ULTIMATE EMAIL FINDER
# ============================================================================
class UltimateEmailFinder:
    """Find emails for any company worldwide"""
    
    def __init__(self, db: UltimateDatabase):
        self.db = db
        self.session = requests.Session()
    
    def find_company_emails(self, company_name, domain=None):
        """Find email addresses for a company"""
        emails = []
        
        if domain:
            domains = [domain]
        else:
            # Guess domains based on company name
            clean_name = company_name.lower().replace(' ', '').replace('.', '')
            domains = [
                f"{clean_name}.com",
                f"{clean_name}.co",
                f"{clean_name}.io",
                f"{clean_name}.org",
            ]
        
        for domain in domains:
            # Try common email patterns
            patterns = ULTIMATE_CONFIG.EMAIL_PATTERNS['default']
            
            for pattern in patterns[:10]:  # Limit to avoid too many attempts
                email = pattern.replace('{domain}', domain)
                
                # Quick verification
                if self._verify_email(email):
                    emails.append(email)
                    logger.info(f"✅ Found: {email}")
                    break
            
            if emails:
                break
        
        return emails[:5]  # Return max 5 emails
    
    def _verify_email(self, email):
        """Verify if email likely exists (basic check)"""
        try:
            # Simple check - look for common invalid patterns
            invalid = ['example.com', 'test.com', 'sample.com', 'fake.com']
            if any(i in email.lower() for i in invalid):
                return False
            
            # Extract domain and check if resolvable
            domain = email.split('@')[1] if '@' in email else ''
            if domain:
                # Try to resolve domain
                import socket
                try:
                    socket.gethostbyname(domain)
                    return True
                except:
                    return False
            
            return False
        except:
            return False
    
    def find_on_linkedin(self, company_name):
        """Find company email on LinkedIn"""
        try:
            import urllib.parse
            query = urllib.parse.quote(f"{company_name} careers email")
            url = f"https://www.google.com/search?q={query}"
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = self.session.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find emails in search results
            text = soup.get_text()
            emails = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', text)
            
            return [e for e in emails if 'linkedin' not in e.lower()][:3]
            
        except Exception as e:
            logger.debug(f"LinkedIn email search failed: {e}")
            return []


# ============================================================================
# ULTIMATE MAIN ENGINE
# ============================================================================
class UltimateEngine:
    """The Ultimate Worldwide Job Application Engine"""
    
    def __init__(self):
        self.db = UltimateDatabase()
        self.smtp = UltimateSMTPEngine(self.db)
        self.scraper = UltimateScraperEngine(self.db)
        self.email_finder = UltimateEmailFinder(self.db)
        self.running = False
        self.stats = {
            'jobs_found': 0,
            'applications_sent': 0,
            'emails_sent': 0,
            'accounts_created': 0,
        }
    
    def print_banner(self):
        banner = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██████╗ ███████╗███████╗ ██████╗██╗   ██╗███████╗                       ║
║   ██╔══██╗██╔════╝██╔════╝██╔════╝██║   ██║██╔════╝                       ║
║   ██████╔╝█████╗  ███████╗██║     ██║   ██║█████╗                         ║
║   ██╔══██╗██╔══╝  ╚════██║██║     ██║   ██║██╔══╝                         ║
║   ██║  ██║███████╗███████║╚██████╗╚██████╔╝███████╗                       ║
║   ╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚══════╝                       ║
║                                                                              ║
║   ██╗  ██╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗                              ║
║   ██║  ██║██║██╔════╝ ████╗  ██║██╔══██╗██║                              ║
║   ███████║██║██║  ███╗██╔██╗ ██║███████║██║                              ║
║   ██╔══██║██║██║   ██║██║╚██╗██║██╔══██║██║                              ║
║   ██║  ██║██║╚██████╔╝██║ ╚████║██║  ██║███████╗                         ║
║   ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝╚══════╝                         ║
║                                                                              ║
║   ██████╗ ███████╗███╗   ███╗██████╗ ██╗     ███████╗                     ║
║   ██╔══██╗██╔════╝████╗ ████║██╔══██╗██║     ██╔════╝                     ║
║   ██████╔╝█████╗  ██╔████╔██║██████╔╝██║     █████╗                       ║
║   ██╔═══╝ ██╔══╝  ██║╚██╔╝██║██╔═══╝ ██║     ██╔══╝                       ║
║   ██║     ███████╗██║ ╚═╝ ██║██║     ███████╗███████╗                     ║
║   ╚═╝     ╚══════╝╚═╝     ╚═╝╚═╝     ╚══════╝╚══════╝                     ║
║                                                                              ║
║   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗ ██████╗ ██╗   ██╗██╗            ║
║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗██╔══██╗╚██╗ ██╔╝██║            ║
║   ███████╗███████║███████║██║  ██║██║   ██║██████╔╝ ╚████╔╝ ██║            ║
║   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║██╔══██╗  ╚██╔╝  ╚═╝           ║
║   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝██║  ██║   ██║   ██╗           ║
║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚═╝           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def run_max_power(self):
        """Run the Ultimate Engine at maximum power"""
        self.print_banner()
        
        print("\n" + "="*70)
        print("🚀 ULTIMATE MAX POWER MODE ACTIVATED")
        print("="*70)
        print(f"📊 Countries: {len(ULTIMATE_CONFIG.COUNTRIES)}")
        print(f"📋 Platforms: {len(ULTIMATE_CONFIG.JOB_PLATFORMS)}")
        print(f"🌐 Social Networks: {len(ULTIMATE_CONFIG.SOCIAL_PLATFORMS)}")
        print(f"💼 Job Groups: {len(ULTIMATE_CONFIG.JOB_GROUPS)}")
        print(f"📧 SMTP Providers: {len(ULTIMATE_CONFIG.SMTP_PROVIDERS)}")
        print("="*70 + "\n")
        
        self.running = True
        
        try:
            # Phase 1: DuckDuckGo Worldwide Scraping
            print("\n📡 PHASE 1: Worldwide Intelligence Gathering (DuckDuckGo)...")
            jobs = self.scraper.scrape_duckduckgo_worldwide()
            print(f"✅ Found {len(jobs)} job leads worldwide")
            self.stats['jobs_found'] = len(jobs)
            
            # Phase 2: Indeed for Major Countries
            print("\n📡 PHASE 2: Indeed Multi-Country Scraping...")
            major_countries = ['US', 'UK', 'AE', 'SA', 'QA', 'CA', 'AU', 'DE', 'FR', 'IN', 'SG', 'HK', 'JP']
            for country in major_countries:
                try:
                    jobs = self.scraper.scrape_indeed_worldwide(country)
                    print(f"  ✅ {country}: {len(jobs)} jobs")
                    time.sleep(random.uniform(1, 3))
                except Exception as e:
                    print(f"  ❌ {country}: {e}")
            
            # Phase 3: LinkedIn Global
            print("\n📡 PHASE 3: LinkedIn Global Scraping...")
            locations = ["Worldwide", "Gulf", "Europe", "Asia", "Americas", "Middle East"]
            for loc in locations:
                try:
                    jobs = self.scraper.scrape_linkedin_worldwide(loc)
                    print(f"  ✅ {loc}: {len(jobs)} jobs")
                    time.sleep(random.uniform(2, 4))
                except Exception as e:
                    print(f"  ❌ {loc}: {e}")
            
            # Phase 4: Company Directory Scraping
            print("\n📡 PHASE 4: Company Directory Mining...")
            companies = self.scraper.scrape_company_directories()
            print(f"✅ Mined {len(companies)} companies")
            
            # Phase 5: Email Discovery & Application
            print("\n📧 PHASE 5: Email Discovery & Mass Application...")
            leads = self._get_pending_leads(limit=100)
            
            for lead in leads:
                if not self.running:
                    break
                
                try:
                    # Find emails
                    emails = self.email_finder.find_company_emails(lead['company'])
                    
                    for email in emails:
                        # Send application email
                        subject = f"{lead['title']} | Sam Salameh - HR & Operations | Available Now"
                        body = self._generate_personalized_email(lead)
                        
                        if self.smtp.send_email(email, subject, body):
                            self.stats['applications_sent'] += 1
                            self.stats['emails_sent'] += 1
                            print(f"  ✅ {lead['company']}: {email}")
                        else:
                            print(f"  ❌ {lead['company']}: Failed")
                        
                        time.sleep(random.uniform(1, 3))
                
                except Exception as e:
                    print(f"  ❌ Lead error: {e}")
                    continue
            
            # Phase 6: Report
            self.print_final_report()
            
        except KeyboardInterrupt:
            print("\n\n🛑 Engine stopped by user")
            self.print_final_report()
        except Exception as e:
            print(f"\n\n💥 Engine crash: {e}")
            import traceback
            traceback.print_exc()
        
        self.running = False
        self.db.close()
    
    def _get_pending_leads(self, limit=100):
        """Get pending job leads from database"""
        cursor = self.db.conn.cursor()
        cursor.execute("""
            SELECT DISTINCT title, company, location, url, email, salary, platform
            FROM job_leads
            WHERE applied = 0
            LIMIT ?
        """, (limit,))
        
        leads = []
        for row in cursor.fetchall():
            leads.append({
                'title': row[0],
                'company': row[1],
                'location': row[2],
                'url': row[3],
                'email': row[4],
                'salary': row[5],
                'platform': row[6]
            })
        
        return leads
    
    def _generate_personalized_email(self, lead):
        """Generate personalized email for a job lead"""
        company = lead.get('company', 'Unknown Company')
        title = lead.get('title', 'Opportunity')
        body = f"""
<div style="background-color: #0b0f19; padding: 40px 20px; font-family: Arial, sans-serif;">
  <table width="100%" max-width="650" align="center" style="max-width: 650px; margin: 0 auto; background-color: #111827; border-radius: 16px; overflow: hidden;">
    <tr>
      <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 40px; text-align: center;">
        <div style="width: 60px; height: 60px; background-color: #06b6d4; border-radius: 50%; line-height: 60px; color: white; font-size: 24px; font-weight: bold; margin: 0 auto 15px;">RC</div>
        <div style="font-size: 28px; font-weight: 800; color: white;">SAM CORDAHI</div>
        <div style="font-size: 12px; color: #94a3b8; text-transform: uppercase; letter-spacing: 3px; margin-top: 5px;">HR & Operations Professional</div>
      </td>
    </tr>
    <tr>
      <td height="4" style="background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);"></td>
    </tr>
    <tr>
      <td style="padding: 35px;">
        <p style="font-size: 17px; color: #f8fafc;">Dear <strong>{company}</strong> Hiring Team,</p>
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">I am reaching out to express my strong interest in the <span style="color: #06b6d4; font-weight: 600;">{title}</span> position at {company}.</p>
        
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">With extensive experience in HR operations, customer service, and process optimization, I am confident I can bring significant value to your organization.</p>
        
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;"><strong>Key Qualifications:</strong></p>
        <ul style="color: #cbd5e1; font-size: 14px; line-height: 1.8;">
          <li>5+ years HR & Operations experience</li>
          <li>100% compliance accuracy in employee records</li>
          <li>50+ daily customer inquiries resolved</li>
          <li>25% operational cost reduction achieved</li>
          <li>Available immediately for relocation</li>
        </ul>
        
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">Please find my CV attached. I am available for immediate discussion and can start at your earliest convenience.</p>
        
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">Best regards,<br><strong>Sam Salameh</strong><br>+961 76 005 412<br>sam.dev1@outlook.com</p>
      </td>
    </tr>
    <tr>
      <td style="background-color: #0f172a; padding: 30px; text-align: center;">
        <a href="https://www.linkedin.com/in/sam-cordahi/" style="display: inline-block; padding: 12px 30px; background-color: #06b6d4; color: white; text-decoration: none; border-radius: 25px; font-weight: bold;">VIEW LINKEDIN</a>
        <p style="color: #94a3b8; font-size: 12px; margin-top: 20px;">HR & Customer Operations Specialist | Available Worldwide</p>
      </td>
    </tr>
  </table>
</div>
        """
        return body
    
    def print_final_report(self):
        """Print final statistics"""
        print("\n" + "="*70)
        print("📊 ULTIMATE ENGINE - FINAL REPORT")
        print("="*70)
        
        stats = self.db.get_statistics(days=1)
        
        print(f"\n🌐 TODAY'S ACHIEVEMENTS:")
        print(f"   • Jobs Found: {self.stats['jobs_found']}")
        print(f"   • Applications Sent: {self.stats['applications_sent']}")
        print(f"   • Emails Sent: {self.stats['emails_sent']}")
        print(f"   • Accounts Created: {self.stats['accounts_created']}")
        
        print(f"\n📈 ALL-TIME STATISTICS:")
        print(f"   • Applications: {stats['applications']}")
        print(f"   • Emails: {stats['emails']}")
        print(f"   • Jobs Scraped: {stats['jobs_scraped']}")
        print(f"   • Responses: {stats['responses']}")
        
        print("\n" + "="*70)
        print("🛑 ENGINE STOPPED")
        print("="*70 + "\n")


# ============================================================================
# LAUNCHER
# ============================================================================
if __name__ == "__main__":
    engine = UltimateEngine()
    engine.run_max_power()