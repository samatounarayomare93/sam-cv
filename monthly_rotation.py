"""
Monthly Rotation Script - Run this when build minutes run out.
Switches between Account 1 and Account 2 automatically.

Usage:
  python monthly_rotation.py          # Auto-detect and rotate
  python monthly_rotation.py account1 # Force switch to Account 1
  python monthly_rotation.py account2 # Force switch to Account 2
"""
import os, sys, requests
from dotenv import load_dotenv
load_dotenv()

# Account 1 (samatou683@gmail.com)
ACCOUNT1 = {
    'api_key': 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg',
    'email': 'samatou683@gmail.com',
    'services': {
        'bot': 'srv-d7s6rf6gvqtc73bt431g',  # sam-job-automator
        'bot_name': 'sam-job-automator',
        'bot_url': 'https://sam-job-automator.onrender.com',
    }
}

# Account 2 (samsalameh.cv@gmail.com)
ACCOUNT2 = {
    'api_key': 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra',
    'email': 'samsalameh.cv@gmail.com',
    'services': {
        'bot': 'srv-d80th10g4nts738vk7b0',  # sam-bot-v2
        'bot_name': 'sam-bot-v2',
        'bot_url': 'https://sam-bot-v2.onrender.com',
    }
}

def get_headers(api_key):
    return {'Authorization': f'Bearer {api_key}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

def suspend_service(api_key, service_id, name):
    r = requests.post(f'https://api.render.com/v1/services/{service_id}/suspend',
        headers=get_headers(api_key), timeout=15)
    status = "SUSPENDED" if r.status_code in (200,201,202,204) else f"ERROR {r.status_code}"
    print(f"  {status}: {name}")
    return r.status_code in (200,201,202,204)

def resume_service(api_key, service_id, name):
    r = requests.post(f'https://api.render.com/v1/services/{service_id}/resume',
        headers=get_headers(api_key), timeout=15)
    status = "RESUMED" if r.status_code in (200,201,202,204) else f"ERROR {r.status_code}"
    print(f"  {status}: {name}")
    return r.status_code in (200,201,202,204)

def check_service_status(api_key, service_id):
    r = requests.get(f'https://api.render.com/v1/services/{service_id}',
        headers=get_headers(api_key), timeout=15)
    if r.status_code == 200:
        return r.json().get('suspended', 'unknown')
    return 'error'

def update_env(api_key, service_id, url):
    """Update local .env with new active service"""
    import re
    env_path = '.env'
    with open(env_path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = re.sub(r'^RENDER_API_KEY=.*$', f'RENDER_API_KEY={api_key}', content, flags=re.MULTILINE)
    content = re.sub(r'^RENDER_SERVICE_ID=.*$', f'RENDER_SERVICE_ID={service_id}', content, flags=re.MULTILINE)
    with open(env_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"  .env updated: RENDER_SERVICE_ID={service_id}")

print("="*60)
print("MONTHLY ROTATION MANAGER")
print("="*60)

# Determine which account to activate
force = sys.argv[1].lower() if len(sys.argv) > 1 else None

# Check current status
status1 = check_service_status(ACCOUNT1['api_key'], ACCOUNT1['services']['bot'])
status2 = check_service_status(ACCOUNT2['api_key'], ACCOUNT2['services']['bot'])

print(f"\nCurrent status:")
print(f"  Account 1 ({ACCOUNT1['email']}): {status1}")
print(f"  Account 2 ({ACCOUNT2['email']}): {status2}")

# Determine target
if force == 'account1':
    activate = ACCOUNT1
    deactivate = ACCOUNT2
    print("\nForcing switch to Account 1...")
elif force == 'account2':
    activate = ACCOUNT2
    deactivate = ACCOUNT1
    print("\nForcing switch to Account 2...")
else:
    # Auto: activate the suspended one, deactivate the running one
    if status1 == 'not_suspended' and status2 == 'suspended':
        # Account 1 running, Account 2 suspended → switch to Account 2
        activate = ACCOUNT2
        deactivate = ACCOUNT1
        print("\nAuto: Switching from Account 1 → Account 2")
    elif status2 == 'not_suspended' and status1 == 'suspended':
        # Account 2 running, Account 1 suspended → switch to Account 1
        activate = ACCOUNT1
        deactivate = ACCOUNT2
        print("\nAuto: Switching from Account 2 → Account 1")
    else:
        print(f"\nBoth accounts status unclear. Use: python monthly_rotation.py account1/account2")
        sys.exit(0)

print(f"\nActivating: {activate['email']} → {activate['services']['bot_name']}")
print(f"Suspending: {deactivate['email']} → {deactivate['services']['bot_name']}")

# Execute rotation
print("\nStep 1: Suspend old service...")
suspend_service(deactivate['api_key'], deactivate['services']['bot'], deactivate['services']['bot_name'])

print("\nStep 2: Resume new service...")
resume_service(activate['api_key'], activate['services']['bot'], activate['services']['bot_name'])

print("\nStep 3: Update local .env...")
update_env(activate['api_key'], activate['services']['bot'], activate['services']['bot_url'])

print("\nStep 4: Sync env vars to new service...")
# Re-run sync
import subprocess
result = subprocess.run(
    ['.sovereign_runtime/python.exe', 'sync_all_to_account2.py'],
    capture_output=True, text=True, timeout=60
)
if 'SUCCESS' in result.stdout:
    print("  Env vars synced!")
else:
    print(f"  Sync output: {result.stdout[:100]}")

print("\nStep 5: Update keep_alive.py with new URL...")
import re as _re
ka_path = 'core/keep_alive.py'
with open(ka_path, 'r', encoding='utf-8') as f:
    ka_content = f.read()
new_url = activate['services']['bot_url']
ka_content = _re.sub(
    r'url = "https://[^"]+\.onrender\.com"',
    f'url = "{new_url}"',
    ka_content
)
with open(ka_path, 'w', encoding='utf-8') as f:
    f.write(ka_content)
print(f"  keep_alive.py updated to ping: {new_url}")

print("\n" + "="*60)
print("ROTATION COMPLETE!")
print("="*60)
print(f"Active bot: {activate['services']['bot_url']}")
print(f"Next rotation: When build minutes run out again")
print(f"Command: python monthly_rotation.py")
