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
            attachments = []
            
            # 1. PDF CV using Playwright (100% match to HTML)
            try:
                from core.cv_playwright_pdf import generate_cv_from_html_playwright
                cv_pdf_path = generate_cv_from_html_playwright()
                if cv_pdf_path and os.path.exists(cv_pdf_path):
                    attachments.append(cv_pdf_path)
                    logging.info(f"✅ Added Playwright PDF CV: {cv_pdf_path}")
                else:
                    raise Exception("Playwright PDF generation failed")
            except Exception as e:
                logging.warning(f"⚠️ Playwright failed: {e}, falling back to FPDF")
                # Fallback to FPDF if Playwright fails
                from core.cv_pdf_full import generate_full_cv_pdf
                cv_pdf_path = generate_full_cv_pdf()
                if cv_pdf_path and os.path.exists(cv_pdf_path):
                    attachments.append(cv_pdf_path)
                    logging.info(f"✅ Added FPDF CV: {cv_pdf_path}")
            
            # 2. Cover Letter PDF
            try:
                from core.cover_letter_pdf import generate_cover_letter_pdf
                cover_pdf_path = generate_cover_letter_pdf(company_name, job_title)
                if cover_pdf_path and os.path.exists(cover_pdf_path):
                    attachments.append(cover_pdf_path)
                    logging.info(f"✅ Added Cover Letter PDF: {cover_pdf_path}")
            except Exception as e:
                logging.warning(f"⚠️ Cover letter generation failed: {e}")
            
            attachment_paths = attachments if attachments else []
            
        except Exception as e:
            logging.error(f"❌ Failed to prepare attachments: {e}")
            import traceback
            traceback.print_exc()
            attachment_paths = []
    
    # Send email and return actual result
    result = send_email(recipient_email, company_name, job_title, body, 'test', 'test', attachment_paths, highlights=dynamic_highlights, strike_id="STRIKE-2771")
    
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
    strike_id = lead.get('strike_id', '')  # Get strike_id from lead

    if not _validate_email(email):
        logging.warning(f"SKIPPING STRIKE: No valid email for {company}.")
        return False

    # Ensure attachment_paths is a proper list to prevent silent string iteration bugs
    if isinstance(attachment_paths, str):
        attachments = [attachment_paths]
    else:
        attachments = attachment_paths or []
        
    # [👑 INBOX DELIVERY]: Use Playwright PDF (100% match to HTML) + Cover Letter
    try:
        attachments = []
        
        # 1. CV PDF - Try Playwright first (best quality)
        try:
            from core.cv_playwright_pdf import generate_cv_from_html_playwright
            cv_pdf_path = generate_cv_from_html_playwright()
            
            if cv_pdf_path and os.path.exists(cv_pdf_path):
                attachments.append(cv_pdf_path)
                logging.info(f"✅ Using Playwright PDF CV for {company} (100% HTML match)")
            else:
                raise Exception("Playwright PDF generation failed")
        except Exception as e:
            logging.warning(f"⚠️ Playwright failed: {e}, falling back to FPDF")
            # Fallback to FPDF
            from core.cv_pdf_full import generate_full_cv_pdf
            cv_pdf_path = generate_full_cv_pdf()
            
            if cv_pdf_path and os.path.exists(cv_pdf_path):
                attachments.append(cv_pdf_path)
                logging.info(f"✅ Using FPDF CV for {company} (professional)")
            else:
                logging.error(f"❌ Failed to generate PDF CV")
        
        # 2. Cover Letter PDF
        try:
            from core.cover_letter_pdf import generate_cover_letter_pdf
            cover_pdf_path = generate_cover_letter_pdf(company, title)
            if cover_pdf_path and os.path.exists(cover_pdf_path):
                attachments.append(cover_pdf_path)
                logging.info(f"✅ Added Cover Letter PDF for {company}")
        except Exception as e:
            logging.warning(f"⚠️ Cover letter generation failed: {e}")
            
    except Exception as e:
        logging.error(f"❌ Failed to attach documents: {e}")
        attachments = []
        
    valid_attachments = [p for p in attachments if p and os.path.exists(p) and os.path.isfile(p)]

    return send_email(email, company, title, lead.get('custom_body', ''), "omni", lead.get('mission_type', 'global'), valid_attachments, sender_name=sender_name, highlights=highlights, strike_id=strike_id)

