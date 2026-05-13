import asyncio
import logging
import os
import sys
from dotenv import load_dotenv

# Ensure we can import modules from core and root
sys.path.append(os.getcwd())

from core.main_bot import AlphaOrchestrator
import config

async def execute_truth_test():
    load_dotenv()
    
    # Force high-signal logging
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - [TRUTH-TEST] %(levelname)s - %(message)s")
    
    print("\n" + "="*60)
    print("PROJECT CHRONOS: TRANSCENDENCE TRUTH TEST")
    print("="*60)
    print("TARGET EMAIL: sam.dev1@hotmail.com")
    print("TARGET COMPANY: Microsoft")
    print("ROLE: Senior Operations Manager")
    print("="*60 + "\n")

    # 1. Initialize the Brain
    orchestrator = AlphaOrchestrator()
    
    # 2. Mock a High-Value Lead
    mock_lead = {
        "company_name": "Microsoft",
        "job_title": "Senior Operations Manager",
        "description": "We are looking for a world-class strategic leader to drive operational excellence across our Cloud + AI division. You will work on massive scale, optimizing performance and culture.",
        "location": "Redmond, WA (Remote Friendly)",
        "mission_type": "Founding_Strike",
        "email": "sam.dev1@hotmail.com", 
    }

    print("INITIATING END-TO-END STRIKE PACKAGE...")
    
    try:
        # We call the real orchestrator. This will trigger the full Transcendence pipeline.
        await orchestrator.process_single_lead(mock_lead, variant_weights=None)
        
        print("\n" + "="*60)
        print("TRUTH TEST EXECUTION COMPLETE")
        print("Check your email at sam.dev1@hotmail.com")
        print("Check Telegram for the Singularity Strike broadcast")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"\nCRITICAL SYSTEM FAILURE: {e}")
    finally:
        await orchestrator.close()

if __name__ == "__main__":
    asyncio.run(execute_truth_test())
