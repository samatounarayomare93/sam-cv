import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# Quick test
response = requests.get(f"https://api.telegram.org/bot{TOKEN}/getMe", timeout=5)
print(f"Bot Status: {response.json()}")

# Send message
msg = "🎉 Bot is working 10000%! System verified at " + str(__import__('datetime').datetime.now())
response = requests.post(
    f"https://api.telegram.org/bot{TOKEN}/sendMessage",
    json={'chat_id': CHAT_ID, 'text': msg},
    timeout=5
)
print(f"Message sent: {response.json().get('ok')}")
