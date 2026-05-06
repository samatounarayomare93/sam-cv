"""Fix double CRLF and remaining issues in scraper.py"""
import re, ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

# Fix double carriage returns \r\r -> \r
fixed = raw.replace(b'\r\r', b'\r')
# Normalize to Unix line endings
fixed = fixed.replace(b'\r\n', b'\n').replace(b'\r', b'\n')

content = fixed.decode('utf-8', errors='replace')

# Fix remaining mojibake in logging lines (safe - just comments/strings)
content = re.sub(r'ð[^\x00-\x7F\n"\']*', '', content)

# Fix fake email patterns
content = re.sub(
    r'"email":\s*f"careers@\{safe_company\.lower\(\)\.replace\([^)]+\)\}\.com"',
    '"email": ""',
    content
)
content = re.sub(
    r'"email":\s*f"info@\{safe_company\.lower\(\)\.replace\([^)]+\)\}\.com"',
    '"email": ""',
    content
)
content = re.sub(
    r'"email":\s*email or f"info@\{safe_company\.lower\(\)\.replace\([^)]+\)\}\.com"',
    '"email": email or ""',
    content
)
content = re.sub(
    r'valid_emails\.append\(f"careers@\{domain\}"\)',
    'pass  # Skip fake domain email',
    content
)

with open('core/scrapers/scraper.py', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# Verify
try:
    ast.parse(content)
    fake_remaining = len(re.findall(r'careers@.*replace|info@.*replace', content))
    empty_emails = len(re.findall(r'"email":\s*""', content))
    print(f'OK  scraper.py - syntax clean')
    print(f'    Fake email patterns removed: {fake_remaining} remaining (should be 0)')
    print(f'    Clean empty email fields: {empty_emails}')
except SyntaxError as e:
    print(f'ERR line {e.lineno}: {e.msg}')
    lines = content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+3)):
        print(f'  {i+1}: {repr(lines[i][:100])}')
