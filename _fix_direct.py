"""Direct line-by-line fix for scraper.py"""
import ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')
lines = content.split('\n')

fixed = []
for i, line in enumerate(lines):
    # Fix: "email": ""  # any comment,  -> "email": "",
    if '"email": ""' in line and '#' in line:
        # Find the position of the comment
        eq_pos = line.find('"email": ""')
        comment_pos = line.find('#', eq_pos)
        if comment_pos > 0:
            # Keep everything before comment, add comma
            before_comment = line[:comment_pos].rstrip()
            # Make sure it ends with comma
            if not before_comment.rstrip().endswith(','):
                before_comment = before_comment.rstrip() + ','
            fixed.append(before_comment)
            continue
    
    # Fix: "email": email or ""  # any comment,
    if '"email": email or ""' in line and '#' in line:
        eq_pos = line.find('"email": email or ""')
        comment_pos = line.find('#', eq_pos)
        if comment_pos > 0:
            before_comment = line[:comment_pos].rstrip()
            if not before_comment.rstrip().endswith(','):
                before_comment = before_comment.rstrip() + ','
            fixed.append(before_comment)
            continue
    
    fixed.append(line)

content = '\n'.join(fixed)

# Also fix em-dash in any remaining comments
content = content.replace('\u2014', '-').replace('\u2013', '-')

# Fix valid_emails fake append
import re
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
    
    # Count remaining fake emails
    fake = content.count('f"careers@{') + content.count("f'careers@{")
    print(f'Remaining fake email patterns: {fake}')
    
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines2 = content.split('\n')
    for j in range(max(0, e.lineno-5), min(len(lines2), e.lineno+3)):
        print(f'  {j+1}: {repr(lines2[j][:90])}')
