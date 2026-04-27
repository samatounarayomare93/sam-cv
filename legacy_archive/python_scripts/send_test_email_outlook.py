"""
SAM TEST EMAIL - OUTLOOK SMTP (FIXES JUNK PROBLEM)
===================================================
Send email using Outlook SMTP directly - emails will go to INBOX, not junk
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import email.utils

# Outlook SMTP Configuration
SENDER_EMAIL = "sam.dev1@outlook.com"
SENDER_PASSWORD = "your-outlook-password"  # Replace with your actual Outlook password
SENDER_NAME = "Sam Salameh"
TEST_EMAIL = "sam.dev1@hotmail.com"

# ORIGINAL DARK THEME TEMPLATE
EMAIL_BODY_TEMPLATE = """
<div style="background-color: #0b0f19; padding: 40px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table width="100%" max-width="650" align="center" cellpadding="0" cellspacing="0" style="max-width: 650px; margin: 0 auto; background-color: #111827; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);">

    <tr>
      <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 40px 30px; text-align: center;">
        <div style="display: inline-block; width: 60px; height: 60px; background-color: #06b6d4; border-radius: 30px; line-height: 60px; color: #ffffff; font-size: 24px; font-weight: bold; margin-bottom: 15px; box-shadow: 0 4px 10px rgba(6, 182, 212, 0.4);">
          <span style="display: block; margin-top: 15px;">RC</span>
        </div>
        <div style="font-size: 13px; letter-spacing: 4px; color: #94a3b8; text-transform: uppercase; margin-bottom: 5px;">Executive Candidacy</div>
        <div style="font-size: 28px; font-weight: 800; color: #ffffff; letter-spacing: -0.5px; line-height: 1.2;">SAM CORDAHI</div>
      </td>
    </tr>

    <tr>
      <td height="4" style="background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);"></td>
    </tr>

    <tr>
      <td style="padding: 40px 35px;">
        <p style="font-size: 17px; margin-top: 0; color: #f8fafc;">Dear <strong>Hiring Manager</strong>,</p>
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">I am formally reaching out to express my high-level interest in the <span style="color: #06b6d4; font-weight: 600;">HR & Operations Manager</span> position. With a robust track record in HR administration and customer operations, I specialize in architecting workflows that prioritize precision, compliance, and exceptional service delivery.</p>

        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1;">My methodology is built specifically for organizations that focus heavily on <strong>automation, KPIs, and scaling corporate culture</strong>. Here are the precise competencies I bring to the table:</p>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin: 30px 0;">
          <tr>
            <td style="padding: 20px; background-color: #1e293b; border-radius: 12px; border-left: 4px solid #06b6d4;">
              <span style="font-size: 14px; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 1px;">01. Operations Lifecycle</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.6;">Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with <span style="color: #4ade80;">100% data integrity</span>.</span>
            </td>
          </tr>
          <tr><td height="15"></td></tr>
          <tr>
            <td style="padding: 20px; background-color: #1e293b; border-radius: 12px; border-left: 4px solid #3b82f6;">
              <span style="font-size: 14px; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 1px;">02. Service & Retention</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.6;">A track record of resolving 50+ daily complex technical and billing inquiries while maintaining strict SLA compliance.</span>
            </td>
          </tr>
          <tr><td height="15"></td></tr>
          <tr>
            <td style="padding: 20px; background-color: #1e293b; border-radius: 12px; border-left: 4px solid #8b5cf6;">
              <span style="font-size: 14px; font-weight: 700; color: #ffffff; text-transform: uppercase; letter-spacing: 1px;">03. Workflow Optimization</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.6;">Experience in standardizing onboarding templates and operational diagnostics to significantly reduce departmental overhead.</span>
            </td>
          </tr>
        </table>

        <div style="padding: 20px 25px; background-color: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 12px; margin-bottom: 30px; text-align: center;">
          <p style="margin: 0; font-style: italic; color: #e2e8f0; font-size: 16px; line-height: 1.5;">
            "I am looking to bring rigorous accountability, structured scaling, and high-conversion problem-solving to your team."
          </p>
        </div>

        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1; margin-bottom: 0;">I have attached <b>My CV</b> for your comprehensive review.</p>
      </td>
    </tr>

    <tr>
      <td style="background-color: #0f172a; padding: 40px 30px; text-align: center; border-top: 1px solid #1e293b;">
        <a href="https://www.linkedin.com/in/sam-cordahi/" style="display: inline-block; padding: 14px 32px; background-color: #06b6d4; color: #ffffff; text-decoration: none; border-radius: 30px; font-weight: bold; font-size: 14px; letter-spacing: 1.5px; box-shadow: 0 4px 12px rgba(6, 182, 212, 0.3);">
          VIEW LINKEDIN PORTFOLIO
        </a>

        <div style="margin-top: 30px; margin-bottom: 10px;">
          <a href="mailto:sam.dev1@outlook.com" style="color: #94a3b8; font-size: 14px; text-decoration: none;">sam.dev1@outlook.com</a>
          <span style="color: #334155; margin: 0 10px;">|</span>
          <a href="tel:+96176005412" style="color: #94a3b8; font-size: 14px; text-decoration: none;">+961 76 005 412</a>
        </div>

        <div style="font-size: 12px; color: #475569; margin-top: 20px;">
          HR & Customer Operations Specialist
        </div>
      </td>
    </tr>
  </table>