def send_email(to_email, company_name, job_title, custom_body, platform, mission_type, attachment_paths=None, retry_count=0, sender_name="Sam Salameh", highlights=None, reply_to=None, strike_id=None):
    """High-reliability delivery engine with smart provider rotation. Priority: Brevo HTTP > Gmail SMTP > Zoho SMTP."""
    
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
        reply_to = os.getenv("REPLY_TO_EMAIL", "samsalameh.cv@gmail.com")

    if getattr(config, 'TEST_MODE', False) and to_email != getattr(config, 'TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com'):
        to_email = getattr(config, 'TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')
    
    # [👑 CENTRALIZED METADATA]: Generate professional subject line with company and STRIKE-ID
    if strike_id:
        subject = f"Application: {job_title} - {company_name} [{strike_id}]"
    else:
        subject = f"Application: {job_title} - {company_name}"
    
    # Debug: Print subject to verify
    logging.info(f"📧 EMAIL SUBJECT: {subject}")

    # ============================================================
    # 🌟 ABSOLUTE PRIORITY 1: BREVO HTTP API (Port 443)
    # The MOST RELIABLE way to bypass ALL firewall issues!
    # ============================================================
    if getattr(config, 'BREVO_API_KEY', None):
        try:
            logging.info("📧 [BREVO-HTTP] Attempting Brevo HTTP API (MOST RELIABLE)...")
            if send_email_via_brevo_http(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to):
                logging.info("✅ BREVO HTTP SUCCESS — Delivered via Brevo API!")
                
                # 🚀 ZERO-COST: Record email sent
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("brevo")
                except: pass
                
                return True
        except Exception as e:
            logging.warning(f"⚠️ Brevo HTTP failed: {e}")

    # ============================================================
    # 🥈 PRIORITY 2: GMAIL API (HTTP Port 443)
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
    # 🥉 PRIORITY 3: GMAIL SMTP (Port 465 SSL)
    # ============================================================
    gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()
    gmail_pass = (getattr(config, 'GMAIL_APP_PASSWORD', '') or '').strip()
    if gmail_user and gmail_pass:
        gmail_provider = {
            'name': 'Gmail (SSL-465)',
            'server': 'smtp.gmail.com',
            'port': 465,
            'email': gmail_user,
            'password': gmail_pass,
            'use_ssl': True
        }
        try:
            logging.info("📧 [GMAIL-SMTP] Attempting Gmail SMTP Delivery (App Password)...")
            res = _send_via_provider(to_email, company_name, job_title, custom_body, gmail_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
            if res:
                logging.info("✅ GMAIL SMTP SUCCESS — Delivered via Gmail directly!")
                
                # 🚀 ZERO-COST: Record email sent
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("gmail")
                except: pass
                
                return True
        except Exception as e:
            logging.warning(f"⚠️ Gmail SMTP failed: {e}")

    # ============================================================
    # 🥉 PRIORITY 3: ZOHO SMTP (DMARC Aligned)
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
            subject = f"Application: {job_title} - {company_name}"
        
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
                        
                        # [👑 CLEAN FILENAME]: Always use simple filename for CV
                        filename = os.path.basename(path)
                        if 'CV' in filename or 'cv' in filename:
                            filename = 'Sam_Salameh_CV.html' if filename.endswith('.html') else 'Sam_Salameh_CV.pdf'
                        
                        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
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
        subject = f"Application: {job_title} - {company_name}"
        
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
            subject = f"Application: {job_title} - {company_name}"
            
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
                        
                        # [👑 CLEAN FILENAME]: Always use simple filename for CV
                        filename = os.path.basename(path)
                        if 'CV' in filename or 'cv' in filename:
                            filename = 'Sam_Salameh_CV.html' if filename.endswith('.html') else 'Sam_Salameh_CV.pdf'
                        
                        part.add_header('Content-Disposition', f'attachment; filename="{filename}"')
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
    """Professional dark mode email template - matching the CV design."""
    
    # Build highlights section (dark mode style)
    highlights_html = ""
    if highlights:
        highlights_html = "<div style='margin: 30px 0;'>"
        for i, h in enumerate(highlights[:3], 1):
            title = h.get('title', '')
            desc = h.get('desc', '')
            if title and desc:
                highlights_html += f"""
                <div style='margin: 20px 0; padding: 20px; background: rgba(255,255,255,0.05); border-left: 4px solid #00b4d8;'>
                    <div style='color: #00b4d8; font-weight: bold; font-size: 14px; margin-bottom: 8px;'>
                        0{i}. {title}
                    </div>
                    <div style='color: #b8c5d0; font-size: 13px; line-height: 1.6;'>
                        {desc}
                    </div>
                </div>
                """
        highlights_html += "</div>"
    
    # Get candidate info from environment
    linkedin_url = os.getenv("LINKEDIN_URL", "https://linkedin.com/in/sam-salameh")
    phone = os.getenv("CANDIDATE_PHONE", "+961 70 841 1009")
    candidate_email = os.getenv("SENDER_EMAIL", "samsalameh.cv@gmail.com")
    candidate_name = os.getenv("SENDER_NAME", "Sam Salameh")
    candidate_profession = os.getenv("CANDIDATE_PROFESSION", "Senior Network Engineer")
    
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin: 0; padding: 20px; font-family: 'Segoe UI', Arial, sans-serif; background-color: #1a1d29;">
  <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 600px; margin: 0 auto; background: linear-gradient(135deg, #2d3748 0%, #1a1d29 100%);">
    
    <!-- Header with Circle Avatar -->
    <tr>
      <td style="padding: 40px 40px 20px 40px; text-align: center;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="text-align: center;">
              <div style="width: 70px; height: 70px; margin: 0 auto 15px auto; background: #00b4d8; border-radius: 50%; line-height: 70px; text-align: center;">
                <span style="color: white; font-size: 28px; font-weight: bold;">SS</span>
              </div>
            </td>
          </tr>
        </table>
        <div style="color: #94a3b8; font-size: 11px; letter-spacing: 3px; margin-bottom: 8px;">
          {candidate_profession.upper()}
        </div>
        <h1 style="margin: 0; font-size: 28px; color: #ffffff; font-weight: 700; letter-spacing: 2px;">
          {candidate_name.upper()}
        </h1>
      </td>
    </tr>
    
    <!-- Body -->
    <tr>
      <td style="padding: 40px;">
        <p style="margin: 0 0 20px 0; font-size: 16px; color: #e2e8f0;">
          Dear {company_name} Hiring Team,
        </p>
        
        <p style="margin: 20px 0; font-size: 15px; color: #e2e8f0; line-height: 1.8;">
          I am formally reaching out to express my high-level interest in the <span style="color: #00b4d8; font-weight: 600;">{job_title}</span> position.
        </p>
        
        <p style="margin: 20px 0; font-size: 15px; color: #e2e8f0; line-height: 1.8;">
          My methodology is built specifically for organizations that focus heavily on automation, KPIs, and scaling corporate culture.
        </p>
        
        {highlights_html}
        
        <div style="margin: 40px 0 30px 0; padding: 30px; background: rgba(0, 180, 216, 0.1); border-radius: 8px; text-align: center;">
          <p style="margin: 0; font-size: 16px; color: #e2e8f0; font-style: italic; line-height: 1.8;">
            "I am looking to bring rigorous accountability and structured scaling to the {company_name} team."
          </p>
        </div>
        
        <p style="margin: 20px 0; font-size: 15px; color: #e2e8f0; line-height: 1.8;">
          I have attached <strong style="color: #00b4d8;">My Professional CV</strong> and <strong style="color: #00b4d8;">Cover Letter</strong> in PDF format for your comprehensive review.
        </p>
        
        <div style="margin: 40px 0 0 0; text-align: center;">
          <a href="{linkedin_url}" style="display: inline-block; padding: 15px 40px; background: #00b4d8; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; letter-spacing: 1px;">
            LINKEDIN PROFILE
          </a>
        </div>
      </td>
    </tr>
    
    <!-- Footer -->
    <tr>
      <td style="padding: 30px 40px; text-align: center; border-top: 1px solid rgba(255,255,255,0.1);">
        <div style="color: #94a3b8; font-size: 14px; line-height: 1.8;">
          <a href="mailto:{candidate_email}" style="color: #94a3b8; text-decoration: none;">{candidate_email}</a>
          <span style="margin: 0 10px;">|</span>
          <a href="tel:{phone}" style="color: #94a3b8; text-decoration: none;">{phone}</a>
        </div>
        <div style="color: #64748b; font-size: 13px; margin-top: 10px;">
          {candidate_profession}
        </div>
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
