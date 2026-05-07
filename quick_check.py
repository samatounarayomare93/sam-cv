#!/usr/bin/env python3
import asyncio, httpx, os
from dotenv import load_dotenv
load_dotenv()

async def check():
    sb_url = os.getenv('SUPABASE_URL')
    sb_key = os.getenv('SUPABASE_KEY')
    headers = {'apikey': sb_key, 'Authorization': 'Bearer ' + sb_key}
    async with httpx.AsyncClient(timeout=15) as c:
        # Last 5 applications
        r = await c.get(sb_url + '/rest/v1/applications?select=company_name,company_email,created_at&order=created_at.desc&limit=5', headers=headers)
        apps = r.json() if r.status_code == 200 else []
        print('Last 5 applications:')
        for a in apps:
            ts = a.get('created_at', '')[:19]
            co = a.get('company_name', '?')
            em = a.get('company_email', '?')
            print(f'  {ts} | {co} | {em}')
        
        # Counts
        r2 = await c.get(sb_url + '/rest/v1/leads?status=eq.pending&select=id', headers=headers)
        pending = len(r2.json()) if r2.status_code == 200 else 0
        r3 = await c.get(sb_url + '/rest/v1/leads?status=eq.processing&select=id', headers=headers)
        processing = len(r3.json()) if r3.status_code == 200 else 0
        print(f'Pending: {pending} | Processing: {processing}')

asyncio.run(check())
