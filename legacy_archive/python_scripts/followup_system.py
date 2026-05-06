"""
SAM FOLLOW-UP SYSTEM
=====================
Automatic follow-up emails after 3-7 days
"""

import json
import os
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class FollowUpSystem:
    """Automatic follow-up email sender"""
    
    def __init__(self, tracker_file="tracker.json"):
        self.tracker_file = tracker_file
        self.followup_days = 5  # Follow up after 5 days
        self.max_followups = 2  # Max 2 follow-ups per company
        
    def load_tracker(self):
        """Load application tracker"""
        if os.path.exists(self.tracker_file):
            try:
                with open(self.tracker_file, 'r') as f:
                    return json.load(f)
            except Exception:
                return {"applications": []}
        return {"applications": []}
    
    def save_tracker(self, data):
        """Save tracker"""
        try:
            with open(self.tracker_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            logger.error(f"Save error: {e}")
    
    def get_followup_targets(self):
        """Get companies that need follow-up"""
        tracker = self.load_tracker()
        applications = tracker.get("applications", [])
        targets = []
        
        now = datetime.now()
        
        for app in applications:
            applied_date = app.get("date", "")
            company = app.get("company_name", "Unknown")
            email = app.get("email", "")
            job_title = app.get("job_title", "")
            followup_count = app.get("followup_count", 0)
            last_followup = app.get("last_followup", "")
            
            # Skip if max followups reached
            if followup_count >= self.max_followups:
                continue
            
            # Calculate days since application
            try:
                app_date = datetime.fromisoformat(applied_date.replace('Z', '+00:00'))
                days_since = (now - app_date).days
            except Exception:
                continue
            
            # If it's been more than followup_days and no recent followup
            if days_since >= self.followup_days:
                # Check if we followed up recently
                if last_followup:
                    try:
                        last_date = datetime.fromisoformat(last_followup.replace('Z', '+00:00'))
                        days_since_followup = (now - last_date).days
                        if days_since_followup < self.followup_days:
                            continue
                    except Exception:
                        pass
                
                targets.append({
                    "company": company,
                    "email": email,
                    "job_title": job_title,
                    "days_since": days_since,
                    "followup_count": followup_count,
                    "applied_date": applied_date
                })
        
        logger.info(f"Found {len(targets)} companies needing follow-up")
        return targets
    
    def mark_followup_sent(self, company, email):
        """Mark that follow-up was sent"""
        tracker = self.load_tracker()
        
        for app in tracker.get("applications", []):
            if app.get("company_name") == company or app.get("email") == email:
                app["followup_count"] = app.get("followup_count", 0) + 1
                app["last_followup"] = datetime.now().isoformat()
                break
        
        self.save_tracker(tracker)
    
    def generate_followup_email(self, company, job_title):
        """Generate a follow-up email"""
        templates = [
            """Dear HR Team at {company},

I hope this email finds you well. I wanted to follow up on my application for the {job_title} position that I submitted recently.

I remain very interested in this opportunity and would love to discuss how my skills and experience align with your team's needs.

Please let me know if you need any additional information from my end.

Thank you for your time and consideration.

Best regards,
Sam Salameh
HR & Operations Professional
+961 76 005 412
sam.dev1@outlook.com""",
            
            """Dear Hiring Manager at {company},

I am writing to follow up on my application for the {job_title} role.

I understand that the hiring process takes time, and I wanted to express my continued enthusiasm for this position.

I would be happy to provide any additional information or references upon request.

Looking forward to hearing from you.

Best regards,
Sam Salameh""",
            
            """Hello {company} Team,

I recently applied for the {job_title} position and wanted to check on the status of my application.

I am very excited about the possibility of joining your organization and believe my HR and operations background would be a great fit.

Please don't hesitate to contact me if you need anything.

Best regards,
Sam Salameh"""
        ]
        
        import random
        template = random.choice(templates)
        return template.format(company=company, job_title=job_title)

# ============================================
# QUICK FOLLOWUP SCRIPT
# ============================================

def run_followup():
    """Run follow-up system"""
    print("=" * 50)
    print("SAM FOLLOW-UP SYSTEM")
    print("=" * 50)
    
    system = FollowUpSystem()
    targets = system.get_followup_targets()
    
    if not targets:
        print("\nNo follow-ups needed at this time.")
        return
    
    print(f"\nFound {len(targets)} companies to follow up with:\n")
    
    for i, target in enumerate(targets[:10], 1):
        print(f"{i}. {target['company']}")
        print(f"   Position: {target['job_title']}")
        print(f"   Days since application: {target['days_since']}")
        print(f"   Follow-ups sent: {target['followup_count']}")
        print()
    
    print(f"\nRun the main bot to send these follow-up emails.")
    print(f"Total pending: {len(targets)}")

if __name__ == "__main__":
    run_followup()
