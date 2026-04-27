import os
import sys
import logging
import asyncio
from dotenv import load_dotenv

# Ensure core imports work
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

load_dotenv()
logging.basicConfig(level=logging.INFO)

from core.smtp_engine import send_strike
from core.pdf_generator import create_personalized_pdf
from core.ai_agent import OmniIntelligence

async def run_test():
    target_email = "sam.dev1@hotmail.com"
    
    lead = {
        'company_name': 'Stark Industries (Simulation)',
        'job_title': 'VP of Talent & Operations',
        'email': target_email,
        'mission_type': 'Alpha_Omega_Strike',
        'link': 'https://example.com/job/123'
    }
    
    print("="*50)
    print(f"INITIATING DIVINE STRIKE SIMULATION")
    print(f"Target: {target_email} ({lead['company_name']})")
    print("="*50)
    
    # 1. AI Analysis
    print("1. Querying Omni-Intelligence...")
    ai = OmniIntelligence()
    description = "We are seeking a highly skilled VP of Talent and Operations to scale our engineering teams globally. Requires supreme organizational skills and 10x talent acquisition strategies."
    
    is_relevant, reason, cover_letter, salary = await ai.analyze_job(lead['job_title'], description)
    print(f"   -> AI Assessment: {reason}")
    print(f"   -> Extracted Salary: {salary}")
    
    if not cover_letter:
        print("   [!] AI Generation Failed, using fallback body.")
        cover_letter = "<p>Dear Hiring Team,</p><p>Please find attached my application for the role.</p><p>Best,<br>Sam Salameh</p>"
    
    lead['custom_body'] = cover_letter
    
    print("-" * 30)
    print("DRAFTING STRIKE PAYLOAD:")
    print(cover_letter.replace("<p>", "\n").replace("</p>", "").replace("<strong>", "").replace("</strong>", ""))
    print("-" * 30)
    
    # 2. PDF Synthesis
    print("2. Synthesizing Sovereign PDF...")
    pdf_path = create_personalized_pdf(lead)
    
    if pdf_path and os.path.exists(pdf_path):
        print(f"   [OK] PDF successfully generated at: {pdf_path}")
    else:
        print("   [ERROR] PDF Generation failed!")
    
    # 3. SMTP Delivery
    print("3. Engaging SMTP Strike Engine...")
    success = send_strike(lead, pdf_path)
    
    if success:
        print(f"[SUCCESS] MISSION ACCOMPLISHED: The strike was successfully delivered to {target_email}!")
    else:
        print("[FAILED] MISSION FAILED: The SMTP engine could not dispatch the payload.")
        
    print("="*50)

if __name__ == "__main__":
    asyncio.run(run_test())
