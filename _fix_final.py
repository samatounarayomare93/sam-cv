"""Fix scraper.py - surgical fix of the broken docstring on line 801"""
import ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')
lines = content.split('\n')

# Fix line 800 (index 800) - the broken docstring
# Replace whatever is there with a clean version
for i, line in enumerate(lines):
    if 'scrape_monster_jobs' in line and 'def ' in line:
        print(f"Found monster func at line {i+1}")
        # Check next line
        if i+1 < len(lines):
            next_line = lines[i+1]
            print(f"  Next line raw: {repr(next_line[:80])}")
            # Fix the docstring line
            if '"""' in next_line:
                lines[i+1] = '    """Enhanced Monster scraper"""'
                print(f"  Fixed to: {repr(lines[i+1])}")

# Also fix ALL fake email patterns properly
import re
fixed_content = '\n'.join(lines)

# Pattern: "email": f"careers@{...}.com"  -> "email": ""
fixed_content = re.sub(
    r'"email":\s*f"careers@\{[^}]+\}\.com"',
    '"email": ""',
    fixed_content
)
# Pattern: "email": f"info@{...}.com"
fixed_content = re.sub(
    r'"email":\s*email or f"info@\{[^}]+\}\.com"',
    '"email": email or ""',
    fixed_content
)
# Pattern: valid_emails.append(f"careers@{domain}")
fixed_content = re.sub(
    r'valid_emails\.append\(f"careers@\{domain\}"\)',
    'pass  # skip fake domain email',
    fixed_content
)

# Write back
with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
    f.write(fixed_content)

# Verify
try:
    ast.parse(fixed_content)
    print('\nOK - scraper.py syntax clean')
except SyntaxError as e:
    print(f'\nERR line {e.lineno}: {e.msg}')
    lines2 = fixed_content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines2), e.lineno+3)):
        print(f'  {i+1}: {repr(lines2[i][:80])}')
