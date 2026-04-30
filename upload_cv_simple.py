#!/usr/bin/env python3
"""
Upload CV to a simple free hosting service
Using: https://tmpfiles.org (no account needed)
"""
import requests

# Read CV HTML
with open('Sam_Salameh_CV.html', 'r', encoding='utf-8') as f:
    cv_html = f.read()

print("\n" + "="*70)
print("📤 UPLOADING CV TO FREE HOSTING")
print("="*70)
print("\nTrying tmpfiles.org (no account needed)...")

try:
    # Upload to tmpfiles.org
    files = {'file': ('Sam_Salameh_CV.html', cv_html, 'text/html')}
    response = requests.post('https://tmpfiles.org/api/v1/upload', files=files)
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            url = result['data']['url']
            # Convert to direct link
            direct_url = url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
            
            print(f"\n✅ SUCCESS! CV uploaded!")
            print(f"\n📎 URL: {direct_url}")
            print(f"\n💡 Use this URL in the 'VIEW CV ONLINE' button")
            
            # Save URL
            with open('cv_online_url.txt', 'w') as f:
                f.write(direct_url)
            
            print(f"\n✅ URL saved to: cv_online_url.txt")
        else:
            print(f"\n❌ Upload failed: {result}")
    else:
        print(f"\n❌ Upload failed: Status {response.status_code}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*70)
print("⚠️ NOTE: tmpfiles.org links expire after 1 hour")
print("For permanent hosting, we need a different solution")
print("="*70 + "\n")
