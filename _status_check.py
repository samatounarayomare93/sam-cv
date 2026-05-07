"""Full system status check."""
import os, httpx, asyncio
from dotenv import load_dotenv
from datetime import datetime, timezone
load_dotenv()

async def check():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    headers = {"apikey": key, "Authorization": "Bearer " + key}

    async with httpx.AsyncClient(timeout=15) as c:
        # 1. All leads by status
        r = await c.get(url + "/rest/v1/leads?select=status&limit=500", headers=headers)
        if r.status_code == 200:
            data = r.json()
            from collections import Counter
            counts = Counter(l.get("status") for l in data)
            print("=== ALL LEADS BY STATUS ===")
            for status, count in sorted(counts.items(), key=lambda x: -x[1]):
                print(f"  {status}: {count}")
            print(f"  TOTAL: {len(data)}")

        # 2. Last 5 leads
        print()
        r2 = await c.get(url + "/rest/v1/leads?select=company_name,status,email,created_at&order=created_at.desc&limit=5", headers=headers)
        if r2.status_code == 200:
            print("=== LAST 5 LEADS ===")
            for l in r2.json():
                email = (l.get("email") or "no email")[:25]
                print(f"  {l.get('company_name')} | {l.get('status')} | {email}")

        # 3. Last 5 applications
        print()
        r3 = await c.get(url + "/rest/v1/applications?select=company_name,status,timestamp&order=timestamp.desc&limit=5", headers=headers)
        if r3.status_code == 200:
            print("=== LAST 5 APPLICATIONS ===")
            for a in r3.json():
                ts = str(a.get("timestamp", ""))[:19]
                print(f"  {a.get('company_name')} | {a.get('status')} | {ts}")

        # 4. System settings
        print()
        r4 = await c.get(url + "/rest/v1/system_settings?select=key,value", headers=headers)
        if r4.status_code == 200:
            print("=== SYSTEM SETTINGS ===")
            for s in r4.json():
                val = str(s.get("value", ""))[:50]
                print(f"  {s.get('key')} = {val}")

        # 5. Heartbeat freshness
        print()
        r5 = await c.get(url + "/rest/v1/system_settings?key=eq.active_bot_heartbeat&select=value", headers=headers)
        if r5.status_code == 200 and r5.json():
            hb_str = r5.json()[0].get("value", "")
            try:
                hb = datetime.fromisoformat(hb_str.replace("Z", "+00:00"))
                # Ensure both are timezone-aware for comparison
                if hb.tzinfo is None:
                    hb = hb.replace(tzinfo=timezone.utc)
                now = datetime.now(timezone.utc)
                age_sec = (now - hb).total_seconds()
                print(f"=== BOT HEARTBEAT ===")
                print(f"  Last heartbeat: {hb_str[:19]}")
                print(f"  Age: {age_sec:.0f} seconds ago")
                if age_sec < 60:
                    print("  Status: BOT IS ALIVE AND RUNNING!")
                elif age_sec < 300:
                    print("  Status: Bot was active recently (< 5 min)")
                else:
                    print(f"  Status: BOT MAY BE STOPPED (last seen {age_sec/60:.0f} min ago)")
            except Exception as e:
                print(f"  Heartbeat parse error: {e}")

asyncio.run(check())
