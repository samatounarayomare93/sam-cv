"""Check GitHub Actions status"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

PAT = os.getenv('GITHUB_PAT', '')
h = {'Authorization': f'token {PAT}', 'Accept': 'application/vnd.github.v3+json'}

r = requests.get('https://api.github.com/repos/samatounarayomare93/sam-cv/actions/runs?per_page=5', headers=h, timeout=10)
if r.status_code == 200:
    runs = r.json().get('workflow_runs', [])
    print(f"Last {len(runs)} GitHub Action runs:")
    for run in runs:
        name = run.get('name', '?')
        status = run.get('status', '?')
        conclusion = run.get('conclusion', '?')
        created = run.get('created_at', '?')[:19]
        print(f"  {name} | {status} | {conclusion} | {created}")
else:
    print(f"HTTP {r.status_code}: {r.text[:200]}")

# Also check current Render env vars count
A2_KEY = 'rnd_m4ozEoc4nQYOT16Omj0U9QGd3pra'
A2_SVC = 'srv-d80th10g4nts738vk7b0'
h2 = {'Authorization': f'Bearer {A2_KEY}', 'Accept': 'application/json'}
r2 = requests.get(f'https://api.render.com/v1/services/{A2_SVC}/env-vars', headers=h2, timeout=10)
if r2.status_code == 200:
    evars = r2.json()
    print(f"\nRender env vars count: {len(evars)}")
    keys = {e.get('key','') for e in evars}
    critical = ['TELEGRAM_BOT_TOKEN', 'SUPABASE_URL', 'GROQ_API_KEY', 'ZOHO_SMTP_USER', 'GMAIL_SMTP_USER']
    for k in critical:
        status = "✅" if k in keys else "❌ MISSING"
        print(f"  {status} {k}")
