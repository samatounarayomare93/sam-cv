import os, httpx, asyncio, json
from dotenv import load_dotenv

load_dotenv('.env')
token = os.getenv('TELEGRAM_BOT_TOKEN')

async def check():
    async with httpx.AsyncClient() as client:
        r = await client.get(f'https://api.telegram.org/bot{token}/getMe')
        print(r.status_code)
        print(json.dumps(r.json(), indent=2))

asyncio.run(check())
