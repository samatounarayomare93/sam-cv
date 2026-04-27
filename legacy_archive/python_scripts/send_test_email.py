"""
SAM TEST EMAIL - OUTLOOK SMTP WITH CV ATTACHMENT
================================================
Send email via Outlook SMTP - goes to INBOX, not junk
Includes CV attachment properly
"""

import os
import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.header import Header
import email.utils

# Outlook SMTP Configuration
SENDER_EMAIL = "sam.dev1@outlook.com"
SENDER_PASSWORD = "Sam123456!"
SENDER_NAME = "Sam Salameh"
TEST_EMAIL = "sam.dev1@hotmail.com"

# Original dark theme template (enhanced)
EMAIL_BODY_TEMPLATE = """
<div style="background-color: #0b0f19; padding: 40px 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;">
  <table width="100%" max-width="650" align="center" cellpadding="0" cellspacing="0" style="max-width: 650px; margin: 0 auto; background-color: #111827; border-radius: 16px; overflow: hidden; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.5);">

    <tr>
      <td style="background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); padding: 45px 30px; text-align: center;">
        <div style="display: inline-block; width: 65px; height: 65px; background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%); border-radius: 50%; line-height: 65px; color: #ffffff; font-size: 26px; font-weight: 800; margin-bottom: 18px; box-shadow: 0 0 30px rgba(6, 182, 212, 0.5);">
          <span style="display: block; margin-top: 18px;">RC</span>
        </div>
        <div style="font-size: 12px; letter-spacing: 4px; color: #94a3b8; text-transform: uppercase; margin-bottom: 6px; font-weight: 500;">Executive Candidacy</div>
        <div style="font-size: 32px; font-weight: 800; color: #ffffff; letter-spacing: 1px; line-height: 1.2;">SAM CORDAHI</div>
        <div style="font-size: 13px; color: #06b6d4; margin-top: 8px; font-weight: 500;">HR & Customer Operations Specialist</div>
      </td>
    </tr>

    <tr>
      <td height="5" style="background: linear-gradient(90deg, #06b6d4 0%, #3b82f6 50%, #8b5cf6 100%);"></td>
    </tr>

    <tr>
      <td style="padding: 40px 35px;">
        <p style="font-size: 18px; margin-top: 0; margin-bottom: 15px; color: #f8fafc;">Dear <strong>Hiring Manager</strong>,</p>
        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1; margin-bottom: 20px;">I am formally reaching out to express my high-level interest in the <span style="color: #06b6d4; font-weight: 700;">HR & Operations Manager</span> position. With a robust track record in HR administration and customer operations, I specialize in architecting workflows that prioritize precision, compliance, and exceptional service delivery.</p>

        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1; margin-bottom: 25px;">My methodology is built specifically for organizations that focus heavily on <strong style="color: #e2e8f0;">automation, KPIs, and scaling corporate culture</strong>. Here are the precise competencies I bring to the table:</p>

        <table width="100%" cellpadding="0" cellspacing="0" style="margin: 25px 0;">
          <tr>
            <td style="padding: 22px; background-color: #1e293b; border-radius: 12px; border-left: 5px solid #06b6d4;">
              <span style="font-size: 13px; font-weight: 700; color: #06b6d4; text-transform: uppercase; letter-spacing: 1.5px;">01. Operations Lifecycle</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.7; margin-top: 8px; display: block;">Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with <span style="color: #4ade80; font-weight: 600;">100% data integrity</span>.</span>
            </td>
          </tr>
          <tr><td height="12"></td></tr>
          <tr>
            <td style="padding: 22px; background-color: #1e293b; border-radius: 12px; border-left: 5px solid #3b82f6;">
              <span style="font-size: 13px; font-weight: 700; color: #3b82f6; text-transform: uppercase; letter-spacing: 1.5px;">02. Service & Retention</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.7; margin-top: 8px; display: block;">A track record of resolving <strong style="color: #e2e8f0;">50+ daily complex technical and billing inquiries</strong> while maintaining strict SLA compliance.</span>
            </td>
          </tr>
          <tr><td height="12"></td></tr>
          <tr>
            <td style="padding: 22px; background-color: #1e293b; border-radius: 12px; border-left: 5px solid #8b5cf6;">
              <span style="font-size: 13px; font-weight: 700; color: #8b5cf6; text-transform: uppercase; letter-spacing: 1.5px;">03. Workflow Optimization</span><br>
              <span style="font-size: 14px; color: #94a3b8; line-height: 1.7; margin-top: 8px; display: block;">Experience in standardizing onboarding templates and operational diagnostics to significantly <strong style="color: #e2e8f0;">reduce departmental overhead by 25%</strong>.</span>
            </td>
          </tr>
        </table>

        <div style="padding: 22px 28px; background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 12px; margin: 25px 0; text-align: center;">
          <p style="margin: 0; font-style: italic; color: #e2e8f0; font-size: 15px; line-height: 1.6;">
            "I am looking to bring rigorous accountability, structured scaling, and high-conversion problem-solving to your team."
          </p>
        </div>

        <div style="text-align: center; margin: 20px 0 25px 0;">
          <span style="display: inline-block; padding: 10px 20px; background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 25px; color: #4ade80; font-size: 13px; font-weight: 600;">
            &#10003; Available Immediately for Relocation
          </span>
        </div>

        <p style="font-size: 15px; line-height: 1.8; color: #cbd5e1; margin-bottom: 0;">I have attached my <strong style="color: #ffffff;">CV</strong> for your comprehensive review. Please find it attached to this email.</p>
      </td>
    </tr>

    <tr>
      <td style="background-color: #0f172a; padding: 35px 30px; text-align: center; border-top: 1px solid #1e293b;">
        <a href="https://www.linkedin.com/in/sam-cordahi/" style="display: inline-block; padding: 14px 35px; background: linear-gradient(135deg, #06b6d4 0%, #0284c7 100%); color: #ffffff; text-decoration: none; border-radius: 30px; font-weight: 700; font-size: 13px; letter-spacing: 1.5px; box-shadow: 0 4px 15px rgba(6, 182, 212, 0.4);">
          VIEW LINKEDIN PROFILE
        </a>

        <div style="margin-top: 28px; padding-top: 20px; border-top: 1px solid #1e293b;">
          <div style="margin-bottom: 10px;">
            <a href="mailto:sam.dev1@outlook.com" style="color: #94a3b8; font-size: 14px; text-decoration: none; margin: 0 12px;">sam.dev1@outlook.com</a>
            <span style="color: #334155; margin: 0 5px;">|</span>
            <a href="tel:+96176005412" style="color: #94a3b8; font-size: 14px; text-decoration: none; margin: 0 12px;">+961 76 005 412</a>
          </div>
          <div style="font-size: 11px; color: #475569; letter-spacing: 1px; text-transform: uppercase;">
            HR & Customer Operations Specialist
          </div>
        </div>
      </td>
    </tr>
  </table>
</div>
"""

