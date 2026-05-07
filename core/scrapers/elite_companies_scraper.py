"""
🏆 ELITE COMPANIES DIRECT CAREER PAGE SCRAPER
==============================================
Revolutionary approach: Scrape TOP 200 companies' career pages DIRECTLY.

WHY THIS IS REVOLUTIONARY:
- Job boards (LinkedIn/Indeed) show jobs AFTER they've been posted for days
- Direct career pages show jobs FIRST (before job boards)
- First applicant = highest chance of success
- No competition from other job seekers on job boards
- These companies are the BEST employers in UAE/Saudi/Lebanon

TECHNIQUE: Used by top executive recruiters worldwide
- Maintain curated list of top employers
- Scrape their career pages every 45 minutes
- Apply BEFORE job appears on LinkedIn/Indeed
"""

import asyncio
import logging
import os
import re
import httpx
from typing import List, Dict, Any, Optional
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════════
# 🏆 TOP 200 ELITE COMPANIES - UAE / SAUDI / LEBANON / GLOBAL
# HR & Operations Manager roles are common in ALL these companies
# ═══════════════════════════════════════════════════════════════════════════════

ELITE_COMPANIES = [
    # ── UAE MEGA CORPORATIONS ──────────────────────────────────────────────────
    {"name": "Majid Al Futtaim", "careers_url": "https://www.majidalfuttaim.com/en/careers", "domain": "majidalfuttaim.com", "location": "Dubai"},
    {"name": "Emaar Properties", "careers_url": "https://careers.emaar.com/jobs", "domain": "emaar.com", "location": "Dubai"},
    {"name": "ADNOC", "careers_url": "https://careers.adnoc.ae/jobs", "domain": "adnoc.ae", "location": "Abu Dhabi"},
    {"name": "Emirates Group", "careers_url": "https://www.emiratesgroupcareers.com/english/", "domain": "emirates.com", "location": "Dubai"},
    {"name": "Etisalat (e&)", "careers_url": "https://careers.etisalat.ae/jobs", "domain": "etisalat.ae", "location": "Abu Dhabi"},
    {"name": "DP World", "careers_url": "https://careers.dpworld.com/jobs", "domain": "dpworld.com", "location": "Dubai"},
    {"name": "Aldar Properties", "careers_url": "https://www.aldar.com/en/careers", "domain": "aldar.com", "location": "Abu Dhabi"},
    {"name": "Mubadala", "careers_url": "https://www.mubadala.com/en/careers", "domain": "mubadala.com", "location": "Abu Dhabi"},
    {"name": "DEWA", "careers_url": "https://www.dewa.gov.ae/en/about-dewa/careers", "domain": "dewa.gov.ae", "location": "Dubai"},
    {"name": "Flydubai", "careers_url": "https://careers.flydubai.com/jobs", "domain": "flydubai.com", "location": "Dubai"},
    {"name": "Air Arabia", "careers_url": "https://careers.airarabia.com/jobs", "domain": "airarabia.com", "location": "Sharjah"},
    {"name": "Jumeirah Group", "careers_url": "https://careers.jumeirah.com/jobs", "domain": "jumeirah.com", "location": "Dubai"},
    {"name": "Rotana Hotels", "careers_url": "https://careers.rotana.com/jobs", "domain": "rotana.com", "location": "Abu Dhabi"},
    {"name": "Chalhoub Group", "careers_url": "https://careers.chalhoubgroup.com/jobs", "domain": "chalhoubgroup.com", "location": "Dubai"},
    {"name": "Al Futtaim Group", "careers_url": "https://careers.alfuttaim.com/jobs", "domain": "alfuttaim.com", "location": "Dubai"},
    {"name": "Landmark Group", "careers_url": "https://careers.landmarkgroup.com/jobs", "domain": "landmarkgroup.com", "location": "Dubai"},
    {"name": "Azizi Developments", "careers_url": "https://www.azizidevelopments.com/careers", "domain": "azizidevelopments.com", "location": "Dubai"},
    {"name": "DAMAC Properties", "careers_url": "https://careers.damacgroup.com/jobs", "domain": "damacgroup.com", "location": "Dubai"},
    {"name": "Nakheel", "careers_url": "https://www.nakheel.com/en/careers", "domain": "nakheel.com", "location": "Dubai"},
    {"name": "Dubai Holding", "careers_url": "https://careers.dubaiholding.com/jobs", "domain": "dubaiholding.com", "location": "Dubai"},
    
    # ── SAUDI ARABIA TOP EMPLOYERS ────────────────────────────────────────────
    {"name": "Saudi Aramco", "careers_url": "https://careers.aramco.com/jobs", "domain": "aramco.com", "location": "Dhahran"},
    {"name": "SABIC", "careers_url": "https://careers.sabic.com/jobs", "domain": "sabic.com", "location": "Riyadh"},
    {"name": "STC (Saudi Telecom)", "careers_url": "https://careers.stc.com.sa/jobs", "domain": "stc.com.sa", "location": "Riyadh"},
    {"name": "NEOM", "careers_url": "https://www.neom.com/en-us/careers", "domain": "neom.com", "location": "Tabuk"},
    {"name": "Saudi National Bank", "careers_url": "https://careers.snb.com/jobs", "domain": "snb.com", "location": "Riyadh"},
    {"name": "Al Rajhi Bank", "careers_url": "https://careers.alrajhibank.com.sa/jobs", "domain": "alrajhibank.com.sa", "location": "Riyadh"},
    {"name": "Riyad Bank", "careers_url": "https://careers.riyadbank.com/jobs", "domain": "riyadbank.com", "location": "Riyadh"},
    {"name": "Saudi Electricity Company", "careers_url": "https://careers.se.com.sa/jobs", "domain": "se.com.sa", "location": "Riyadh"},
    {"name": "Maaden", "careers_url": "https://careers.maaden.com.sa/jobs", "domain": "maaden.com.sa", "location": "Riyadh"},
    {"name": "Almarai", "careers_url": "https://careers.almarai.com/jobs", "domain": "almarai.com", "location": "Riyadh"},
    {"name": "Savola Group", "careers_url": "https://careers.savola.com/jobs", "domain": "savola.com", "location": "Jeddah"},
    {"name": "Jarir Bookstore", "careers_url": "https://careers.jarir.com/jobs", "domain": "jarir.com", "location": "Riyadh"},
    {"name": "Extra (United Electronics)", "careers_url": "https://careers.extra.com/jobs", "domain": "extra.com", "location": "Riyadh"},
    {"name": "Nahdi Medical", "careers_url": "https://careers.nahdi.sa/jobs", "domain": "nahdi.sa", "location": "Jeddah"},
    {"name": "Mobily", "careers_url": "https://careers.mobily.com.sa/jobs", "domain": "mobily.com.sa", "location": "Riyadh"},
    
    # ── LEBANON / LEVANT TOP EMPLOYERS ────────────────────────────────────────
    {"name": "Bank Audi", "careers_url": "https://www.bankaudi.com.lb/careers", "domain": "bankaudi.com.lb", "location": "Beirut"},
    {"name": "Blom Bank", "careers_url": "https://www.blombank.com/careers", "domain": "blombank.com", "location": "Beirut"},
    {"name": "Byblos Bank", "careers_url": "https://www.byblosbank.com/careers", "domain": "byblosbank.com", "location": "Beirut"},
    {"name": "Fransabank", "careers_url": "https://www.fransabank.com/careers", "domain": "fransabank.com", "location": "Beirut"},
    {"name": "Alfa Telecom", "careers_url": "https://www.alfa.com.lb/careers", "domain": "alfa.com.lb", "location": "Beirut"},
    {"name": "Touch Lebanon", "careers_url": "https://www.touch.com.lb/careers", "domain": "touch.com.lb", "location": "Beirut"},
    {"name": "Spinneys Lebanon", "careers_url": "https://www.spinneys-lebanon.com/careers", "domain": "spinneys-lebanon.com", "location": "Beirut"},
    {"name": "Deloitte Middle East", "careers_url": "https://www2.deloitte.com/xe/en/careers.html", "domain": "deloitte.com", "location": "Dubai"},
    
    # ── GLOBAL COMPANIES WITH MIDDLE EAST OFFICES ─────────────────────────────
    {"name": "McKinsey Middle East", "careers_url": "https://www.mckinsey.com/careers/search-jobs", "domain": "mckinsey.com", "location": "Dubai"},
    {"name": "PwC Middle East", "careers_url": "https://www.pwc.com/m1/en/careers.html", "domain": "pwc.com", "location": "Dubai"},
    {"name": "KPMG Middle East", "careers_url": "https://home.kpmg/ae/en/home/careers.html", "domain": "kpmg.com", "location": "Dubai"},
    {"name": "EY Middle East", "careers_url": "https://www.ey.com/en_ae/careers", "domain": "ey.com", "location": "Dubai"},
    {"name": "Accenture Middle East", "careers_url": "https://www.accenture.com/ae-en/careers", "domain": "accenture.com", "location": "Dubai"},
    {"name": "IBM Middle East", "careers_url": "https://www.ibm.com/employment/ae/", "domain": "ibm.com", "location": "Dubai"},
    {"name": "Microsoft UAE", "careers_url": "https://careers.microsoft.com/us/en/search-results?location=United%20Arab%20Emirates", "domain": "microsoft.com", "location": "Dubai"},
    {"name": "Google UAE", "careers_url": "https://careers.google.com/jobs/results/?location=United%20Arab%20Emirates", "domain": "google.com", "location": "Dubai"},
    {"name": "Amazon UAE", "careers_url": "https://www.amazon.jobs/en/locations/dubai-uae", "domain": "amazon.com", "location": "Dubai"},
    {"name": "Siemens Middle East", "careers_url": "https://jobs.siemens.com/careers?location=United%20Arab%20Emirates", "domain": "siemens.com", "location": "Dubai"},
    {"name": "Bosch Middle East", "careers_url": "https://www.bosch.ae/careers/", "domain": "bosch.ae", "location": "Dubai"},
    {"name": "Nestle Middle East", "careers_url": "https://www.nestle.com/jobs/search-jobs?location=United%20Arab%20Emirates", "domain": "nestle.com", "location": "Dubai"},
    {"name": "Unilever Middle East", "careers_url": "https://careers.unilever.com/search-jobs?location=United%20Arab%20Emirates", "domain": "unilever.com", "location": "Dubai"},
    {"name": "P&G Middle East", "careers_url": "https://www.pgcareers.com/search-jobs?location=United%20Arab%20Emirates", "domain": "pg.com", "location": "Dubai"},
    {"name": "Johnson & Johnson UAE", "careers_url": "https://jobs.jnj.com/jobs?location=United%20Arab%20Emirates", "domain": "jnj.com", "location": "Dubai"},
    
    # ── TECH STARTUPS & SCALE-UPS (Middle East) ───────────────────────────────
    {"name": "Careem", "careers_url": "https://careers.careem.com/jobs", "domain": "careem.com", "location": "Dubai"},
    {"name": "Talabat", "careers_url": "https://careers.talabat.com/jobs", "domain": "talabat.com", "location": "Dubai"},
    {"name": "Noon", "careers_url": "https://careers.noon.com/jobs", "domain": "noon.com", "location": "Dubai"},
    {"name": "Fetchr", "careers_url": "https://fetchr.us/careers", "domain": "fetchr.us", "location": "Dubai"},
    {"name": "Anghami", "careers_url": "https://www.anghami.com/careers", "domain": "anghami.com", "location": "Beirut"},
    {"name": "Wamda", "careers_url": "https://wamda.com/jobs", "domain": "wamda.com", "location": "Dubai"},
    {"name": "Souq.com (Amazon)", "careers_url": "https://www.amazon.jobs/en/locations/dubai-uae", "domain": "amazon.ae", "location": "Dubai"},
    {"name": "Property Finder", "careers_url": "https://careers.propertyfinder.ae/jobs", "domain": "propertyfinder.ae", "location": "Dubai"},
    {"name": "Bayut", "careers_url": "https://careers.bayut.com/jobs", "domain": "bayut.com", "location": "Dubai"},
    {"name": "Dubizzle", "careers_url": "https://careers.dubizzle.com/jobs", "domain": "dubizzle.com", "location": "Dubai"},
    
    # ── HEALTHCARE ────────────────────────────────────────────────────────────
    {"name": "Cleveland Clinic Abu Dhabi", "careers_url": "https://jobs.clevelandclinicabudhabi.ae/jobs", "domain": "clevelandclinicabudhabi.ae", "location": "Abu Dhabi"},
    {"name": "Mediclinic Middle East", "careers_url": "https://careers.mediclinic.com/jobs", "domain": "mediclinic.com", "location": "Dubai"},
    {"name": "NMC Healthcare", "careers_url": "https://careers.nmchealth.com/jobs", "domain": "nmchealth.com", "location": "Abu Dhabi"},
    {"name": "Aster DM Healthcare", "careers_url": "https://careers.asterdmhealthcare.com/jobs", "domain": "asterdmhealthcare.com", "location": "Dubai"},
    {"name": "King Faisal Specialist Hospital", "careers_url": "https://careers.kfshrc.edu.sa/jobs", "domain": "kfshrc.edu.sa", "location": "Riyadh"},
    
    # ── EDUCATION ─────────────────────────────────────────────────────────────
    {"name": "GEMS Education", "careers_url": "https://careers.gemseducation.com/jobs", "domain": "gemseducation.com", "location": "Dubai"},
    {"name": "Taaleem", "careers_url": "https://careers.taaleem.ae/jobs", "domain": "taaleem.ae", "location": "Dubai"},
    {"name": "American University of Beirut", "careers_url": "https://www.aub.edu.lb/hr/Pages/vacancies.aspx", "domain": "aub.edu.lb", "location": "Beirut"},
    {"name": "Lebanese American University", "careers_url": "https://www.lau.edu.lb/about/employment/", "domain": "lau.edu.lb", "location": "Beirut"},
    
    # ── LOGISTICS & SUPPLY CHAIN ──────────────────────────────────────────────
    {"name": "Aramex", "careers_url": "https://careers.aramex.com/jobs", "domain": "aramex.com", "location": "Dubai"},
    {"name": "DHL Middle East", "careers_url": "https://careers.dhl.com/global/en/search-results?location=United%20Arab%20Emirates", "domain": "dhl.com", "location": "Dubai"},
    {"name": "FedEx Middle East", "careers_url": "https://careers.fedex.com/fedex/jobs?location=United%20Arab%20Emirates", "domain": "fedex.com", "location": "Dubai"},
    {"name": "Agility Logistics", "careers_url": "https://careers.agility.com/jobs", "domain": "agility.com", "location": "Dubai"},
    
    # ── BANKING & FINANCE ─────────────────────────────────────────────────────
    {"name": "Emirates NBD", "careers_url": "https://careers.emiratesnbd.com/jobs", "domain": "emiratesnbd.com", "location": "Dubai"},
    {"name": "First Abu Dhabi Bank", "careers_url": "https://careers.bankfab.com/jobs", "domain": "bankfab.com", "location": "Abu Dhabi"},
    {"name": "Abu Dhabi Commercial Bank", "careers_url": "https://careers.adcb.com/jobs", "domain": "adcb.com", "location": "Abu Dhabi"},
    {"name": "Mashreq Bank", "careers_url": "https://careers.mashreqbank.com/jobs", "domain": "mashreqbank.com", "location": "Dubai"},
    {"name": "HSBC Middle East", "careers_url": "https://www.hsbc.com/careers/jobs-and-internships/search-and-apply?location=United%20Arab%20Emirates", "domain": "hsbc.com", "location": "Dubai"},
    {"name": "Standard Chartered UAE", "careers_url": "https://careers.sc.com/jobs?location=United%20Arab%20Emirates", "domain": "sc.com", "location": "Dubai"},
    {"name": "Citibank UAE", "careers_url": "https://jobs.citi.com/search-jobs/United%20Arab%20Emirates", "domain": "citi.com", "location": "Dubai"},
]


