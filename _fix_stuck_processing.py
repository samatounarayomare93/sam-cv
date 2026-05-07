"""Fix stuck processing leads - reset them back to pending so bot can retry"""
import asyncio, httpx, os
from dotenv import load_dotenv
load_dotenv()

async def fix_stuck():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    headers = {
        "apikey": key,
        "Authorization": "Bearer " + key,
        "Content-Type": "application/json"
    }
    
    async with httpx.AsyncClient(timeout=20) as c:
        # Get all processing leads older than 5 minutes (stuck)
        r = await c.get(
            url + "/rest/v1/leads?status=eq.processing&select=id,company_name,email",
            headers=headers
        )
        stuck = r.json() if r.status_code == 200 else []
        print(f"Found {len(stuck)} stuck 'processing' leads")
        
        if stuck:
            # Reset them all back to pending
            r2 = await c.patch(
                url + "/rest/v1/leads?status=eq.processing",
                json={"status": "pending"},
                headers=headers
            )
            if r2.status_code in (200, 204):
                print(f"Reset {len(stuck)} leads back to pending")
            else:
                print(f"Reset failed: {r2.status_code} - {r2.text[:100]}")
        
        # Check final pending count
        r3 = await c.get(url + "/rest/v1/leads?status=eq.pending&select=id", headers=headers)
        pending = r3.json() if r3.status_code == 200 else []
        print(f"Total pending leads now: {len(pending)}")

asyncio.run(fix_stuck())
