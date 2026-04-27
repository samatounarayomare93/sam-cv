"""
SAM EMAIL HUNTER - Find Any Company Email
==========================================
Generates emails for any company automatically
"""

import requests
from bs4 import BeautifulSoup
import re
import random
import time
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Common HR/Recruitment email patterns
EMAIL_PATTERNS = [
    "hr@{domain}",
    "careers@{domain}",
    "recruitment@{domain}",
    "jobs@{domain}",
    "talent@{domain}",
    "humanresources@{domain}",
    "personnel@{domain}",
    "employment@{domain}",
    "staffing@{domain}",
    "apply@{domain}",
    "info@{domain}",
    "contact@{domain}",
    "admin@{domain}",
    "office@{domain}",
    "resumes@{domain}",
    "hiring@{domain}",
]

# Common domain patterns
DOMAIN_PATTERNS = [
    "{name}.com",
    "{name}.co",
    "{name}.ae",
    "{name}.com.lb",
    "{name}.com.sa",
    "{name}.qa",
    "{name}.net",
    "careers.{name}.com",
    "jobs.{name}.com",
    "hr.{name}.com",
]

def clean_company_name(name):
    """Clean company name for email"""
    # Remove special chars
    clean = re.sub(r'[^a-zA-Z0-9\s]', '', str(name))
    # Remove common words
    for word in ['Inc', 'LLC', 'Ltd', 'Group', 'Co', 'Corp', 'Company', 'International', 'Holding']:
        clean = re.sub(r'\b' + word + r'\b', '', clean, flags=re.IGNORECASE)
    return clean.strip()

def generate_email_variants(company_name):
    """Generate all possible email variants for a company"""
    emails = []
    clean_name = clean_company_name(company_name).lower().replace(' ', '').replace('-', '')
    clean_name_spaces = clean_company_name(company_name).lower().replace(' ', '-')
    
    for pattern in EMAIL_PATTERNS:
        # Try with domain
        for domain_pattern in DOMAIN_PATTERNS:
            domain = domain_pattern.replace('{name}', clean_name)
            email = pattern.replace('{domain}', domain)
            emails.append(email)
            
            # Also try with spaces replaced by hyphens
            domain_spaces = domain_pattern.replace('{name}', clean_name_spaces)
            email_spaces = pattern.replace('{domain}', domain_spaces)
            emails.append(email_spaces)
    
    return list(set(emails))  # Remove duplicates

def verify_email(email):
    """Verify if email exists using SMTP check"""
    try:
        import socket
        domain = email.split('@')[1]
        
        # Simple MX lookup check
        try:
            import dns.resolver
            mx_records = dns.resolver.resolve(domain, 'MX')
            return True
        except:
            pass
        
        # Try connecting to common SMTP ports
        for port in [25, 587, 465]:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                result = sock.connect_ex((domain, port))
                sock.close()
                if result == 0:
                    return True
            except:
                pass
        
        return False
    except:
        return False

def find_email_on_website(company_name, website=None):
    """Find email on company's website"""
    if not website:
        # Try common website patterns
        clean_name = clean_company_name(company_name).lower().replace(' ', '')
        websites = [
            f"https://www.{clean_name}.com",
            f"https://{clean_name}.com",
            f"https://www.{clean_name}.ae",
            f"https://{clean_name}.com.lb",
        ]
    else:
        websites = [website]
    
    for url in websites:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
            }
            resp = requests.get(url, headers=headers, timeout=10, allow_redirects=True)
            if resp.status_code == 200:
                # Find emails in page
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, resp.text)
                
                # Filter out social media and common non-contact emails
                filtered = [e for e in emails if not any(x in e.lower() for x in ['facebook', 'twitter', 'linkedin', 'instagram', 'youtube', 'noreply', 'no-reply'])]
                
                if filtered:
                    return filtered[0]
                    
        except:
            pass
    
    return None

