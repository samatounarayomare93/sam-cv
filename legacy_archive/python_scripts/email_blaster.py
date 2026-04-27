"""
SAM EMAIL BLAST - MASS EMAIL TO MILLIONS
==========================================
"""

import os
import time
import random
import sqlite3
import smtplib
import requests
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from datetime import datetime
from bs4 import BeautifulSoup
import re

# SMTP Providers
SMTP_PROVIDERS = [
    {"name": "Brevo", "host": "smtp-relay.brevo.com", "port": 587, "user": "", "pass": ""},
    {"name": "Gmail", "host": "smtp.gmail.com", "port": 587, "user": "", "pass": ""},
    {"name": "Outlook", "host": "smtp-mail.outlook.com", "port": 587, "user": "", "pass": ""},
    {"name": "Yahoo", "host": "smtp.mail.yahoo.com", "port": 587, "user": "", "pass": ""},
    {"name": "Zoho", "host": "smtp.zoho.com", "port": 587, "user": "", "pass": ""},
    {"name": "Mailgun", "host": "smtp.mailgun.org", "port": 587, "user": "", "pass": ""},
    {"name": "SendGrid", "host": "smtp.sendgrid.net", "port": 587, "user": "", "pass": ""},
    {"name": "Amazon SES", "host": "email-smtp.us-east-1.amazonaws.com", "port": 587, "user": "", "pass": ""},
]

# Email patterns
EMAIL_PATTERNS = [
    "careers@{domain}", "jobs@{domain}", "hr@{domain}", "recruitment@{domain}",
    "hiring@{domain}", "talent@{domain}", "employment@{domain}", "info@{domain}",
    "contact@{domain}", "admin@{domain}", "apply@{domain}", "job@{domain}",
    "vacancies@{domain}", "openings@{domain}", "resumes@{domain}", "recruit@{domain}",
    "personnel@{domain}", "staffing@{domain}", "hello@{domain}", "team@{domain}",
]

class EmailBlaster:
    def __init__(self):
        self.db = sqlite3.connect("email_targets.db", check_same_thread=False)
        self.create_tables()
        self.current_provider = 0
    
    def create_tables(self):
        c = self.db.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE, company TEXT, status TEXT DEFAULT 'pending'
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS sent (
                id INTEGER PRIMARY KEY,
                email TEXT, sent_at TIMESTAMP
            )
        """)
        self.db.commit()
    
    def _get_provider(self):
        p = self.SMTP_PROVIDERS[self.current_provider]
        self.current_provider = (self.current_provider + 1) % len(self.SMTP_PROVIDERS)
        return p
    
    def scrape_yellowpages(self):
        """Scrape emails from YellowPages"""
        print("📍 Scraping YellowPages...")
        
        categories = ["hr-services", "employment-agencies", "staffing-agencies"]
        states = ["california", "new-york", "texas", "florida", "illinois"]
        
        for category in categories:
            for state in states:
                try:
                    url = f"https://www.yellowpages.com/{state}/{category}"
                    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        listings = soup.select('.result')[:30]
                        
                        for listing in listings:
                            try:
                                name_elem = listing.select_one('.business-name')
                                website_elem = listing.select_one('a.website-link')
                                
                                name = name_elem.get_text(strip=True) if name_elem else ""
                                
                                if website_elem and name:
                                    href = website_elem.get('href', '')
                                    if 'url=' in href:
                                        domain = href.split('url=')[1].split('&')[0]
                                        domain = domain.replace('https://', '').replace('http://', '').replace('www.', '')
                                        
                                        for pattern in EMAIL_PATTERNS[:10]:
                                            email = pattern.replace('{domain}', domain)
                                            c = self.db.cursor()
                                            c.execute("INSERT OR IGNORE INTO emails (email, company) VALUES (?, ?)", 
                                                     (email, name))
                                        self.db.commit()
                                        
                            except:
                                continue
                    
                    time.sleep(random.uniform(1, 2))
                    
                except Exception as e:
                    continue
        
        print("  ✅ YellowPages scrape complete")
    
    def generate_company_emails(self):
        """Generate emails for common company domains"""
        print("📧 Generating company emails...")
        
        # Common company domains
        companies = [
            ("Google", "google.com"), ("Microsoft", "microsoft.com"), ("Amazon", "amazon.com"),
            ("Facebook", "meta.com"), ("Apple", "apple.com"), ("Netflix", "netflix.com"),
            ("Adobe", "adobe.com"), ("IBM", "ibm.com"), ("Oracle", "oracle.com"),
            ("Salesforce", "salesforce.com"), ("SAP", "sap.com"), ("Intel", "intel.com"),
            ("Cisco", "cisco.com"), ("Dell", "dell.com"), ("HP", "hp.com"),
            ("VMware", "vmware.com"), ("Slack", "slack.com"), ("Zoom", "zoom.us"),
            ("Twitter", "twitter.com"), ("LinkedIn", "linkedin.com"), ("Uber", "uber.com"),
            ("Airbnb", "airbnb.com"), ("Lyft", "lyft.com"), ("Spotify", "spotify.com"),
            ("Dropbox", "dropbox.com"), ("Square", "squareup.com"), ("Stripe", "stripe.com"),
            ("Shopify", "shopify.com"), ("Walmart", "walmart.com"), ("Target", "target.com"),
        ]
        
        for name, domain in companies:
            for pattern in EMAIL_PATTERNS[:10]:
                email = pattern.replace('{domain}', domain)
                c = self.db.cursor()
                c.execute("INSERT OR IGNORE INTO emails (email, company) VALUES (?, ?)", (email, name))
        self.db.commit()
        
        print("  ✅ Generated emails for common companies")
    
    def send_blast(self, count=100):
        """Send mass email blast"""
        c = self.db.cursor()
        c.execute("SELECT id, email, company FROM emails WHERE status = 'pending' LIMIT ?", (count,))
        targets = c.fetchall()
        
        sent = 0
        for email_id, email, company in targets:
            provider = self._get_provider()
            
            if not provider.get('user') or not provider.get('pass'):
                continue
            
            try:
                msg = MIMEMultipart('mixed')
                msg['From'] = f'"Sam Salameh" <{provider["user"]}>'
                msg['To'] = email
                msg['Subject'] = f"Application: HR & Operations | Sam Salameh"
                
                html_body = self._create_body(company)
                plain = re.sub(r'<[^>]+>', ' ', html_body)
                plain = re.sub(r'\s+', ' ', plain)
                
                alt = MIMEMultipart('alternative')
                alt.attach(MIMEText(plain, 'plain', 'utf-8'))
                alt.attach(MIMEText(html_body, 'html', 'utf-8'))
                msg.attach(alt)
                
                # Attach CV
                if os.path.exists("Sam_Cordahi_CV.html"):
                    with open("Sam_Cordahi_CV.html", 'rb') as f:
                        cv = MIMEApplication(f.read(), _subtype='html')
                        cv['Content-Disposition'] = 'attachment; filename="Sam_Cordahi_CV.html"'
                        msg.attach(cv)
                
                server = smtplib.SMTP(provider['host'], provider['port'], timeout=30)
                server.starttls()
                server.login(provider['user'], provider['pass'])
                server.send_message(msg)
                server.quit()
                
                c.execute("UPDATE emails SET status = 'sent' WHERE id = ?", (email_id,))
                c.execute("INSERT INTO sent (email) VALUES (?)", (email,))
                self.db.commit()
                
                sent += 1
                print(f"  ✅ Sent to: {email}")
                
                time.sleep(random.uniform(1, 3))
                
            except Exception as e:
                print(f"  ❌ Failed: {email} - {e}")
                continue
        
        print(f"\n📤 Sent {sent} emails")
        return sent
    
    def _create_body(self, company):
        return f"""
