#!/usr/bin/env python3
"""Send a test email to verify the new white template + AI cover letter."""
import sys, os, asyncio
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

async def main():
    from core.ai_agent import OmniIntelligence
    from core.smtp_engine import send_email
    
    print("Step 1: Generating AI cover letter...")
    ai = OmniIntelligence()
    
    test_lead = {
        "job_title": "Senior Network Engineer",
        "description": "We are looking for a Senior Network Engineer with 5+ years experience in Cisco IOS, Fortinet FortiGate, and OSPF/BGP routing. CCNA certification required. Experience with IPSec VPN and network security is essential. The role involves managing enterprise network infrastructure for 500+ users across multiple sites in Dubai.",
        "company_name": "Etisalat e&",
        "location": "Dubai, UAE"
    }
    
    try:
        result = await asyncio.wait_for(
            ai.analyze_job(
                test_lead["job_title"],
                test_lead["description"],
                location=test_lead["location"]
            ),
            timeout=30.0
        )
        is_relevant, reason, cover_letter, salary, score, advantage, keywords, persona, psych_variant, archetype, highlights = result
        print(f"AI Score: {score} | Relevant: {is_relevant}")
        print(f"Cover letter length: {len(cover_letter)} chars")
        print(f"Cover letter preview: {cover_letter[:200]}...")
    except Exception as e:
        print(f"AI failed: {e} — using fallback")
        cover_letter = """<p>Dear Etisalat e& Hiring Team,</p>
<p>I am writing to express my strong interest in the Senior Network Engineer position at Etisalat e&. With 15+ years of enterprise network engineering experience and active certifications in Cisco CCNA, Fortinet NSE, MikroTik MTCNA, and Ubiquiti UBWA, I am confident I can deliver immediate value to your team.</p>
<p>Throughout my career, I have deployed enterprise networks for 20+ clients achieving 99.9% uptime SLA, reduced security incidents by 100% through FortiGate/Cisco ASA hardening, and configured IPSec VPN for 50+ branch offices. My expertise in OSPF/BGP/EIGRP routing and network security aligns perfectly with your requirements.</p>
<p>I am available for immediate relocation to Dubai and would welcome the opportunity to discuss how my background can contribute to Etisalat e&'s network infrastructure goals.</p>
<p>Best regards,<br><strong>Sam Salameh</strong><br>Senior Network Engineer | CCNA · NSE · MTCNA · UBWA<br>+961 70 841 1009 | samsalameh.cv@gmail.com<br>https://www.linkedin.com/in/sam-salameh</p>"""
        highlights = [
            {"title": "ENTERPRISE DELIVERY", "desc": "Deployed networks for 20+ clients (ISPs, banks, universities) achieving 99.9% uptime SLA."},
            {"title": "SECURITY EXPERTISE", "desc": "Reduced security incidents by 100% through FortiGate/Cisco ASA hardening. IPSec VPN for 50+ branches."},
            {"title": "CERTIFIED ENGINEER", "desc": "Active Cisco CCNA, Fortinet NSE, MikroTik MTCNA, Ubiquiti UBWA. 15+ years hands-on experience."}
        ]
        score = 88
    
    print("\nStep 2: Sending test email...")
    test_email = os.getenv('TEST_RECEIVER_EMAIL', 'samsalameh.cv@gmail.com')
    
    result = send_email(
        to_email=test_email,
        company_name="Etisalat e& [TEST]",
        job_title="Senior Network Engineer",
        custom_body=cover_letter,
        platform="test",
        mission_type="test",
        attachment_paths=[],
        highlights=highlights,
        strike_id="TEST-TEMPLATE-001"
    )
    
    print(f"\nResult: {'✅ SUCCESS' if result else '❌ FAILED'}")
    if result:
        print(f"Check your inbox at: {test_email}")
        print("The email should have:")
        print("  - White/light background")
        print("  - AI-generated personalized cover letter")
        print("  - Professional header with certifications")
        print("  - 3 key highlights")
        print("  - LinkedIn button")

asyncio.run(main())