def find_careers_page(company_name, website=None):
    """Find careers page and extract contact"""
    if not website:
        clean_name = clean_company_name(company_name).lower().replace(' ', '')
        websites = [
            f"https://www.{clean_name}.com/careers",
            f"https://www.{clean_name}.com/jobs",
            f"https://{clean_name}.com/careers",
            f"https://careers.{clean_name}.com",
        ]
    else:
        websites = [f"{website}/careers", f"{website}/jobs", f"{website}/careers/"]
    
    for url in websites:
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36'
            }
            resp = requests.get(url, headers=headers, timeout=10)
            if resp.status_code == 200:
                # Find emails
                email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
                emails = re.findall(email_pattern, resp.text)
                
                # Look for HR/Careers related
                for email in emails:
                    if any(x in email.lower() for x in ['hr', 'careers', 'jobs', 'recruit', 'talent', 'hiring']):
                        return email
                
                # Otherwise return first valid email
                for email in emails:
                    if not any(x in email.lower() for x in ['facebook', 'twitter', 'linkedin', 'noreply']):
                        return email
                        
        except:
            pass
    
    return None

def get_company_email(company_name, website=None):
    """
    Get the best email for a company
    Priority:
    1. Find on careers page
    2. Find on main website
    3. Generate best guess
    """
    # Try careers page first
    email = find_careers_page(company_name, website)
    if email:
        logger.info(f"Found careers email: {email}")
        return email, "careers_page"
    
    # Try main website
    email = find_email_on_website(company_name, website)
    if email:
        logger.info(f"Found website email: {email}")
        return email, "website"
    
    # Generate best guess
    variants = generate_email_variants(company_name)
    
    # Return most likely pattern
    likely_patterns = [
        f"hr@{clean_company_name(company_name).lower().replace(' ', '')}.com",
        f"careers@{clean_company_name(company_name).lower().replace(' ', '')}.com",
        f"recruitment@{clean_company_name(company_name).lower().replace(' ', '')}.com",
    ]
    
    for pattern in likely_patterns:
        if pattern in variants:
            logger.info(f"Generated email: {pattern}")
            return pattern, "generated"
    
    return variants[0] if variants else None, "none"

# ============================================
# BULK EMAIL GENERATOR
# ============================================

def generate_bulk_emails(companies):
    """
    Generate emails for a list of companies
    companies = [{"name": "Company Name", "website": "https://..."}]
    """
    results = []
    
    for company in companies:
        name = company.get('name', company.get('company_name', ''))
        website = company.get('website')
        
        if not name:
            continue
        
        email, source = get_company_email(name, website)
        results.append({
            "company": name,
            "email": email,
            "source": source,
            "website": website or "auto-generated"
        })
        
        time.sleep(random.uniform(0.5, 1.5))
    
    return results

# ============================================
# TOP GCC COMPANIES DATABASE
# ============================================

