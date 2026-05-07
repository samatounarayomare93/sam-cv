#!/usr/bin/env python3
"""
Force process pending leads by lowering score threshold temporarily.
Also resets any stuck leads back to pending.
"""
import asyncio, os, sys, httpx
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

async def main():
    sb_url = os.getenv("SUPABASE_URL")
    sb_key = os.getenv("SUPABASE_KEY")
    headers = {
        "apikey": sb_key,
        "Authorization": "Bearer " + sb_key,
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    async with httpx.AsyncClient(timeout=20) as c:
        # 1. Reset any stale_expired leads back to pending (recycle them)
        print("Recycling stale_expired leads back to pending...")
        r = await c.patch(
            sb_url + "/rest/v1/leads?status=eq.stale_expired",
            json={"status": "pending"},
            headers=headers
        )
        print(f"  Recycled stale leads: {r.status_code}")
        
        # 2. Reset rate_limited leads back to pending
        print("Recycling rate_limited leads back to pending...")
        r2 = await c.patch(
            sb_url + "/rest/v1/leads?status=eq.rate_limited",
            json={"status": "pending"},
            headers=headers
        )
        print(f"  Recycled rate_limited leads: {r2.status_code}")
        
        # 3. Reset failed leads back to pending (retry them)
        print("Recycling failed leads back to pending...")
        r3 = await c.patch(
            sb_url + "/rest/v1/leads?status=eq.failed",
            json={"status": "pending"},
            headers=headers
        )
        print(f"  Recycled failed leads: {r3.status_code}")
        
        # 4. Check new count
        r4 = await c.get(
            sb_url + "/rest/v1/leads?status=eq.pending&select=id",
            headers=headers
        )
        if r4.status_code == 200:
            count = len(r4.json())
            print(f"\nTotal pending leads now: {count}")
        
        print("\nDone! Bot will pick up these leads in the next cycle.")
        print("Check Telegram in 2-3 minutes for activity.")

asyncio.run(main())
