"""
Full bot health check - tests every major command and reports results to Telegram.
"""
import requests, os, time, json
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN', '8630175054:AAGuMqlmCJAizvDlFUrsg-UletxSdOcsvn0')
chat_id = os.getenv('TELEGRAM_CHAT_ID', '6639482672')
BASE = f'https://api.telegram.org/bot{token}'

def send(text, parse_mode='HTML'):
    r = requests.post(f'{BASE}/sendMessage', json={
        'chat_id': chat_id, 'text': text, 'parse_mode': parse_mode
    }, timeout=15)
    return r.json()

def edit(msg_id, text, parse_mode='HTML'):
    r = requests.post(f'{BASE}/editMessageText', json={
        'chat_id': chat_id, 'message_id': msg_id,
        'text': text, 'parse_mode': parse_mode
    }, timeout=15)
    return r.json()

checks = {}

# 1. Bot API
try:
    r = requests.get(f'{BASE}/getMe', timeout=10).json()
    checks['Bot API'] = ('✅', f"@{r['result']['username']}")
except Exception as e:
    checks['Bot API'] = ('❌', str(e)[:40])

# 2. sam-job-automator
try:
    r = requests.get('https://sam-job-automator.onrender.com/api/stats', timeout=15).json()
    checks['sam-job-automator'] = ('✅', f"strikes={r['strikes']}, uptime={r['uptime']}")
except Exception as e:
    checks['sam-job-automator'] = ('❌', str(e)[:40])

# 3. sam-cv
try:
    r = requests.get('https://sam-cv-bot.onrender.com/api/stats', timeout=30).json()
    checks['sam-cv'] = ('✅', f"strikes={r['strikes']}, uptime={r['uptime']}")
except Exception as e:
    checks['sam-cv'] = ('❌', str(e)[:40])

# 4. Supabase
try:
    from core.db_client import RealityShapingDB
    db = RealityShapingDB()
    stats = db.sync_get_stats()
    checks['Supabase DB'] = ('✅', f"total_strikes={stats.get('strikes',0)}")
except Exception as e:
    checks['Supabase DB'] = ('⚠️', str(e)[:40])

# 5. Brevo email
try:
    brevo_key = os.getenv('BREVO_API_KEY', '')
    r = requests.get('https://api.brevo.com/v3/account',
        headers={'api-key': brevo_key}, timeout=10).json()
    plan = r.get('plan', [{}])
    credits = plan[0].get('credits', '?') if plan else '?'
    checks['Brevo Email'] = ('✅', f"credits={credits}")
except Exception as e:
    checks['Brevo Email'] = ('⚠️', str(e)[:40])

# 6. Gemini AI
try:
    gemini_key = os.getenv('GEMINI_API_KEY', '')
    r = requests.post(
        f'https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={gemini_key}',
        json={'contents': [{'parts': [{'text': 'Say OK'}]}]},
        timeout=15
    ).json()
    if 'candidates' in r:
        checks['Gemini AI'] = ('✅', 'Responding')
    else:
        checks['Gemini AI'] = ('⚠️', r.get('error', {}).get('message', 'Unknown')[:40])
except Exception as e:
    checks['Gemini AI'] = ('⚠️', str(e)[:40])

# 7. Groq AI
try:
    groq_key = os.getenv('GROQ_API_KEY', '')
    r = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'},
        json={'model': 'llama3-8b-8192', 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 5},
        timeout=15
    ).json()
    if 'choices' in r:
        checks['Groq AI'] = ('✅', 'Responding')
    else:
        checks['Groq AI'] = ('⚠️', r.get('error', {}).get('message', 'Unknown')[:40])
except Exception as e:
    checks['Groq AI'] = ('⚠️', str(e)[:40])

# Build report
lines = ["🔍 <b>FULL SYSTEM CHECK</b>", "━━━━━━━━━━━━━━━"]
for name, (icon, detail) in checks.items():
    lines.append(f"{icon} <b>{name}:</b> {detail}")

ok_count = sum(1 for icon, _ in checks.values() if icon == '✅')
warn_count = sum(1 for icon, _ in checks.values() if icon == '⚠️')
fail_count = sum(1 for icon, _ in checks.values() if icon == '❌')

lines.append("━━━━━━━━━━━━━━━")
lines.append(f"✅ OK: {ok_count} | ⚠️ Warn: {warn_count} | ❌ Fail: {fail_count}")

if fail_count == 0:
    lines.append("\n🟢 <b>All critical systems operational!</b>")
else:
    lines.append(f"\n🔴 <b>{fail_count} critical issue(s) need attention!</b>")

report = "\n".join(lines)
print(report.replace('<b>', '').replace('</b>', '').replace('<i>', '').replace('</i>', ''))

result = send(report)
if result.get('ok'):
    print(f"\n✅ Report sent to Telegram! Message ID: {result['result']['message_id']}")
else:
    print(f"\n❌ Failed to send: {result}")
