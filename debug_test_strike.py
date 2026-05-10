"""
Debug the test strike flow end-to-end with timing.
Simulates exactly what the bot does when you type an email.
"""
import asyncio
import logging
import time
import os
import sys

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

async def simulate_test_strike(email):
    """Simulate the exact bot flow for test strike."""
    print(f"\n{'='*60}")
    print(f"SIMULATING TEST STRIKE TO: {email}")
    print(f"{'='*60}\n")
    
    from core import smtp_engine
    
    start = time.time()
    print(f"[{time.time()-start:.1f}s] Starting asyncio.wait_for with 90s timeout...")
    
    try:
        success = await asyncio.wait_for(
            asyncio.to_thread(smtp_engine.send_test_email, email),
            timeout=90.0
        )
        elapsed = time.time() - start
        print(f"\n[{elapsed:.1f}s] RESULT: {'SUCCESS ✅' if success else 'FAILED ❌'}")
        return success
    except asyncio.TimeoutError:
        elapsed = time.time() - start
        print(f"\n[{elapsed:.1f}s] TIMEOUT ⏰ - took too long!")
        return False
    except Exception as e:
        elapsed = time.time() - start
        print(f"\n[{elapsed:.1f}s] ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    email = sys.argv[1] if len(sys.argv) > 1 else "samsalameh.cv@gmail.com"
    result = asyncio.run(simulate_test_strike(email))
    print(f"\nFinal result: {result}")
