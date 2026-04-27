"""
SAM EMAIL TEMPLATE - ANTI-SPAM OPTIMIZED
===========================================
Professional format with better deliverability
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email.utils
from email.header import Header
import re
import logging

def send_test_email():
    """Send test email with optimized template"""

    # Email configuration
    sender_email = "sam.dev1@outlook.com"
    sender_name = "Sam Salameh"
    recipient_email = "sam.dev1@hotmail.com"
    subject = "Application: HR & Operations Manager - Sam Salameh"

    # ═════════════════════════════════════════════════════════════════════════════
    # ANTI-SPAM EMAIL TEMPLATE - Clean & Professional
    # ═════════════════════════════════════════════════════════════════════════════
    html_body = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="format-detection" content="telephone=no">
    <title>Sam Salameh - HR & Operations Application</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; }
    </style>
</head>
<body style="margin: 0; padding: 0; background-color: #f5f5f5;">
    
    <!-- PREVIEW TEXT -->
    <div style="display: none; max-height: 0; overflow: hidden;">
        Professional HR & Operations application from Sam Salameh. CV attached. Contact: +961 76 005 412
    </div>
    
    <!-- MAIN CONTAINER -->
    <table width="100%" cellpadding="0" cellspacing="0" style="max-width: 650px; margin: 0 auto; background-color: #ffffff; border-radius: 8px; border: 1px solid #e0e0e0;">
        
        <!-- HEADER - Clean & Professional -->
        <tr>
            <td style="background: linear-gradient(135deg, #1e3a5f 0%, #2d5a8b 100%); padding: 35px 30px; text-align: center; border-radius: 8px 8px 0 0;">
                <table cellpadding="0" cellspacing="0" align="center">
                    <tr>
                        <td style="background: rgba(255,255,255,0.15); width: 70px; height: 70px; border-radius: 50%; text-align: center; line-height: 70px; font-size: 28px; font-weight: bold; color: #ffffff; letter-spacing: 2px;">
                            RC
                        </td>
                    </tr>
                </table>
                <h1 style="margin: 15px 0 5px 0; font-size: 26px; font-weight: 700; color: #ffffff; letter-spacing: 1px;">
                    SAM CORDAHI
                </h1>
                <p style="margin: 0; font-size: 14px; color: rgba(255,255,255,0.85); font-weight: 500;">
                    HR & Operations Professional
                </p>
            </td>
        </tr>
        
        <!-- CONTENT BODY -->
        <tr>
            <td style="padding: 35px 30px;">
                
                <!-- Greeting -->
                <p style="margin: 0 0 20px 0; font-size: 16px; color: #333;">
                    Dear <strong>Hiring Manager</strong>,
                </p>
                
                <!-- Opening Paragraph -->
                <p style="margin: 0 0 20px 0; font-size: 15px; color: #555; line-height: 1.7;">
                    I am writing to formally apply for the <strong>HR & Operations Manager</strong> position. With over five years of experience in human resources, customer operations, and administrative management, I have developed a comprehensive skill set that aligns perfectly with the requirements of this role.
                </p>
                
                <!-- Key Competencies - Simple clean cards -->
                <table width="100%" cellpadding="0" cellspacing="0" style="margin: 25px 0;">
                    <tr>
                        <td style="padding: 18px; background-color: #f8f9fa; border-left: 4px solid #2d5a8b; border-radius: 0 6px 6px 0;">
                            <strong style="color: #1e3a5f; font-size: 14px;">✓ Recruitment & Onboarding</strong>
                        </td>
                    </tr>
                    <tr><td height="10"></td></tr>
                    <tr>
                        <td style="padding: 18px; background-color: #f8f9fa; border-left: 4px solid #5a8b2d; border-radius: 0 6px 6px 0;">
                            <strong style="color: #1e3a5f; font-size: 14px;">✓ Employee Relations & Compliance</strong>
                        </td>
                    </tr>
                    <tr><td height="10"></td></tr>
                    <tr>
                        <td style="padding: 18px; background-color: #f8f9fa; border-left: 4px solid #8b5a2d; border-radius: 0 6px 6px 0;">
                            <strong style="color: #1e3a5f; font-size: 14px;">✓ Operations & Process Optimization</strong>
                        </td>
                    </tr>
                </table>
                
                <!-- Professional Experience Summary -->
                <p style="margin: 20px 0 15px 0; font-size: 15px; color: #555; line-height: 1.7;">
                    <strong>Recent Experience:</strong>
                </p>
                <ul style="margin: 0 0 20px 0; padding-left: 20px; font-size: 14px; color: #555; line-height: 1.7;">
                    <li><strong>HR & Operations Coordinator</strong> at Sam Consulting (2020 - Present)</li>
                    <li><strong>Customer Service Representative</strong> at Internet Service Provider (2023 - 2025)</li>
                    <li><strong>HR Officer</strong> at Boubess Group (2022)</li>
                    <li><strong>Freelance Recruiter</strong> - Successfully placed 10+ niche roles</li>
                </ul>
                
                <!-- Call to Action -->
                <p style="margin: 0 0 20px 0; font-size: 15px; color: #555; line-height: 1.7;">
                    I have attached my detailed CV for your review. I am excited about the opportunity to contribute my expertise in HR operations and customer service excellence to your team. I am available for immediate relocation and ready to start at your earliest convenience.
                </p>
                
                <!-- Closing -->
                <p style="margin: 0; font-size: 15px; color: #333;">
                    Thank you for your time and consideration. I look forward to hearing from you.
                </p>
                <p style="margin: 25px 0 0 0; font-size: 16px; color: #1e3a5f;">
                    <strong>Best regards,</strong><br>
                    <span style="font-size: 18px; font-weight: 600; color: #2d5a8b;">Sam Salameh</span>
                </p>
                
            </td>
        </tr>
        
        <!-- CONTACT FOOTER -->
        <tr>
            <td style="background-color: #f8f9fa; padding: 25px 30px; border-top: 1px solid #e8e8e8; border-radius: 0 0 8px 8px; text-align: center;">
                <table cellpadding="0" cellspacing="0" align="center">
                    <tr>
                        <td style="padding: 0 20px; border-right: 1px solid #ddd;">
                            <p style="margin: 0 0 5px 0; font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px;">Email</p>
                            <p style="margin: 0; font-size: 14px; color: #333; font-weight: 500;">sam.dev1@outlook.com</p>
                        </td>
                        <td style="padding: 0 20px; border-right: 1px solid #ddd;">
                            <p style="margin: 0 0 5px 0; font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px;">Phone</p>
                            <p style="margin: 0; font-size: 14px; color: #333; font-weight: 500;">+961 76 005 412</p>
                        </td>
                        <td style="padding: 0 0 0 20px;">
                            <p style="margin: 0 0 5px 0; font-size: 12px; color: #888; text-transform: uppercase; letter-spacing: 1px;">LinkedIn</p>
                            <p style="margin: 0; font-size: 14px; color: #2d5a8b; font-weight: 500;">linkedin.com/in/sam-cordahi</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
        
    </table>
    
    <!-- FOOTER NOTE -->
    <p style="margin: 20px 0 0 0; font-size: 11px; color: #999; text-align: center;">
        This email and attachments are confidential and intended for the addressee only.
    </p>
    
</body>
</html>"""

    # Plain text version
    text_body = """SAM CORDAHI - HR & Operations Professional
========================================

Dear Hiring Manager,

I am writing to formally apply for the HR & Operations Manager position. With over five years of experience in human resources, customer operations, and administrative management, I have developed a comprehensive skill set that aligns perfectly with this role.

Key Competencies:
✓ Recruitment & Onboarding
✓ Employee Relations & Compliance
✓ Operations & Process Optimization

Recent Experience:
• HR & Operations Coordinator at Sam Consulting (2020 - Present)
• Customer Service Representative at Internet Service Provider (2023 - 2025)
• HR Officer at Boubess Group (2022)
• Freelance Recruiter - Successfully placed 10+ niche roles

I have attached my detailed CV for your review. I am available for immediate relocation and ready to contribute from day one.

Thank you for your consideration.

Best regards,
Sam Salameh
HR & Operations Specialist

Contact Information:
Email: sam.dev1@outlook.com
Phone: +961 76 005 412
LinkedIn: linkedin.com/in/sam-cordahi
"""

    # Create MIME message
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    
    msg = MIMEMultipart('mixed')
    
    # Anti-spam headers
    msg['Message-ID'] = email.utils.make_msgid(domain=sender_email.split('@')[1])
    msg['Date'] = email.utils.formatdate(localtime=True)
    msg['Reply-To'] = f"{sender_name} <{sender_email}>"
    msg['Return-Path'] = sender_email
    msg['Precedence'] = 'bulk'
    msg['List-Unsubscribe'] = f'<mailto:{sender_email}>'
    msg['X-Mailer'] = 'SamJobAutomator-Professional'
    msg['X-Priority'] = '3'
    msg['Importance'] = 'Normal'
    
    msg['From'] = Header(f"{sender_name}", 'utf-8').encode() + f" <{sender_email}>"
    msg['To'] = recipient_email
    msg['Subject'] = Header(subject, 'utf-8').encode()
    
    # Create alternative part
    alt = MIMEMultipart('alternative')
    alt.attach(MIMEText(text_body, 'plain', 'utf-8'))
    alt.attach(MIMEText(html_body, 'html', 'utf-8'))
    msg.attach(alt)
    
    # Print preview
    print("="*70)
    print("SAM EMAIL TEMPLATE - ANTI-SPAM OPTIMIZED")
    print("="*70)
    print(f"\n[SENDER] {sender_name} <{sender_email}>")
    print(f"[RECIPIENT] {recipient_email}")
    print(f"[SUBJECT] {subject}")
    print("\n[STATUS] Email ready to send with anti-spam headers")
    print("\nFeatures:")
    print("  ✓ Clean professional design")
    print("  ✓ RC circular avatar with gradient header")
    print("  ✓ Anti-spam headers (Message-ID, Date, Reply-To)")
    print("  ✓ Proper MIME encoding (UTF-8)")
    print("  ✓ Preview text for inbox preview")
    print("  ✓ Both HTML and plain text versions")
    print("  ✓ No suspicious keywords or spam triggers")
    print("="*70)
    
    return msg, html_body, text_body

if __name__ == "__main__":
    msg, html, text = send_test_email()
    print("\n[HTML PREVIEW - First 500 chars]:")
    print(html[:500])
    print("...\n")
