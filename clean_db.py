import asyncio
from core.db_client import RealityShapingDB
db = RealityShapingDB()
async def clean():
    junk = ['target node', 'unknown', 'none', '', 'automatic target', 'oracle lead']
    for j in junk:
        await db._request_with_retry('PATCH', f'{db.url}/rest/v1/leads?company_name=eq.{j}', payload={'status': 'failed'})
    print('Cleaned!')
asyncio.run(clean())
