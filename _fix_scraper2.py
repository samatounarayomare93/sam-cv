"""Fix scraper.py - remove fake emails and fix encoding issues."""
import re, ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

# Decode - handle any encoding
try:
    content = raw.decode('utf-8')
except UnicodeDecodeError:
    content = raw.decode('latin-1')

# Fix broken email comment pattern that breaks dict syntax
# Pattern: "email": ""  # No guessing...,
# Should be: "email": "",
content = re.sub(
    r'"email":\s*""[^"\n,]*,',
    '"email": "",',
    content
)

# Fix: "email": email or ""  # comment,
content = re.sub(
    r'"email":\s*email or ""[^"\n,]*,',
    '"email": email or "",',
    content
)

# Remove any remaining broken mojibake by replacing non-ASCII in string literals
# with safe equivalents - just strip the broken chars from logging.info calls
def fix_logging_line(m):
    line = m.group(0)
    # Replace any non-printable/broken chars with ?
    fixed = ''.join(c if ord(c) < 128 or c in '\u2019\u2018\u201c\u201d' else '?' for c in line)
    return fixed

# Fix broken emoji in logging calls only
content = re.sub(r'logging\.(info|warning|error|debug)\(f?"[^"]*"', fix_logging_line, content)

with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

# Verify
try:
    ast.parse(content)
    print('OK  scraper.py - syntax clean')
except SyntaxError as e:
    print(f'ERR line {e.lineno}: {e.msg}')
    lines = content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+3)):
        print(f'  {i+1}: {repr(lines[i][:80])}')