<div style="background:#0b0f19;padding:40px;font-family:Arial;">
  <table width="650" style="margin:0 auto;background:#111827;border-radius:16px;">
    <tr>
      <td style="background:linear-gradient(135deg,#0f172a,#1e293b);padding:40px;text-align:center;">
        <div style="width:60px;height:60px;background:#06b6d4;border-radius:50%;line-height:60px;color:white;font-size:24px;font-weight:bold;margin:0 auto 15px;">RC</div>
        <div style="font-size:28px;font-weight:800;color:white;">SAM CORDAHI</div>
        <div style="font-size:12px;color:#94a3b8;letter-spacing:3px;">HR & OPERATIONS PROFESSIONAL</div>
      </td>
    </tr>
    <tr>
      <td style="height:4px;background:linear-gradient(90deg,#06b6d4,#3b82f6,#8b5cf6);"></td>
    </tr>
    <tr>
      <td style="padding:35px;">
        <p style="font-size:17px;color:#f8fafc;">Dear {company} Hiring Team,</p>
        <p style="font-size:15px;line-height:1.8;color:#cbd5e1;">I am reaching out to express my strong interest in HR and Operations positions.</p>
        <p style="font-size:15px;line-height:1.8;color:#cbd5e1;"><strong>Key Qualifications:</strong></p>
        <ul style="color:#cbd5e1;font-size:14px;line-height:1.8;">
          <li>5+ years HR & Operations experience</li>
          <li>100% compliance accuracy in employee records</li>
          <li>25% operational cost reduction achieved</li>
          <li>Available immediately for relocation worldwide</li>
        </ul>
        <p style="font-size:15px;color:#f8fafc;">Please find my CV attached.</p>
        <p style="font-size:15px;color:#f8fafc;">Best regards,<br><strong>Sam Salameh</strong><br>+961 76 005 412</p>
      </td>
    </tr>
    <tr>
      <td style="background:#0f172a;padding:25px;text-align:center;">
        <a href="https://www.linkedin.com/in/sam-cordahi/" style="display:inline-block;padding:12px 30px;background:#06b6d4;color:white;text-decoration:none;border-radius:25px;font-weight:bold;">VIEW LINKEDIN</a>
        <p style="color:#94a3b8;font-size:12px;margin-top:15px;">sam.dev1@outlook.com</p>
      </td>
    </tr>
  </table>
</div>
        """
    
    def run(self):
        print("\n" + "="*70)
        print("📧 EMAIL BLAST ENGINE - MASS MAILER")
        print("="*70 + "\n")
        
        # Phase 1: Scrape emails
        print("[1/3] Scraping email targets...")
        self.scrape_yellowpages()
        self.generate_company_emails()
        
        # Phase 2: Send blast
        print("\n[2/3] Sending email blast...")
        while True:
            c = self.db.cursor()
            c.execute("SELECT COUNT(*) FROM emails WHERE status = 'pending'")
            pending = c.fetchone()[0]
            
            if pending == 0:
                print("No more emails to send!")
                break
            
            print(f"\n{pending} emails remaining...")
            sent = self.send_blast(50)
            
            cont = input("Continue? (y/n): ").strip().lower()
            if cont != 'y':
                break
        
        # Phase 3: Report
        print("\n[3/3] Final report...")
        c = self.db.cursor()
        c.execute("SELECT COUNT(*) FROM sent")
        total = c.fetchone()[0]
        print(f"Total emails sent: {total}")
        
        self.db.close()
        print("\n[COMPLETE]")


if __name__ == "__main__":
    blaster = EmailBlaster()
    blaster.run()