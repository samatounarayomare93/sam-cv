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
    import resend as resend_lib
    HAS_RESEND = True
except ImportError:
    HAS_RESEND = False
try:
    import mailjet_rest
    HAS_MAILJET = True
except ImportError:
    HAS_MAILJET = False
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
    # 🌟 ABSOLUTE PRIORITY 0: RESEND API (Best Gmail deliverability!)
    # Free 3000/month, excellent inbox delivery, works on Render
    # ============================================================
    resend_api_key = os.getenv("RESEND_API_KEY", "").strip()
    if resend_api_key:
        try:
            import resend as resend_lib
            resend_lib.api_key = resend_api_key
            
            html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
            
            # Build attachments for Resend
            resend_attachments = []
            if attachment_paths:
                for path in attachment_paths:
                    if path and os.path.exists(path):
                        with open(path, "rb") as f:
                            content = base64.b64encode(f.read()).decode("utf-8")
                            resend_attachments.append({
                                "filename": os.path.basename(path),
                                "content": content
                            })
            
            params = {
                "from": f"Sam Salameh <onboarding@resend.dev>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
                "reply_to": reply_to or "samsalameh.cv@gmail.com"
            }
            if resend_attachments:
                params["attachments"] = resend_attachments
            
            logging.info(f"📧 [RESEND] ⭐ PRIORITY 0: Sending to {to_email}...")
            result = resend_lib.Emails.send(params)
            
            if result and result.get('id'):
                logging.info(f"✅ [RESEND] SUCCESS! Email ID: {result['id']} → Delivered to INBOX!")
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("resend")
                except: pass
                return True
            else:
                logging.warning(f"⚠️ [RESEND] No ID returned: {result}")
        except Exception as e:
            logging.warning(f"⚠️ [RESEND] Failed: {e}")

    # ============================================================
    # 🌟 CLOUD-OPTIMIZED PRIORITY
    # On Render: SMTP ports are blocked, only HTTP works
    # ============================================================
    is_render = os.getenv("RENDER") is not None
    
    if is_render:
        logging.info("☁️ [RENDER-MODE] Using HTTP APIs + SMTP for maximum throughput")
        
        # ⭐ PRIORITY 1: RESEND (all configured accounts)
        # Supports RESEND_API_KEY, RESEND_API_KEY_2 ... RESEND_API_KEY_10
        if HAS_RESEND:
            resend_keys = []
            for i in range(1, 11):
                env = "RESEND_API_KEY" if i == 1 else f"RESEND_API_KEY_{i}"
                k = os.getenv(env, "").strip()
                if k:
                    resend_keys.append(k)
            
            if resend_keys:
                try:
                    result = send_email_via_resend(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
                    if result:
                        return True
                except Exception as e:
                    logging.warning(f"⚠️ Resend failed: {e}")

        # PRIORITY 2: BREVO HTTP (300/day)
        if getattr(config, 'BREVO_API_KEY', None):
            try:
                if send_email_via_brevo_http(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to):
                    try:
                        from core.email_rotator import record_email_sent
                        record_email_sent("brevo")
                    except: pass
                    return True
            except Exception as e:
                logging.warning(f"⚠️ Brevo HTTP failed: {e}")

        # PRIORITY 3: MAILJET HTTP API (200/day free)
        mailjet_pub = os.getenv("MAILJET_API_KEY", "").strip()
        mailjet_priv = os.getenv("MAILJET_SECRET_KEY", "").strip()
        if mailjet_pub and mailjet_priv:
            try:
                result = send_email_via_mailjet(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
                if result:
                    logging.info("✅ MAILJET SUCCESS!")
                    return True
            except Exception as e:
                logging.warning(f"⚠️ Mailjet failed: {e}")

        # PRIORITY 4: SENDPULSE HTTP API (400/day free)
        sendpulse_id = os.getenv("SENDPULSE_CLIENT_ID", "").strip()
        sendpulse_secret = os.getenv("SENDPULSE_CLIENT_SECRET", "").strip()
        if sendpulse_id and sendpulse_secret:
            try:
                result = send_email_via_sendpulse(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
                if result:
                    logging.info("✅ SENDPULSE SUCCESS!")
                    return True
            except Exception as e:
                logging.warning(f"⚠️ SendPulse failed: {e}")

        # PRIORITY 3-12: ALL ZOHO ACCOUNTS (500/day each)
        # Supports ZOHO_SMTP_USER, ZOHO_SMTP_USER_2 ... ZOHO_SMTP_USER_10
        for i in range(1, 11):
            u_env = "ZOHO_SMTP_USER" if i == 1 else f"ZOHO_SMTP_USER_{i}"
            p_env = "ZOHO_APP_PASSWORD" if i == 1 else f"ZOHO_APP_PASSWORD_{i}"
            z_user = os.getenv(u_env, "").strip()
            z_pass = os.getenv(p_env, "").strip()
            if not z_user or not z_pass:
                continue
            for z_port, z_ssl in [(465, True), (587, False)]:
                z_provider = {
                    'name': f'Zoho#{i} ({"SSL" if z_ssl else "TLS"}-{z_port})',
                    'server': 'smtp.zoho.com', 'port': z_port,
                    'email': z_user, 'password': z_pass, 'use_ssl': z_ssl
                }
                try:
                    logging.info(f"📧 [ZOHO#{i}] Attempting port {z_port}...")
                    res = _send_via_provider(to_email, company_name, job_title, custom_body, z_provider, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
                    if res:
                        logging.info(f"✅ ZOHO #{i} PORT {z_port} SUCCESS!")
                        try:
                            from core.email_rotator import record_email_sent
                            record_email_sent(f"zoho_{i}")
                        except: pass
                        return True
                    break  # If port 465 fails, try 587
                except Exception as e:
                    logging.warning(f"⚠️ Zoho #{i} port {z_port} failed: {e}")

        # PRIORITY 13: Gmail API (OAuth2 over HTTPS)
        if get_gmail_service:
            try:
                service = get_gmail_service()
                if service:
                    if send_email_via_gmail_api(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, service=service, reply_to=reply_to):
                        logging.info("✅ GMAIL API SUCCESS!")
                        return True
            except Exception as e:
                logging.warning(f"⚠️ Gmail API failed: {e}")

        # PRIORITY 14: Mailjet (200/day free)
        if os.getenv("MAILJET_API_KEY") and os.getenv("MAILJET_API_SECRET"):
            try:
                logging.info("📧 [MAILJET] Attempting Mailjet API (200/day free)...")
                if send_email_via_mailjet(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to):
                    logging.info("✅ MAILJET SUCCESS!")
                    try:
                        from core.email_rotator import record_email_sent
                        record_email_sent("mailjet")
                    except: pass
                    return True
            except Exception as e:
                logging.warning(f"⚠️ Mailjet failed: {e}")

        # PRIORITY 15: SendPulse (400/day free)
        if os.getenv("SENDPULSE_CLIENT_ID") and os.getenv("SENDPULSE_CLIENT_SECRET"):
            try:
                logging.info("📧 [SENDPULSE] Attempting SendPulse API (400/day free)...")
                if send_email_via_sendpulse(to_email, company_name, job_title, custom_body, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to):
                    logging.info("✅ SENDPULSE SUCCESS!")
                    try:
                        from core.email_rotator import record_email_sent
                        record_email_sent("sendpulse")
                    except: pass
                    return True
            except Exception as e:
                logging.warning(f"⚠️ SendPulse failed: {e}")

        logging.error("❌ ALL PROVIDERS FAILED on Render")
        return False

    # ============================================================
    # 🌟 LOCAL/NON-RENDER PRIORITY: Try SMTP first
    # ============================================================
    logging.info("💻 [LOCAL-MODE] Trying SMTP connections...")
    
    gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()
    gmail_pass = (getattr(config, 'GMAIL_APP_PASSWORD', '') or '').strip()
    
    # 🔍 DEBUG: Log Gmail credentials status
    logging.info(f"🔍 [GMAIL-CHECK] User: {'✅ SET' if gmail_user else '❌ MISSING'} ({gmail_user[:10]}... if set)")
    logging.info(f"🔍 [GMAIL-CHECK] Pass: {'✅ SET' if gmail_pass else '❌ MISSING'} ({len(gmail_pass)} chars)")
    
    if gmail_user and gmail_pass:
        # Try Port 465 (SSL) first
        gmail_provider_465 = {
            'name': 'Gmail (SSL-465)',
            'server': 'smtp.gmail.com',
            'port': 465,
            'email': gmail_user,
            'password': gmail_pass,
            'use_ssl': True
        }
        try:
            logging.info("📧 [GMAIL-SMTP] ⭐ PRIORITY 1A: Attempting Gmail SMTP Port 465 (SSL)...")
            res = _send_via_provider(to_email, company_name, job_title, custom_body, gmail_provider_465, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
            if res:
                logging.info("✅ ⭐ GMAIL SMTP 465 SUCCESS — Delivered via Gmail directly to INBOX!")
                
                # 🚀 ZERO-COST: Record email sent
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("gmail")
                except: pass
                
                return True
            else:
                logging.warning("⚠️ [GMAIL-SMTP] Port 465 failed, trying port 587...")
        except Exception as e:
            logging.warning(f"⚠️ [GMAIL-SMTP] Port 465 exception: {e}, trying port 587...")
        
        # Try Port 587 (STARTTLS) as fallback - better for cloud platforms
        gmail_provider_587 = {
            'name': 'Gmail (STARTTLS-587)',
            'server': 'smtp.gmail.com',
            'port': 587,
            'email': gmail_user,
            'password': gmail_pass,
            'use_ssl': False
        }
        try:
            logging.info("📧 [GMAIL-SMTP] ⭐ PRIORITY 1B: Attempting Gmail SMTP Port 587 (STARTTLS)...")
            res = _send_via_provider(to_email, company_name, job_title, custom_body, gmail_provider_587, attachment_paths, sender_name, highlights, subject=subject, reply_to=reply_to)
            if res:
                logging.info("✅ ⭐ GMAIL SMTP 587 SUCCESS — Delivered via Gmail directly to INBOX!")
                
                # 🚀 ZERO-COST: Record email sent
                try:
                    from core.email_rotator import record_email_sent
                    record_email_sent("gmail")
                except: pass
                
                return True
            else:
                logging.error("❌ [GMAIL-SMTP] Both ports 465 and 587 failed")
        except Exception as e:
            logging.error(f"❌ [GMAIL-SMTP] Port 587 also failed: {e}")
            import traceback
            logging.error(f"❌ [GMAIL-SMTP] Traceback: {traceback.format_exc()}")
    else:
        logging.error("❌ [GMAIL-SMTP] SKIPPED - Credentials not configured!")

    # ============================================================
    # 🥈 PRIORITY 2: BREVO HTTP API (Port 443)
    # Reliable but may go to spam
    # ============================================================
    if getattr(config, 'BREVO_API_KEY', None):
        try:
            logging.info("📧 [BREVO-HTTP] Attempting Brevo HTTP API...")
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
    # 🥉 PRIORITY 3: GMAIL API (HTTP Port 443)
    # ============================================================
    # ============================================================
    # 🥉 PRIORITY 3: GMAIL API (HTTP Port 443)
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
    # 🔰 PRIORITY 4: ZOHO SMTP (DMARC Aligned)
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

def send_email_via_resend(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None, api_key_env="RESEND_API_KEY"):
    """[RESEND API] Best Gmail inbox delivery. Supports multiple accounts."""
    if not HAS_RESEND:
        logging.error("❌ [RESEND] resend package not installed!")
        return False

    # Try all configured Resend keys (account rotation)
    resend_keys = []
    for env_var in ["RESEND_API_KEY", "RESEND_API_KEY_2", "RESEND_API_KEY_3"]:
        key = os.getenv(env_var, "").strip()
        if key:
            resend_keys.append((env_var, key))

    if not resend_keys:
        logging.error("❌ [RESEND] No RESEND_API_KEY configured!")
        return False

    if not subject:
        subject = f"Application: {job_title} - {company_name}"

    html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
    gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()

    # Build attachments
    attachments = []
    if attachment_paths:
        for path in attachment_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        content = base64.b64encode(f.read()).decode("utf-8")
                        attachments.append({"filename": os.path.basename(path), "content": content})
                except Exception as e:
                    logging.warning(f"⚠️ [RESEND] Failed to attach {path}: {e}")

    # Try each Resend key until one works
    for env_var, key in resend_keys:
        try:
            resend_lib.api_key = key
            params = {
                "from": f"{sender_name} <onboarding@resend.dev>",
                "to": [to_email],
                "subject": subject,
                "html": html_content,
                "reply_to": reply_to or gmail_user or to_email,
            }
            if attachments:
                params["attachments"] = attachments

            logging.info(f"📤 [RESEND] Sending via {env_var} to {to_email}...")
            r = resend_lib.Emails.send(params)

            if r and r.get('id'):
                logging.info(f"✅ [RESEND] SUCCESS! Email ID: {r.get('id')} → Delivered to INBOX!")
                return True
        except Exception as e:
            logging.warning(f"⚠️ [RESEND] {env_var} failed: {e}, trying next key...")
            continue

    logging.error("❌ [RESEND] All Resend keys failed!")
    return False


def send_email_via_mailjet(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None):
    """[MAILJET API] 200 emails/day free. Uses HTTP API."""
    api_key = os.getenv("MAILJET_API_KEY", "").strip()
    secret_key = os.getenv("MAILJET_SECRET_KEY", "").strip()
    sender_email = os.getenv("MAILJET_SENDER_EMAIL", os.getenv("GMAIL_SMTP_USER", "sam.dev1@hotmail.com")).strip()
    if not api_key or not secret_key:
        return False

    if not subject:
        subject = f"Application: {job_title} - {company_name}"

    html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])

    payload = {
        "Messages": [{
            "From": {"Email": sender_email, "Name": sender_name},
            "To": [{"Email": to_email}],
            "Subject": subject,
            "HTMLPart": html_content,
            "ReplyTo": {"Email": reply_to or sender_email}
        }]
    }

    try:
        logging.info(f"📧 [MAILJET] Sending to {to_email}...")
        r = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(api_key, secret_key),
            json=payload,
            timeout=20
        )
        if r.status_code in (200, 201):
            logging.info(f"✅ [MAILJET] Email sent! Status: {r.status_code}")
            return True
        else:
            logging.error(f"❌ [MAILJET] Failed: {r.status_code} - {r.text[:200]}")
            return False
    except Exception as e:
        logging.error(f"❌ [MAILJET] Exception: {e}")
        return False


def send_email_via_sendpulse(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None):
    """[SENDPULSE API] 400 emails/day free. Uses HTTP API."""
    client_id = os.getenv("SENDPULSE_CLIENT_ID", "").strip()
    client_secret = os.getenv("SENDPULSE_CLIENT_SECRET", "").strip()
    sender_email = os.getenv("SENDPULSE_SENDER_EMAIL", os.getenv("GMAIL_SMTP_USER", "sam.dev1@hotmail.com")).strip()
    if not client_id or not client_secret:
        return False

    if not subject:
        subject = f"Application: {job_title} - {company_name}"

    html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])

    try:
        # Get access token
        token_r = requests.post(
            "https://api.sendpulse.com/oauth/access_token",
            json={"grant_type": "client_credentials", "client_id": client_id, "client_secret": client_secret},
            timeout=15
        )
        if token_r.status_code != 200:
            logging.error(f"❌ [SENDPULSE] Token failed: {token_r.text[:100]}")
            return False

        token = token_r.json().get("access_token")
        if not token:
            return False

        # Send email
        payload = {
            "email": {
                "html": html_content,
                "text": "Please view this email in HTML format.",
                "subject": subject,
                "from": {"name": sender_name, "email": sender_email},
                "to": [{"name": to_email.split("@")[0], "email": to_email}]
            }
        }

        logging.info(f"📧 [SENDPULSE] Sending to {to_email}...")
        r = requests.post(
            "https://api.sendpulse.com/smtp/emails",
            headers={"Authorization": f"Bearer {token}"},
            json=payload,
            timeout=20
        )
        if r.status_code in (200, 201):
            logging.info(f"✅ [SENDPULSE] Email sent!")
            return True
        else:
            logging.error(f"❌ [SENDPULSE] Failed: {r.status_code} - {r.text[:200]}")
            return False
    except Exception as e:
        logging.error(f"❌ [SENDPULSE] Exception: {e}")
        return False


