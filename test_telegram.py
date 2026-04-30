#!/usr/bin/env python3
"""Test Telegram bot"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Send test message
response = requests.post(
    f'https://api.telegram.org/bot{token}/sendMessage',
    json={
        'chat_id': chat_id,
        'text': '✅ البوت شغال 100%!\n\nجرب الأوامر:\n• /menu\n• /test_strike\n• /status',
        'parse_mode': 'HTML'
    }
)

print(f'Status: {response.status_code}')
print(f'Success: {response.json().get("ok")}')
if response.json().get("ok"):
    print('✅ رسالة انبعتت على Telegram!')
else:
    print(f'❌ Error: {response.json()}')
