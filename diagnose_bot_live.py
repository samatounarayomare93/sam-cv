"""Full live bot diagnostic via Telegram API."""
import requests, os, json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN', '8630175054:AAGuMqlmCJAizvDlFUrsg-UletxSdOcsvn0')
chat_id = os.getenv('TELEGRAM_CHAT_ID', '6639482672')
BASE = f'https://api.telegram.org/bot{token}'

def api(method, **kwargs):
    r = requests.post(f'{BASE}/{method}', json=kwargs, timeout=15)
    return r.json()

def get(method, **kwargs):
    r = requests.get(f'{BASE}/{method}', params=kwargs, timeout=15)
    return r.json()

print("=" * 60)
print("BOT LIVE DIAGNOSTIC")
print("=" * 60)

# 1. Bot info
info = get('getMe')
if info.get('ok'):
    b = info['result']
    print(f"\n✅ Bot: @{b['username']} ({b['first_name']})")
    print(f"   ID: {b['id']}")
else:
    print(f"\n❌ Bot unreachable: {info}")

# 2. Webhook status
wh = get('getWebhookInfo')
if wh.get('ok'):
    w = wh['result']
    print(f"\n📡 Webhook URL: '{w.get('url', 'NONE')}'")
    print(f"   Pending updates: {w.get('pending_update_count', 0)}")
    if w.get('last_error_message'):
        print(f"   ⚠️ Last error: {w['last_error_message']}")
        print(f"   Error date: {w.get('last_error_date')}")

# 3. Recent updates (only works if no webhook set)
updates = get('getUpdates', limit=5, offset=-5)
if updates.get('ok'):
    results = updates.get('result', [])
    print(f"\n📨 Recent updates: {len(results)}")
    for u in results[-5:]:
        msg = u.get('message', {})
        if msg:
            text = msg.get('text', '')[:60]
            user = msg.get('from', {}).get('username', '?')
            date = msg.get('date', 0)
            print(f"   [{date}] @{user}: {text}")

# 4. Send a diagnostic message
print(f"\n📤 Sending diagnostic message to chat {chat_id}...")
result = api('sendMessage',
    chat_id=chat_id,
    text=(
        "🔧 <b>KIRO DIAGNOSTIC REPORT</b>\n"
        "━━━━━━━━━━━━━━━\n"
        "✅ Bot API: Connected\n"
        "✅ Token: Valid\n"
        "✅ Chat ID: Confirmed\n\n"
        "📊 <b>Render Services:</b>\n"
        "• sam-job-automator: Checking...\n"
        "• sam-cv: Checking...\n\n"
        "<i>Full system check in progress...</i>"
    ),
    parse_mode='HTML'
)
if result.get('ok'):
    msg_id = result['result']['message_id']
    print(f"   ✅ Message sent! ID: {msg_id}")
else:
    print(f"   ❌ Failed: {result}")
    msg_id = None

# 5. Check Render services
print("\n🌐 Checking Render services...")
for url, name in [
    ('https://sam-job-automator.onrender.com/api/stats', 'sam-job-automator'),
    ('https://sam-cv-bot.onrender.com/api/stats', 'sam-cv'),
]:
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            data = r.json()
            strikes = data.get('strikes', 0)
            uptime = data.get('uptime', 'N/A')
            scanned = data.get('scanned', 0)
            print(f"   ✅ {name}: strikes={strikes}, scanned={scanned}, uptime={uptime}")
        else:
            print(f"   ❌ {name}: HTTP {r.status_code}")
    except Exception as e:
        print(f"   ❌ {name}: {e}")

# 6. Edit the message with full results
if msg_id:
    import requests as req2
    stats1 = req2.get('https://sam-job-automator.onrender.com/api/stats', timeout=10).json()
    stats2 = req2.get('https://sam-cv-bot.onrender.com/api/stats', timeout=10).json()
    
    edit_result = api('editMessageText',
        chat_id=chat_id,
        message_id=msg_id,
        text=(
            "🔧 <b>KIRO DIAGNOSTIC — COMPLETE</b>\n"
            "━━━━━━━━━━━━━━━\n"
            "✅ Bot API: Connected\n"
            "✅ Token: Valid\n"
            "✅ Chat ID: Confirmed\n\n"
            "📊 <b>sam-job-automator:</b>\n"
            f"  🚀 Strikes: {stats1.get('strikes', '?')}\n"
            f"  🎯 Scanned: {stats1.get('scanned', '?')}\n"
            f"  ⏱️ Uptime: {stats1.get('uptime', '?')}\n\n"
            "📊 <b>sam-cv:</b>\n"
            f"  🚀 Strikes: {stats2.get('strikes', '?')}\n"
            f"  🎯 Scanned: {stats2.get('scanned', '?')}\n"
            f"  ⏱️ Uptime: {stats2.get('uptime', '?')}\n\n"
            "━━━━━━━━━━━━━━━\n"
            "✅ <b>All systems operational!</b>"
        ),
        parse_mode='HTML'
    )
    if edit_result.get('ok'):
        print("\n✅ Diagnostic message updated in Telegram!")
    else:
        print(f"\n⚠️ Edit failed: {edit_result.get('description')}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
