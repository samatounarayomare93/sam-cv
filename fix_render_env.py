"""Fix critical env vars on Render Account 2 for memory/performance"""
import requests

A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h = {'Authorization': f'Bearer {A2_KEY}', 'Content-Type': 'application/json', 'Accept': 'application/json'}

# Fix the performance-critical env vars
fixes = [
    {'key': 'MAX_PARALLEL_STRIKES',      'value': '3'},    # was 15 → OOM
    {'key': 'MAX_QUALIFIED_LEADS_PER_CYCLE', 'value': '50'},  # was 300 → too many
    {'key': 'BATCH_SIZE',                'value': '10'},   # was 75 → too large
    {'key': 'MAX_PARALLEL_SCRAPERS',     'value': '2'},    # was 12 → too many
    {'key': 'SCRAPE_INTERVAL_MINUTES',   'value': '90'},   # was 45 → too frequent
    {'key': 'MEMORY_THRESHOLD_MB',       'value': '400'},  # was 450 → too late
    {'key': 'GC_INTERVAL',              'value': '60'},    # was 90 → more frequent GC
    {'key': 'RENDER',                    'value': 'true'}, # ensure Render mode
    {'key': 'RENDER_EXTERNAL_URL',       'value': 'https://sam-bot-v2.onrender.com'},
]

r = requests.put(
    f'https://api.render.com/v1/services/{A2_SVC}/env-vars',
    headers=h, json=fixes, timeout=15
)
if r.status_code == 200:
    print(f"✅ Fixed {len(fixes)} performance env vars on Render")
    for f in fixes:
        print(f"  {f['key']} = {f['value']}")
else:
    print(f"❌ Failed: {r.status_code} - {r.text[:200]}")