TOP_GCC_COMPANIES = [
    # UAE
    {"name": "Emirates", "website": "https://www.emirates.com"},
    {"name": "Etihad Airways", "website": "https://www.etihad.com"},
    {"name": "Mubadala", "website": "https://www.mubadala.com"},
    {"name": "ADNOC", "website": "https://www.adnoc.ae"},
    {"name": "DP World", "website": "https://www.dpworld.com"},
    {"name": "Emaar", "website": "https://www.emaar.com"},
    {"name": "Majid Al Futtaim", "website": "https://www.maf.ae"},
    {"name": "Chalhoub Group", "website": "https://www.chalhoub.com"},
    {"name": "Al Futtaim Group", "website": "https://www.al-futtaim.com"},
    {"name": "Alshaya Group", "website": "https://www.alshaya.com"},
    {"name": "Azadea Group", "website": "https://www.azadea.com"},
    {"name": "Al Tayer Group", "website": "https://www.altayer.com"},
    {"name": "Al Naboodah Group", "website": "https://www.alnaboodah.com"},
    {"name": "Dubai Holding", "website": "https://www.dubaiholding.com"},
    {"name": "Dubai Airports", "website": "https://www.dubaiairports.ae"},
    {"name": "flydubai", "website": "https://www.flydubai.com"},
    {"name": "Dubai Police", "website": "https://www.dubaipolice.gov.ae"},
    {"name": "Dubai Health Authority", "website": "https://www.dha.gov.ae"},
    {"name": "Abu Dhabi Health Authority", "website": "https://www.doh.gov.ae"},
    {"name": "Aldar Properties", "website": "https://www.aldar.com"},
    {"name": "Abu Dhabi Commercial Bank", "website": "https://www.adcb.com"},
    {"name": "First Abu Dhabi Bank", "website": "https://www.fab.ae"},
    {"name": "Abu Dhabi Islamic Bank", "website": "https://www.adib.ae"},
    {"name": "Dubai Islamic Bank", "website": "https://www.dib.ae"},
    {"name": "RAKBANK", "website": "https://www.rakbank.ae"},
    
    # Saudi Arabia
    {"name": "Saudi Aramco", "website": "https://www.aramco.com"},
    {"name": "SABIC", "website": "https://www.sabic.com"},
    {"name": "Saudi Airlines", "website": "https://www.saudia.com"},
    {"name": "Saudi Basic Industries", "website": "https://www.sabic.com"},
    {"name": "Saudi Telecom", "website": "https://www.stc.com.sa"},
    {"name": "Mobily", "website": "https://www.mobily.com.sa"},
    {"name": "King Abdullah University", "website": "https://www.kaust.edu.sa"},
    {"name": "King Faisal Specialist Hospital", "website": "https://www.kfsh.med.sa"},
    {"name": "Riyadh Bank", "website": "https://www.riyadbank.com"},
    {"name": "Saudi National Bank", "website": "https://www.ahli.com"},
    {"name": "Al Rajhi Bank", "website": "https://www.alrajhi.com"},
    {"name": "Saudi British Bank", "website": "https://www.sabb.com"},
    
    # Qatar
    {"name": "Qatar Airways", "website": "https://www.qatarairways.com"},
    {"name": "Qatar Petroleum", "website": "https://www.qp.com.qa"},
    {"name": "Qatar Foundation", "website": "https://www.qf.org.qa"},
    {"name": "Qatar University", "website": "https://www.qu.edu.qa"},
    {"name": "Qatar Development Bank", "website": "https://www.qdb.qa"},
    {"name": "Qatar Islamic Bank", "website": "https://www.qib.com.qa"},
    {"name": "Ooredoo", "website": "https://www.ooredoo.qa"},
    
    # Kuwait
    {"name": "Kuwait Airways", "website": "https://www.kuwaitairways.com"},
    {"name": "Kuwait Oil Company", "website": "https://www.kockw.com"},
    {"name": "National Bank of Kuwait", "website": "https://www.nbk.com"},
    {"name": "Kuwait Finance House", "website": "https://www.kfh.com"},
    
    # Bahrain
    {"name": "Bahrain Petroleum", "website": "https://www.bapco.net"},
    {"name": "Bahrain Bay", "website": "https://www.bahrainbay.com"},
    {"name": "Al Baraka Banking Group", "website": "https://www.albaraka.com"},
    
    # Oman
    {"name": "Oman Air", "website": "https://www.omanair.com"},
    {"name": "OQ", "website": "https://www.oq.com"},
    {"name": "Oman Telecommunications", "website": "https://www.omantel.com.om"},
]

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("SAM EMAIL HUNTER")
    print("=" * 50)
    
    # Test with one company
    email, source = get_company_email("Emirates Airlines")
    print(f"Emirates: {email} ({source})")
    
    email, source = get_company_email("Majid Al Futtaim")
    print(f"Majid Al Futtaim: {email} ({source})")
    
    email, source = get_company_email("Saudi Aramco")
    print(f"Saudi Aramco: {email} ({source})")
    
    print(f"\nTop GCC companies loaded: {len(TOP_GCC_COMPANIES)}")
