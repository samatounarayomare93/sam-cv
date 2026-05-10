import os
from dotenv import load_dotenv
import requests
import time
from datetime import datetime

load_dotenv()

url = os.getenv('SUPABASE_URL')
key = os.getenv('SUPABASE_KEY')
headers = {'apikey': key, 'Authorization': f'Bearer {key}'}

print("=" * 80)
print("🔍 MONITORING BOT RECOVERY")
print("=" * 80)
print("\nWaiting for bot to restart and start processing...")
print("This will check every 30 seconds for 5 minutes.\n")

for i in range(10):  # Check 10 times (5 minutes)
    print(f"\n[{i+1}/10] Checking at {datetime.now().strftime('%H:%M:%S')}...")
    print("-" * 80)
    
    # Check heartbeat
    r = requests.get(
        f'{url}/rest/v1/system_settings?key=eq.active_bot_heartbeat&select=value',
        headers=headers,
        timeout=15
    )
    
    if r.status_code == 200:
        data = r.json()
        if data:
            heartbeat = data[0].get('value', '')
            try:
                hb_time = datetime.fromisoformat(heartbeat.replace('Z', '+00:00'))
                now = datetime.now(hb_time.tzinfo)
                diff = (now - hb_time).total_seconds()
                print(f"  Bot heartbeat: {int(diff)} seconds ago")
                
                if diff < 60:
                    print(f"  ✅ Bot is ACTIVE!")
                elif diff < 300:
                    print(f"  ⏳ Bot is warming up...")
                else:
                    print(f"  ⚠️ Bot still not active")
            except:
                print(f"  ⚠️ Could not parse heartbeat")
    
    # Check if any new emails sent
    r = requests.get(
        f'{url}/rest/v1/applications?select=status,created_at&status=eq.sent&order=created_at.desc&limit=5',
        headers=headers,
        timeout=15
    )
    
    if r.status_code == 200:
        sent = r.json()
        if sent:
            print(f"  📧 Recent emails sent: {len(sent)}")
            for app in sent[:3]:
                created = app.get('created_at', 'unknown')[:19]
                print(f"     • {created}")
        else:
            print(f"  ⏳ No emails sent yet")
    
    # Check pending leads
    r = requests.get(
        f'{url}/rest/v1/applications?select=status&status=eq.pending',
        headers=headers,
        timeout=15
    )
    
    if r.status_code == 200:
        pending = r.json()
        print(f"  📊 Pending leads: {len(pending)}")
    
    if i < 9:  # Don't wait after last check
        print("\n  ⏰ Waiting 30 seconds...")
        time.sleep(30)

print("\n" + "=" * 80)
print("✅ MONITORING COMPLETE")
print("=" * 80)
print("\nIf bot is still not active:")
print("  1. Check Render dashboard: https://dashboard.render.com")
print("  2. View logs: .sovereign_runtime\\python.exe get_render_logs.py")
print("  3. Send /status to @samcvbot on Telegram")
print("=" * 80)
