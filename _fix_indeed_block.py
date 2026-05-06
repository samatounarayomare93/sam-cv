"""Fix the broken indeed block in scraper.py"""
import ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')

# The broken block spans multiple lines with \r\n issues
# Find and replace the entire broken jobs.append block for indeed
import re

# Pattern: find the broken block
# It has "email": ""  # comment\n  "location"  (missing comma after "")
# and salary.replace('\n', '').replace(',', '')

# Fix 1: email line with comment breaking dict
content = re.sub(
    r'"email":\s*""[^\n]*\n(\s*"location")',
    r'"email": "",\n\1',
    content
)

# Fix 2: salary.replace that's broken across lines
# salary.replace('\n', '').replace(',', '')  -> salary.replace('$', '').replace(',', '')
content = re.sub(
    r"salary\.replace\('\\n',\s*''\)\.replace\(',',\s*''\)",
    "salary.replace('$', '').replace(',', '')",
    content
)

# Also fix any remaining broken salary.replace patterns
content = re.sub(
    r"salary\.replace\('\s*\n\s*',\s*''\)\.replace\(',',\s*''\)",
    "salary.replace('$', '').replace(',', '')",
    content
)

# Fix 3: Remove all remaining fake email patterns
content = re.sub(
    r'"email":\s*f"careers@\{[^"{}]+\}\.com"',
    '"email": ""',
    content
)
content = re.sub(
    r'"email":\s*(?:email or )?f"info@\{[^"{}]+\}\.com"',
    '"email": email or ""',
    content
)
content = re.sub(
    r'valid_emails\.append\(f"careers@\{[^}]+\}"\)',
    'pass  # No fake emails',
    content
)

# Fix em-dash
content = content.replace('\u2014', '-').replace('\u2013', '-')

# Verify
try:
    ast.parse(content)
    print('OK - syntax clean!')
    with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved.')
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines = content.split('\n')
    for j in range(max(0, e.lineno-4), min(len(lines), e.lineno+3)):
        print(f'  {j+1}: {repr(lines[j][:90])}')
