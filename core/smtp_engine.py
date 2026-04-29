import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formatdate
import logging
import time
import random
from core import config
import os
import base64
import requests
import re
import threading
from datetime import datetime
try:
    from core.gmail_auth import get_gmail_service
except ImportError:
    get_gmail_service = None


class _SafeFormatDict(dict):
    def __missing__(self, key):
        return "{" + key + "}"

# MAXIMUM POWER: Pre-built connection pool for SMTP
_SMTP_POOL = {}
_POOL_LOCK = threading.Lock()

def _get_smtp_connection(provider):
    """MAXIMUM POWER: Reuse SMTP connections from pool. Supports both TLS and SSL."""
    key = f"{provider['name']}_{provider['server']}"
    use_ssl = provider.get('use_ssl', False)
    with _POOL_LOCK:
        if key in _SMTP_POOL:
            conn, last_used = _SMTP_POOL[key]
            # Verify if connection is still alive (roughly)
            if time.time() - last_used > 60:
                try: conn.quit()
                except: pass
                del _SMTP_POOL[key]
            else:
                return conn
        try:
            smtp_timeout = int(getattr(config, 'SMTP_CONNECT_TIMEOUT_SECONDS', 10) or 10)
            if use_ssl:
                server = smtplib.SMTP_SSL(provider['server'], provider['port'], timeout=smtp_timeout)
            else:
                server = smtplib.SMTP(provider['server'], provider['port'], timeout=smtp_timeout)
                server.ehlo()
                server.starttls()
                server.ehlo()
            server.login(provider['email'], provider['password'])
            _SMTP_POOL[key] = (server, time.time())
            return server
        except Exception as e:
            logging.error(f"Failed to create SMTP connection: {e}")
            return None

def _render_template(template, company_name, job_title):
    try:
        return template.format_map(_SafeFormatDict(company_name=company_name, job_title=job_title))
    except Exception as exc:
        logging.warning(f"Template render fallback used: {exc}")
        return template

def _validate_email(email):
    if not email or "@" not in email: return False
    parts = email.split("@")
    return len(parts) == 2 and "." in parts[1]

def _get_available_providers():
    providers = []
    brevo_user = (getattr(config, 'BREVO_SMTP_LOGIN', '') or '').strip()
    brevo_pass = (getattr(config, 'BREVO_SMTP_PASSWORD', '') or '').strip()
    if brevo_user and brevo_pass:
        providers.append({'name': 'Brevo (2525)', 'server': 'smtp-relay.brevo.com', 'port': 2525, 'email': brevo_user, 'password': brevo_pass, 'use_ssl': False})
        providers.append({'name': 'Brevo (587)', 'server': 'smtp-relay.brevo.com', 'port': 587, 'email': brevo_user, 'password': brevo_pass, 'use_ssl': False})
    
    gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()
    gmail_pass = (getattr(config, 'GMAIL_APP_PASSWORD', '') or '').strip()
    if gmail_user and gmail_pass:
        providers.append({'name': 'Gmail (465)', 'server': 'smtp.gmail.com', 'port': 465, 'email': gmail_user, 'password': gmail_pass, 'use_ssl': True})
    
    outlook_user = (getattr(config, 'OUTLOOK_USER', '') or '').strip()
    outlook_pass = (getattr(config, 'OUTLOOK_PASSWORD', '') or '').strip()
    if outlook_user and outlook_pass:
        providers.append({'name': 'Outlook', 'server': 'smtp-mail.outlook.com', 'port': 587, 'email': outlook_user, 'password': outlook_pass, 'use_ssl': False})
    
    return providers

