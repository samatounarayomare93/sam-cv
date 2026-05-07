#!/usr/bin/env python3
"""Test processing a single lead end-to-end to find the exact error."""
import asyncio, os, sys, logging
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

async def main():
    from core.db_client import RealityShapingDB
    from core.ai_agent import OmniIntelligence
    from core.main_bot import AlphaOrchestrator
    
    db = RealityShapingDB()
    ai = OmniIntelligence()
    engine = AlphaOrchestrator(db=db, ai=ai)
    
    # Use a real lead from the queue
    test_lead = {
        "company_name": "Help AG UAE",
        "email": "careers@helpag.com",
        "job_title": "Senior Network Engineer",
        "job_url": "https://helpag.com/careers/senior-network-engineer-test-001",
        "status": "pending",
        "priority_score": 88,
        "description": "We are looking for a Senior Network Engineer with 5+ years experience in Cisco, Fortinet, and network security. CCNP certification preferred. Experience with SD-WAN, MPLS, and BGP required."
    }
    
    print(f"\n{'='*60}")
    print(f"Testing single lead: {test_lead['company_name']}")
    print(f"{'='*60}\n")
    
    try:
        await engine.process_single_lead(test_lead)
        print("\n✅ Lead processed successfully!")
    except Exception as e:
        import traceback
        print(f"\n❌ Exception: {type(e).__name__}: {e}")
        traceback.print_exc()
    
    await engine.close()

asyncio.run(main())
