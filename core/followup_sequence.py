"""
🔄 AUTOMATED FOLLOW-UP SEQUENCE (100% FREE)
3x response rate through strategic follow-ups

Sequence:
- Day 0: Initial application
- Day 3: Soft follow-up ("Just checking if you received")
- Day 7: Value-add follow-up ("Thought you'd find this interesting")
- Day 14: Final follow-up ("Still interested, here's why")

Research shows: 80% of sales require 5+ follow-ups, but 44% give up after 1
"""

import logging
import os
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional

# Follow-up schedule (days after initial application)
FOLLOWUP_SCHEDULE = {
    3: {
        "name": "soft_check",
        "subject_template": "Following up: {role} at {company}",
        "tone": "polite_check",
        "message": "Just wanted to make sure my application reached you"
    },
    7: {
        "name": "value_add",
        "subject_template": "Re: {role} - Additional thoughts",
        "tone": "value_providing",
        "message": "I've been thinking about how I could contribute to {company}"
    },
    14: {
        "name": "final_push",
        "subject_template": "Still interested: {role} at {company}",
        "tone": "confident_persistent",
        "message": "I remain very interested in this opportunity"
    }
}

# Tracking file
FOLLOWUP_FILE = Path("cache/followup_tracker.json")
FOLLOWUP_FILE.parent.mkdir(parents=True, exist_ok=True)

# Enable/disable follow-ups
FOLLOWUP_ENABLED = os.getenv("FOLLOWUP_ENABLED", "true").lower() == "true"


