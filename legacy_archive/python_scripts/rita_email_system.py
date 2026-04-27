"""
SAM EMAIL SYSTEM v2 - Professional Application Emails
======================================================
Sends personalized emails to companies with CV and Cover Letter attachments
Design matches exactly what you specified
"""

import os
import smtplib
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import config
import base64
import requests
import re
import time
import random

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Email design template - matches your specified design exactly
EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            margin: 0;
            padding: 0;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background-color: #0b0f19;
        }}
        .email-container {{
            max-width: 650px;
            margin: 0 auto;
            background-color: #111827;
            border-radius: 16px;
            overflow: hidden;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);
        }}
        .header {{
            background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
            padding: 45px 30px;
            text-align: center;
        }}
        .initials {{
            display: inline-block;
            width: 65px;
            height: 65px;
            background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%);
            border-radius: 50%;
            line-height: 65px;
            color: #ffffff;
            font-size: 26px;
            font-weight: 800;
            margin-bottom: 18px;
            box-shadow: 0 0 30px rgba(6, 182, 212, 0.5);
        }}
        .subtitle {{
            font-size: 12px;
            letter-spacing: 4px;
            color: #94a3b8;
            text-transform: uppercase;
            margin-bottom: 6px;
            font-weight: 500;
        }}
        .name {{
            font-size: 32px;
            font-weight: 800;
            color: #ffffff;
            letter-spacing: 1px;
            margin: 0;
        }}
        .title {{
            font-size: 13px;
            color: #06b6d4;
            margin-top: 8px;
            font-weight: 500;
        }}
        .gradient-bar {{
            height: 5px;
            background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);
        }}
        .content {{
            padding: 40px 35px;
            background-color: #ffffff;
        }}
        .greeting {{
            font-size: 18px;
            margin-top: 0;
            margin-bottom: 15px;
            color: #f8fafc;
        }}
        .message {{
            font-size: 15px;
            line-height: 1.8;
            color: #cbd5e1;
            margin-bottom: 20px;
        }}
        .highlight {{
            color: #06b6d4;
            font-weight: 700;
        }}
        .company-name {{
            color: #06b6d4;
            font-weight: 700;
        }}
        .section {{
            margin: 25px 0;
        }}
        .section-box {{
            padding: 22px;
            background-color: #1e293b;
            border-radius: 12px;
            border-left: 5px solid #06b6d4;
            margin-bottom: 12px;
        }}
        .section-title {{
            font-size: 13px;
            font-weight: 700;
            color: #06b6d4;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
        }}
        .section-content {{
            font-size: 14px;
            color: #94a3b8;
            line-height: 1.7;
            margin-top: 8px;
        }}
        .highlight-green {{
            color: #4ade80;
            font-weight: 600;
        }}
        .quote-box {{
            padding: 22px 28px;
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%);
            border: 1px solid rgba(6, 182, 212, 0.2);
            border-radius: 12px;
            text-align: center;
        }}
        .quote-text {{
            margin: 0;
            font-style: italic;
            color: #e2e8f0;
            font-size: 15px;
            line-height: 1.6;
        }}
        .available-badge {{
            display: inline-block;
            padding: 10px 20px;
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 25px;
            color: #4ade80;
            font-size: 13px;
            font-weight: 600;
            margin: 20px 0 25px 0;
        }}
        .footer {{
            background-color: #0f172a;
            padding: 35px 30px;
            text-align: center;
            border-top: 1px solid #1e293b;
        }}
        .cta-button {{
            display: inline-block;
            padding: 14px 35px;
            background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%);
            color: #ffffff;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 700;
            font-size: 13px;
            letter-spacing: 1.5px;
            box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);
            margin-bottom: 28px;
        }}
        .contact-info {{
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid #1e293b;
        }}
        .contact-link {{
            color: #94a3b8;
            font-size: 14px;
            text-decoration: none;
            margin: 0 12px;
        }}
        .contact-link:hover {{
            color: #06b6d4;
        }}
        .divider {{
            color: #334155;
            margin: 0 5px;
        }}
        .role-title {{
            color: #06b6d4;
            font-weight: 700;
        }}
        .attachment-note {{
            background: rgba(16, 185, 129, 0.15);
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 8px;
            padding: 12px 16px;
            margin: 20px 0;
            color: #4ade80;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <!-- HEADER -->
        <div class="header">
            <div class="initials">RC</div>
            <div class="subtitle">EXECUTIVE CANDIDACY</div>
            <h1 class="name">SAM CORDAHI</h1>
            <div class="title">HR & Customer Operations Specialist</div>
        </div>
        
        <!-- GRADIENT BAR -->
        <div class="gradient-bar"></div>
        
        <!-- CONTENT -->
        <div class="content">
            <p class="greeting">Dear <strong>Hiring Team at {company_name}</strong>,</p>
            
            <p class="message">
                I am formally reaching out to express my high-level interest in the <span class="highlight">{job_title}</span> position at <span class="company-name">{company_name}</span>. With a robust track record in HR administration and customer operations, I specialize in architecting workflows that prioritize precision, compliance, and exceptional service delivery.
            </p>
            
            <p class="message">
                My methodology is built specifically for organizations that focus heavily on <strong style="color: #e2e8f0;">automation, KPIs, and scaling corporate culture</strong>. Here are the precise competencies I bring to the table:
            </p>
            
            <!-- SKILLS SECTION -->
            <div class="section">
                <div class="section-box" style="border-left-color: #06b6d4;">
                    <div class="section-title">01. Operations Lifecycle</div>
                    <div class="section-content">
                        Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with <span class="highlight-green">100% data integrity</span>.
                    </div>
                </div>
                
                <div class="section-box" style="border-left-color: #3b82f6;">
                    <div class="section-title">02. Service & Retention</div>
                    <div class="section-content">
                        A track record of resolving <strong style="color: #e2e8f0;">50+ daily complex technical and billing inquiries</strong> while maintaining strict SLA compliance.
                    </div>
                </div>
                
                <div class="section-box" style="border-left-color: #8b5cf6;">
                    <div class="section-title">03. Workflow Optimization</div>
                    <div class="section-content">
                        Experience in standardizing onboarding templates and operational diagnostics to significantly <strong style="color: #e2e8f0;">reduce departmental overhead by 25%</strong>.
                    </div>
                </div>
            </div>
            
            <!-- QUOTE BOX -->
            <div class="quote-box">
                <p class="quote-text">
                    "I am looking to bring rigorous accountability, structured scaling, and high-conversion problem-solving to the <strong style="color: #06b6d4;">{company_name}</strong> team."
                </p>
            </div>
            
            <!-- AVAILABLE BADGE -->
            <div style="text-align: center;">
                <span class="available-badge">✓ Available Immediately for Relocation</span>
            </div>
            
            <!-- ATTACHMENT NOTE -->
            <div class="attachment-note">
                📎 Please find my CV and Cover Letter attached for your comprehensive review.
            </div>
            
            <p class="message" style="margin-bottom: 0;">
                I am available for immediate discussion and can start at your earliest convenience. Thank you for considering my application.
            </p>
        </div>
        
        <!-- FOOTER -->
        <div class="footer">
            <a href="https://www.linkedin.com/in/sam-cordahi/" class="cta-button">VIEW LINKEDIN PROFILE</a>
            
            <div class="contact-info">
                <div style="margin-bottom: 10px;">
                    <a href="mailto:sam.dev1@outlook.com" class="contact-link">sam.dev1@outlook.com</a>
                    <span class="divider">|</span>
                    <a href="tel:+96176005412" class="contact-link">+961 76 005 412</a>
                </div>
                <div style="font-size: 11px; color: #475569; letter-spacing: 1px; text-transform: uppercase;">
                    HR & Customer Operations Specialist
                </div>
            </div>
        </div>
    </div>
</body>
</html>
"""

# Plain text version
EMAIL_PLAIN_TEXT = """
SAM CORDAHI
HR & Customer Operations Specialist

Dear Hiring Team at {company_name},

I am formally reaching out to express my high-level interest in the {job_title} position at {company_name}. With a robust track record in HR administration and customer operations, I specialize in architecting workflows that prioritize precision, compliance, and exceptional service delivery.

My key competencies include:
• Operations Lifecycle: Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with 100% data integrity.
• Service & Retention: A track record of resolving 50+ daily complex inquiries while maintaining strict SLA compliance.
• Workflow Optimization: Experience in standardizing onboarding templates and operational diagnostics to significantly reduce departmental overhead by 25%.

Please find my CV and Cover Letter attached for your comprehensive review.

I am available for immediate discussion and can start at your earliest convenience.

Best regards,
Sam Salameh

Contact:
Email: sam.dev1@outlook.com
Phone: +961 76 005 412
LinkedIn: linkedin.com/in/sam-cordahi
"""

def load_companies():
    """Load company list from company_emails.json"""
    try:
        with open("company_emails.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load companies: {e}")
        return []

def load_cv():
    """Load CV file"""
    cv_path = "Sam_Cordahi_CV.html"
    if os.path.exists(cv_path):
        with open(cv_path, "r", encoding="utf-8") as f:
            return f.read(), cv_path
    return None, None

def create_cover_letter(company_name, job_title):
    """Create personalized cover letter for company"""
    return f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: 'Segoe UI', Arial, sans-serif;
            max-width: 800px;
            margin: 0 auto;
            padding: 40px;
            background: #f8f9fa;
        }}
        .letter {{
            background: white;
            padding: 40px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #06b6d4;
        }}
        .header h1 {{
            margin: 0;
            color: #1e293b;
            font-size: 28px;
        }}
        .header p {{
            margin: 5px 0 0 0;
            color: #06b6d4;
            font-size: 14px;
        }}
        .date {{
            color: #666;
            margin-bottom: 20px;
        }}
        .recipient {{
            margin-bottom: 20px;
        }}
        .subject {{
            font-weight: bold;
            margin-bottom: 20px;
            color: #1e293b;
        }}
        .body {{
            line-height: 1.8;
            color: #333;
        }}
        .body p {{
            margin-bottom: 15px;
        }}
        .signature {{
            margin-top: 30px;
        }}
        .signature p {{
            margin-bottom: 5px;
        }}
        .contact-info {{
            margin-top: 20px;
            color: #666;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="letter">
        <div class="header">
            <h1>Sam Salameh</h1>
            <p>HR & Customer Operations Specialist</p>
            <p>+961 76 005 412 | sam.dev1@outlook.com</p>
        </div>
        
        <div class="date">{time.strftime("%B %d, %Y")}</div>
        
        <div class="recipient">
            <p>Dear Hiring Team at <strong>{company_name}</strong>,</p>
        </div>
        
        <div class="subject">Application for {job_title}</div>
        
        <div class="body">
            <p>I am writing to express my strong interest in the {job_title} position at {company_name}. With over 5 years of experience in Human Resources and Customer Operations, I am confident that my skills and background align well with your requirements.</p>
            
            <p>In my current role as HR & Operations Coordinator, I have developed expertise in:</p>
            <ul>
                <li>Full-cycle recruitment and talent acquisition</li>
                <li>Employee onboarding and documentation</li>
                <li>Payroll administration with 100% compliance accuracy</li>
                <li>Customer service excellence with high first-contact resolution rates</li>
                <li>Process optimization resulting in 25% cost reduction</li>
            </ul>
            
            <p>I am particularly drawn to {company_name} because of your reputation for excellence in the region. I am confident that my proactive approach and dedication to operational excellence would make me a valuable addition to your team.</p>
            
            <p>I am available for immediate relocation and prepared to contribute meaningfully from day one. Please find my CV attached for your review. I look forward to discussing how I can add value to your organization.</p>
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

def send_professional_email(to_email, company_name, job_title, pdf_cv_path=None):
    """Send professional application email with CV and Cover Letter attachments"""
    
    # Render templates
    html_body = EMAIL_TEMPLATE.format(
        company_name=company_name,
        job_title=job_title
    )
    
    plain_body = EMAIL_PLAIN_TEXT.format(
        company_name=company_name,
        job_title=job_title
    )
    
    cover_letter_html = create_cover_letter(company_name, job_title)
    
    # Create message
    msg = MIMEMultipart('mixed')
    msg['From'] = "Sam Salameh <sam.dev1@outlook.com>"
    msg['To'] = to_email
    msg['Subject'] = f"{job_title} | Sam Salameh - HR & Operations | Available Immediately"
    msg['Reply-To'] = "Sam Salameh <sam.dev1@outlook.com>"
    
    # Add email headers for deliverability
    import email.utils
    msg['Message-ID'] = email.utils.make_msgid(domain='outlook.com')
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['X-Mailer'] = 'SamJobAutomator-v2'
    
    # Create multipart message
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(plain_body, 'plain', 'utf-8'))
    alt.attach(MIMEText(html_body, 'html', 'utf-8'))
    msg.attach(alt)
    
    # Attach Cover Letter (HTML)
    try:
        cover_part = MIMEApplication(cover_letter_html.encode('utf-8'), Name=f"{company_name}_Cover_Letter_Sam_Cordahi.html")
        cover_part['Content-Disposition'] = f'attachment; filename="{company_name}_Cover_Letter_Sam_Cordahi.html"'
        msg.attach(cover_part)
        logger.info(f"Attached cover letter for {company_name}")
    except Exception as e:
        logger.warning(f"Could not attach cover letter: {e}")
    
    # Attach CV (HTML)
    try:
        if os.path.exists("Sam_Cordahi_CV.html"):
            with open("Sam_Cordahi_CV.html", "rb") as f:
                cv_part = MIMEApplication(f.read(), Name="Sam_Cordahi_CV.html")
            cv_part['Content-Disposition'] = 'attachment; filename="Sam_Cordahi_CV.html"'
            msg.attach(cv_part)
            logger.info(f"Attached CV for {company_name}")
    except Exception as e:
        logger.warning(f"Could not attach CV: {e}")
    
    # Attach PDF CV if exists
    if pdf_cv_path and os.path.exists(pdf_cv_path):
        try:
            with open(pdf_cv_path, "rb") as f:
                pdf_part = MIMEApplication(f.read(), Name=f"{company_name}_Sam_Cordahi.pdf")
            pdf_part['Content-Disposition'] = f'attachment; filename="{company_name}_Sam_Cordahi.pdf"'
            msg.attach(pdf_part)
            logger.info(f"Attached PDF for {company_name}")
        except Exception as e:
            logger.warning(f"Could not attach PDF: {e}")
    
    # Send email
    return send_via_smtp(msg, to_email)

def send_via_smtp(msg, to_email):
    """Send email via SMTP with fallbacks"""
    
    # Try Gmail first if configured
    gmail_user = getattr(config, 'GMAIL_SMTP_USER', '') or ''
    gmail_pass = getattr(config, 'GMAIL_APP_PASSWORD', '') or ''
    
    if gmail_user and gmail_pass:
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587, timeout=15)
            server.starttls()
            server.login(gmail_user, gmail_pass)
            server.send_message(msg)
            server.quit()
            logger.info(f"✅ Email sent via Gmail to {to_email}")
            return True
        except Exception as e:
            logger.warning(f"Gmail failed: {e}")
    
    # Try Outlook
    try:
        server = smtplib.SMTP('smtp-mail.outlook.com', 587, timeout=15)
        server.starttls()
        server.login('sam.dev1@outlook.com', getattr(config, 'OUTLOOK_PASSWORD', '') or '')
        server.send_message(msg)
        server.quit()
        logger.info(f"✅ Email sent via Outlook to {to_email}")
        return True
    except Exception as e:
        logger.warning(f"Outlook failed: {e}")
    
    # Try Brevo HTTP
    return send_via_brevo_http(msg, to_email)

def send_via_brevo_http(msg, to_email):
    """Fallback to Brevo HTTP API"""
    brevo_key = getattr(config, 'BREVO_API_KEY', '') or ''
    if not brevo_key:
        brevo_key = getattr(config, 'BREVO_SMTP_PASSWORD', '') or ''
    
    if not brevo_key:
        logger.error("No Brevo API key available")
        return False
    
    try:
        # Extract content from msg
        html_content = None
        for part in msg.walk():
            if part.get_content_type() == 'text/html':
                html_content = part.get_payload()
                break
        
        payload = {
            "sender": {
                "name": "Sam Salameh",
                "email": "a6e5bb001@smtp-brevo.com"
            },
            "to": [{"email": to_email}],
            "subject": msg['Subject'],
            "htmlContent": html_content or EMAIL_TEMPLATE.format(company_name="Company", job_title="Position")
        }
        
        headers = {
            "accept": "application/json",
            "api-key": brevo_key,
            "content-type": "application/json"
        }
        
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers=headers,
            json=payload,
            timeout=20
        )
        
        if response.status_code in [200, 201, 202]:
            logger.info(f"✅ Email sent via Brevo HTTP to {to_email}")
            return True
        
        logger.error(f"Brevo HTTP failed: {response.status_code} - {response.text}")
        return False
        
    except Exception as e:
        logger.error(f"Brevo HTTP error: {e}")
        return False

def send_to_all_companies():
    """Send application emails to all companies in the database"""
    companies = load_companies()
    
    if not companies:
        logger.error("No companies found in company_emails.json")
        return
    
    logger.info(f"📧 Starting email campaign to {len(companies)} companies...")
    
    success_count = 0
    fail_count = 0
    
    for i, company in enumerate(companies):
        company_name = company.get('company', 'Unknown')
        email = company.get('email', '')
        
        if not email or '@' not in email:
            logger.warning(f"Skipping {company_name} - no valid email")
            continue
        
        # Determine job title based on company type
        job_title = determine_job_title(company_name)
        
        logger.info(f"[{i+1}/{len(companies)}] Sending to {company_name}...")
        
        # Add delay between emails
        if i > 0:
            delay = random.uniform(2, 5)
            time.sleep(delay)
        
        # Send email
        success = send_professional_email(email, company_name, job_title)
        
        if success:
            success_count += 1
            logger.info(f"✅ SUCCESS: {company_name}")
        else:
            fail_count += 1
            logger.error(f"❌ FAILED: {company_name}")
    
    logger.info(f"\n{'='*50}")
    logger.info(f"EMAIL CAMPAIGN COMPLETE")
    logger.info(f"✅ Success: {success_count}")
    logger.info(f"❌ Failed: {fail_count}")
    logger.info(f"{'='*50}")

def determine_job_title(company_name):
    """Determine the best job title based on company"""
    name_lower = company_name.lower()
    
    if any(k in name_lower for k in ['airline', 'airways', 'aviation']):
        return "HR & Operations Manager"
    elif any(k in name_lower for k in ['bank', 'finance', 'investment']):
        return "HR Business Partner"
    elif any(k in name_lower for k in ['oil', 'petroleum', 'energy', 'gas']):
        return "HR & Admin Manager"
    elif any(k in name_lower for k in ['telecom', 'telecommunications', 'stc', 'ooredoo', 'mobily']):
        return "HR & Customer Operations Manager"
    elif any(k in name_lower for k in ['university', 'education', 'school']):
        return "HR & Administrative Coordinator"
    elif any(k in name_lower for k in ['hospital', 'health', 'medical']):
        return "HR Manager"
    elif any(k in name_lower for k in ['airport', 'holding', 'investment']):
        return "Operations Manager"
    else:
        return "HR & Operations Manager"

def send_test_email():
    """Send a test email to verify configuration"""
    test_email = getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com')
    logger.info(f"📧 Sending test email to {test_email}...")
    
    success = send_professional_email(
        test_email,
        "TEST COMPANY",
        "HR & Operations Manager"
    )
    
    if success:
        logger.info("✅ Test email sent successfully!")
    else:
        logger.error("❌ Test email failed!")
    
    return success

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            send_test_email()
        elif sys.argv[1] == "all":
            send_to_all_companies()
        else:
            # Send to specific company
            company = sys.argv[1]
            email = sys.argv[2] if len(sys.argv) > 2 else f"careers@{company.lower().replace(' ','')}.com"
            job_title = sys.argv[3] if len(sys.argv) > 3 else "HR & Operations Manager"
            send_professional_email(email, company, job_title)
    else:
        print("""
SAM EMAIL SYSTEM v2
====================
Usage:
    python sam_email_system.py test     - Send test email
    python sam_email_system.py all      - Send to all companies
    python sam_email_system.py "Company Name" "email@company.com" "Job Title"
        """)
