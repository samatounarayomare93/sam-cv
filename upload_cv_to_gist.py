#!/usr/bin/env python3
"""
Upload CV to GitHub Gist to get a working public URL
"""
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Read CV HTML
with open('Sam_Salameh_CV.html', 'r', encoding='utf-8') as f:
    cv_html = f.read()

# GitHub Personal Access Token
github_token = os.getenv('GITHUB_PAT')

if not github_token:
    print("❌ GITHUB_PAT not found in .env")
    exit(1)

# Create Gist
gist_data = {
    "description": "Sam Salameh - Professional CV",
    "public": True,
    "files": {
        "Sam_Salameh_CV.html": {
            "content": cv_html
        }
    }
}

print("\n" + "="*70)
print("📤 UPLOADING CV TO GITHUB GIST")
print("="*70)

response = requests.post(
    'https://api.github.com/gists',
    headers={
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    },
    json=gist_data
)

if response.status_code == 201:
    gist = response.json()
    gist_url = gist['html_url']
    raw_url = gist['files']['Sam_Salameh_CV.html']['raw_url']
    
    print(f"\n✅ SUCCESS! CV uploaded to GitHub Gist")
    print(f"\n📎 Gist URL: {gist_url}")
    print(f"📎 Raw HTML URL: {raw_url}")
    print(f"\n💡 Use this URL in the 'VIEW CV ONLINE' button:")
    print(f"   {raw_url}")
    
    # Save URL to file
    with open('cv_online_url.txt', 'w') as f:
        f.write(raw_url)
    
    print(f"\n✅ URL saved to: cv_online_url.txt")
else:
    print(f"\n❌ FAILED! Status: {response.status_code}")
    print(f"Response: {response.text}")

print("="*70 + "\n")
