#!/usr/bin/env python3
"""
🧪 PDF EMAIL TEST
Tests email with PDF attachments (not HTML)
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("TESTING EMAIL WITH PDF ATTACHMENTS")
print("=" * 70)

# Test lead
test_lead = {
    'company_name': 'Tech Solutions Inc',
    'job_title': 'Senior Network Engineer',
    'email': os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com'),
    'custom_body': '''Dear Tech Solutions Inc Hiring Team,

I am reaching out to express my interest in the Senior Network Engineer position.

With over 15 years of experience in network infrastructure, I have:
- Designed enterprise networks for 50+ clients
- Achieved 99.8% uptime across managed infrastructure
- Reduced network costs by 40% through optimization

I am confident I can bring the same excellence to Tech Solutions Inc.

Best regards,
Sam Salameh''',
    'highlights': [
        {'title': 'NETWORK DESIGN', 'desc': 'Designed and deployed enterprise-grade networks for 50+ clients with 99.8% uptime.'},
        {'title': 'SECURITY EXPERT', 'desc': 'Implemented security protocols preventing 100% of breach attempts over 5 years.'},
        {'title': 'COST OPTIMIZATION', 'desc': 'Reduced infrastructure costs by 40% through strategic optimization.'}
    ]
}

print(f"\nEmail Test Details:")
print(f"   Company: {test_lead['company_name']}")
print(f"   Job Title: {test_lead['job_title']}")
print(f"   To: {test_lead['email']}")
print(f"   From: Sam Salameh")
print(f"   Attachments: PDF CV + PDF Cover Letter")

print("\nGenerating PDF attachments and sending...")

try:
    from core.smtp_engine import send_strike
    
    result = send_strike(test_lead, sender_name="Sam Salameh")
    
    if result:
        print("\nEMAIL SENT SUCCESSFULLY!")
        print(f"\nCheck your inbox: {test_lead['email']}")
        print("\nVerify:")
        print("   1. Subject: Senior Network Engineer Application - Sam Salameh")
        print("   2. From: Sam Salameh")
        print("   3. Attachments: 2 PDF files (CV + Cover Letter)")
        print("   4. NOT HTML code in attachment")
        print("   5. Location: INBOX (not Spam)")
        print("\nPDF files are professional and won't trigger spam filters!")
    else:
        print("\nEMAIL FAILED TO SEND")
        print("Check logs for details")
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
