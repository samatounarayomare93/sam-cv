"""Check GitHub Action logs"""
import requests, os
from dotenv import load_dotenv
load_dotenv()

PAT = os.getenv('GITHUB_PAT', '')
h = {'Authorization': f'token {PAT}', 'Accept': 'application/vnd.github.v3+json'}

# Get latest run
r = requests.get('https://api.github.com/repos/samatounarayomare93/sam-cv/actions/runs?per_page=1', headers=h, timeout=10)
runs = r.json().get('workflow_runs', [])
if not runs:
    print("No runs found")
    exit()

run = runs[0]
run_id = run['id']
print(f"Latest run: {run['name']} | {run['status']} | {run['conclusion']} | {run['created_at'][:19]}")

# Get jobs
r2 = requests.get(f'https://api.github.com/repos/samatounarayomare93/sam-cv/actions/runs/{run_id}/jobs', headers=h, timeout=10)
jobs = r2.json().get('jobs', [])
for job in jobs:
    print(f"\nJob: {job['name']} | {job['status']} | {job['conclusion']}")
    for step in job.get('steps', []):
        status = step.get('conclusion', step.get('status', '?'))
        print(f"  Step: {step['name']} | {status}")

# Get logs
r3 = requests.get(f'https://api.github.com/repos/samatounarayomare93/sam-cv/actions/runs/{run_id}/logs', 
                  headers={**h, 'Accept': 'application/vnd.github.v3+json'}, 
                  timeout=10, allow_redirects=True)
print(f"\nLogs status: {r3.status_code}")
if r3.status_code == 200:
    # It's a zip file
    import zipfile, io
    try:
        z = zipfile.ZipFile(io.BytesIO(r3.content))
        for name in z.namelist():
            if 'deploy' in name.lower():
                content = z.read(name).decode('utf-8', errors='ignore')
                # Show last 50 lines
                lines = content.strip().split('\n')
                print(f"\n=== {name} (last 30 lines) ===")
                for line in lines[-30:]:
                    print(line[:200])
    except Exception as e:
        print(f"Log parse error: {e}")
