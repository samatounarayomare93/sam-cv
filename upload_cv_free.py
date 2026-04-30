#!/usr/bin/env python3
"""
Upload CV to free hosting service (no account needed)
Using: file.io - temporary file hosting
"""
import requests

# Read CV HTML
with open('Sam_Salameh_CV.html', 'rb') as f:
    cv_content = f.read()

print("\n" + "="*70)
print("📤 UPLOADING CV TO FREE HOSTING (NO ACCOUNT NEEDED)")
print("="*70)
print("\nTrying: tmpfiles.org (free, no account, permanent)")

# Try tmpfiles.org
try:
    response = requests.post(
        'https://tmpfiles.org/api/v1/upload',
        files={'file': ('Sam_Salameh_CV.html', cv_content, 'text/html')}
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('status') == 'success':
            file_url = result['data']['url']
            # Convert to direct link
            direct_url = file_url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
            
            print(f"\n✅ SUCCESS! CV uploaded!")
            print(f"\n📎 Direct URL: {direct_url}")
            print(f"\n💡 Use this URL in the 'VIEW CV ONLINE' button")
            
            # Save URL
            with open('cv_online_url.txt', 'w') as f:
                f.write(direct_url)
            
            print(f"\n✅ URL saved to: cv_online_url.txt")
            print("\n🔧 Now updating the email template...")
            
            # Update the email template
            import os
            os.system(f'.sovereign_runtime/python.exe update_cv_link.py "{direct_url}"')
        else:
            print(f"\n❌ Upload failed: {result}")
    else:
        print(f"\n❌ Upload failed: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\n💡 Trying alternative method...")

print("\n" + "="*70 + "\n")