def send_email_with_cv():
    """Send email via Outlook SMTP with CV attachment"""

    print("="*70)
    print("SAM EMAIL - OUTLOOK SMTP WITH CV ATTACHMENT")
    print("="*70)

    # Create message
    msg = MIMEMultipart('mixed')
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

Please find my CV attached for your comprehensive review.

Best regards,
Sam Salameh
+961 76 005 412
sam.dev1@outlook.com
linkedin.com/in/sam-cordahi

Available Immediately for Relocation
"""

    # Create alternative part (text + html)
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(plain_text, 'plain', 'utf-8'))
    alt.attach(MIMEText(EMAIL_BODY_TEMPLATE, 'html', 'utf-8'))
    msg.attach(alt)

    # Attach CV file
    cv_path = "Sam_Cordahi_CV.html"
    if os.path.exists(cv_path):
        try:
            with open(cv_path, 'rb') as f:
                cv_content = f.read()
            cv_part = MIMEApplication(cv_content, Name='Sam_Cordahi_CV.html', _subtype='html')
            cv_part['Content-Disposition'] = 'attachment; filename="Sam_Cordahi_CV.html"'
            cv_part['Content-ID'] = '<cv_attachment>'
            msg.attach(cv_part)
            print(f"\n[CV ATTACHED] {cv_path}")
        except Exception as e:
            print(f"\n[CV ERROR] Could not attach CV: {e}")
    else:
        print(f"\n[CV WARNING] CV file not found: {cv_path}")

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
        print("[INBOX] Should go to INBOX (not junk)")
        print("[ATTACHMENT] CV file attached")
        print("="*70)
        print(f"\nCheck inbox: {TEST_EMAIL}")
        print("\nOriginal dark theme features:")
        print("  - Dark blue background (#0b0f19)")
        print("  - RC circular avatar")
        print("  - Rainbow divider (cyan-blue-purple)")
        print("  - 3 colored competency cards")
        print("  - Quote box with teal border")
        print("  - LinkedIn button")
        print("  - Availability badge")
        print("="*70)
        return True

    except smtplib.SMTPAuthenticationError:
        print("\n[ERROR] Authentication failed!")
        print("Please check your Outlook password")
        return False
    except Exception as e:
        print(f"\n[ERROR] {e}")
        return False

if __name__ == "__main__":
    success = send_email_with_cv()
    sys.exit(0 if success else 1)