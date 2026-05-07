#!/usr/bin/env python3
"""Test email sending directly to verify it works."""
import sys, os
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

# Test send one email directly
from core.smtp_engine import send_email

print("Testing email send directly...")
result = send_email(
    to_email=os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com'),
    company_name='Test Company UAE',
    job_title='Senior Network Engineer',
    custom_body='This is a test application from the bot. If you receive this, email sending is working.',
    platform='test',
    mission_type='test',
    attachment_paths=[],
    sender_name='Sam Salameh',
    highlights=[
        {'title': 'NETWORK EXPERTISE', 'desc': '15+ years in network engineering'},
        {'title': 'CERTIFICATIONS', 'desc': 'CCNP, Fortinet NSE4, MikroTik MTCNA'},
    ],
    strike_id='TEST-001'
)

print(f"Email send result: {result}")
if result:
    print("SUCCESS: Email sending is working!")
else:
    print("FAILED: Email sending is broken!")
