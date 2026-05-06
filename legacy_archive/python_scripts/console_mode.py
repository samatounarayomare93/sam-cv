"""
SAM CONSOLE MODE - Simple Version
Run without Telegram for testing
"""

import os
import sys
import time
import json
import random
import logging
from datetime import datetime

# Change to script directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Import project modules
import config
from scraper import get_latest_jobs, scrape_linkedin_jobs, scrape_hirelebanese_jobs, scrape_monster_jobs, scrape_bayt_jobs
from system_health import HealthCheck, CompanyDatabase, MetricsTracker
from global_company_scraper import GlobalCompanyScraper

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def load_tracker():
    if os.path.exists("tracker.json"):
        try:
            with open("tracker.json", 'r') as f:
                return json.load(f)
        except Exception:
            return {"applications": []}
    return {"applications": []}

def save_tracker(data):
    with open("tracker.json", 'w') as f:
        json.dump(data, f, indent=2)

def run_console_mode():
    print("\n" + "="*60)
    print("SAM JOB AUTOMATOR - CONSOLE MODE")
    print("="*60)
    print("\n[OK] Initializing components...")
    
    # Initialize health check
    try:
        health_check = HealthCheck()
        print("[OK] Health check initialized")
    except Exception as e:
        print(f"[WARN] Health check failed: {e}")
        health_check = None
    
    # Initialize company database
    try:
        company_db = CompanyDatabase()
        print(f"[OK] Company database: {company_db.count} companies")
    except Exception as e:
        print(f"[WARN] Company database failed: {e}")
        company_db = None
    
    # Initialize metrics tracker
    try:
        metrics = MetricsTracker()
        print("[OK] Metrics tracker initialized")
    except Exception as e:
        print(f"[WARN] Metrics failed: {e}")
        metrics = None
    
    # Initialize company scraper
    try:
        company_scraper = GlobalCompanyScraper()
        print("[OK] Company scraper initialized")
    except Exception as e:
        print(f"[WARN] Company scraper failed: {e}")
        company_scraper = None
    
    print("\n" + "-"*60)
    print("Starting auto-pilot mission loop...")
    print("Press Ctrl+C to stop")
    print("-"*60)
    
    cycle = 0
    try:
        while True:
            cycle += 1
            print(f"\n[CYCLE {cycle}] Starting mission cycle...")
            
            try:
                # Scrape jobs from all sources
                print("[SCRAP] Searching for jobs...")
                all_jobs = []
                
                # LinkedIn
                print("  - LinkedIn...")
                try:
                    li_jobs = scrape_linkedin_jobs("UAE", "HR Manager")
                    all_jobs.extend(li_jobs)
                except: pass
                
                # Hire Lebanese
                print("  - HireLebanese...")
                try:
                    hl_jobs = scrape_hirelebanese_jobs()
                    all_jobs.extend(hl_jobs)
                except: pass
                
                # Monster
                print("  - Monster...")
                try:
                    mo_jobs = scrape_monster_jobs("Lebanon", "HR")
                    all_jobs.extend(mo_jobs)
                except: pass
                
                # Bayt
                print("  - Bayt...")
                try:
                    ba_jobs = scrape_bayt_jobs("lebanon", "hr")
                    all_jobs.extend(ba_jobs)
                except: pass
                
                print(f"[FOUND] {len(all_jobs)} jobs discovered")
                
                if all_jobs and metrics:
                    metrics.increment_today('jobs_analyzed', len(all_jobs))
                
                # Save to tracker
                tracker = load_tracker()
                for job in all_jobs[:10]:  # Save top 10
                    company = job.get('company_name', 'Unknown')
                    already_applied = any(
                        a.get('company_name', '').lower() == company.lower() 
                        for a in tracker.get('applications', [])
                    )
                    if not already_applied:
                        tracker.setdefault('applications', []).append({
                            'company_name': company,
                            'email': job.get('email', ''),
                            'job_title': job.get('job_title', ''),
                            'location': job.get('location', ''),
                            'platform': job.get('platform', 'direct'),
                            'date': datetime.now().isoformat(),
                            'status': 'discovered'
                        })
                
                save_tracker(tracker)
                print(f"[TRACKER] {len(tracker.get('applications', []))} total applications")
                
                # Update metrics
                if metrics:
                    metrics.increment_today('applications_sent', min(len(all_jobs), 10))
                
            except Exception as e:
                print(f"[ERROR] Cycle failed: {e}")
            
            print(f"\n[SLEEP] Next cycle in 15 minutes...")
            print("-"*60)
            time.sleep(900)  # 15 minutes
            
    except KeyboardInterrupt:
        print("\n\n[STOP] Sam stopped by user")
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
    
    print("\n[DONE] Sam stopped.")

if __name__ == "__main__":
    run_console_mode()
