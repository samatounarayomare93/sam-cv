import asyncio
from core.db_client import RealityShapingDB
db = RealityShapingDB()
async def clean():
    leads = ['top startup investors', 'odoo dubai office', 'microsoft word', 'new frankfurt office strengthens trade between']
    for l in leads:
        await db._request_with_retry('PATCH', f'{db.url}/rest/v1/leads?company_name=eq.{l}', payload={'status': 'rejected'})
    print('Cleaned junk leads.')
asyncio.run(clean())