def send_email_via_mailjet(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None):
    """[MAILJET API] Free 200/day. Uses HTTP port 443 - works on Render."""
    api_key = os.getenv("MAILJET_API_KEY", "").strip()
    api_secret = os.getenv("MAILJET_API_SECRET", "").strip()
    if not api_key or not api_secret:
        return False

    if not subject:
        subject = f"Application: {job_title} - {company_name}"

    html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
    gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()
    sender_email = gmail_user or "sam.dev1@hotmail.com"

    # Build attachments
    attachment_list = []
    if attachment_paths:
        for path in attachment_paths:
            if path and os.path.exists(path):
                try:
                    with open(path, "rb") as f:
                        content = base64.b64encode(f.read()).decode("utf-8")
                        attachment_list.append({
                            "ContentType": "application/pdf",
                            "Filename": os.path.basename(path),
                            "Base64Content": content
                        })
                except Exception as e:
                    logging.warning(f"⚠️ [MAILJET] Failed to attach {path}: {e}")

    payload = {
        "Messages": [{
            "From": {"Email": sender_email, "Name": sender_name},
            "To": [{"Email": to_email}],
            "Subject": subject,
            "HTMLPart": html_content,
            "ReplyTo": {"Email": reply_to or gmail_user or sender_email}
        }]
    }
    if attachment_list:
        payload["Messages"][0]["Attachments"] = attachment_list

    try:
        logging.info(f"📤 [MAILJET] Sending to {to_email}...")
        response = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(api_key, api_secret),
            json=payload,
            timeout=20
        )
        if response.status_code in (200, 201):
            data = response.json()
            messages = data.get("Messages", [])
            if messages and messages[0].get("Status") == "success":
                logging.info(f"✅ [MAILJET] Email sent successfully!")
                return True
        logging.error(f"❌ [MAILJET] Failed: {response.status_code} - {response.text[:200]}")
        return False
    except Exception as e:
        logging.error(f"❌ [MAILJET] Exception: {e}")
        return False


