#!/usr/bin/env python3
"""Trace exactly what the bot is doing with leads."""
import asyncio, httpx, os, sys
sys.path.insert(0, '.')
sys.path.insert(0, 'core')
from dotenv import load_dotenv
load_dotenv()

async def main():
    sb_url = os.getenv('SUPABASE_URL')
    sb_key = os.getenv('SUPABASE_KEY')
    h = {'apikey': sb_key, 'Authorization': 'Bearer ' + sb_key, 'Content-Type': 'application/json'}

    async with httpx.AsyncClient(timeout=20) as c:
        # 1. Get a sample pending lead
        r = await c.get(sb_url + '/rest/v1/leads?status=eq.pending&order=priority_score.desc&limit=3&select=*', headers=h)
        leads = r.json() if r.status_code == 200 else []
        print(f"Sample pending leads: {len(leads)}")
        for l in leads:
            print(f"  company={l.get('company_name')} email={l.get('email')} title={l.get('job_title')} score={l.get('priority_score')} is_guessed={l.get('is_guessed')}")

        # 2. Check the bot_logs table if it exists
        r2 = await c.get(sb_url + '/rest/v1/bot_logs?order=created_at.desc&limit=20&select=level,message,created_at', headers=h)
        if r2.status_code == 200:
            logs = r2.json()
            print(f"\nBot logs ({len(logs)}):")
            for log in logs:
                ts = log.get('created_at', '')[:19]
                lvl = log.get('level', '?')
                msg = log.get('message', '')[:120]
                print(f"  [{ts}] {lvl}: {msg}")
        else:
            print(f"\nBot logs table: {r2.status_code} - {r2.text[:100]}")

        # 3. Check system_logs or logs table
        for table in ['logs', 'system_logs', 'activity_log', 'events']:
            r3 = await c.get(sb_url + f'/rest/v1/{table}?order=created_at.desc&limit=5', headers=h)
            if r3.status_code == 200:
                data = r3.json()
                if data:
                    print(f"\n{table} table ({len(data)} entries):")
                    for entry in data[:3]:
                        print(f"  {str(entry)[:150]}")

        # 4. Check if applications table has today's entries
        r4 = await c.get(sb_url + '/rest/v1/applications?select=company_name,created_at&order=created_at.desc&limit=20', headers=h)
        if r4.status_code == 200:
            apps = r4.json()
            print(f"\nAll recent applications ({len(apps)}):")
            for a in apps[:10]:
                print(f"  {a.get('created_at','')[:19]} | {a.get('company_name','?')}")

        # 5. Simulate what bot does: check is_duplicate for a pending lead
        if leads:
            lead = leads[0]
            job_url = lead.get('job_url', '')
            email = lead.get('email', '')
            
            # Check applications table for this email
            r5 = await c.get(
                sb_url + f'/rest/v1/applications?select=job_url&or=(job_url.eq.{job_url},company_email.eq.{email})',
                headers=h
            )
            print(f"\nDuplicate check for {lead.get('company_name')}:")
            print(f"  job_url={job_url[:60]}")
            print(f"  email={email}")
            print(f"  is_duplicate result: {r5.status_code} - {len(r5.json()) if r5.status_code==200 else r5.text[:50]} entries")

asyncio.run(main())
