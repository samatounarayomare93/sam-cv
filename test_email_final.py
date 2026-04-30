#!/usr/bin/env python3
"""
🧪 FINAL EMAIL TEST
Tests email with Sam's information only
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))

from dotenv import load_dotenv
load_dotenv()

print("=" * 70)
print("🧪 TESTING EMAIL WITH SAM'S INFO")
print("=" * 70)

# Test lead
test_lead = {
    'company_name': 'Test Company',
    'job_title': 'Senior Network Engineer',
    'email': os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com'),
    'custom_body': '''Dear Test Company Hiring Team,

I am reaching out to express my interest in the Senior Network Engineer position.

With over 15 years of experience in network infrastructure design and implementation, I have:
- Designed and deployed enterprise-grade networks for 50+ clients
- Reduced network downtime by 95% through proactive monitoring
- Implemented security protocols that prevented 100% of breach attempts

I am confident I can bring the same level of excellence to Test Company.

Best regards,
Sam Salameh''',
    'highlights': [
        {'title': 'NETWORK DESIGN', 'desc': 'Designed and deployed enterprise-grade networks for 50+ clients with 100% uptime.'},
        {'title': 'SECURITY EXPERT', 'desc': 'Implemented security protocols that prevented 100% of breach attempts over 5 years.'},
        {'title': 'COST OPTIMIZATION', 'desc': 'Reduced infrastructure costs by 40% through strategic vendor negotiations.'}
    ]
}

print(f"\n📧 Test Email Details:")
print(f"   Company: {test_lead['company_name']}")
print(f"   Job Title: {test_lead['job_title']}")
print(f"   To: {test_lead['email']}")
print(f"   From: Sam Salameh")

print("\n🚀 Sending test email...")

try:
    from core.smtp_engine import send_strike
    
    result = send_strike(test_lead, sender_name="Sam Salameh")
    
    if result:
        print("\n✅ EMAIL SENT SUCCESSFULLY!")
        print(f"\n📱 Check your inbox: {test_lead['email']}")
        print("\n🔍 Verify:")
        print("   1. Subject: Senior Network Engineer Application - Sam Salameh")
        print("   2. From: Sam Salameh (NOT Rita)")
        print("   3. Content: Sam's information")
        print("   4. Attachments: Sam's CV (if any)")
        print("   5. Location: INBOX (not Spam)")
    else:
        print("\n❌ EMAIL FAILED TO SEND")
        print("Check logs for details")
        
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