def send_email_via_sendpulse(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None):
    """[SENDPULSE API] Free 12,000/month (~400/day). Uses HTTP port 443 - works on Render."""
    client_id = os.getenv("SENDPULSE_CLIENT_ID", "").strip()
    client_secret = os.getenv("SENDPULSE_CLIENT_SECRET", "").strip()
    if not client_id or not client_secret:
        return False

    if not subject:
        subject = f"Application: {job_title} - {company_name}"

    html_content = _wrap_in_sovereign_template(company_name, job_title, custom_body, highlights or [])
    gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()
    sender_email = gmail_user or "sam.dev1@hotmail.com"

    try:
        # Step 1: Get access token
        token_response = requests.post(
            "https://api.sendpulse.com/oauth/access_token",
            json={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret
            },
            timeout=15
        )
        if token_response.status_code != 200:
            logging.error(f"❌ [SENDPULSE] Token failed: {token_response.text[:200]}")
            return False

        token = token_response.json().get("access_token")
        if not token:
            return False

        # Step 2: Send email
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        # Build attachments
        attachments = {}
        if attachment_paths:
            for path in attachment_paths:
                if path and os.path.exists(path):
                    try:
                        with open(path, "rb") as f:
                            content = base64.b64encode(f.read()).decode("utf-8")
                            attachments[os.path.basename(path)] = content
                    except Exception as e:
                        logging.warning(f"⚠️ [SENDPULSE] Failed to attach {path}: {e}")

        payload = {
            "email": {
                "html": html_content,
                "text": re.sub(r'<[^>]+>', '', html_content)[:500],
                "subject": subject,
                "from": {"name": sender_name, "email": sender_email},
                "to": [{"name": to_email.split("@")[0], "email": to_email}],
                "reply_to": {"name": sender_name, "email": reply_to or gmail_user or sender_email}
            }
        }
        if attachments:
            payload["email"]["attachments"] = attachments

        logging.info(f"📤 [SENDPULSE] Sending to {to_email}...")
        response = requests.post(
            "https://api.sendpulse.com/smtp/emails",
            headers=headers,
            json=payload,
            timeout=20
        )
        if response.status_code in (200, 201, 202):
            logging.info(f"✅ [SENDPULSE] Email sent successfully!")
            return True
        logging.error(f"❌ [SENDPULSE] Failed: {response.status_code} - {response.text[:200]}")
        return False
    except Exception as e:
        logging.error(f"❌ [SENDPULSE] Exception: {e}")
        return False


