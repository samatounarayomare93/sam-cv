#!/usr/bin/env python3
"""
🧪 TEST: Inline CV in Email Body
The CV will be displayed directly in the email (no attachment needed)
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

from core.smtp_engine import send_email
import logging

logging.basicConfig(level=logging.INFO)

# Read the CV HTML file
with open('Sam_Salameh_CV.html', 'r', encoding='utf-8') as f:
    cv_html = f.read()

# Prepare email
recipient = 'samsalameh.cv@gmail.com'
company_name = 'Future Tech Industries'
job_title = 'Lead Automation Engineer'
strike_id = 'STRIKE-2771'

# Custom body with inline CV
custom_body = f"""
<div style="font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto;">
    <p style="font-size: 16px; color: #333; margin-bottom: 20px;">
        Dear {company_name} Hiring Team,
    </p>
    
    <p style="font-size: 15px; color: #555; line-height: 1.6; margin-bottom: 20px;">
        I am formally reaching out to express my high-level interest in the <strong>{job_title}</strong> position.
    </p>
    
    <p style="font-size: 15px; color: #555; line-height: 1.6; margin-bottom: 30px;">
        Please find my complete CV below for your review.
    </p>
    
    <hr style="border: none; border-top: 2px solid #3498db; margin: 30px 0;">
    
    <!-- INLINE CV -->
    {cv_html}
    
    <hr style="border: none; border-top: 2px solid #3498db; margin: 30px 0;">
    
    <p style="font-size: 15px; color: #555; line-height: 1.6; margin-top: 30px;">
        I look forward to discussing how my expertise can contribute to {company_name}'s success.
    </p>
    
    <p style="font-size: 15px; color: #555; margin-top: 20px;">
        Best regards,<br>
        <strong>Sam Salameh</strong><br>
        Senior Network Engineer<br>
        +961 70 841 1009<br>
        <a href="https://linkedin.com/in/sam-salameh" style="color: #3498db;">LinkedIn Profile</a>
    </p>
</div>
"""

print("\n" + "="*70)
print("📧 SENDING EMAIL WITH INLINE CV")
print("="*70)
print(f"\n📬 To: {recipient}")
print(f"📧 Subject: Application: {job_title} - {company_name} [{strike_id}]")
print(f"📄 CV: Displayed directly in email body (no attachment)")
print(f"\n⏳ Sending...\n")

# Send email with inline CV (no attachments)
result = send_email(
    to_email=recipient,
    company_name=company_name,
    job_title=job_title,
    custom_body=custom_body,
    platform='test',
    mission_type='test',
    attachment_paths=[],  # No attachments
    strike_id=strike_id
)

print("\n" + "="*70)
if result:
    print("✅ SUCCESS! Email sent with inline CV!")
    print(f"\n📱 CHECK YOUR INBOX: {recipient}")
    print("\n🔍 The CV should be displayed directly in the email body")
    print("   - No need to download anything")
    print("   - No need to click any links")
    print("   - Just scroll down in the email to see the full CV")
    print("\n💡 This is the easiest way for recruiters to view your CV!")
else:
    print("❌ FAILED! Check the error above")
print("="*70 + "\n")
