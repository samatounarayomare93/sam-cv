#!/usr/bin/env python3
"""
Test email with ALL CV format options
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from dotenv import load_dotenv
load_dotenv()

print("\n" + "="*70)
print("📧 SENDING TEST EMAIL WITH ALL CV OPTIONS")
print("="*70)

from core.smtp_engine import send_email

recipient = 'samsalameh.cv@gmail.com'
company_name = 'Future Tech Industries'
job_title = 'Lead Automation Engineer'

body = (
    "I am formally reaching out to express my high-level interest in the Lead Automation Engineer position.\n\n"
    "My methodology is built specifically for organizations that focus heavily on automation, "
    "KPIs, and scaling corporate culture."
)

highlights = [
    {"title": "OPERATIONS LIFECYCLE", "desc": "Proven expertise in managing high-volume recruitment logistics, employee records, and payroll synchronization with 100% data integrity."},
    {"title": "SERVICE & RETENTION", "desc": "A track record of resolving 50+ daily complex technical and billing inquiries while maintaining strict SLA compliance."},
    {"title": "WORKFLOW OPTIMIZATION", "desc": "Experience in standardizing onboarding templates and operational diagnostics to significantly reduce departmental overhead."}
]

# Prepare all attachments
attachments = []

# 1. HTML CV
cv_html_path = os.path.abspath('Sam_Salameh_CV.html')
if os.path.exists(cv_html_path):
    attachments.append(cv_html_path)
    print("✅ Added: Sam_Salameh_CV.html")

# 2. PDF CV
try:
    from core.cv_pdf_full import generate_full_cv_pdf
    cv_pdf_path = generate_full_cv_pdf()
    if cv_pdf_path and os.path.exists(cv_pdf_path):
        attachments.append(cv_pdf_path)
        print("✅ Added: Sam_Salameh_CV.pdf")
except Exception as e:
    print(f"⚠️ Could not generate PDF: {e}")

print(f"\n📬 To: {recipient}")
print(f"📧 Subject: Application: {job_title} - {company_name} [STRIKE-2771]")
print(f"📎 Attachments: {len(attachments)} files")
print(f"🔗 Online CV Link: https://samatounarayomare93.github.io/sam-cv/Sam_Salameh_CV.html")
print(f"\n⏳ Sending...\n")

result = send_email(
    recipient, 
    company_name, 
    job_title, 
    body, 
    'test', 
    'test', 
    attachments, 
    highlights=highlights,
    strike_id="STRIKE-2771"
)

print("\n" + "="*70)
if result:
    print("✅ SUCCESS! Email sent!")
    print(f"\n📱 CHECK YOUR INBOX: {recipient}")
    print("\n🔍 You should see:")
    print("   • Subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
    print("   • Attachments:")
    print("     - Sam_Salameh_CV.html (complete HTML)")
    print("     - Sam_Salameh_CV.pdf (PDF version)")
    print("   • Email body with:")
    print("     - Dark mode design")
    print("     - VIEW CV ONLINE button (opens in browser)")
    print("     - LINKEDIN PROFILE button")
    print("\n💡 Try all options and tell me which one you prefer!")
else:
    print("❌ FAILED! Check the error above")
print("="*70 + "\n")
