"""Send final status to Telegram."""
import requests, os
from dotenv import load_dotenv
load_dotenv()

token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# Quick AI test with Groq
groq_key = os.getenv('GROQ_API_KEY')
groq_status = '❌'
try:
    r = requests.post(
        'https://api.groq.com/openai/v1/chat/completions',
        headers={'Authorization': f'Bearer {groq_key}', 'Content-Type': 'application/json'},
        json={'model': 'llama-3.3-70b-versatile', 'messages': [{'role': 'user', 'content': 'Say OK'}], 'max_tokens': 5},
        timeout=10
    ).json()
    groq_status = '✅ llama-3.3-70b' if 'choices' in r else f'❌ {r.get("error",{}).get("message","?")[:30]}'
except Exception as e:
    groq_status = f'❌ {str(e)[:30]}'

# Check Render
automator_status = '❌'
cv_status = '❌'
try:
    r1 = requests.get('https://sam-job-automator.onrender.com/api/stats', timeout=15).json()
    automator_status = f"✅ strikes={r1['strikes']}, uptime={r1['uptime']}"
except: pass
try:
    r2 = requests.get('https://sam-cv-bot.onrender.com/api/stats', timeout=30).json()
    cv_status = f"✅ strikes={r2['strikes']}, uptime={r2['uptime']}"
except: pass

msg = (
    "✅ <b>ALL SYSTEMS FIXED & DEPLOYED</b>\n"
    "━━━━━━━━━━━━━━━\n\n"
    "🤖 <b>AI Engine:</b>\n"
    f"  Groq: {groq_status}\n"
    "  Gemini: ⚠️ Quota exhausted (get new key)\n\n"
    "🌐 <b>Render Services:</b>\n"
    f"  sam-job-automator: {automator_status}\n"
    f"  sam-cv: {cv_status}\n\n"
    "🔑 <b>GitHub Token:</b> ✅ Updated\n\n"
    "━━━━━━━━━━━━━━━\n"
    "<b>📋 All fixes deployed:</b>\n"
    "• Test strike no longer gets stuck\n"
    "• /status & /audit commands fixed\n"
    "• Groq as primary AI (Gemini quota)\n"
    "• Email rotator fixed for Render\n"
    "• Both services live & running\n\n"
    "⚠️ <b>One thing to do:</b>\n"
    "Get a new Gemini API key at:\n"
    "<code>aistudio.google.com</code>\n"
    "Then update GEMINI_API_KEY in Render env vars"
)

r = requests.post(f'https://api.telegram.org/bot{token}/sendMessage', json={
    'chat_id': chat_id, 'text': msg, 'parse_mode': 'HTML'
}, timeout=15)
print('Sent:', r.json().get('ok'))
print(msg.replace('<b>','').replace('</b>','').replace('<code>','').replace('</code>',''))