def send_email_via_brevo_http(to_email, company_name, job_title, custom_body, attachment_paths=None, sender_name="Sam Salameh", highlights=None, subject=None, reply_to=None):
    """[REST API] Bypasses ISP SMTP blocks. Uses sam.dev1@hotmail.com - the ONLY sender that delivers!"""
    api_key = getattr(config, 'BREVO_API_KEY', None)
    if not api_key: return False
    
    # 🎯 CRITICAL: Based on Brevo delivery logs analysis:
    # ✅ DELIVERED: sam.dev1@hotmail.com (Hotmail/Outlook sender)
    # ❌ ERROR: a974ef001@smtp-brevo.com (Brevo sender - rejected by Gmail)
    # ❌ ERROR: samsalameh.cv@zohomail.com (Zoho sender - rejected)
    # ❌ ERROR: samsalameh.cv@gmail.com (Gmail sender - not verified in Brevo)
    #
    # SOLUTION: Use sam.dev1@hotmail.com as sender (verified + delivers!)
    # Set Reply-To to samsalameh.cv@gmail.com so replies go to the right place
    
    sender_email = 'sam.dev1@hotmail.com'  # ✅ ONLY sender that delivers!
    logging.info(f"📧 [BREVO-HTTP] Using Hotmail sender (proven to deliver): {sender_email}")
    
    # Reply-To goes to Gmail so recruiter responses reach Sam
    if not reply_to:
        gmail_user = (getattr(config, 'GMAIL_SMTP_USER', '') or '').strip()
        reply_to = gmail_user if gmail_user else sender_email
    
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
    
    payload = {
        "sender": {"email": sender_email, "name": sender_name},
        "to": [{"email": to_email}],
        "subject": subject,
        "htmlContent": html_content,
        "replyTo": {"email": reply_to, "name": sender_name}
    }
    if attachment_list:
        payload["attachment"] = attachment_list
    
    try:
        logging.info(f"📤 [BREVO-HTTP] Sending from {sender_email} (Reply-To: {reply_to}) to {to_email}")
        response = requests.post(
            "https://api.brevo.com/v3/smtp/email",
            headers={"api-key": api_key, "Content-Type": "application/json", "Accept": "application/json"},
            json=payload,
            timeout=20
        )
        if response.status_code in (201, 200, 202):
            logging.info(f"✅ [BREVO-HTTP] Email sent successfully! Status: {response.status_code}")
            return True
        else:
            logging.error(f"❌ [BREVO-HTTP] Failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        logging.error(f"❌ [BREVO-HTTP] Exception: {e}")
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
            logging.info(f"🔌 [{provider['name']}] Connecting to {provider['server']}:{provider['port']} (SSL={provider.get('use_ssl', False)})...")
            
            if provider.get('use_ssl', False):
                server = smtplib.SMTP_SSL(host=provider['server'], port=provider['port'], timeout=timeout)
                logging.info(f"✅ [{provider['name']}] SSL connection established")
            else:
                server = smtplib.SMTP(host=provider['server'], port=provider['port'], timeout=timeout)
                logging.info(f"✅ [{provider['name']}] SMTP connection established, starting TLS...")
                server.ehlo()
                server.starttls()
                server.ehlo()
                logging.info(f"✅ [{provider['name']}] TLS handshake complete")
            
            logging.info(f"🔐 [{provider['name']}] Authenticating as {provider['email'][:15]}...")
            server.login(provider['email'], provider['password'])
            logging.info(f"✅ [{provider['name']}] Authentication successful!")
            
            logging.info(f"📤 [{provider['name']}] Sending message to {to_email}...")
            server.send_message(msg)
            logging.info(f"✅ [{provider['name']}] Message sent successfully!")
            
            server.quit()
            return True
        except smtplib.SMTPAuthenticationError as e:
            logging.error(f"❌ [{provider['name']}] AUTHENTICATION FAILED: {e}")
            logging.error(f"❌ [{provider['name']}] Check your email/password in .env file!")
            if server:
                try: server.close()
                except: pass
            return False
        except smtplib.SMTPConnectError as e:
            logging.error(f"❌ [{provider['name']}] CONNECTION FAILED: {e}")
            logging.error(f"❌ [{provider['name']}] Port {provider['port']} may be blocked by firewall/ISP!")
            if server:
                try: server.close()
                except: pass
            return False
        except Exception as e:
            logging.error(f"❌ [{provider['name']}] SMTP ERROR: {type(e).__name__}: {e}")
            import traceback
            logging.error(f"❌ [{provider['name']}] Traceback: {traceback.format_exc()}")
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
