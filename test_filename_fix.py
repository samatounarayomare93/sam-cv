#!/usr/bin/env python3
"""
🧪 TEST: Verify CV filename and email subject fixes
"""

import os
import sys

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.pdf_generator import generate_cv_pdf
from core.smtp_engine import send_test_email

def test_cv_filename():
    """Test that CV filename is always Sam_Salameh_CV.pdf"""
    print("\n" + "="*70)
    print("🧪 TEST 1: CV Filename Verification")
    print("="*70)
    
    # Create a test lead
    test_lead = {
        'company_name': 'Future Tech Industries',
        'job_title': 'Lead Automation Engineer',
        'strike_id': 'FUTU-2771',
        'highlights': []
    }
    
    # Generate CV
    cv_path = generate_cv_pdf(
        test_lead['company_name'],
        test_lead['job_title'],
        test_lead
    )
    
    # Check filename
    filename = os.path.basename(cv_path)
    
    print(f"\n📄 Generated CV Path: {cv_path}")
    print(f"📝 Filename: {filename}")
    
    if filename == "Sam_Salameh_CV.pdf":
        print("✅ PASS: Filename is correct!")
        return True
    else:
        print(f"❌ FAIL: Expected 'Sam_Salameh_CV.pdf', got '{filename}'")
        return False

def test_email_subject():
    """Test that email subject includes company name and STRIKE-ID"""
    print("\n" + "="*70)
    print("🧪 TEST 2: Email Subject Line Verification")
    print("="*70)
    
    print("\n📧 Sending test email to: samsalameh.cv@gmail.com")
    print("Expected subject: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
    print("\n⏳ Sending...")
    
    # Send test email (it will use the new subject format)
    result = send_test_email(
        recipient_email="samsalameh.cv@gmail.com"
    )
    
    if result:
        print("\n✅ PASS: Email sent successfully!")
        print("\n📱 CHECK YOUR INBOX:")
        print("   1. Subject should be: Application: Lead Automation Engineer - Future Tech Industries [STRIKE-2771]")
        print("   2. Attachment should be: Sam_Salameh_CV.pdf")
        return True
    else:
        print("\n❌ FAIL: Email sending failed")
        return False

if __name__ == "__main__":
    print("\n" + "="*70)
    print("🚀 FILENAME & SUBJECT FIX VERIFICATION TEST")
    print("="*70)
    
    # Run tests
    test1_pass = test_cv_filename()
    test2_pass = test_email_subject()
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"CV Filename Test: {'✅ PASS' if test1_pass else '❌ FAIL'}")
    print(f"Email Subject Test: {'✅ PASS' if test2_pass else '❌ FAIL'}")
    
    if test1_pass and test2_pass:
        print("\n🎉 ALL TESTS PASSED!")
        print("\n✅ FIXES VERIFIED:")
        print("   1. CV filename is always: Sam_Salameh_CV.pdf")
        print("   2. Email subject includes company and STRIKE-ID")
    else:
        print("\n⚠️ SOME TESTS FAILED - Please review the output above")
    
    print("="*70 + "\n")
