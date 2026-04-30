#!/usr/bin/env python3
"""
Upload CV to catbox.moe - free file hosting, no account needed
"""
import requests

# Read CV HTML
with open('Sam_Salameh_CV.html', 'rb') as f:
    cv_content = f.read()

print("\n" + "="*70)
print("📤 UPLOADING CV TO CATBOX.MOE (FREE, NO ACCOUNT)")
print("="*70)

try:
    response = requests.post(
        'https://catbox.moe/user/api.php',
        data={'reqtype': 'fileupload'},
        files={'fileToUpload': ('Sam_Salameh_CV.html', cv_content, 'text/html')}
    )
    
    if response.status_code == 200:
        file_url = response.text.strip()
        
        if file_url.startswith('http'):
            print(f"\n✅ SUCCESS! CV uploaded!")
            print(f"\n📎 Direct URL: {file_url}")
            print(f"\n💡 This URL will work in the 'VIEW CV ONLINE' button")
            
            # Save URL
            with open('cv_online_url.txt', 'w') as f:
                f.write(file_url)
            
            print(f"\n✅ URL saved to: cv_online_url.txt")
            print(f"\n🔧 Now I'll update the email template with this URL...")
            
            # Update email template
            with open('core/smtp_engine.py', 'r', encoding='utf-8') as f:
                smtp_code = f.read()
            
            # Add the VIEW CV ONLINE button back with the new URL
            old_button = '''        <div style="margin: 40px 0 0 0; text-align: center;">
          <a href="{linkedin_url}" style="display: inline-block; padding: 15px 40px; background: #00b4d8; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; letter-spacing: 1px;">
            LINKEDIN PROFILE
          </a>
        </div>'''
            
            new_button = f'''        <div style="margin: 40px 0 0 0; text-align: center;">
          <a href="{file_url}" target="_blank" style="display: inline-block; padding: 15px 40px; background: #00b4d8; color: white; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; letter-spacing: 1px; margin-right: 15px;">
            VIEW CV ONLINE
          </a>
          <a href="{{linkedin_url}}" style="display: inline-block; padding: 15px 40px; background: transparent; border: 2px solid #00b4d8; color: #00b4d8; text-decoration: none; border-radius: 6px; font-weight: 600; font-size: 14px; letter-spacing: 1px;">
            LINKEDIN PROFILE
          </a>
        </div>'''
            
            smtp_code = smtp_code.replace(old_button, new_button)
            
            with open('core/smtp_engine.py', 'w', encoding='utf-8') as f:
                f.write(smtp_code)
            
            print(f"\n✅ Email template updated!")
            print(f"\n🚀 Now sending test email...")
            
            # Send test email
            import os
            os.system('.sovereign_runtime/python.exe test_all_cv_formats.py')
            
        else:
            print(f"\n❌ Upload failed: {file_url}")
    else:
        print(f"\n❌ Upload failed: Status {response.status_code}")
        print(f"Response: {response.text}")
        
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70 + "\n")
