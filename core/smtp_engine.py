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
        
    zoho_user = (getattr(config, 'ZOHO_SMTP_USER', '') or '').strip()
    zoho_pass = (getattr(config, 'ZOHO_APP_PASSWORD', '') or '').strip()
    if zoho_user and zoho_pass:
        providers.append({'name': 'Zoho (587)', 'server': 'smtp.zoho.com', 'port': 587, 'email': zoho_user, 'password': zoho_pass, 'use_ssl': False})
        providers.append({'name': 'Zoho (465)', 'server': 'smtp.zoho.com', 'port': 465, 'email': zoho_user, 'password': zoho_pass, 'use_ssl': True})
    
    return providers

def send_test_email(recipient_email=None, attachment_paths=None, highlights=None):
    """[👑 OMEGA] Sends a premium visual verification strike to verify the dual PDF package."""
    recipient_email = recipient_email or getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com')
    
    logging.info(f"🧪 TEST STRIKE: Sending to {recipient_email}")
    
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
        try:
            from core.pdf_generator import generate_dynamic_cover_letter
            dummy_lead = {
                'company_name': company_name,
                'job_title': job_title,
                'custom_body': body,
                'highlights': dynamic_highlights
            }
            
            # 👑 [INBOX DELIVERY]: Use PDF CV + PDF Cover Letter (Professional Standard)
            from core.pdf_generator import generate_cv_pdf
            
            # Generate PDF CV from HTML
            cv_pdf_path = generate_cv_pdf(company_name, job_title, dummy_lead)
            
            # Generate PDF Cover Letter
            cl_path = generate_dynamic_cover_letter(company_name, job_title, dummy_lead.get('custom_body', ''), strike_id=8551)
            
            attachment_paths = [cv_pdf_path, cl_path]
            logging.info(f"✅ Generated PDF attachments: CV + Cover Letter")
        except Exception as e:
            logging.error(f"❌ Failed to generate attachments: {e}")
            attachment_paths = []
    
    # Send email and return actual result
    result = send_email(recipient_email, company_name, job_title, body, 'test', 'test', attachment_paths, highlights=dynamic_highlights)
    
    if result:
        logging.info(f"✅ TEST STRIKE SUCCESS: Email sent to {recipient_email}")
    else:
        logging.error(f"❌ TEST STRIKE FAILED: Could not send to {recipient_email}")
    
    return result



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
        
    # [👑 INBOX DELIVERY]: Always generate PDF CV + PDF Cover Letter for professional delivery
    try:
        from core.pdf_generator import generate_cv_pdf, generate_dynamic_cover_letter
        
        # Generate PDF CV
        cv_pdf_path = generate_cv_pdf(company, title, lead)
        
        # Generate PDF Cover Letter if custom_body exists
        if lead.get('custom_body'):
            cl_pdf_path = generate_dynamic_cover_letter(company, title, lead.get('custom_body', ''))
            attachments = [cv_pdf_path, cl_pdf_path]
        else:
            attachments = [cv_pdf_path]
            
        logging.info(f"✅ Generated PDF attachments for {company}")
    except Exception as e:
        logging.error(f"❌ Failed to generate PDF attachments: {e}")
        # Fallback to HTML CV if PDF generation fails
        cv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Sam_Salameh_CV.html'))
        if os.path.exists(cv_path):
            attachments = [cv_path]
        else:
            attachments = []
        
    valid_attachments = [p for p in attachments if p and os.path.exists(p) and os.path.isfile(p)]

    return send_email(email, company, title, lead.get('custom_body', ''), "omni", lead.get('mission_type', 'global'), valid_attachments, sender_name=sender_name, highlights=highlights)

