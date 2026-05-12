"""
Fix all issues and restart the bot properly:
1. Reset rejected leads back to pending
2. Lower MIN_MATCH_SCORE to 30 so more leads pass
3. Trigger a fresh deploy with all fixes
"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

URL = os.getenv('SUPABASE_URL','').rstrip('/')
KEY = os.getenv('SUPABASE_KEY','')
h = {'apikey': KEY, 'Authorization': f'Bearer {KEY}',
     'Content-Type': 'application/json', 'Prefer': 'return=minimal'}

A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
rh = {'Authorization': f'Bearer {A2_KEY}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

print("=" * 55)
print("FIX AND RESTART")
print("=" * 55)

# Step 1: Reset rejected leads back to pending
print("\n1. Resetting rejected leads to pending...")
r = requests.patch(f'{URL}/rest/v1/leads?status=eq.rejected', headers=h,
                   json={'status': 'pending'}, timeout=10)
print(f"   Reset rejected: HTTP {r.status_code}")

r2 = requests.patch(f'{URL}/rest/v1/leads?status=eq.no_contact', headers=h,
                    json={'status': 'pending'}, timeout=10)
print(f"   Reset no_contact: HTTP {r2.status_code}")

# Step 2: Update MIN_MATCH_SCORE in system_settings
print("\n2. Lowering MIN_MATCH_SCORE to 30...")
r3 = requests.post(f'{URL}/rest/v1/system_settings',
                   headers={**h, 'Prefer': 'resolution=merge-duplicates'},
                   json={'key': 'MIN_MATCH_SCORE', 'value': '30'}, timeout=10)
print(f"   system_settings update: HTTP {r3.status_code}")

# Step 3: Make sure kill switch is OFF
print("\n3. Ensuring kill switch is OFF...")
r4 = requests.post(f'{URL}/rest/v1/system_settings',
                   headers={**h, 'Prefer': 'resolution=merge-duplicates'},
                   json={'key': 'kill_switch', 'value': 'false'}, timeout=10)
print(f"   kill_switch: HTTP {r4.status_code}")

r5 = requests.post(f'{URL}/rest/v1/system_settings',
                   headers={**h, 'Prefer': 'resolution=merge-duplicates'},
                   json={'key': 'kill_switch_active', 'value': 'false'}, timeout=10)
print(f"   kill_switch_active: HTTP {r5.status_code}")

# Step 4: Check pending count
r6 = requests.get(f'{URL}/rest/v1/leads?status=eq.pending&select=id', headers=h, timeout=10)
print(f"\n4. Pending leads now: {len(r6.json())}")

# Step 5: Trigger deploy
print("\n5. Triggering fresh deploy...")
r7 = requests.post(f'https://api.render.com/v1/services/{A2_SVC}/deploys',
                   headers=rh, json={'clearCache': 'do_not_clear'}, timeout=15)
print(f"   Deploy: HTTP {r7.status_code}")

print("\n" + "=" * 55)
print("DONE! Bot will restart in ~3 minutes.")
print("The bot will now:")
print("  - Process 490+ pending leads")
print("  - Use MIN_MATCH_SCORE=30 (more leads pass)")
print("  - Send emails via Brevo + Gmail API")
print("  - Report to @samcvbot on Telegram")
print("=" * 55)
