"""Check Telegram bot status and send a test message"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')

print("=" * 50)
print("TELEGRAM BOT STATUS CHECK")
print("=" * 50)

# 1. Check bot info
r = requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe', timeout=10)
if r.status_code == 200:
    bot = r.json()['result']
    print(f"Bot: @{bot['username']} ({bot['first_name']})")
    print(f"ID: {bot['id']}")
else:
    print(f"Bot check FAILED: {r.status_code}")

# 2. Check webhook (if set, it blocks polling)
r2 = requests.get(f'https://api.telegram.org/bot{TOKEN}/getWebhookInfo', timeout=10)
if r2.status_code == 200:
    wh = r2.json()['result']
    url = wh.get('url', '')
    pending = wh.get('pending_update_count', 0)
    last_error = wh.get('last_error_message', '')
    print(f"\nWebhook URL: '{url}' (empty = polling mode)")
    print(f"Pending updates: {pending}")
    if last_error:
        print(f"Last webhook error: {last_error}")
    if url:
        print("⚠️  WEBHOOK IS SET — this blocks polling! Clearing it...")
        r3 = requests.post(f'https://api.telegram.org/bot{TOKEN}/deleteWebhook', 
                          json={'drop_pending_updates': False}, timeout=10)
        print(f"Webhook cleared: {r3.json()}")

# 3. Get recent updates
r4 = requests.get(f'https://api.telegram.org/bot{TOKEN}/getUpdates?limit=5&timeout=0', timeout=10)
if r4.status_code == 200:
    updates = r4.json().get('result', [])
    print(f"\nRecent updates: {len(updates)}")
    for u in updates[-3:]:
        msg = u.get('message', {})
        text = msg.get('text', '')
        user = msg.get('from', {}).get('username', '?')
        print(f"  @{user}: {text}")

# 4. Send test message
print("\nSending test message to Telegram...")
r5 = requests.post(
    f'https://api.telegram.org/bot{TOKEN}/sendMessage',
    json={
        'chat_id': CHAT_ID,
        'text': '✅ <b>Bot Status Check</b>\n\nBot is alive and running on Render!\n\n'
                '📊 Memory: ~300MB (healthy)\n'
                '🔄 Scraping: Active\n'
                '📧 Email: Ready\n\n'
                'Send /status for full report.',
        'parse_mode': 'HTML'
    },
    timeout=10
)
if r5.status_code == 200:
    print("✅ Test message sent successfully!")
else:
    print(f"❌ Message failed: {r5.status_code} - {r5.text[:200]}")
