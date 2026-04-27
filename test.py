import asyncio
from core.db_client import RealityShapingDB
db = RealityShapingDB()
async def test():
    succ, data = await db._request_with_retry('GET', f'{db.url}/rest/v1/leads?order=created_at.desc&limit=1')
    print(data)
asyncio.run(test())
