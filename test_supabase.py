import os, httpx, asyncio, json
from dotenv import load_dotenv

load_dotenv('.env')
url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

async def check():
    async with httpx.AsyncClient() as client:
        r = await client.get(f'{url}/rest/v1/leads?select=id&limit=1', headers=headers)
        print(r.status_code)
        print(r.text)

asyncio.run(check())
