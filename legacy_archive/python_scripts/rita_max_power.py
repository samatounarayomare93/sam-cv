"""
SAM MAX POWER - Ultimate Job Hunter
===================================
Combined power of all scrapers and tools
"""

import os
import sys
import time
import json
import random
import logging
from datetime import datetime

# Add project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import all our tools
try:
    import config
    from mega_scraper import mega_scrape
    from email_hunter import get_company_email, TOP_GCC_COMPANIES
    from followup_system import FollowUpSystem
    from self_healer import healer
except ImportError as e:
    print(f"Import error: {e}")
    print("Some modules not available, continuing with core features...")

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_tracker():
    """Load application tracker"""
    if os.path.exists("tracker.json"):
        try:
            with open("tracker.json", 'r') as f:
                return json.load(f)
        except Exception:
            return {"applications": []}
    return {"applications": []}

def save_tracker(data):
    """Save tracker"""
    try:
        with open("tracker.json", 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        logger.error(f"Save error: {e}")

def apply_to_company(company_data):
    """Apply to a company - simplified version"""
    company_name = company_data.get("company_name", "Unknown")
    email = company_data.get("email", "")
    job_title = company_data.get("job_title", "General Application")
    location = company_data.get("location", "Unknown")
    platform = company_data.get("platform", "direct")
    
    if not email or "@" not in str(email):
        logger.warning(f"No email for {company_name}, skipping")
        return False
    
    # Load tracker
    tracker = load_tracker()
    
    # Check if already applied
    for app in tracker.get("applications", []):
        if app.get("company_name", "").lower() == company_name.lower():
            logger.info(f"Already applied to {company_name}")
            return False
    
    # Add application
    application = {
        "company_name": company_name,
        "email": email,
        "job_title": job_title,
        "location": location,
        "platform": platform,
        "date": datetime.now().isoformat(),
        "status": "applied",
        "followup_count": 0
    }
    
    tracker.setdefault("applications", []).append(application)
    save_tracker(tracker)
    
    logger.info(f"APPLIED: {company_name} ({email})")
    return True

def run_max_power():
    """Run MAX POWER mode"""
    print("=" * 60)
    print("SAM MAX POWER - ULTIMATE JOB HUNTER")
    print("=" * 60)
    
    # Run health check
    print("\n[1/5] Running system health check...")
    try:
        results = healer.run_full_diagnostic()
        print(f"    Status: {results['overall']}")
        healer.auto_repair(results)
    except Exception as e:
        print(f"    Warning: {e}")
    
    # Run mega scraper
    print("\n[2/5] Scraping 20+ job sources...")
    try:
        jobs = mega_scrape()
        print(f"    Found {len(jobs)} jobs from all sources")
    except Exception as e:
        print(f"    Warning: {e}")
        jobs = []
    
    # Apply to jobs
    print("\n[3/5] Applying to discovered jobs...")
    applied = 0
    max_apply = 25  # MAX POWER: Apply to 25 jobs
    
    for job in jobs[:max_apply]:
        try:
            if apply_to_company(job):
                applied += 1
            time.sleep(random.uniform(1, 3))  # Delay between applications
        except Exception as e:
            logger.error(f"Apply error: {e}")
    
    print(f"    Applied to {applied} companies")
    
    # Apply to TOP GCC companies
    print("\n[4/5] Targeting TOP GCC companies...")
    gcc_applied = 0
    max_gcc = 20  # Apply to 20 GCC companies
    
    for company in TOP_GCC_COMPANIES[:max_gcc]:
        try:
            name = company.get("name", "")
            website = company.get("website", "")
            
            # Get email
            email, source = get_company_email(name, website)
            
            job_data = {
                "company_name": name,
                "email": email,
                "job_title": "HR & Operations",
                "location": "GCC",
                "platform": "gcc_direct"
            }
            
            if apply_to_company(job_data):
                gcc_applied += 1
            
            time.sleep(random.uniform(0.5, 2))
        except Exception as e:
            logger.error(f"GCC apply error: {e}")
    
    print(f"    Applied to {gcc_applied} GCC companies")
    
    # Run follow-up
    print("\n[5/5] Checking for follow-ups...")
    try:
        followup = FollowUpSystem()
        targets = followup.get_followup_targets()
        print(f"    {len(targets)} companies need follow-up")
    except Exception as e:
        print(f"    Warning: {e}")
    
    # Summary
    print("\n" + "=" * 60)
    print("MAX POWER SUMMARY")
    print("=" * 60)
    
    tracker = load_tracker()
    total = len(tracker.get("applications", []))
    
    print(f"\n  Jobs scraped:    {len(jobs)}")
    print(f"  Applied today:   {applied + gcc_applied}")
    print(f"  Total applied:  {total}")
    print(f"  Follow-ups:     {len(targets) if 'targets' in dir() else 0}")
    
    print("\n" + "=" * 60)
    print("SAM MAX POWER COMPLETE!")
    print("=" * 60)

if __name__ == "__main__":
    run_max_power()
