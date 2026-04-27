import requests
import subprocess
import os

token = "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"
headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 1. Create Repo
data = {"name": "sam-cv", "private": True}
print("Creating repo...")
r = requests.post("https://api.github.com/user/repos", json=data, headers=headers)

clone_url = ""
if r.status_code in [201, 200]:
    repo_data = r.json()
    clone_url = repo_data.get("clone_url")
    print(f"Repo created successfully: {clone_url}")
elif r.status_code == 422:
    print("Repo might already exist. Fetching info...")
    user_r = requests.get("https://api.github.com/user", headers=headers)
    username = user_r.json().get("login")
    repo_r = requests.get(f"https://api.github.com/repos/{username}/sam-cv", headers=headers)
    clone_url = repo_r.json().get("clone_url")
    print(f"Repo exists: {clone_url}")
else:
    print(f"Failed to create repo: {r.text}")
    exit(1)

if not clone_url:
    print("Failed to get clone URL.")
    exit(1)

# 2. Add auth to clone URL
auth_url = clone_url.replace("https://", f"https://{token}@")

# 3. Git Init & Push
commands = [
    "git init",
    "git add .",
    'git commit -m "Initial commit for Sam CV Job Automator"',
    "git branch -M main",
    f"git remote add origin {auth_url}",
    "git push -u origin main"
]

for cmd in commands:
    safe_cmd = cmd.replace(token, '***') if token in cmd else cmd
    print(f"Running: {safe_cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        if "remote origin already exists" in result.stderr:
            print("Remote exists, updating URL...")
            subprocess.run(f"git remote set-url origin {auth_url}", shell=True)
            subprocess.run("git push -u origin main", shell=True)
        elif "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
            print("Nothing to commit (already committed).")
        else:
            print(f"Error output: {result.stderr}")
            print(f"Stdout: {result.stdout}")

print("GitHub repository setup and push complete!")
