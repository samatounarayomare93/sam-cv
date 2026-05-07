#!/usr/bin/env python3
"""Diagnose why hourly rate is 0 - check queue, email limits, kill switch."""
import asyncio, os, sys
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

async def main():
    from core.db_client import RealityShapingDB
    db = RealityShapingDB()
    
    print("=" * 60)
    print("QUEUE DIAGNOSIS")
    print("=" * 60)
    
    # 1. Check kill switch
    ks = os.getenv('KILL_SWITCH_ACTIVE', 'false')
    print(f"Kill Switch: {ks}")
    
    # 2. Check pending leads count
    try:
        pending = await db.get_pending_leads(limit=5)
        print(f"Pending leads in queue: {len(pending)}")
        if pending:
            for l in pending[:3]:
                print(f"  - {l.get('company_name','?')} | {l.get('status','?')} | {l.get('email','no email')}")
    except Exception as e:
        print(f"Pending leads error: {e}")
    
    # 3. Check total leads by status
    try:
        success, data = await db._request_with_retry(
            'GET',
            db.url + '/rest/v1/leads?select=status&limit=1000'
        )
        if success and data:
            from collections import Counter
            counts = Counter(r.get('status','?') for r in data)
            print(f"\nLeads by status (last 1000):")
            for status, count in sorted(counts.items(), key=lambda x: -x[1]):
                print(f"  {status}: {count}")
    except Exception as e:
        print(f"Status count error: {e}")
    
    # 4. Check email rotator limits
    try:
        from core.email_rotator import get_rotator
        rotator = get_rotator()
        print(f"\nEmail rotator usage today:")
        for name, info in rotator.usage.items():
            count = info.get('count', 0)
            print(f"  {name}: {count} sent")
        total = sum(info.get('count',0) for info in rotator.usage.values())
        print(f"  TOTAL: {total} emails sent today")
    except Exception as e:
        print(f"Email rotator error: {e}")
    
    # 5. Check anti-ban protection
    try:
        from core.anti_ban_protection import get_protection
        prot = get_protection()
        apps_today = getattr(prot, 'applications_today', 0)
        max_apps = int(os.getenv('MAX_APPLICATIONS_PER_DAY', 1500))
        print(f"\nAnti-ban: {apps_today}/{max_apps} applications today")
    except Exception as e:
        print(f"Anti-ban error: {e}")
    
    # 6. Check system settings (kill switch in DB)
    try:
        success, data = await db._request_with_retry(
            'GET',
            db.url + '/rest/v1/system_settings?select=key,value&limit=20'
        )
        if success and data:
            print(f"\nSystem settings:")
            for row in data:
                print(f"  {row.get('key')}: {row.get('value')}")
    except Exception as e:
        print(f"System settings error: {e}")

    print("=" * 60)

asyncio.run(main())