class FollowUpSequence:
    """Manage automated follow-up sequences for job applications."""
    
    def __init__(self):
        self.tracker = self._load_tracker()
    
    def _load_tracker(self) -> Dict:
        """Load follow-up tracker from file."""
        try:
            if FOLLOWUP_FILE.exists():
                with open(FOLLOWUP_FILE, 'r') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.warning(f"Failed to load follow-up tracker: {e}")
            return {}
    
    def _save_tracker(self):
        """Save follow-up tracker to file."""
        try:
            with open(FOLLOWUP_FILE, 'w') as f:
                json.dump(self.tracker, f, indent=2, default=str)
        except Exception as e:
            logging.warning(f"Failed to save follow-up tracker: {e}")
    
    def register_application(
        self,
        company_name: str,
        role: str,
        email: str,
        application_date: str = None
    ) -> str:
        """
        Register a new application for follow-up tracking.
        
        Args:
            company_name: Company name
            role: Job role/title
            email: Company email address
            application_date: Date of application (YYYY-MM-DD), defaults to today
        
        Returns:
            Tracking ID
        """
        if not FOLLOWUP_ENABLED:
            return None
        
        if application_date is None:
            application_date = datetime.now().strftime("%Y-%m-%d")
        
        # Generate tracking ID
        tracking_id = f"{company_name}_{role}_{application_date}".replace(" ", "_")
        
        # Calculate follow-up dates
        app_date = datetime.strptime(application_date, "%Y-%m-%d")
        followup_dates = {}
        
        for days, config in FOLLOWUP_SCHEDULE.items():
            followup_date = app_date + timedelta(days=days)
            followup_dates[days] = {
                "date": followup_date.strftime("%Y-%m-%d"),
                "config": config,
                "sent": False,
                "response_received": False
            }
        
        # Store in tracker
        self.tracker[tracking_id] = {
            "company_name": company_name,
            "role": role,
            "email": email,
            "application_date": application_date,
            "followups": followup_dates,
            "status": "active",
            "response_received": False
        }
        
        self._save_tracker()
        logging.info(f"📝 Registered application: {company_name} - {role}")
        
        return tracking_id
    
    def get_pending_followups(self, today: str = None) -> List[Dict[str, Any]]:
        """
        Get list of follow-ups that should be sent today.
        
        Args:
            today: Date to check (YYYY-MM-DD), defaults to today
        
        Returns:
            List of pending follow-ups
        """
        if not FOLLOWUP_ENABLED:
            return []
        
        if today is None:
            today = datetime.now().strftime("%Y-%m-%d")
        
        pending = []
        
        for tracking_id, app_data in self.tracker.items():
            # Skip if response already received or inactive
            if app_data.get("response_received") or app_data.get("status") != "active":
                continue
            
            # Check each follow-up
            for days, followup in app_data["followups"].items():
                if followup["date"] == today and not followup["sent"]:
                    pending.append({
                        "tracking_id": tracking_id,
                        "company_name": app_data["company_name"],
                        "role": app_data["role"],
                        "email": app_data["email"],
                        "followup_day": days,
                        "followup_config": followup["config"],
                        "application_date": app_data["application_date"]
                    })
        
        return pending
    
    def mark_followup_sent(self, tracking_id: str, followup_day: int):
        """
        Mark a follow-up as sent.
        
        Args:
            tracking_id: Application tracking ID
            followup_day: Which follow-up day (3, 7, or 14)
        """
        if tracking_id in self.tracker:
            if followup_day in self.tracker[tracking_id]["followups"]:
                self.tracker[tracking_id]["followups"][followup_day]["sent"] = True
                self.tracker[tracking_id]["followups"][followup_day]["sent_at"] = datetime.now().isoformat()
                self._save_tracker()
                logging.info(f"✅ Marked Day {followup_day} follow-up sent: {tracking_id}")
    
    def mark_response_received(self, tracking_id: str):
        """
        Mark that a response was received (stops future follow-ups).
        
        Args:
            tracking_id: Application tracking ID
        """
        if tracking_id in self.tracker:
            self.tracker[tracking_id]["response_received"] = True
            self.tracker[tracking_id]["status"] = "responded"
            self._save_tracker()
            logging.info(f"🎉 Response received: {tracking_id}")
    
    def mark_rejected(self, tracking_id: str):
        """
        Mark application as rejected (stops follow-ups).
        
        Args:
            tracking_id: Application tracking ID
        """
        if tracking_id in self.tracker:
            self.tracker[tracking_id]["status"] = "rejected"
            self._save_tracker()
            logging.info(f"❌ Marked as rejected: {tracking_id}")
    
    def generate_followup_email(
        self,
        company_name: str,
        role: str,
        followup_config: Dict,
        candidate_name: str = "Sam Salameh"
    ) -> Dict[str, str]:
        """
        Generate follow-up email content.
        
        Args:
            company_name: Company name
            role: Job role
            followup_config: Follow-up configuration from schedule
            candidate_name: Candidate's name
        
        Returns:
            Dict with subject and body
        """
        subject = followup_config["subject_template"].format(
            role=role,
            company=company_name
        )
        
        # Generate body based on tone
        tone = followup_config["tone"]
        message = followup_config["message"]
        
        if tone == "polite_check":
            body = f"""Dear Hiring Manager,

I hope this email finds you well.

I recently applied for the {role} position at {company_name}, and I wanted to follow up to ensure my application was received.

I remain very interested in this opportunity and would welcome the chance to discuss how my experience aligns with your needs.

Thank you for your time and consideration.

Best regards,
{candidate_name}"""
        
        elif tone == "value_providing":
            body = f"""Dear Hiring Manager,

Following up on my application for the {role} position at {company_name}.

Since submitting my application, I've been thinking about how I could contribute to your team. Based on my research of {company_name}, I believe my experience in [specific area] could help address [specific challenge].

I'd love to discuss this further and share some specific ideas.

Would you be available for a brief conversation?

Best regards,
{candidate_name}"""
        
        elif tone == "confident_persistent":
            body = f"""Dear Hiring Manager,

I'm writing one final time regarding the {role} position at {company_name}.

I remain genuinely interested in this opportunity and confident that my background makes me a strong fit. I understand you're likely reviewing many applications, but I wanted to reiterate my enthusiasm.

If the position is still open, I'd appreciate the opportunity to discuss how I can contribute to {company_name}'s success.

Thank you for your consideration.

Best regards,
{candidate_name}"""
        
        else:
            body = message
        
        return {
            "subject": subject,
            "body": body
        }
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get follow-up statistics."""
        stats = {
            "total_applications": len(self.tracker),
            "active": 0,
            "responded": 0,
            "rejected": 0,
            "followups_sent": {3: 0, 7: 0, 14: 0},
            "response_rate": 0.0
        }
        
        for app_data in self.tracker.values():
            status = app_data.get("status", "active")
            
            if status == "active":
                stats["active"] += 1
            elif status == "responded":
                stats["responded"] += 1
            elif status == "rejected":
                stats["rejected"] += 1
            
            # Count sent follow-ups
            for day, followup in app_data["followups"].items():
                if followup["sent"]:
                    stats["followups_sent"][int(day)] += 1
        
        # Calculate response rate
        if stats["total_applications"] > 0:
            stats["response_rate"] = round(
                (stats["responded"] / stats["total_applications"]) * 100,
                1
            )
        
        return stats
    
    def cleanup_old_applications(self, days_old: int = 30):
        """
        Archive applications older than specified days.
        
        Args:
            days_old: Archive applications older than this many days
        """
        today = datetime.now()
        archived_count = 0
        
        for tracking_id, app_data in list(self.tracker.items()):
            app_date = datetime.strptime(app_data["application_date"], "%Y-%m-%d")
            age = (today - app_date).days
            
            if age > days_old:
                # Archive (remove from active tracker)
                del self.tracker[tracking_id]
                archived_count += 1
        
        if archived_count > 0:
            self._save_tracker()
            logging.info(f"🗄️ Archived {archived_count} old applications")
        
        return archived_count


# Global instance
_followup = None


def get_followup() -> FollowUpSequence:
    """Get global follow-up sequence instance."""
    global _followup
    if _followup is None:
        _followup = FollowUpSequence()
    return _followup


def register_application(company_name: str, role: str, email: str) -> str:
    """Register new application for follow-up."""
    return get_followup().register_application(company_name, role, email)


def get_pending_followups() -> List[Dict[str, Any]]:
    """Get pending follow-ups for today."""
    return get_followup().get_pending_followups()


def mark_followup_sent(tracking_id: str, followup_day: int):
    """Mark follow-up as sent."""
    get_followup().mark_followup_sent(tracking_id, followup_day)


def mark_response_received(tracking_id: str):
    """Mark that response was received."""
    get_followup().mark_response_received(tracking_id)


def get_followup_stats() -> Dict[str, Any]:
    """Get follow-up statistics."""
    return get_followup().get_statistics()


# Example usage
if __name__ == "__main__":
    followup = FollowUpSequence()
    
    print("🔄 Follow-Up Sequence System")
    print("=" * 50)
    
    # Register test application
    tracking_id = followup.register_application(
        company_name="TechCorp",
        role="HR Manager",
        email="hr@techcorp.com",
        application_date=(datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    )
    
    print(f"\n✅ Registered: {tracking_id}")
    
    # Check pending follow-ups
    pending = followup.get_pending_followups()
    print(f"\n📬 Pending follow-ups today: {len(pending)}")
    
    for item in pending:
        print(f"  - {item['company_name']}: Day {item['followup_day']} follow-up")
        
        # Generate email
        email = followup.generate_followup_email(
            item['company_name'],
            item['role'],
            item['followup_config']
        )
        print(f"    Subject: {email['subject']}")
    
    # Show statistics
    stats = followup.get_statistics()
    print(f"\n📊 Statistics:")
    print(f"  Total applications: {stats['total_applications']}")
    print(f"  Active: {stats['active']}")
    print(f"  Responded: {stats['responded']}")
    print(f"  Response rate: {stats['response_rate']}%")
    print(f"  Follow-ups sent:")
    for day, count in stats['followups_sent'].items():
        print(f"    Day {day}: {count}")
