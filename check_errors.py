#!/usr/bin/env python3
import asyncio, httpx, os
from dotenv import load_dotenv
load_dotenv()

async def main():
    sb_url = os.getenv('SUPABASE_URL')
    sb_key = os.getenv('SUPABASE_KEY')
    h = {'apikey': sb_key, 'Authorization': 'Bearer ' + sb_key}
    async with httpx.AsyncClient(timeout=10) as c:
        # Count all statuses
        r = await c.get(sb_url + '/rest/v1/leads?select=status&limit=2000', headers=h)
        from collections import Counter
        counts = Counter(x.get('status') for x in r.json())
        print('=== LEAD STATUS COUNTS ===')
        for s, n in sorted(counts.items(), key=lambda x: -x[1]):
            print(f'  {s}: {n}')

        # Recent error leads
        r2 = await c.get(sb_url + '/rest/v1/leads?status=eq.error&select=company_name,email,job_title,created_at&order=created_at.desc&limit=8', headers=h)
        print('\n=== RECENT ERROR LEADS ===')
        for l in r2.json():
            ts = l.get('created_at', '')[:19]
            co = l.get('company_name', '?')
            em = l.get('email', '?')
            jt = l.get('job_title', '?')
            print(f'  {ts} | {co} | {em} | {jt}')

        # Rate limited
        r3 = await c.get(sb_url + '/rest/v1/leads?status=eq.rate_limited&select=company_name,email,created_at&order=created_at.desc&limit=5', headers=h)
        print('\n=== RATE LIMITED LEADS ===')
        for l in r3.json():
            ts = l.get('created_at', '')[:19]
            co = l.get('company_name', '?')
            em = l.get('email', '?')
            print(f'  {ts} | {co} | {em}')

        # Check anti_ban table if exists
        r4 = await c.get(sb_url + '/rest/v1/anti_ban_stats?select=*&limit=5', headers=h)
        if r4.status_code == 200:
            print('\n=== ANTI-BAN STATS ===')
            for row in r4.json():
                print(f'  {row}')

asyncio.run(main())
