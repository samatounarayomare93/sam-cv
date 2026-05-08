#!/usr/bin/env python3
"""
FINAL STRIKE VERIFICATION
Sends a high-fidelity job application email with CV and Cover Letter.
Verifies the premium dark theme and Brevo HTTP delivery chain.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Setup paths
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'core'))
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def run_final_verification():
    print("=" * 80)
    print("STARTING FINAL STRIKE VERIFICATION")
    print("=" * 80)

    recipient = os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')
    company = "Future Tech Industries"
    job_title = "Lead Automation Engineer"
    
    print(f"Recipient: {recipient}")
    print(f"Company:   {company}")
    print(f"Role:      {job_title}")
    print("-" * 80)

    try:
        from core.smtp_engine import send_test_email
        
        print("Generating attachments (CV + Cover Letter)...")
        # send_test_email in smtp_engine.py is already pre-configured for Future Tech Industries
        # and handles generation of Playwright/FPDF CV and FPDF Cover Letter.
        
        result = send_test_email(recipient_email=recipient)
        
        if result:
            print("\n" + "*" * 80)
            print("SUCCESS! PREMIUM STRIKE DELIVERED")
            print("*" * 80)
            print(f"\nPlease check your inbox: {recipient}")
            print("\nVERIFICATION CHECKLIST:")
            print("   1. Design: Dark theme with linear gradient background?")
            print("   2. Avatar: Blue circle with 'SS' initials?")
            print("   3. Sections: 01. Operations Lifecycle, etc. present?")
            print("   4. Attachments: Sam_Salameh_CV.pdf and Cover_Letter_Future_Tech.pdf present?")
            print("   5. From: Correct sender name and valid email?")
        else:
            print("\nDELIVERY FAILED")
            print("Possible reasons:")
            print("- Brevo API Key invalid or expired")
            print("- No verified senders active in Brevo")
            print("- Network connectivity issues (if running on restricted cloud)")
            
    except Exception as e:
        print(f"\nFATAL ERROR: {e}")
        import traceback
        traceback.print_exc()

    print("\n" + "=" * 80)

if __name__ == "__main__":
    run_final_verification()
