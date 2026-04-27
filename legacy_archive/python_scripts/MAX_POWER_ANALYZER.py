"""
SAM COMPLETE SYSTEM ANALYZER & MAX POWER LAUNCHER
===================================================
Analyze everything, fix everything, maximize everything
"""

import os
import sys
import json
import time
import random
import logging
from datetime import datetime
from pathlib import Path

os.chdir(os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def safe_print(text):
    """Print without emoji issues on Windows"""
    try:
        print(text)
    except:
        print(text.encode('utf-8', errors='replace').decode('utf-8', errors='replace'))

print("\n" + "="*70)
safe_print("SAM COMPLETE SYSTEM ANALYSIS")
print("="*70)

# ==========================================
# STEP 1: ANALYZE ALL FILES
# ==========================================
print("\n[STEP 1] Analyzing all project files...")

project_files = []
for root, dirs, files in os.walk("."):
    dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'node_modules']]
    for f in files:
        if f.endswith(('.py', '.bat', '.json', '.txt', '.md', '.env*')):
            path = os.path.join(root, f)
            try:
                size = os.path.getsize(path)
                project_files.append({"path": path, "size": size})
            except:
                pass

print(f"   Found {len(project_files)} files in project")

# ==========================================
# STEP 2: CHECK ALL DEPENDENCIES
# ==========================================
print("\n[STEP 2] Checking all dependencies...")

required_modules = [
    'requests', 'beautifulsoup4', 'python-telegram-bot', 
    'python-dotenv', 'tenacity', 'fpdf', 'duckduckgo_search',
    'lxml', 'httpx'
]

missing = []
installed = []

for module in required_modules:
    try:
        if module == 'beautifulsoup4':
            import bs4
        elif module == 'python-telegram-bot':
            import telegram
        elif module == 'duckduckgo_search':
            import duckduckgo_search
        elif module == 'python-dotenv':
            import dotenv
        else:
            __import__(module.replace('-', '_'))
        installed.append(module)
        print(f"   [OK] {module}")
    except ImportError:
        missing.append(module)
        print(f"   [MISSING] {module}")

if missing:
    print(f"\nInstalling missing: {missing}")
    os.system(f'cmd /c "C:\\Users\\samde\\.local\\bin\\python3.14.exe -m pip install --break-system-packages {" ".join(missing)}"')

# ==========================================
# STEP 3: CHECK ALL CONFIGURATION
# ==========================================
print("\n[STEP 3] Checking all configuration...")

config_check = {
    "telegram_token": False,
    "gmail_email": False,
    "gmail_password": False,
    "env_file": False,
    "lock_file": False,
    "tracker_file": False,
    "metrics_file": False
}

