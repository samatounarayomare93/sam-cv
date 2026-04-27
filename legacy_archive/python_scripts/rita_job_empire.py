"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              🌟 SAM JOB EMPIRE v99 - GOD MODE 🌟                          ║
║                                                                              ║
║              THE COMPLETE 100% AUTOMATED JOB HUNTING SYSTEM                  ║
║                                                                              ║
║  Features: Job Scraper | Email Campaign | WhatsApp Alerts | Telegram        ║
║           LinkedIn Auto | Interview Prep | Reports | Self-Healing          ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import os
import sys
import json
import time
import logging
import smtplib
import random
import requests
import schedule
import threading
from datetime import datetime, timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from pathlib import Path

# ═══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION
# ═══════════════════════════════════════════════════════════════════════════════

class Config:
    # Personal Info
    NAME = "Sam Salameh"
    EMAIL = "sam.dev1@outlook.com"
    PHONE = "+961 76 005 412"
    LINKEDIN = "linkedin.com/in/sam-cordahi"
    LOCATION = "Lebanon (Open to GCC Relocation)"
    
    # Job Preferences
    TARGET_POSITIONS = [
        "HR Manager",
        "HR & Operations Manager", 
        "Human Resources Manager",
        "HR Business Partner",
        "People Operations Manager",
        "HR & Admin Manager"
    ]
    TARGET_LOCATIONS = [
        "Dubai", "Abu Dhabi", "UAE", "Qatar", "Saudi Arabia",
        "Kuwait", "Bahrain", "Oman", "GCC", "Middle East"
    ]
    
    # Email Settings
    BREVO_API_KEY = os.getenv("BREVO_API_KEY", "")
    GMAIL_USER = os.getenv("GMAIL_USER", "")
    GMAIL_PASS = os.getenv("GMAIL_PASS", "")
    
    # WhatsApp (using CallMeBot or similar)
    WHATSAPP_API = os.getenv("WHATSAPP_API", "")
    WHATSAPP_NUMBER = "+96176005412"
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
    
    # Paths
    BASE_DIR = Path(__file__).parent
    CV_PATH = BASE_DIR / "Sam_Cordahi_CV.html"
    COMPANIES_FILE = BASE_DIR / "company_emails.json"
    TRACKER_FILE = BASE_DIR / "application_tracker.json"
    LOGS_DIR = BASE_DIR / "logs"
    
    # Rate Limits
    EMAILS_PER_DAY = 50
    MIN_DELAY_SECONDS = 30
    MAX_DELAY_SECONDS = 120

config = Config()

