"""
Auto Follow-Up System
Automatically sends follow-up emails after initial application
"""

import os
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any

class AutoFollowUpSystem:
    """Automated follow-up email system"""
    
    def __init__(self):
        self.follow_up_schedule = {
            "day3": {
                "enabled": os.getenv("FOLLOWUP_DAY3", "true").lower() == "true",
                "days": 3,
                "subject_template": "Following up on my application - {title}",
                "body_template": """Dear {company} Team,

I hope this email finds you well.

I wanted to follow up on my application for the {title} position that I submitted on {date}. 
I remain very interested in this opportunity and would love to learn more about the next steps 
in your hiring process.

I believe my experience in network engineering and my skills in {key_skills} would make me 
a strong addition to your team.

Please let me know if you need any additional information from me.

Thank you for your time and consideration.

Best regards,
Sam Salameh
📧 samsalameh.cv@gmail.com
📱 +961 70 841 1009
"""
            },
            "day7": {
                "enabled": os.getenv("FOLLOWUP_DAY7", "true").lower() == "true",
                "days": 7,
                "subject_template": "Checking in - {title} Application",
                "body_template": """Dear {company} Hiring Team,

I hope you're doing well.

I'm writing to check in on the status of my application for the {title} position. 
I submitted my application on {date} and wanted to reiterate my strong interest in 
joining your team.

I'm particularly excited about this opportunity because {reason}.

If there's any additional information I can provide or if you'd like to schedule 
a conversation, I'm available at your convenience.

Thank you again for considering my application.

Best regards,
Sam Salameh
Senior Network Engineer
📧 samsalameh.cv@gmail.com
📱 +961 70 841 1009
🔗 linkedin.com/in/sam-salameh
"""
            },
            "day14": {
                "enabled": os.getenv("FOLLOWUP_DAY14", "true").lower() == "true",
                "days": 14,
                "subject_template": "Final follow-up - {title} Position",
                "body_template": """Dear {company} Team,

I hope this message finds you well.

I wanted to reach out one final time regarding my application for the {title} position 
submitted on {date}.

I understand you're likely reviewing many applications, and I wanted to express my 
continued interest in this opportunity. My background in {experience} aligns well 
with the requirements, and I'm confident I could contribute significantly to your team.

If the position has been filled or if you've decided to move forward with other candidates, 
I completely understand. However, I would appreciate any feedback you could share, and 
I'd love to be considered for future opportunities at {company}.

Thank you for your time and consideration throughout this process.

Best regards,
Sam Salameh
📧 samsalameh.cv@gmail.com
📱 +961 70 841 1009
"""
            }
        }
    
    def should_send_followup(self, application: Dict[str, Any], followup_type: str) -> bool:
        """Check if follow-up should be sent"""
        
        # Check if this follow-up type is enabled
        if not self.follow_up_schedule[followup_type]["enabled"]:
            return False
        
        # Check if already sent
        followups_sent = application.get("followups_sent", [])
        if followup_type in followups_sent:
            return False
        
        # Check if enough time has passed
        sent_date = application.get("sent_date")
        if not sent_date:
            return False
        
        if isinstance(sent_date, str):
            sent_date = datetime.fromisoformat(sent_date)
        
        days_passed = (datetime.now() - sent_date).days
        required_days = self.follow_up_schedule[followup_type]["days"]
        
        if days_passed < required_days:
            return False
        
        # Check if got response
        if application.get("response_received"):
            return False
        
        # Check if rejected
        if application.get("status") == "rejected":
            return False
        
        return True
    
    def generate_followup_email(self, application: Dict[str, Any], followup_type: str) -> Dict[str, str]:
        """Generate follow-up email content"""
        
        schedule = self.follow_up_schedule[followup_type]
        job = application.get("job", {})
        
        # Extract job details
        title = job.get("title", "the position")
        company = job.get("company", "your company")
        sent_date = application.get("sent_date", datetime.now())
        
        if isinstance(sent_date, str):
            sent_date = datetime.fromisoformat(sent_date)
        
        date_str = sent_date.strftime("%B %d, %Y")
        
        # Generate subject
        subject = schedule["subject_template"].format(
            title=title,
            company=company
        )
        
        # Generate body
        body = schedule["body_template"].format(
            title=title,
            company=company,
            date=date_str,
            key_skills="Cisco, Juniper, BGP, OSPF, network security",
            reason="it aligns perfectly with my career goals and expertise",
            experience="network engineering and infrastructure management"
        )
        
        return {
            "subject": subject,
            "body": body,
            "type": followup_type
        }
    
    async def process_followups(self, db_manager) -> Dict[str, int]:
        """Process all pending follow-ups"""
        
        stats = {
            "day3": 0,
            "day7": 0,
            "day14": 0,
            "total": 0
        }
        
        # Get all applications without responses
        applications = await db_manager.get_pending_applications()
        
        for app in applications:
            for followup_type in ["day3", "day7", "day14"]:
                if self.should_send_followup(app, followup_type):
                    # Generate email
                    email_content = self.generate_followup_email(app, followup_type)
                    
                    # Send email
                    success = await self._send_followup_email(app, email_content)
                    
                    if success:
                        # Mark as sent
                        await db_manager.mark_followup_sent(app["id"], followup_type)
                        stats[followup_type] += 1
                        stats["total"] += 1
                        
                        # Log
                        print(f"✅ Sent {followup_type} follow-up to {app['job']['company']}")
                    
                    # Rate limiting
                    await asyncio.sleep(5)
        
        return stats
    
    async def _send_followup_email(self, application: Dict[str, Any], email_content: Dict[str, str]) -> bool:
        """Send follow-up email"""
        try:
            from core.smtp_engine import send_strike
            
            job = application.get("job", {})
            email = application.get("email")
            
            if not email:
                return False
            
            result = await send_strike(
                to_email=email,
                subject=email_content["subject"],
                body=email_content["body"],
                job_data=job,
                attachments=[]  # No attachments for follow-ups
            )
            
            return result.get("success", False)
            
        except Exception as e:
            print(f"❌ Follow-up email error: {e}")
            return False
    
    def get_followup_stats(self, applications: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get follow-up statistics"""
        
        stats = {
            "total_applications": len(applications),
            "pending_day3": 0,
            "pending_day7": 0,
            "pending_day14": 0,
            "sent_day3": 0,
            "sent_day7": 0,
            "sent_day14": 0,
            "responses_received": 0
        }
        
        for app in applications:
            followups_sent = app.get("followups_sent", [])
            
            if "day3" in followups_sent:
                stats["sent_day3"] += 1
            elif self.should_send_followup(app, "day3"):
                stats["pending_day3"] += 1
            
            if "day7" in followups_sent:
                stats["sent_day7"] += 1
            elif self.should_send_followup(app, "day7"):
                stats["pending_day7"] += 1
            
            if "day14" in followups_sent:
                stats["sent_day14"] += 1
            elif self.should_send_followup(app, "day14"):
                stats["pending_day14"] += 1
            
            if app.get("response_received"):
                stats["responses_received"] += 1
        
        return stats


# Global instance
_followup_system = None

def get_followup_system():
    """Get or create follow-up system instance"""
    global _followup_system
    if _followup_system is None:
        _followup_system = AutoFollowUpSystem()
    return _followup_system


async def process_followups(db_manager):
    """Quick helper to process follow-ups"""
    system = get_followup_system()
    return await system.process_followups(db_manager)