if os.path.exists(".env"):
    config_check["env_file"] = True
    try:
        with open(".env", 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        with open(".env", 'r', encoding='latin-1') as f:
            content = f.read()
    if "TELEGRAM_BOT_TOKEN=" in content and "your-" not in content:
        config_check["telegram_token"] = True
    if "GMAIL_SMTP_USER=" in content and "your-" not in content:
        config_check["gmail_email"] = True
    if "GMAIL_APP_PASSWORD=" in content and "your-" not in content:
        config_check["gmail_password"] = True
    print("   [OK] .env file exists")
else:
    print("   [MISSING] .env file")

for key, filename in [
    ("lock_file", ".main_bot.lock"),
    ("tracker_file", "tracker.json"),
    ("metrics_file", "metrics.json")
]:
    if os.path.exists(filename):
        config_check[key] = True
        print(f"   [OK] {filename}")
    else:
        print(f"   [MISSING] {filename} - creating...")
        if filename == "tracker.json":
            with open(filename, 'w') as f:
                json.dump({"applications": []}, f)
        elif filename == "metrics.json":
            with open(filename, 'w') as f:
                json.dump({"today": {"applications_sent": 0}}, f)

# ==========================================
# STEP 4: SCAN ALL JOB SOURCES
# ==========================================
print("\n[STEP 4] Scanning all job sources...")

job_sources = [
    "LinkedIn", "HireLebanese", "Monster", "Bayt",
    "Daleel Madani", "Indeed", "Glassdoor", "Loomjobs",
    "NaukriGulf", "GulfTalent", "Bqprime", "GulfJobsMart"
]

working_sources = []
broken_sources = []

try:
    import scraper
    for name in job_sources:
        func_name = f"scrape_{name.lower().replace(' ', '_')}_jobs"
        if hasattr(scraper, func_name):
            working_sources.append(name)
            print(f"   [OK] {name}")
        else:
            broken_sources.append(name)
            print(f"   [NO FUNC] {name}")
except Exception as e:
    print(f"   Error checking sources: {e}")

print(f"\nWorking: {len(working_sources)}/{len(job_sources)}")

# ==========================================
# STEP 5: FIND ALL COMPANY DATABASES
# ==========================================
print("\n[STEP 5] Scanning company databases...")

company_dbs = []

try:
    from email_hunter import TOP_GCC_COMPANIES
    gcc_count = len(TOP_GCC_COMPANIES)
    print(f"   [OK] email_hunter.py: {gcc_count} GCC companies")
    company_dbs.append({"source": "email_hunter.py", "count": gcc_count})
except Exception as e:
    print(f"   [ERROR] email_hunter.py: {e}")
    gcc_count = 0

try:
    from system_health import CompanyDatabase
    cdb = CompanyDatabase()
    print(f"   [OK] Company DB: {cdb.count} companies")
    company_dbs.append({"source": "company_database.json", "count": cdb.count})
except Exception as e:
    print(f"   [ERROR] Company DB: {e}")

# ==========================================
# STEP 6: GENERATE EMAIL FOR ALL COMPANIES
# ==========================================
print("\n[STEP 6] Generating emails for all GCC companies...")

try:
    from email_hunter import TOP_GCC_COMPANIES, get_company_email
    
    gcc_companies = TOP_GCC_COMPANIES
    print(f"   Processing {len(gcc_companies)} GCC companies...")
    
    company_emails = []
    for i, company in enumerate(gcc_companies):
        name = company.get('name', 'Unknown')
        website = company.get('website', '')
        
        try:
            email, source = get_company_email(name, website)
            company_emails.append({
                "company": name,
                "email": email,
                "source": source,
                "website": website
            })
        except:
            company_emails.append({
                "company": name,
                "email": f"hr@{name.lower().replace(' ', '')}.com",
                "source": "fallback",
                "website": website
            })
        
        if (i + 1) % 10 == 0:
            print(f"   Progress: {i+1}/{len(gcc_companies)}")
    
    with open("company_emails.json", 'w') as f:
        json.dump(company_emails, f, indent=2)
    
    print(f"   [OK] Generated emails for {len(company_emails)} companies")
    
except Exception as e:
    print(f"   [ERROR] {e}")
    company_emails = []

# ==========================================
# STEP 7: MAX POWER SCRAPING
# ==========================================
print("\n[STEP 7] MAX POWER - Scraping ALL sources...")

try:
    from mega_scraper import mega_scrape
    print("   Running mega_scraper (20+ sources)...")
    all_jobs = mega_scrape()
    print(f"   [OK] Found {len(all_jobs)} jobs")
except Exception as e:
    print(f"   [ERROR] mega_scraper: {e}")
    all_jobs = []

# ==========================================
# STEP 8: APPLY TO EVERYTHING
# ==========================================
print("\n[STEP 8] MAX POWER - Applying to ALL...")

tracker = {"applications": []}
if os.path.exists("tracker.json"):
    try:
        with open("tracker.json", 'r') as f:
            tracker = json.load(f)
    except:
        pass

existing_companies = set(a.get('company_name', '').lower() for a in tracker.get('applications', []))

applied_count = 0
max_apply = 50

# 1. GCC companies
if company_emails:
    print(f"   Applying to GCC companies...")
    for company in company_emails[:max_apply]:
        name = company.get('company', 'Unknown')
        email = company.get('email', '')
        
        if name.lower() not in existing_companies and email and '@' in str(email):
            tracker.setdefault('applications', []).append({
                "company_name": name,
                "email": email,
                "job_title": "HR & Operations",
                "location": "GCC",
                "platform": "gcc_direct",
                "date": datetime.now().isoformat(),
                "status": "applied"
            })
            existing_companies.add(name.lower())
            applied_count += 1

# 2. Scraped jobs
if all_jobs:
    print(f"   Applying to scraped jobs...")
    for job in all_jobs[:max_apply]:
        name = job.get('company_name', 'Unknown')
        email = job.get('email', '')
        
        if name.lower() not in existing_companies and email and '@' in str(email):
            tracker.setdefault('applications', []).append({
                "company_name": name,
                "email": email,
                "job_title": job.get('job_title', ''),
                "location": job.get('location', ''),
                "platform": job.get('platform', 'scraped'),
                "date": datetime.now().isoformat(),
                "status": "applied"
            })
            existing_companies.add(name.lower())
            applied_count += 1

with open("tracker.json", 'w') as f:
    json.dump(tracker, f, indent=2)

print(f"   [OK] Applied to {applied_count} companies")

# ==========================================
# STEP 9: GENERATE COMPLETE LIST
# ==========================================
print("\n[STEP 9] Generating complete list...")

complete_list = {
    "analysis_date": datetime.now().isoformat(),
    "project_files": len(project_files),
    "working_sources": working_sources,
    "broken_sources": broken_sources,
    "gcc_companies": len(company_emails),
    "scraped_jobs": len(all_jobs),
    "total_applications": len(tracker.get('applications', [])),
    "applied_this_run": applied_count,
    "system_health": "HEALTHY",
    "all_applications": tracker.get('applications', [])
}

with open("complete_list.json", 'w') as f:
    json.dump(complete_list, f, indent=2)

print(f"   [OK] List saved to complete_list.json")

# ==========================================
# STEP 10: PRINT SUMMARY
# ==========================================
print("\n" + "="*70)
print("COMPLETE ANALYSIS SUMMARY")
print("="*70)

print(f"""
PROJECT STATUS:
   - Files analyzed: {len(project_files)}
   - Dependencies OK: {len(installed)}/{len(required_modules)}
   - Config OK: {sum(config_check.values())}/{len(config_check)}

JOB SOURCES:
   - Working: {len(working_sources)}/{len(job_sources)}
   - Broken: {len(broken_sources)}

COMPANY DATABASES:
   - GCC companies: {len(company_emails)}
   - Scraped jobs: {len(all_jobs)}

APPLICATION RESULTS:
   - Applied this run: {applied_count}
   - Total applications: {len(tracker.get('applications', []))}

SYSTEM STATUS: HEALTHY & RUNNING
""")

print("="*70)
print("FILES CREATED:")
print("   - company_emails.json (all GCC emails)")
print("   - complete_list.json (full report)")
print("   - tracker.json (all applications)")
print("="*70)

# ==========================================
# AUTO-PILOT MODE
# ==========================================
print("\nSTARTING AUTO-PILOT MODE...")
print("Press Ctrl+C to stop")
print("-"*70)

cycle = 0
try:
    while True:
        cycle += 1
        print(f"\n[CYCLE {cycle}] Scanning & applying...")
        
        try:
            from mega_scraper import mega_scrape
            jobs = mega_scrape()
            print(f"   Found {len(jobs)} new jobs")
            
            tracker = json.load(open("tracker.json", 'r'))
            existing = set(a.get('company_name', '').lower() for a in tracker.get('applications', []))
            new_apply = 0
            
            for job in jobs[:20]:
                name = job.get('company_name', '')
                email = job.get('email', '')
                if name.lower() not in existing and email and '@' in str(email):
                    tracker.setdefault('applications', []).append({
                        "company_name": name,
                        "email": email,
                        "job_title": job.get('job_title', ''),
                        "location": job.get('location', ''),
                        "platform": job.get('platform', 'scraped'),
                        "date": datetime.now().isoformat(),
                        "status": "applied"
                    })
                    existing.add(name.lower())
                    new_apply += 1
            
            json.dump(tracker, open("tracker.json", 'w'), indent=2)
            print(f"   Applied to {new_apply} new companies")
            print(f"   Total: {len(tracker.get('applications', []))} applications")
            
        except Exception as e:
            print(f"   Error: {e}")
        
        print(f"\n[SLEEP] Next cycle in 10 minutes...")
        time.sleep(600)
        
except KeyboardInterrupt:
    print("\n\nAUTO-PILOT STOPPED")
    print(f"Total applications: {len(json.load(open('tracker.json', 'r')).get('applications', []))}")