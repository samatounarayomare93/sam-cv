#!/usr/bin/env python3
"""Deep diagnose - check why leads aren't being processed."""
import asyncio, os, sys
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

async def main():
    from core.db_client import RealityShapingDB
    db = RealityShapingDB()
    
    print("=" * 60)
    print("DEEP DIAGNOSIS")
    print("=" * 60)
    
    # 1. Get the actual pending leads with full details
    success, data = await db._request_with_retry(
        'GET',
        db.url + '/rest/v1/leads?status=eq.pending&order=priority_score.desc&limit=10&select=company_name,email,job_url,status,priority_score,created_at'
    )
    if success and data:
        print(f"\nPending leads ({len(data)}):")
        for l in data:
            print(f"  [{l.get('priority_score',0)}] {l.get('company_name','?')} | {l.get('email','?')} | {l.get('job_url','?')[:60]}")
    
    # 2. Check applications table - how many sent today
    success2, apps = await db._request_with_retry(
        'GET',
        db.url + '/rest/v1/applications?select=company_name,company_email,created_at&order=created_at.desc&limit=10'
    )
    if success2 and apps:
        print(f"\nLast 10 applications sent:")
        for a in apps:
            print(f"  {a.get('created_at','?')[:19]} | {a.get('company_name','?')} | {a.get('company_email','?')}")
    else:
        print(f"\nApplications table: {apps}")
    
    # 3. Check if leads are being marked as duplicate
    # Test one lead
    if success and data:
        test_lead = data[0]
        test_url = test_lead.get('job_url', '')
        test_email = test_lead.get('email', '')
        is_dup_url = await db.is_duplicate(test_url)
        is_dup_email = await db.is_duplicate(test_email)
        print(f"\nDuplicate check for '{test_lead.get('company_name')}':")
        print(f"  URL duplicate: {is_dup_url}")
        print(f"  Email duplicate: {is_dup_email}")
    
    # 4. Check bot heartbeat timing
    success3, settings = await db._request_with_retry(
        'GET',
        db.url + '/rest/v1/system_settings?select=key,value'
    )
    if success3 and settings:
        for s in settings:
            print(f"\n  {s.get('key')}: {s.get('value')}")
    
    # 5. Check if there's a processing lock
    success4, processing = await db._request_with_retry(
        'GET',
        db.url + '/rest/v1/leads?status=eq.processing&select=company_name,email,created_at&limit=10'
    )
    if success4:
        print(f"\nLeads stuck in 'processing': {len(processing)}")
        for l in processing[:5]:
            print(f"  {l.get('company_name')} | {l.get('created_at','?')[:19]}")

asyncio.run(main())