def send_test_email(recipient_email=None, attachment_paths=None, highlights=None):
    """[👑 OMEGA] Sends a premium visual verification strike to verify the dual PDF package."""
    recipient_email = recipient_email or getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com')
    
    # [👑 VIP REALISM]: Matching the CEO's requested industry example
    company_name = 'Future Tech Industries'
    job_title = 'Lead Automation Engineer'
    
    # Define actual highly-professional dummy body instead of a test string
    body = (
        "I am formally reaching out to express my high-level interest in the Lead Automation Engineer position.\n\n"
        "My methodology is built specifically for organizations that focus heavily on automation, "
        "KPIs, and scaling corporate culture."
    )
    
    # [👑 VIP FIX] Ensure highlights are passed so they render in the email (Screenshot 3 Parity)
    dynamic_highlights = highlights or [
        {"title": "OPERATIONS LIFECYCLE", "desc": "Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with 100% data integrity."},
        {"title": "SERVICE & RETENTION", "desc": "A track record of resolving 50+ daily complex technical and billing inquiries while maintaining strict SLA compliance."},
        {"title": "WORKFLOW OPTIMIZATION", "desc": "Experience in standardizing onboarding templates and operational diagnostics to significantly reduce departmental overhead."}
    ]
    
    # Send test using exact structural parity with the lead's instruction
    if not attachment_paths:
        from core.pdf_generator import generate_dynamic_cover_letter
        dummy_lead = {
            'company_name': company_name,
            'job_title': job_title,
            'custom_body': body,
            'highlights': dynamic_highlights
        }
        
        # 👑 [VIP EXACT ATTACHMENTS]: Use HTML CV + dynamic PDF Cover Letter
        cv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sam_Salameh_CV.html'))
        cl_path = generate_dynamic_cover_letter(company_name, job_title, dummy_lead.get('custom_body', ''), strike_id=8551)
        attachment_paths = [cv_path, cl_path]
        
    return send_email(recipient_email, company_name, job_title, body, 'test', 'test', attachment_paths, highlights=dynamic_highlights)



def send_strike(lead, attachment_paths=None, sender_name="Sam Salameh"):
    """MAXIMUM POWER: Core strike coordinator for Project Chronos with Triple Attachment support."""
    company = lead.get('company_name', 'Unknown Company')
    email = lead.get('email')
    title = lead.get('job_title', 'Professional Role')
    highlights = lead.get('highlights', [])

    if not _validate_email(email):
        logging.warning(f"SKIPPING STRIKE: No valid email for {company}.")
        return False

    # Ensure attachment_paths is a proper list to prevent silent string iteration bugs
    if isinstance(attachment_paths, str):
        attachments = [attachment_paths]
    else:
        attachments = attachment_paths or []
        
    # [👑 VIP EXACT ATTACHMENTS]: Always ensure the master HTML CV is included in real strikes
    cv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sam_Salameh_CV.html'))
    if cv_path not in attachments and os.path.exists(cv_path):
        attachments.insert(0, cv_path)
        
    valid_attachments = [p for p in attachments if p and os.path.exists(p) and os.path.isfile(p)]

    return send_email(email, company, title, lead.get('custom_body', ''), "omni", lead.get('mission_type', 'global'), valid_attachments, sender_name=sender_name, highlights=highlights)

