#!/usr/bin/env python3
"""
Create a Data URL for the CV that can be used directly in the email button
No hosting needed, no account needed!
"""
import base64

# Read CV HTML
with open('Sam_Salameh_CV.html', 'r', encoding='utf-8') as f:
    cv_html = f.read()

# Create data URL
cv_base64 = base64.b64encode(cv_html.encode('utf-8')).decode('utf-8')
data_url = f"data:text/html;base64,{cv_base64}"

print("\n" + "="*70)
print("📄 CV DATA URL CREATED")
print("="*70)
print(f"\nData URL length: {len(data_url)} characters")
print(f"\n⚠️ WARNING: Data URLs in email links may not work in all email clients")
print(f"   - Gmail: May block data URLs in links")
print(f"   - Outlook: May block data URLs in links")
print(f"   - Apple Mail: Usually works")
print("\n💡 BETTER SOLUTION: Use a free hosting service")
print("="*70 + "\n")

# Save to file
with open('cv_data_url.txt', 'w') as f:
    f.write(data_url)

print("✅ Data URL saved to: cv_data_url.txt")
print("\nBut this won't work well in emails. Let me try a better approach...")
