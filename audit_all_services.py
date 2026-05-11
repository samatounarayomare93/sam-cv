"""
Audit all Render services across both accounts and fix conflicts.
"""
import os, requests, json
from dotenv import load_dotenv
load_dotenv()

# Account 1 (old)
API_KEY_1 = 'rnd_X4vP0V0M4LOJEGbFiKs2TM72NgTg'
# Account 2 (new)
API_KEY_2 = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'

def get_services(api_key, label):
    headers = {'Authorization': f'Bearer {api_key}', 'Accept': 'application/json'}
    r = requests.get('https://api.render.com/v1/services?limit=20', headers=headers, timeout=15)
    if r.status_code != 200:
        print(f"{label}: Error {r.status_code}")
        return []
    services = []
    for item in r.json():
        s = item.get('service', item)
        # Get latest deploy
        r2 = requests.get(
            f"https://api.render.com/v1/services/{s.get('id')}/deploys?limit=1",
            headers=headers, timeout=10
        )
        latest_deploy = 'unknown'
        if r2.status_code == 200 and r2.json():
            d = r2.json()[0].get('deploy', r2.json()[0])
            latest_deploy = d.get('status', 'unknown')
        services.append({
            'account': label,
            'api_key': api_key,
            'id': s.get('id'),
            'name': s.get('name'),
            'url': s.get('serviceDetails', {}).get('url', '?'),
            'region': s.get('serviceDetails', {}).get('region', '?'),
            'suspended': s.get('suspended'),
            'deploy': latest_deploy,
        })
    return services

print("="*70)
print("AUDITING ALL RENDER SERVICES")
print("="*70)

all_services = []
all_services += get_services(API_KEY_1, "Account1")
all_services += get_services(API_KEY_2, "Account2")

print(f"\nTotal services found: {len(all_services)}")
print()
for s in all_services:
    status_icon = "✅" if s['deploy'] == 'live' else "❌"
    print(f"{status_icon} [{s['account']}] {s['name']}")
    print(f"   ID: {s['id']}")
    print(f"   URL: {s['url']}")
    print(f"   Region: {s['region']}")
    print(f"   Deploy: {s['deploy']}")
    print()

# Identify the BEST service (Account 2, live)
best = next((s for s in all_services if s['account'] == 'Account2' and s['deploy'] == 'live'), None)
if not best:
    best = next((s for s in all_services if s['deploy'] == 'live'), None)

print("="*70)
print(f"ACTIVE SERVICE (should be the only one running bot):")
if best:
    print(f"  {best['name']} | {best['url']}")
print("="*70)

# Services that should be SUSPENDED (to avoid conflict)
to_suspend = [s for s in all_services if s['id'] != (best['id'] if best else '') and s['deploy'] == 'live']
print(f"\nServices causing CONFLICT (should be suspended): {len(to_suspend)}")
for s in to_suspend:
    print(f"  {s['name']} | {s['url']}")