def send_email(to_email, company_name, job_title, custom_body, platform, mission_type, attachment_paths=None, retry_count=0, sender_name="Sam Salameh", highlights=None, reply_to=None):
    """High-reliability delivery engine. Priority: Zoho SMTP > Outlook SMTP > Brevo HTTP > Gmail API."""
    
    # [👑 VIP RECOVERY]: Robust fallback for reply-to
    if not reply_to:
        reply_to = os.getenv("REPLY_TO_EMAIL", "sam.dev1@outlook.com")

    if getattr(config, 'TEST_MODE', False) and to_email != getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com'):
        to_email = getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com')
    
    # [👑 CENTRALIZED METADATA]: Generate Strike-ID once for the entire chain
    strike_id = random.randint(1000, 9999)
    subject = f"Application: {job_title} - {company_name} [STRIKE-{strike_id}]"

    # ============================================================
    # 🚀 RENDER OPTIMIZATION: Prioritize Port 2525
    # Render blocks 587/465 but allows 2525.
    # ============================================================
    is_render = os.getenv("RENDER") is not None
    if is_render:
        brevo_smtp_user = (getattr(config, 'BREVO_SMTP_LOGIN', '') or '').strip()
        brevo_smtp_pass = (getattr(config, 'BREVO_SMTP_PASSWORD', '') or '').strip()
        if brevo_smtp_user and brevo_smtp_pass:
            brevo_smtp_provider = {
                'name': 'Brevo SMTP (2525)',
                'server': 'smtp-relay.brevo.com',
                'port': 2525,
                'email': brevo_smtp_user,
                'password': brevo_smtp_pass,
                'use_ssl': False
            }
            try:
                logging.info("📧 [RENDER-BOOST] Prioritizing Brevo Port 2525...")
                res = _send_via_provider(to_email, company_name, job_title, custom_body, brevo_smtp_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
                if res:
                    logging.info("✅ RENDER-BOOST SUCCESS — Port 2525 bypassed Render block!")
                    return True
            except Exception as e:
                logging.warning(f"⚠️ Render-Boost failed: {e}")

    # ============================================================
    # 🥈 PRIORITY 2: BREVO SMTP PORT 2525
    # ============================================================
    brevo_smtp_user = (getattr(config, 'BREVO_SMTP_LOGIN', '') or '').strip()
    brevo_smtp_pass = (getattr(config, 'BREVO_SMTP_PASSWORD', '') or '').strip()
    if brevo_smtp_user and brevo_smtp_pass:
        brevo_smtp_provider = {
            'name': 'Brevo SMTP (2525)',
            'server': 'smtp-relay.brevo.com',
            'port': 2525,
            'email': brevo_smtp_user,
            'password': brevo_smtp_pass,
            'use_ssl': False
        }
        try:
            logging.info("📧 [BREVO-SMTP] Attempting Brevo SMTP port 2525...")
            res = _send_via_provider(to_email, company_name, job_title, custom_body, brevo_smtp_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
            if res:
                logging.info("✅ BREVO SMTP-2525 SUCCESS")
                return True
        except Exception as e:
            logging.warning(f"⚠️ Brevo SMTP-2525 failed: {e}")

    # ============================================================
    # 🥉 PRIORITY 3: YAHOO SMTP
    # ============================================================
    yahoo_user = (getattr(config, 'YAHOO_SMTP_USER', '') or '').strip()
    yahoo_pass = (getattr(config, 'YAHOO_APP_PASSWORD', '') or '').strip()
    if yahoo_user and yahoo_pass:
        yahoo_provider = {
            'name': 'Yahoo (STARTTLS-587)',
            'server': 'smtp.mail.yahoo.com',
            'port': 587,
            'email': yahoo_user,
            'password': yahoo_pass,
            'use_ssl': False
        }
        try:
            res = _send_via_provider(to_email, company_name, job_title, custom_body, yahoo_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
            if res:
                return True
        except Exception as e:
            logging.warning(f"⚠️ Yahoo SMTP failed: {e}")

    # ============================================================
    # 🔰 PRIORITY 4: BREVO REST API
    # ============================================================
    if getattr(config, 'BREVO_API_KEY', None):
        try:
            if send_email_via_brevo_http(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to):
                return True
        except Exception as e:
            logging.warning(f"⚠️ Brevo HTTP failed: {e}")

    # ============================================================
    # 🆘 LAST RESORT: GMAIL API (OAuth)
    # ============================================================
    if get_gmail_service:
        try:
            service = get_gmail_service()
            if service and send_email_via_gmail_api(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, service=service, reply_to=reply_to):
                return True
        except Exception as e:
            logging.warning(f"⚠️ Gmail API failed: {e}")
            
    logging.error("❌ ALL STRIKE PATHS FAILED: Payload could not be delivered.")
    return False

def send_email_via_gmail_api(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, service=None, reply_to=None):
    """[GMAIL API] Bypasses all ISP SMTP blocks by using official Google HTTP API."""
    if not get_gmail_service and not service:
        logging.error("Gmail API libraries not found.")
        return False

    try:
        if not service:
            service = get_gmail_service()
        if not service: return False
        
        if not subject:
            strike_id = random.randint(1000, 9999)
            subject = f"Application: {job_title} - {company_name} [STRIKE-{strike_id}]"
        
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        sender_email_from = (getattr(config, 'SENDER_EMAIL', '') or getattr(config, 'GMAIL_SMTP_USER', '') or '').strip() or 'sam.dev1@hotmail.com'
        msg['From'] = f"{sender_name} <{sender_email_from}>"
        msg['To'] = to_email
        if reply_to:
            msg['Reply-To'] = f"{sender_name} <{reply_to}>"
        
        html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
        alt = MIMEMultipart('alternative')
        alt.attach(MIMEText(html_content, 'html'))
        msg.attach(alt)

        if attachment_paths:
            for path in attachment_paths:
                if path and os.path.exists(path):
                    with open(path, "rb") as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
                        msg.attach(part)

        raw_message = base64.urlsafe_b64encode(msg.as_bytes()).decode('utf-8')
        send_request = service.users().messages().send(userId='me', body={'raw': raw_message})
        send_request.execute()
        return True
        
    except Exception as e:
        logging.error(f"FATAL GMAIL API ERROR: {e}")
        return False

def send_email_via_brevo_http(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None):
    """[REST API] Bypasses ISP SMTP blocks."""
    api_key = getattr(config, 'BREVO_API_KEY', None)
    if not api_key: return False
    
    brevo_smtp_login = (getattr(config, 'BREVO_SMTP_LOGIN', '') or '').strip()
    real_user_email = (getattr(config, 'SENDER_EMAIL', '') or '').strip() or 'sam.dev1@hotmail.com'
    sender_email = brevo_smtp_login if brevo_smtp_login else real_user_email
    
    if not subject:
        strike_id = random.randint(1000, 9999)
        subject = f"Application: {job_title} - {company_name} [STRIKE-{strike_id}]"
        
    html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
    
    attachment_list = []
    if attachment_paths:
        for path in attachment_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        content = base64.b64encode(f.read()).decode("utf-8")
                        attachment_list.append({"content": content, "name": os.path.basename(path)})
                except Exception as e:
                    logging.error(f"Failed to encode attachment {path}: {e}")
    
    payload = {
        "sender": {"name": sender_name, "email": sender_email},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
        "replyTo": {"email": reply_to if reply_to else real_user_email, "name": sender_name}
    }
    if attachment_list:
        payload["attachment"] = attachment_list
    
    try:
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": api_key, "Content-Type": "application/json", "Accept": "application/json"},
            json=payload,
            timeout=20
        )
        return response.status_code in (201, 200, 202)
    except:
        return False

def _send_via_provider(to_email, company_name, job_title, custom_body, provider, attachment_paths, sender_name, highlights, subject=None, reply_to=None):
    """[👑 SMTP IGNITION] Final structural delivery."""
    try:
        if not subject:
            strike_id = random.randint(1000, 9999)
            subject = f"Application: {job_title} - {company_name} [STRIKE-{strike_id}]"
            
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        
        # [👑 SENDER-IDENTITY FIX]: Use the validated SENDER_EMAIL for the From header, not the SMTP login ID.
        real_sender = (getattr(config, 'SENDER_EMAIL', '') or provider['email']).strip()
        msg['From'] = f"{sender_name} <{real_sender}>"
        msg['To'] = to_email
        if reply_to:
            msg['Reply-To'] = f"{sender_name} <{reply_to}>"
        msg['MIME-Version'] = '1.0'
        msg['Date'] = formatdate(localtime=True)
        
        # Body
        alt_part = MIMEMultipart('alternative')
        final_html = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
        plain_text = re.sub(r'<[^>]+>', '', final_html)
        alt_part.attach(MIMEText(plain_text, 'plain'))
        alt_part.attach(MIMEText(final_html, 'html'))
        msg.attach(alt_part)
        
        # Attachments
        if attachment_paths:
            for path in attachment_paths:
                if os.path.exists(path):
                    with open(path, "rb") as f:
                        part = MIMEBase('application', 'octet-stream')
                        part.set_payload(f.read())
                        encoders.encode_base64(part)
                        part.add_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
                        msg.attach(part)

        # Connect & Send
        timeout = int(getattr(config, 'SMTP_CONNECT_TIMEOUT_SECONDS', 10) or 10)
        server = None
        try:
            if provider.get('use_ssl', False):
                server = smtplib.SMTP_SSL(host=provider['server'], port=provider['port'], timeout=timeout)
            else:
                server = smtplib.SMTP(host=provider['server'], port=provider['port'], timeout=timeout)
                server.ehlo()
                server.starttls()
                server.ehlo()
            
            server.login(provider['email'], provider['password'])
            server.send_message(msg)
            server.quit()
            return True
        except Exception as e:
            logging.error(f"❌ SMTP Provider Error ({provider['name']}): {e}")
            if server:
                try: server.close()
                except: pass
            return False
    except Exception as e:
        logging.error(f"❌ Structural Failure in _send_via_provider: {e}")
        return False

def _wrap_in_sovereign_template(company_name, job_title, body_text, highlights):
    """[👑 INBOX PURGE V11] Ultra-Premium Transactional HTML Template."""
    highlights_html = ""
    colors = ["#06b6d4", "#3b82f6", "#8b5cf6"]
    for i, h in enumerate(highlights[:3]):
        color = colors[i % 3]
        title = h.get('title', 'Competency Block')
        desc = h.get('desc', '')
        
        # [💎 ENHANCED]: Rich text highlighting inside the cards
        desc = desc.replace("100%", '<span style="color: #4ade80;">100%</span>')
        
        highlights_html += f"""
          <tr>
            <td style="padding: 20px; background-color: #1e293b; border-radius: 12px; border-left: 4px solid {color};">
              <span style="font-size: 14px; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 1px;">0{i+1}. {title}</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.6;">{desc}</span>
            </td>
          </tr>
          <tr><td height="15"></td></tr>
        """

    linkedin_url = os.getenv("LINKEDIN_URL", "https://linkedin.com/in/sam-salameh")
    phone = os.getenv("CANDIDATE_PHONE", "+961 70 841 1009")
    candidate_email = os.getenv("SENDER_EMAIL", "sam.dev1@hotmail.com")
    candidate_profession = os.getenv("CANDIDATE_PROFESSION", "Senior Network Engineer")

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="background-color: #0b0f19; padding: 40px 20px; font-family: sans-serif; margin: 0;">
  <table width="100%" align="center" cellpadding="0" cellspacing="0" style="max-width: 650px; margin: 0 auto; background-color: #111827; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0,0,0,0.5);">
    <tr>
      <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 40px 30px; text-align: center;">
        <div style="display: inline-block; width: 60px; height: 60px; background-color: #06b6d4; border-radius: 30px; line-height: 60px; color: #ffffff; font-size: 24px; font-weight: bold; margin-bottom: 15px;">
           SS
        </div>
        <div style="font-size: 13px; letter-spacing: 4px; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px;">{candidate_profession}</div>
        <div style="font-size: 28px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px;">SAM SALAMEH</div>
      </td>
    </tr>
    <tr><td height="4" style="background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);"></td></tr>
    <tr>
      <td style="padding: 40px 35px;">
        <p style="font-size: 17px; margin-top: 0; color: #f8fafc;">Dear <strong>{company_name}</strong> Hiring Team,</p>
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">I am formally reaching out to express my high-level interest in the <span style="color: #06b6d4; font-weight: 600;">{job_title}</span> position.</p>
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">My methodology is built specifically for organizations that focus heavily on <strong>automation, KPIs, and scaling corporate culture</strong>.</p>
        
        <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
          {highlights_html}
        </table>

        <div style="padding: 20px 25px; background-color: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 12px; margin-bottom: 30px; text-align: center;">
          <p style="margin: 0; font-style: italic; color: #e2e8f0; font-size: 16px; line-height: 1.5;">
            "I am looking to bring rigorous accountability and structured scaling to the <strong>{company_name}</strong> team."
          </p>
        </div>
        
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1; margin-bottom: 0;">I have attached <b>My CV</b> for your comprehensive review.</p>
      </td>
    </tr>
    <tr>
      <td style="background-color: #0f172a; padding: 40px 30px; text-align: center; border-top: 1px solid #1e293b;">
        <a href="{linkedin_url}" style="display: inline-block; padding: 14px 32px; background-color: #06b6d4; color: #ffffff; text-decoration: none; border-radius: 30px; font-weight: bold; font-size: 14px; letter-spacing: 1.5px;">VIEW LINKEDIN PORTFOLIO</a>
        <div style="margin-top: 30px;">
          <a href="mailto:{candidate_email}" style="color: #94a3b8; font-size: 14px; text-decoration: none;">{candidate_email}</a>
          <span style="color: #334155; margin: 0 10px;">|</span>
          <a href="tel:{phone}" style="color: #94a3b8; font-size: 14px; text-decoration: none;">{phone}</a>
        </div>
        <div style="font-size: 12px; color: #475569; margin-top: 20px;">{candidate_profession}</div>
      </td>
    </tr>
  </table>
</body>
</html>"""


def close_smtp_pool():
    global _SMTP_POOL
    with _POOL_LOCK:
        for key, (conn, _) in _SMTP_POOL.items():
            try: conn.quit()
            except: pass
        _SMTP_POOL.clear()

def test_email_connection():
    providers = _get_available_providers()
    return {'providers': len(providers), 'overall': len(providers) > 0}