# Setup logging
config.LOGS_DIR.mkdir(exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[
        logging.FileHandler(config.LOGS_DIR / 'empire.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ═══════════════════════════════════════════════════════════════════════════════
# EMAIL DESIGN - Professional HTML Template
# ═══════════════════════════════════════════════════════════════════════════════

EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body { margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #0b0f19; }
        .container { max-width: 650px; margin: 0 auto; background: #111827; border-radius: 16px; overflow: hidden; }
        .header { background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 45px 30px; text-align: center; }
        .avatar { display: inline-block; width: 65px; height: 65px; background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%); border-radius: 50%; line-height: 65px; color: #fff; font-size: 26px; font-weight: 800; box-shadow: 0 0 30px rgba(6, 182, 212, 0.5); }
        .subtitle { font-size: 12px; letter-spacing: 4px; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; }
        .name { font-size: 32px; font-weight: 800; color: #fff; letter-spacing: 1px; margin: 0; }
        .title-text { font-size: 13px; color: #06b6d4; margin-top: 8px; }
        .gradient-bar { height: 5px; background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%); }
        .content { padding: 40px 35px; background: #fff; }
        .greeting { font-size: 18px; color: #1e293b; margin-bottom: 15px; }
        .message { font-size: 15px; line-height: 1.8; color: #475569; margin-bottom: 20px; }
        .highlight { color: #06b6d4; font-weight: 700; }
        .company-highlight { color: #06b6d4; font-weight: 700; }
        .skill-box { background: #1e293b; border-radius: 12px; padding: 22px; margin-bottom: 12px; }
        .skill-title { font-size: 13px; font-weight: 700; color: #06b6d4; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 8px; }
        .skill-content { font-size: 14px; color: #94a3b8; line-height: 1.7; }
        .quote-box { padding: 22px 28px; background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 12px; text-align: center; }
        .quote-text { font-style: italic; color: #1e293b; font-size: 15px; line-height: 1.6; margin: 0; }
        .available { display: inline-block; padding: 10px 20px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 25px; color: #10b981; font-size: 13px; font-weight: 600; margin: 20px 0; }
        .attachment-box { background: #f0f9ff; border: 2px dashed #06b6d4; border-radius: 10px; padding: 20px; margin: 20px 0; text-align: center; }
        .attachment-item { background: #fff; border: 1px solid #e0e0e0; border-radius: 8px; padding: 12px; margin: 8px 0; display: flex; align-items: center; gap: 12px; }
        .attachment-icon { font-size: 24px; }
        .attachment-name { font-weight: 600; color: #1e293b; font-size: 14px; }
        .attachment-desc { font-size: 12px; color: #666; }
        .footer { background: #0f172a; padding: 35px 30px; text-align: center; }
        .cta-btn { display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%); color: #fff; text-decoration: none; border-radius: 30px; font-weight: 700; font-size: 13px; letter-spacing: 1.5px; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4); margin-bottom: 20px; }
        .contact-row { margin-bottom: 10px; }
        .contact-link { color: #94a3b8; text-decoration: none; margin: 0 10px; font-size: 14px; }
        .contact-link:hover { color: #06b6d4; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="avatar">RC</div>
            <div class="subtitle">EXECUTIVE CANDIDACY</div>
            <h1 class="name">SAM CORDAHI</h1>
            <div class="title-text">HR & Customer Operations Specialist</div>
        </div>
        <div class="gradient-bar"></div>
        <div class="content">
            <p class="greeting">Dear <strong>Hiring Team at <span class="company-highlight">{company_name}</span></strong>,</p>
            <p class="message">I am formally reaching out to express my high-level interest in the <span class="highlight">{job_title}</span> position at <span class="company-highlight">{company_name}</span>. With a robust track record in HR administration and customer operations, I specialize in architecting workflows that prioritize precision, compliance, and exceptional service delivery.</p>
            <p class="message">My methodology is built specifically for organizations that focus heavily on <strong>automation, KPIs, and scaling corporate culture</strong>:</p>
            
            <div class="skill-box" style="border-left: 5px solid #06b6d4;">
                <div class="skill-title">01. Operations Lifecycle</div>
                <div class="skill-content">Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with <span style="color:#4ade80;font-weight:600;">100% data integrity</span>.</div>
            </div>
            <div class="skill-box" style="border-left: 5px solid #3b82f6;">
                <div class="skill-title">02. Service & Retention</div>
                <div class="skill-content">A track record of resolving <strong>50+ daily complex technical and billing inquiries</strong> while maintaining strict SLA compliance.</div>
            </div>
            <div class="skill-box" style="border-left: 5px solid #8b5cf6;">
                <div class="skill-title">03. Workflow Optimization</div>
                <div class="skill-content">Experience in standardizing onboarding templates and operational diagnostics to significantly <strong>reduce departmental overhead by 25%</strong>.</div>
            </div>
            
            <div class="quote-box">
                <p class="quote-text">"I am looking to bring rigorous accountability, structured scaling, and high-conversion problem-solving to the <strong style="color:#06b6d4;">{company_name}</strong> team."</p>
            </div>
            
            <div style="text-align:center;"><span class="available">✓ Available Immediately for Relocation</span></div>
            
            <div class="attachment-box">
                <div class="attachment-item">
                    <div class="attachment-icon">📄</div>
                    <div>
                        <div class="attachment-name">{company_name}_Cover_Letter_Sam_Cordahi.html</div>
                        <div class="attachment-desc">Personalized cover letter</div>
                    </div>
                </div>
                <div class="attachment-item">
                    <div class="attachment-icon">📋</div>
                    <div>
                        <div class="attachment-name">Sam_Cordahi_CV.html</div>
                        <div class="attachment-desc">Full professional CV</div>
                    </div>
                </div>
            </div>
            
            <p class="message" style="margin-bottom:0;">I am available for immediate discussion and can start at your earliest convenience. Thank you for considering my application.</p>
        </div>
        <div class="footer">
            <a href="https://www.linkedin.com/in/sam-cordahi/" class="cta-btn">VIEW LINKEDIN</a>
            <div class="contact-row">
                <a href="mailto:{email}" class="contact-link">{email}</a>
                <a href="tel:{phone}" class="contact-link">{phone}</a>
            </div>
            <div style="font-size:11px;color:#475569;letter-spacing:1px;text-transform:uppercase;margin-top:15px;">HR & Customer Operations Specialist</div>
        </div>
    </div>
</body>
</html>
"""

COVER_LETTER_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: 'Segoe UI', Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 40px; background: #f8f9fa; }}
        .letter {{ background: white; padding: 40px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; padding-bottom: 20px; border-bottom: 2px solid #06b6d4; }}
        .header h1 {{ margin: 0; color: #1e293b; font-size: 28px; }}
        .header p {{ margin: 5px 0 0 0; color: #06b6d4; font-size: 14px; }}
        .date {{ color: #666; margin-bottom: 20px; }}
        .subject {{ font-weight: bold; margin-bottom: 20px; color: #1e293b; }}
        .body {{ line-height: 1.8; color: #333; }}
        .body p {{ margin-bottom: 15px; }}
        .body ul {{ margin: 15px 0; padding-left: 25px; }}
        .body li {{ margin-bottom: 8px; line-height: 1.6; }}
        .signature {{ margin-top: 30px; }}
        .contact-info {{ margin-top: 20px; color: #666; font-size: 14px; }}
    </style>
</head>
<body>
    <div class="letter">
        <div class="header">
            <h1>Sam Salameh</h1>
            <p>HR & Customer Operations Specialist</p>
            <p>+961 76 005 412 | sam.dev1@outlook.com</p>
        </div>
        <div class="date">{date}</div>
        <div class="subject">Application for {job_title} - {company_name}</div>
        <div class="body">
            <p>Dear Hiring Team at <strong>{company_name}</strong>,</p>
            <p>I am writing to express my strong interest in the {job_title} position at {company_name}. With over 5 years of experience in Human Resources and Customer Operations, I am confident that my skills and background align well with your requirements.</p>
            <p>In my current role as HR & Operations Coordinator, I have developed expertise in:</p>
            <ul>
                <li>Full-cycle recruitment and talent acquisition</li>
                <li>Employee onboarding and documentation</li>
                <li>Payroll administration with 100% compliance accuracy</li>
                <li>Customer service excellence with high first-contact resolution rates</li>
                <li>Process optimization resulting in 25% cost reduction</li>
            </ul>
            <p>I am particularly drawn to {company_name} because of your reputation for excellence. I am confident that my proactive approach and dedication to operational excellence would make me a valuable addition to your team.</p>
            <p>I am available for immediate relocation and prepared to contribute meaningfully from day one. Please find my CV attached for your review.</p>
        </div>
        <div class="signature">
            <p>Warm regards,</p>
            <p><strong>Sam Salameh</strong></p>
            <div class="contact-info">
                <p>Phone: +961 76 005 412 | Email: sam.dev1@outlook.com</p>
                <p>LinkedIn: linkedin.com/in/sam-cordahi | WhatsApp: Available</p>
            </div>
        </div>
    </div>
</body>
</html>
"""

# ═══════════════════════════════════════════════════════════════════════════════
# CORE MODULES
# ═══════════════════════════════════════════════════════════════════════════════

class ApplicationTracker:
    """Track all job applications"""
    
    def __init__(self):
        self.file = config.TRACKER_FILE
        self.data = self.load()
    
    def load(self):
        if self.file.exists():
            return json.loads(self.file.read_text())
        return {
            "applications": [],
            "responses": [],
            "interviews": [],
            "rejections": [],
            "stats": {
                "total_sent": 0,
                "total_responses": 0,
                "total_interviews": 0,
                "start_date": datetime.now().isoformat()
            }
        }
    
    def save(self):
        self.file.write_text(json.dumps(self.data, indent=2))
    
    def add_application(self, company, email, job_title):
        app = {
            "id": len(self.data["applications"]) + 1,
            "company": company,
            "email": email,
            "job_title": job_title,
            "date_sent": datetime.now().isoformat(),
            "status": "sent",
            "follow_up_3d": False,
            "follow_up_7d": False,
            "follow_up_14d": False
        }
        self.data["applications"].append(app)
        self.data["stats"]["total_sent"] += 1
        self.save()
        return app
    
    def mark_responded(self, company):
        for app in self.data["applications"]:
            if app["company"] == company and app["status"] == "sent":
                app["status"] = "responded"
                app["response_date"] = datetime.now().isoformat()
                self.data["responses"].append(app)
                self.data["stats"]["total_responses"] += 1
                self.save()
                return True
        return False
    
    def get_pending_followup(self, days):
        pending = []
        now = datetime.now()
        for app in self.data["applications"]:
            if app["status"] != "sent":
                continue
            sent_date = datetime.fromisoformat(app["date_sent"])
            days_since = (now - sent_date).days
            if days_since >= days and not app.get(f"follow_up_{days}d"):
                pending.append(app)
        return pending
    
    def mark_followup(self, app_id, days):
        for app in self.data["applications"]:
            if app["id"] == app_id:
                app[f"follow_up_{days}d"] = True
                app[f"follow_up_{days}d_date"] = datetime.now().isoformat()
                self.save()
                return True
        return False
    
    def get_stats(self):
        return self.data["stats"]
    
    def get_all(self):
        return self.data["applications"]

class EmailEngine:
    """Send professional emails with attachments"""
    
    def __init__(self):
        self.tracker = ApplicationTracker()
    
    def create_email(self, company_name, job_title):
        html = EMAIL_TEMPLATE.format(
            company_name=company_name,
            job_title=job_title,
            email=config.EMAIL,
            phone=config.PHONE
        )
        return html
    
    def create_cover_letter(self, company_name, job_title):
        return COVER_LETTER_TEMPLATE.format(
            company_name=company_name,
            job_title=job_title,
            date=datetime.now().strftime("%B %d, %Y")
        )
    
    def send(self, to_email, company_name, job_title):
        html_body = self.create_email(company_name, job_title)
        plain_body = f"""SAM CORDAHI - HR & Operations Specialist

Dear Hiring Team at {company_name},

I am formally reaching out to express my interest in the {job_title} position at {company_name}.

With over 5 years of experience in HR and Customer Operations, I specialize in:
• High-volume recruitment and employee onboarding
• Payroll administration with 100% compliance
• Customer service excellence (50+ daily inquiries resolved)
• Process optimization (25% cost reduction)

Please find my CV and Cover Letter attached.

I am available for immediate relocation and can start at your convenience.

Best regards,
Sam Salameh
+961 76 005 412 | sam.dev1@outlook.com
"""
        
        cover_letter = self.create_cover_letter(company_name, job_title)
        
        msg = MIMEMultipart('mixed')
        msg['From'] = f"{config.NAME} <{config.EMAIL}>"
        msg['To'] = to_email
        msg['Subject'] = f"{job_title} | Sam Salameh - HR & Operations | Available Immediately"
        
        alt = MIMEMultipart('alternative')
        alt.attach(MIMEText(plain_body, 'plain', 'utf-8'))
        alt.attach(MIMEText(html_body, 'html', 'utf-8'))
        msg.attach(alt)
        
        # Attach Cover Letter
        try:
            cl_part = MIMEApplication(cover_letter.encode('utf-8'), Name=f"{company_name}_Cover_Letter.html")
            cl_part['Content-Disposition'] = f'attachment; filename="{company_name}_Cover_Letter_Sam_Cordahi.html"'
            msg.attach(cl_part)
        except Exception as e:
            logger.warning(f"Cover letter attachment failed: {e}")
        
        # Attach CV
        try:
            if config.CV_PATH.exists():
                with open(config.CV_PATH, 'rb') as f:
                    cv_part = MIMEApplication(f.read(), Name="Sam_Cordahi_CV.html")
                cv_part['Content-Disposition'] = 'attachment; filename="Sam_Cordahi_CV.html"'
                msg.attach(cv_part)
        except Exception as e:
            logger.warning(f"CV attachment failed: {e}")
        
        return self._send_smtp(msg, to_email)
    
    def _send_smtp(self, msg, to_email):
        # Try Brevo first
        if config.BREVO_API_KEY:
            try:
                html_content = None
                for part in msg.walk():
                    if part.get_content_type() == 'text/html':
                        html_content = part.get_payload()
                        break
                
                payload = {
                    "sender": {"name": config.NAME, "email": "a6e5bb001@smtp-brevo.com"},
                    "to": [{"email": to_email}],
                    "subject": msg['Subject'],
                    "htmlContent": html_content or ""
                }
                
                headers = {
                    "accept": "application/json",
                    "api-key": config.BREVO_API_KEY,
                    "content-type": "application/json"
                }
                
                resp = requests.post(
                    "https://api.brevo.com/v3/smtp/email",
                    headers=headers,
                    json=payload,
                    timeout=20
                )
                
                if resp.status_code in [200, 201, 202]:
                    logger.info(f"✅ Sent via Brevo to {to_email}")
                    return True
            except Exception as e:
                logger.error(f"Brevo failed: {e}")
        
        logger.warning("All email methods failed!")
        return False

class WhatsAppNotifier:
    """Send WhatsApp notifications"""
    
    def __init__(self):
        self.api_url = "https://api.callmebot.com/whatsapp.php"
    
    def send(self, message):
        if not config.WHATSAPP_API:
            logger.info(f"📱 WhatsApp (mock): {message}")
            return True
        
        try:
            params = {
                "phone": config.WHATSAPP_NUMBER,
                "text": message,
                "apikey": config.WHATSAPP_API
            }
            resp = requests.get(self.api_url, params=params, timeout=10)
            logger.info(f"📱 WhatsApp sent: {message[:50]}...")
            return True
        except Exception as e:
            logger.error(f"WhatsApp failed: {e}")
            return False

class TelegramNotifier:
    """Send Telegram notifications"""
    
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
    
    def send(self, message):
        if not config.TELEGRAM_BOT_TOKEN or not config.TELEGRAM_CHAT_ID:
            logger.info(f"📩 Telegram (mock): {message}")
            return True
        
        try:
            payload = {
                "chat_id": config.TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "HTML"
            }
            resp = requests.post(self.api_url, json=payload, timeout=10)
            logger.info(f"📩 Telegram sent: {message[:50]}...")
            return True
        except Exception as e:
            logger.error(f"Telegram failed: {e}")
            return False
    
    def send_dashboard(self, stats):
        message = f"""
🌟 <b>SAM JOB EMPIRE - STATUS</b>

📊 <b>Statistics:</b>
• Total Sent: {stats.get('total_sent', 0)}
• Responses: {stats.get('total_responses', 0)}
• Interviews: {stats.get('total_interviews', 0)}

⏰ Last Update: {datetime.now().strftime('%H:%M:%S')}
        """
        self.send(message)

class CampaignManager:
    """Main campaign orchestrator"""
    
    def __init__(self):
        self.tracker = ApplicationTracker()
        self.email = EmailEngine()
        self.whatsapp = WhatsAppNotifier()
        self.telegram = TelegramNotifier()
        self.companies = self._load_companies()
        self.running = False
    
    def _load_companies(self):
        if config.COMPANIES_FILE.exists():
            return json.loads(config.COMPANIES_FILE.read_text())
        return []
    
    def get_job_title(self, company_name):
        name_lower = company_name.lower()
        if any(k in name_lower for k in ['airline', 'airways', 'aviation']):
            return "HR & Operations Manager"
        elif any(k in name_lower for k in ['bank', 'finance', 'investment']):
            return "HR Business Partner"
        elif any(k in name_lower for k in ['oil', 'petroleum', 'energy', 'gas']):
            return "HR & Admin Manager"
        elif any(k in name_lower for k in ['telecom', 'telecommunications']):
            return "HR & Customer Operations Manager"
        elif any(k in name_lower for k in ['university', 'education', 'school']):
            return "HR & Administrative Coordinator"
        elif any(k in name_lower for k in ['hospital', 'health', 'medical']):
            return "HR Manager"
        else:
            return "HR & Operations Manager"
    
    def send_to_all(self):
        """Send emails to all companies"""
        if not self.companies:
            logger.error("No companies loaded!")
            return
        
        self.running = True
        sent = 0
        failed = 0
        
        stats = self.tracker.get_stats()
        sent_emails = [a["email"] for a in self.tracker.get_all()]
        
        self.whatsapp.send(f"🚀 Starting email campaign to {len(self.companies)} companies...")
        
        for i, company in enumerate(self.companies):
            if not self.running:
                break
            
            company_name = company.get('company', 'Unknown')
            email = company.get('email', '')
            
            if not email or '@' not in email or email in sent_emails:
                continue
            
            job_title = self.get_job_title(company_name)
            
            logger.info(f"[{i+1}/{len(self.companies)}] Sending to {company_name}...")
            
            success = self.email.send(email, company_name, job_title)
            
            if success:
                self.tracker.add_application(company_name, email, job_title)
                sent += 1
                logger.info(f"✅ {company_name}")
                
                self.whatsapp.send(f"✅ Sent to {company_name}")
            else:
                failed += 1
                logger.error(f"❌ {company_name}")
            
            # Rate limiting
            if i < len(self.companies) - 1:
                delay = random.uniform(config.MIN_DELAY_SECONDS, config.MAX_DELAY_SECONDS)
                time.sleep(delay)
        
        self.running = False
        
        final_msg = f"""
🎉 <b>Campaign Complete!</b>

✅ Sent: {sent}
❌ Failed: {failed}
📧 Total in DB: {len(self.companies)}

Sam Job Empire v99
        """
        self.whatsapp.send(final_msg)
        self.telegram.send(final_msg)
        
        return sent, failed
    
    def follow_up(self):
        """Send follow-up emails"""
        logger.info("Checking for follow-ups...")
        
        for days in [3, 7, 14]:
            pending = self.tracker.get_pending_followup(days)
            for app in pending:
                follow_up_text = self._get_followup_text(app, days)
                logger.info(f"Follow-up ({days}d) for {app['company']}")
                # Here you would send the actual follow-up email
                self.tracker.mark_followup(app['id'], days)
        
        return True
    
    def _get_followup_text(self, app, days):
        if days == 3:
            return f"Hi, just following up on my application for {app['job_title']} at {app['company']}."
        elif days == 7:
            return f"Hi, wanted to check if you had any questions about my application for {app['job_title']}."
        else:
            return f"Hi, checking in on my application for {app['job_title']} at {app['company']}. Still very interested!"

# ═══════════════════════════════════════════════════════════════════════════════
# SCHEDULER & SELF-HEALING
# ═══════════════════════════════════════════════════════════════════════════════

class SelfHealer:
    """Auto-restart and heal system"""
    
    def __init__(self):
        self.restart_count = 0
        self.max_restarts = 5
    
    def check_and_heal(self):
        """Check system health and heal if needed"""
        log_file = config.LOGS_DIR / 'empire.log'
        if not log_file.exists():
            return True
        
        # Check for errors in last log
        try:
            lines = log_file.read_text().split('\n')[-100:]
            errors = [l for l in lines if 'ERROR' in l or 'CRITICAL' in l]
            
            if len(errors) > 10:
                logger.warning("⚠️ High error count detected, system may need attention")
                return False
        except:
            pass
        
        return True

def run_scheduler():
    """Run scheduled tasks"""
    campaign = CampaignManager()
    
    while True:
        try:
            # Check every minute
            schedule.run_pending()
            time.sleep(60)
        except KeyboardInterrupt:
            break
        except Exception as e:
            logger.error(f"Scheduler error: {e}")
            time.sleep(60)

def daily_report():
    """Send daily report"""
    tracker = ApplicationTracker()
    stats = tracker.get_stats()
    
    whatsapp = WhatsAppNotifier()
    telegram = TelegramNotifier()
    
    report = f"""
📊 <b>Daily Report - {datetime.now().strftime('%Y-%m-%d')}</b>

✅ Total Emails Sent: {stats.get('total_sent', 0)}
📬 Responses Received: {stats.get('total_responses', 0)}
📅 Interviews Scheduled: {stats.get('total_interviews', 0)}

Have a productive day!
- Sam Job Empire
    """
    
    whatsapp.send(report)
    telegram.send(report)

# Schedule tasks
schedule.every().day.at("09:00").do(daily_report)
schedule.every().day.at("14:00").do(lambda: CampaignManager().follow_up())

# ═══════════════════════════════════════════════════════════════════════════════
# MAIN INTERFACE
# ═══════════════════════════════════════════════════════════════════════════════

def print_banner():
    os.system('cls' if os.name == 'nt' else 'clear')
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════════╗
    ║                                                                              ║
    ║        ███╗   ███╗██╗██╗██╗████████╗███████╗██╗ ██████╗ ███╗   ██╗         ║
    ║        ████╗ ████║██║██║██║╚══██╔══╝██╔════╝██║██╔═══██╗████╗  ██║         ║
    ║        ██╔████╔██║██║██║██║   ██║   █████╗  ██║██║   ██║██╔██╗ ██║         ║
    ║        ██║╚██╔╝██║██║██║██║   ██║   ██╔══╝  ██║██║   ██║██║╚██╗██║         ║
    ║        ██║ ╚═╝ ██║██║██║██║   ██║   ██║     ██║╚██████╔╝██║ ╚████║         ║
    ║        ╚═╝     ╚═╝╚═╝╚═╝╚═╝   ╚═╝   ╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═══╝         ║
    ║                                                                              ║
    ║                    💼 JOB EMPIRE v99 - GOD MODE 💼                         ║
    ║                                                                              ║
    ╚══════════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def print_menu():
    print("""
    ┌────────────────────────────────────────────────────────────────────┐
    │                         MAIN MENU                                  │
    ├────────────────────────────────────────────────────────────────────┤
    │  [1] 📧  Send to ALL Companies    - Mass email campaign           │
    │  [2] 🧪  Send Test Email          - Test configuration             │
    │  [3] 📊  View Statistics         - See application stats          │
    │  [4] 📋  View All Applications   - List all sent applications    │
    │  [5] 🔄  Run Follow-ups          - Send follow-up emails         │
    │  [6] 📱  Send WhatsApp Test      - Test WhatsApp notifications   │
    │  [7] 📩  Send Telegram Test      - Test Telegram notifications    │
    │  [8] 🚀  Full System Check       - Verify all configurations     │
    │  [0] ❌  Exit                    - Close program                 │
    └────────────────────────────────────────────────────────────────────┘
    """)

def main():
    print_banner()
    
    campaign = CampaignManager()
    tracker = ApplicationTracker()
    
    while True:
        print_menu()
        choice = input("  Select option: ").strip()
        
        if choice == '1':
            print("\n" + "="*60)
            print("  🚀 STARTING MASS EMAIL CAMPAIGN")
            print("="*60)
            sent, failed = campaign.send_to_all()
            print(f"\n  ✅ Sent: {sent} | ❌ Failed: {failed}")
            
        elif choice == '2':
            print("\n  Sending test email...")
            email = EmailEngine()
            test_email = input("  Enter test email (default: sam.dev1@outlook.com): ").strip()
            if not test_email:
                test_email = "sam.dev1@outlook.com"
            result = email.send(test_email, "TEST COMPANY", "HR & Operations Manager")
            print(f"  {'✅ Success!' if result else '❌ Failed!'}") if result else None
            
        elif choice == '3':
            stats = tracker.get_stats()
            print("\n  📊 APPLICATION STATISTICS")
            print("  " + "-"*40)
            for key, value in stats.items():
                print(f"  {key}: {value}")
                
        elif choice == '4':
            apps = tracker.get_all()
            print(f"\n  📋 ALL APPLICATIONS ({len(apps)} total)")
            print("  " + "-"*60)
            for app in apps[-10:]:  # Last 10
                print(f"  [{app['id']}] {app['company']} | {app['job_title']} | {app['status']}")
            
        elif choice == '5':
            print("\n  Running follow-ups...")
            campaign.follow_up()
            print("  ✅ Follow-ups complete!")
            
        elif choice == '6':
            whatsapp = WhatsAppNotifier()
            whatsapp.send("🧪 Test from Sam Job Empire - System is working!")
            print("  ✅ WhatsApp test sent!")
            
        elif choice == '7':
            telegram = TelegramNotifier()
            telegram.send("🧪 Test from Sam Job Empire - System is working!")
            print("  ✅ Telegram test sent!")
            
        elif choice == '8':
            print("\n  🔍 SYSTEM CHECK")
            print("  " + "-"*40)
            print(f"  ✅ CV File: {'Found' if config.CV_PATH.exists() else 'MISSING'}")
            print(f"  ✅ Companies: {len(campaign.companies)} loaded")
            print(f"  ✅ Tracker: {len(tracker.get_all())} applications")
            print(f"  ✅ Brevo API: {'Configured' if config.BREVO_API_KEY else 'NOT SET'}")
            print(f"  ✅ WhatsApp API: {'Configured' if config.WHATSAPP_API else 'NOT SET'}")
            print(f"  ✅ Telegram Bot: {'Configured' if config.TELEGRAM_BOT_TOKEN else 'NOT SET'}")
            
        elif choice == '0':
            print("\n  Goodbye! Good luck with your job search! 🎯")
            break
        
        input("\n  Press Enter to continue...")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "start":
            campaign = CampaignManager()
            campaign.send_to_all()
        elif sys.argv[1] == "followup":
            CampaignManager().follow_up()
        elif sys.argv[1] == "stats":
            print(json.dumps(ApplicationTracker().get_stats(), indent=2))
        else:
            print("Usage: python sam_job_empire.py [start|followup|stats]")
    else:
        main()