def send_email(to_email, company_name, job_title, custom_body, platform, mission_type, attachment_paths=None, retry_count=0, sender_name="Sam Salameh", highlights=None, reply_to=None):
    """High-reliability delivery engine with smart provider rotation. Priority: Zoho SMTP > Outlook SMTP > Brevo HTTP > Gmail API."""
    
    # 🚀 ZERO-COST: Check email rotation system
    try:
        from core.email_rotator import can_send_email, get_next_email_provider, record_email_sent
        
        if not can_send_email():
            logging.error("❌ DAILY EMAIL LIMIT REACHED for all providers!")
            return False
        
        # Get next available provider
        next_provider = get_next_email_provider()
        if next_provider:
            logging.info(f"📧 Using provider: {next_provider['display_name']} (rotation system)")
    except Exception as e:
        logging.debug(f"Email rotation check failed: {e}")
    
    # [👑 VIP RECOVERY]: Robust fallback for reply-to
    if not reply_to:
        reply_to = os.getenv("REPLY_TO_EMAIL", "sam.dev1@outlook.com")

    if getattr(config, 'TEST_MODE', False) and to_email != getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com'):
        to_email = getattr(config, 'TEST_RECEIVER_EMAIL', 'sam.dev1@hotmail.com')
    
    # [👑 CENTRALIZED METADATA]: Generate professional subject line
    subject = f"{job_title} Application - {sender_name}"

    # ============================================================
    # 🌟 ABSOLUTE PRIORITY 1: GMAIL API (HTTP Port 443)
    # The ONLY way to bypass Render's Free Tier firewall AND hit the Inbox.
    # ============================================================
    if get_gmail_service:
        try:
            # [👑 CLOUD SHIELD]: Attempt to initialize the service
            service = get_gmail_service()
            if service:
                if send_email_via_gmail_api(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, service=service, reply_to=reply_to):
                    logging.info("✅ GMAIL API SUCCESS — Bypassed Render firewall and hit Inbox perfectly.")
                    return True
                else:
                    logging.error("❌ GMAIL API FAILED structural delivery.")
            else:
                logging.warning("⚠️ Gmail API service initialization returned None.")
        except PermissionError as pe:
            logging.error(f"🚫 GMAIL AUTH BLOCKED ON CLOUD: {pe}. Falling back to SMTP...")
        except Exception as e:
            if "invalid_grant" in str(e):
                logging.error("🚨 GMAIL TOKEN EXPIRED: You MUST run the bot LOCALLY on your computer once to refresh the token, then push the new token.json to GitHub.")
            logging.warning(f"⚠️ Gmail API unexpected failure: {e}")

    # ============================================================
    # 🥈 PRIORITY 2: ZOHO SMTP (DMARC Aligned)
    # ============================================================
    zoho_user = (getattr(config, 'ZOHO_SMTP_USER', '') or '').strip()
    zoho_pass = (getattr(config, 'ZOHO_APP_PASSWORD', '') or '').strip()
    if zoho_user and zoho_pass:
        zoho_provider = {
            'name': 'Zoho (STARTTLS-587)',
            'server': 'smtp.zoho.com',
            'port': 587,
            'email': zoho_user,
            'password': zoho_pass,
            'use_ssl': False
        }
        try:
            logging.info("📧 [ZOHO-SMTP] Attempting Native Zoho Delivery (DMARC Aligned)...")
            res = _send_via_provider(to_email, company_name, job_title, custom_body, zoho_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
            if res:
                logging.info("✅ ZOHO SMTP SUCCESS — Delivered to Inbox natively.")
                
                # 🚀 ZERO-COST: Record email sent
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("zoho")
                except: pass
                
                return True
        except Exception as e:
            logging.warning(f"⚠️ Zoho SMTP failed: {e}")

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
                # [👑 CLOUD DELIVERABILITY FIX]: If we use Hotmail via Brevo, Outlook blackholes it.
                # We use the Zoho address as the VISIBLE sender, but the Brevo Login for AUTH.
                neutral_sender = (getattr(config, 'ZOHO_SMTP_USER', '') or brevo_smtp_user).strip()
                
                logging.info(f"📧 [RENDER-BOOST] Using Neutral Identity: {neutral_sender} (Auth: {brevo_smtp_user})")
                res = _send_via_provider(to_email, company_name, job_title, custom_body, brevo_smtp_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to, sender_override=neutral_sender)
                if res:
                    logging.info("✅ RENDER-BOOST SUCCESS — Port 2525 bypassed Render block!")
                    
                    # 🚀 ZERO-COST: Record email sent
                    try:
                        from core.email_rotator import record_email_sent
                        record_email_sent("brevo")
                    except: pass
                    
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
                
                # 🚀 ZERO-COST: Record email sent
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("brevo")
                except: pass
                
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
            subject = f"{job_title} Application - {sender_name}"
        
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        
        # [👑 OMEGA CLOUD FIX]: We fetch the authenticated email address directly from Google
        # to ensure the 'From' header is 100% genuine and passes all Outlook security checks.
        try:
            profile = service.users().getProfile(userId='me').execute()
            authenticated_email = profile.get('emailAddress')
            logging.info(f"🟢 GMAIL API: Authenticated as {authenticated_email}")
            msg['From'] = f"{sender_name} <{authenticated_email}>"
        except Exception as e:
            logging.warning(f"⚠️ Could not fetch Gmail profile: {e}. Omitting From header.")
        
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
        subject = f"{job_title} Application - {sender_name}"
        
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
    
    # [👑 CLOUD-SURVIVAL OVERRIDE] 
    # Force the technical sender to be the Brevo authenticated email to pass DMARC perfectly.
    # The 'Reply-To' guarantees the recruiter's response goes to Sam.
    technical_sender_email = (getattr(config, 'BREVO_SMTP_LOGIN', '') or real_user_email).strip()
    
    payload = {
        "sender": {"email": technical_sender_email, "name": sender_name},
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

def _send_via_provider(to_email, company_name, job_title, custom_body, provider, attachment_paths, sender_name, highlights, subject=None, reply_to=None, sender_override=None):
    """[👑 SMTP IGNITION] Final structural delivery."""
    try:
        if not subject:
            subject = f"{job_title} Application - {sender_name}"
            
        msg = MIMEMultipart('mixed')
        msg['Subject'] = subject
        
        # [👑 CLOUD-SURVIVAL OVERRIDE]: Pass DMARC by aligning technical sender.
        # Use sender_override if provided (for Neutral Identity), otherwise use provider login.
        technical_sender = (sender_override or provider['email']).strip()
        msg['From'] = f"{sender_name} <{technical_sender}>"
        msg['To'] = to_email
        if reply_to:
            msg['Reply-To'] = f"{sender_name} <{reply_to}>"
        else:
            real_user_email = (getattr(config, 'SENDER_EMAIL', '')).strip()
            if real_user_email:
                msg['Reply-To'] = f"{sender_name} <{real_user_email}>"

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
    """Professional clean email template - INBOX optimized."""
    
    # Build highlights section
    highlights_html = ""
    if highlights:
        highlights_html = "<div style='margin: 20px 0;'><strong style='color: #2563eb;'>Key Qualifications:</strong><ul style='margin: 10px 0; padding-left: 20px;'>"
        for h in highlights[:3]:
            title = h.get('title', '')
            desc = h.get('desc', '')
            if title and desc:
                highlights_html += f"<li style='margin: 8px 0; color: #374151;'><strong>{title}:</strong> {desc}</li>"
        highlights_html += "</ul></div>"
    
    # Get candidate info from environment
    linkedin_url = os.getenv("LINKEDIN_URL", "https://linkedin.com/in/sam-salameh")
    phone = os.getenv("CANDIDATE_PHONE", "+961 70 841 1009")
    candidate_email = os.getenv("SENDER_EMAIL", "sam.dev1@hotmail.com")
    candidate_name = os.getenv("SENDER_NAME", "Sam Salameh")
    candidate_profession = os.getenv("CANDIDATE_PROFESSION", "Senior Network Engineer")
    
    # Use custom body if provided, otherwise use default
    if body_text and len(body_text.strip()) > 50:
        main_content = f"<p style='color: #374151; line-height: 1.6; margin: 15px 0;'>{body_text}</p>"
    else:
        main_content = f"""
        <p style='color: #374151; line-height: 1.6; margin: 15px 0;'>
            I am writing to express my strong interest in the <strong>{job_title}</strong> position at {company_name}. 
            With my extensive background in {candidate_profession.lower()}, I am confident in my ability to contribute 
            meaningfully to your team.
        </p>
        <p style='color: #374151; line-height: 1.6; margin: 15px 0;'>
            My experience includes designing and implementing enterprise-grade network infrastructure, managing complex 
            technical projects, and delivering solutions that drive business growth. I am particularly drawn to this 
            opportunity because of {company_name}'s reputation for excellence and innovation.
        </p>
        """
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 20px; font-family: Arial, Helvetica, sans-serif; background-color: #f3f4f6;">
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background-color: #ffffff; border: 1px solid #e5e7eb;">
    <!-- Header -->
    <tr>
      <td style="padding: 30px 40px; background-color: #ffffff; border-bottom: 3px solid #2563eb;">
        <h1 style="margin: 0; font-size: 24px; color: #1f2937; font-weight: 600;">{candidate_name}</h1>
        <p style="margin: 5px 0 0 0; font-size: 14px; color: #6b7280;">{candidate_profession}</p>
      </td>
    </tr>
    
    <!-- Body -->
    <tr>
      <td style="padding: 40px;">
        <p style="margin: 0 0 15px 0; font-size: 16px; color: #1f2937;">Dear {company_name} Hiring Team,</p>
        
        <p style="margin: 15px 0; font-size: 16px; color: #1f2937; font-weight: 600;">
            Re: Application for {job_title}
        </p>
        
        {main_content}
        
        {highlights_html}
        
        <p style='color: #374151; line-height: 1.6; margin: 15px 0;'>
            I have attached my CV for your review. I would welcome the opportunity to discuss how my skills and 
            experience align with your needs.
        </p>
        
        <p style='color: #374151; line-height: 1.6; margin: 15px 0;'>
            Thank you for considering my application. I look forward to hearing from you.
        </p>
        
        <p style='color: #374151; line-height: 1.6; margin: 25px 0 5px 0;'>
            Best regards,<br>
            <strong>{candidate_name}</strong>
        </p>
      </td>
    </tr>
    
    <!-- Footer -->
    <tr>
      <td style="padding: 30px 40px; background-color: #f9fafb; border-top: 1px solid #e5e7eb;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="font-size: 14px; color: #6b7280; line-height: 1.6;">
              <strong style="color: #1f2937;">{candidate_name}</strong><br>
              {candidate_profession}<br>
              <a href="mailto:{candidate_email}" style="color: #2563eb; text-decoration: none;">{candidate_email}</a><br>
              <a href="tel:{phone}" style="color: #2563eb; text-decoration: none;">{phone}</a><br>
              <a href="{linkedin_url}" style="color: #2563eb; text-decoration: none;">LinkedIn Profile</a>
            </td>
          </tr>
        </table>
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