</div>
"""

def send_email_via_outlook():
    """Send email using Outlook SMTP - this will go to INBOX, not junk"""

    print("="*70)
    print("SAM EMAIL - OUTLOOK SMTP (FIXES JUNK)")
    print("="*70)

    # Create message
    msg = MIMEMultipart('alternative')
    msg['From'] = f'"{SENDER_NAME}" <{SENDER_EMAIL}>'
    msg['To'] = TEST_EMAIL
    msg['Subject'] = "Application: HR & Operations Manager - Sam Salameh"

    # Professional headers
    msg['Message-ID'] = email.utils.make_msgid(domain='outlook.com')
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Reply-To'] = SENDER_EMAIL
    msg['X-Mailer'] = 'Microsoft Outlook 16.0'

    # Plain text version
    plain_text = """SAM CORDAHI
HR & Customer Operations Specialist

Dear Hiring Manager,

I am formally reaching out to express my high-level interest in the HR & Operations Manager position.

Key Competencies:
01. Operations Lifecycle - Recruitment logistics, employee records, payroll with 100% data integrity.
02. Service & Retention - 50+ daily technical inquiries with SLA compliance.
03. Workflow Optimization - Standardizing onboarding templates and operational diagnostics.

I have attached my CV for your comprehensive review.

Best regards,
Sam Salameh

Contact:
sam.dev1@outlook.com | +961 76 005 412
linkedin.com/in/sam-cordahi
"""

    # Attach both versions
    msg.attach(MIMEText(plain_text, 'plain', 'utf-8'))
    msg.attach(MIMEText(EMAIL_BODY_TEMPLATE, 'html', 'utf-8'))

    print(f"\n[FROM] {SENDER_NAME} <{SENDER_EMAIL}>")
    print(f"[TO] {TEST_EMAIL}")
    print("\n[SENDING] Using Outlook SMTP directly...")

    try:
        # Connect to Outlook SMTP
        server = smtplib.SMTP('smtp-mail.outlook.com', 587, timeout=30)
        server.ehlo()
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()

        print("\n" + "="*70)
        print("[SUCCESS] Email sent via Outlook SMTP!")
        print("[INBOX] Should go to INBOX, not junk (proper authentication)")
        print("="*70)
        print(f"\nCheck your inbox: {TEST_EMAIL}")
        print("\nWhy this works:")
        print("  - Uses Outlook's own SMTP server")
        print("  - Properly authenticated (your actual Outlook account)")
        print("  - SPF/DKIM/DMARC all valid (Outlook's own domain)")
        print("  - No spoofing detected")
        print("\nOriginal dark theme features:")
        print("  - Dark blue background (#0b0f19)")
        print("  - RC circular avatar")
        print("  - Rainbow divider (cyan-blue-purple)")
        print("  - 3 colored competency cards")
        print("  - Quote box with teal border")
        print("  - LinkedIn button")
        print("="*70)
        return True

    except smtplib.SMTPAuthenticationError:
        print("\n[ERROR] Authentication failed!")
        print("Please replace 'your-outlook-password' with your actual Outlook password")
        print("Or use an App Password if you have 2FA enabled on your Outlook account")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    success = send_email_via_outlook()
    sys.exit(0 if success else 1)