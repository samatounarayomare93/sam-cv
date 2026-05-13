import asyncio
import logging
import os
from core.db_client import get_db
from core.ai_agent import get_ai_agent
from core.scrapers.omni_crawler import OmniCrawler

async def verify_stealth():
    print("Verification: Testing curl_cffi Stealth...")
    db = get_db()
    try:
        # Check if DB session (curl_cffi AsyncSession) works
        stats = await db.get_stats()
        print(f"OK: DB Stealth Session: Connected. Stats: {stats}")
    except Exception as e:
        print(f"FAIL: DB Stealth Session Failed: {e}")

async def verify_social_recon():
    print("\nVerification: Testing Social Recon (Name Harvesting)...")
    ai = get_ai_agent()
    crawler = OmniCrawler(ai)
    
    test_snippet = "Looking for a Senior Operations Manager at Google. Contact Larry Page for details."
    name = crawler._extract_person_name("Job Alert", test_snippet)
    if name and "Larry" in name:
        print(f"OK: Social Recon: Success. Extracted Name: {name}")
    else:
        print(f"FAIL: Social Recon: Failed or Unknown. Result: {name}")

async def verify_human_jitter():
    print("\nVerification: Testing Human Jitter Prompts...")
    ai = get_ai_agent()
    rel, reason, body, salary, score, adv, keys, persona, variant = await ai.analyze_job(
        "Operations Lead", 
        "Responsible for $5M budget and scaling teams.",
        person_name="John Doe"
    )
    if "John Doe" in body or "Dear John" in body:
        print("OK: Human Jitter: Salutation Personalized.")
    else:
        print("WARN: Human Jitter: Salutation not found in body.")
    print(f"Variant: {variant} | Persona: {persona}")
    print(f"Body Preview: {body[:100]}...")

async def main():
    await verify_stealth()
    await verify_social_recon()
    await verify_human_jitter()
    print("\nPhase Omega Verification Complete.")

if __name__ == "__main__":
    asyncio.run(main())
