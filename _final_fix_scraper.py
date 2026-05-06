"""Final fix for scraper.py"""
import re, ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')

# Fix 1: broken "email": ""  # comment,  -> "email": "",
# The comment is inside the dict value position, breaking syntax
content = re.sub(
    r'"email":\s*""[^\n"]*,',
    '"email": "",',
    content
)

# Fix 2: broken "email": email or ""  # comment,
content = re.sub(
    r'"email":\s*email or ""[^\n"]*,',
    '"email": email or "",',
    content
)

# Fix 3: safe_company string that got cut: c in ' -
# Pattern: c in ' -').strip()  -> should be c in ' -').strip()
# Check if there's a broken string join
content = re.sub(
    r"c in ' -'\s*\n\s*'\)\.strip\(\)",
    "c in ' -').strip()",
    content
)

# Fix 4: Remove em-dash and other unicode in comments that break things
# Replace em-dash with regular dash in comments
content = content.replace('\u2014', '-')  # em dash
content = content.replace('\u2013', '-')  # en dash  
content = content.replace('\u2019', "'")  # right single quote
content = content.replace('\u2018', "'")  # left single quote

# Fix 5: valid_emails.append fake email
content = re.sub(
    r'valid_emails\.append\(f"careers@\{[^}]+\}"\)',
    'pass  # No fake emails',
    content
)

# Verify
try:
    ast.parse(content)
    print('OK - syntax clean!')
    with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved.')
    
    # Verify no fake emails remain
    fake_count = len(re.findall(r'"email":\s*f"(?:careers|info)@\{', content))
    print(f'Fake email patterns remaining: {fake_count}')
    
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines = content.split('\n')
    for j in range(max(0, e.lineno-5), min(len(lines), e.lineno+3)):
        print(f'  {j+1}: {repr(lines[j][:90])}')