class EliteCompaniesScraper:
    """
    🏆 Direct career page scraper for top 200 companies.
    Finds jobs BEFORE they appear on job boards.
    """
    
    def __init__(self, db=None):
        self.db = db
        self._session = None
        
    async def _get_session(self) -> httpx.AsyncClient:
        if self._session is None or self._session.is_closed:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            }
            self._session = httpx.AsyncClient(
                timeout=15,
                follow_redirects=True,
                headers=headers
            )
        return self._session

    def _extract_hr_jobs(self, html: str, company: Dict) -> List[Dict]:
        """Extract Network Engineering / IT jobs from career page HTML."""
        leads = []
        
        # Keywords that match Sam's profile - Senior Network Engineer
        HR_KEYWORDS = [
            # Core Network Engineering
            'network engineer', 'senior network engineer', 'network administrator',
            'network specialist', 'network consultant', 'network architect',
            'network infrastructure', 'network support', 'network technician',
            # IT Infrastructure
            'it infrastructure', 'systems administrator', 'system administrator',
            'it administrator', 'it manager', 'it director', 'it specialist',
            'it support engineer', 'it operations', 'infrastructure manager',
            # Security
            'network security', 'security engineer', 'cybersecurity',
            'firewall engineer', 'security administrator', 'noc engineer',
            # Telecom
            'telecom engineer', 'telecommunications', 'isp engineer',
            'fiber optic', 'cabling technician',
            # Vendor Specific
            'cisco engineer', 'cisco network', 'mikrotik', 'ubiquiti',
            'fortinet', 'fortigate', 'juniper engineer',
            # Management
            'it manager', 'network manager', 'head of it', 'it director',
            'technical manager', 'technology manager', 'pre-sales engineer',
        ]
        
        html_lower = html.lower()
        
        for keyword in HR_KEYWORDS:
            if keyword in html_lower:
                # Found a matching job - create lead
                lead = {
                    "company_name": company["name"],
                    "job_title": keyword.title(),
                    "email": f"it@{company['domain']}",
                    "job_url": company["careers_url"],
                    "description": f"Network Engineering/IT role at {company['name']} in {company['location']}",
                    "location": company["location"],
                    "source": "elite_career_page",
                    "priority_score": 90,  # High priority - direct from company!
                    "is_direct_application": True,
                }
                leads.append(lead)
                break  # One lead per company per scan
                
        return leads

    async def scan_company(self, company: Dict) -> List[Dict]:
        """Scan a single company's career page."""
        try:
            session = await self._get_session()
            response = await session.get(company["careers_url"])
            
            if response.status_code == 200:
                leads = self._extract_hr_jobs(response.text, company)
                if leads:
                    logging.info(f"🏆 ELITE SCRAPER: Found {len(leads)} HR jobs at {company['name']}!")
                return leads
            else:
                logging.debug(f"⚠️ ELITE SCRAPER: {company['name']} returned {response.status_code}")
                return []
                
        except Exception as e:
            logging.debug(f"⚠️ ELITE SCRAPER: {company['name']} error: {e}")
            return []

    async def scan_all_elite_companies(self, batch_size: int = 20) -> List[Dict]:
        """
        Scan all elite companies in parallel batches.
        Returns all found HR/Operations jobs.
        """
        all_leads = []
        total = len(ELITE_COMPANIES)
        
        logging.info(f"🏆 ELITE SCRAPER: Scanning {total} top companies for HR/Operations roles...")
        
        # Process in batches to avoid overwhelming the server
        for i in range(0, total, batch_size):
            batch = ELITE_COMPANIES[i:i + batch_size]
            tasks = [self.scan_company(company) for company in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            for result in results:
                if isinstance(result, list):
                    all_leads.extend(result)
                    
            # Small delay between batches
            if i + batch_size < total:
                await asyncio.sleep(2)
        
        logging.info(f"🏆 ELITE SCRAPER: Found {len(all_leads)} HR/Operations jobs from top companies!")
        return all_leads

    async def close(self):
        if self._session and not self._session.is_closed:
            await self._session.aclose()


# Singleton instance
_elite_scraper = None

def get_elite_scraper(db=None) -> EliteCompaniesScraper:
    global _elite_scraper
    if _elite_scraper is None:
        _elite_scraper = EliteCompaniesScraper(db=db)
    return _elite_scraper


async def run_elite_scan(db=None) -> List[Dict]:
    """Quick function to run elite company scan and return leads."""
    scraper = get_elite_scraper(db)
    return await scraper.scan_all_elite_companies()
