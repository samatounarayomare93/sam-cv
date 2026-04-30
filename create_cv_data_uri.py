#!/usr/bin/env python3
"""
Create a Data URI for the CV so it can be opened directly from email
No hosting needed!
"""
import base64

# Read CV HTML
with open('Sam_Salameh_CV.html', 'r', encoding='utf-8') as f:
    cv_html = f.read()

# Create data URI
cv_base64 = base64.b64encode(cv_html.encode('utf-8')).decode('utf-8')
data_uri = f"data:text/html;base64,{cv_base64}"

print("\n" + "="*70)
print("📄 CV DATA URI CREATED")
print("="*70)
print(f"\nData URI length: {len(data_uri)} characters")
print(f"\n⚠️ WARNING: Data URIs longer than 2MB may not work in all email clients")
print(f"Current size: {len(data_uri) / 1024:.2f} KB")

if len(data_uri) > 2000000:
    print("\n❌ Data URI is too long for email!")
    print("We need to use a different approach.")
else:
    print("\n✅ Data URI size is acceptable!")
    
    # Save to file
    with open('cv_data_uri.txt', 'w') as f:
        f.write(data_uri)
    
    print(f"\n✅ Data URI saved to: cv_data_uri.txt")
    print(f"\nYou can use this in the 'VIEW CV ONLINE' button href")

print("="*70 + "\n")
