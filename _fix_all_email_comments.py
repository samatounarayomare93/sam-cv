"""Fix ALL broken email comment patterns in scraper.py"""
import ast, re

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')

# Fix ALL patterns where "email": "..." has a comment before the comma
# This breaks Python dict syntax

lines = content.split('\n')
fixed_lines = []

for i, line in enumerate(lines):
    # Pattern: "email": "something"  # comment text,
    # or:      "email": email or ""  # comment text,
    # The comment must be removed, keeping just the value and comma
    
    if '"email":' in line and '#' in line:
        # Find the email value part
        email_pos = line.find('"email":')
        hash_pos = line.find('#', email_pos)
        
        if hash_pos > email_pos:
            # Get everything before the comment
            before = line[:hash_pos].rstrip()
            # Ensure it ends with a comma
            if not before.rstrip().endswith(','):
                before = before.rstrip() + ','
            fixed_lines.append(before)
            continue
    
    fixed_lines.append(line)

content = '\n'.join(fixed_lines)

# Also fix salary.replace broken across lines
# Pattern: salary.replace('\n', '').replace(',', '')
content = re.sub(
    r"salary\.replace\('\\n',\s*''\)\.replace\(',',\s*''\)",
    "salary.replace('$', '').replace(',', '')",
    content
)

# Fix remaining fake email patterns
content = re.sub(r'"email":\s*f"careers@\{[^"{}]+\}\.com"', '"email": ""', content)
content = re.sub(r'"email":\s*(?:email or )?f"info@\{[^"{}]+\}\.com"', '"email": email or ""', content)
content = re.sub(r'valid_emails\.append\(f"careers@\{[^}]+\}"\)', 'pass  # No fake emails', content)
content = content.replace('\u2014', '-').replace('\u2013', '-')

# Verify
try:
    ast.parse(content)
    print('OK - syntax clean!')
    with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved.')
    
    # Count remaining fake emails
    fake = len(re.findall(r'"email":\s*f"(?:careers|info)@', content))
    print(f'Remaining fake email patterns: {fake}')
    
    # Count fixed emails
    empty = content.count('"email": "",')
    print(f'Empty email fields (will use recon): {empty}')
    
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines2 = content.split('\n')
    for j in range(max(0, e.lineno-4), min(len(lines2), e.lineno+3)):
        print(f'  {j+1}: {repr(lines2[j][:90])}')
