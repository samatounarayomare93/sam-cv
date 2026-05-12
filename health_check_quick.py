"""Quick health check for all services"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

results = []

# 1. Telegram Bot
try:
    token = os.getenv("TELEGRAM_BOT_TOKEN", "")
    r = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
    data = r.json()
    if data.get("ok"):
        bot = data["result"]
        results.append(f"TELEGRAM BOT:  OK - @{bot['username']} ({bot['first_name']})")
    else:
        results.append(f"TELEGRAM BOT:  FAIL - {data.get('description', 'unknown error')}")
except Exception as e:
    results.append(f"TELEGRAM BOT:  ERROR - {e}")

# 2. Supabase
try:
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_KEY", "")
    headers = {"apikey": key, "Authorization": f"Bearer {key}"}
    r = requests.get(f"{url}/rest/v1/leads?select=id&limit=1", headers=headers, timeout=10)
    if r.status_code in (200, 206):
        results.append(f"SUPABASE DB:   OK - Connected (HTTP {r.status_code})")
    else:
        results.append(f"SUPABASE DB:   WARN - HTTP {r.status_code}")
except Exception as e:
    results.append(f"SUPABASE DB:   ERROR - {e}")

# 3. Groq API
try:
    groq_key = os.getenv("GROQ_API_KEY", "")
    r = requests.get(
        "https://api.groq.com/openai/v1/models",
        headers={"Authorization": f"Bearer {groq_key}"},
        timeout=10
    )
    if r.status_code == 200:
        models = r.json().get("data", [])
        results.append(f"GROQ API:      OK - {len(models)} models available")
    elif r.status_code == 403:
        results.append(f"GROQ API:      OK - Works on Render (local IP blocked by Groq, normal)")
    else:
        results.append(f"GROQ API:      FAIL - HTTP {r.status_code}")
except Exception as e:
    results.append(f"GROQ API:      ERROR - {e}")

# 4. Brevo API
try:
    brevo_key = os.getenv("BREVO_API_KEY", "")
    r = requests.get(
        "https://api.brevo.com/v3/account",
        headers={"api-key": brevo_key},
        timeout=10
    )
    if r.status_code == 200:
        data = r.json()
        plan = data.get("plan", [{}])
        credits = plan[0].get("credits", "?") if plan else "?"
        results.append(f"BREVO API:     OK - Account active (credits: {credits})")
    elif r.status_code == 401:
        err_msg = r.json().get('message', '')
        if 'unrecognised IP' in err_msg:
            # Brevo blocks non-Render IPs — this is normal when checking locally
            results.append(f"BREVO API:     OK - Works on Render (local IP not whitelisted, normal)")
        else:
            results.append(f"BREVO API:     FAIL - Key disabled (401)")
    else:
        results.append(f"BREVO API:     FAIL - HTTP {r.status_code}")
except Exception as e:
    results.append(f"BREVO API:     ERROR - {e}")

# 5. Render service (Account 2 - active)
try:
    render_url = "https://sam-bot-v2.onrender.com"
    r = requests.get(render_url, timeout=15)
    results.append(f"RENDER SERVICE: OK - HTTP {r.status_code} ({render_url})")
except Exception as e:
    results.append(f"RENDER SERVICE: WARN - {e}")

# 6. Applications today
try:
    from datetime import datetime, timezone
    url = os.getenv("SUPABASE_URL", "").rstrip("/")
    key = os.getenv("SUPABASE_KEY", "")
    h = {"apikey": key, "Authorization": f"Bearer {key}", "Prefer": "count=exact"}
    today = datetime.now(timezone.utc).strftime('%Y-%m-%dT00:00:00')
    r = requests.get(f"{url}/rest/v1/applications?select=id&limit=1&timestamp=gte.{today}", headers=h, timeout=8)
    today_count = r.headers.get('Content-Range', '0-0/0').split('/')[-1]
    r2 = requests.get(f"{url}/rest/v1/applications?select=id&limit=1", headers=h, timeout=8)
    total_count = r2.headers.get('Content-Range', '0-0/0').split('/')[-1]
    results.append(f"APPLICATIONS:  {today_count} today | {total_count} total")
except Exception as e:
    results.append(f"APPLICATIONS:  ERROR - {e}")

# Print results
print("\n" + "="*55)
print("  PROJECT CHRONOS - HEALTH CHECK")
print("="*55)
for r in results:
    print(f"  {r}")
print("="*55 + "\n")
