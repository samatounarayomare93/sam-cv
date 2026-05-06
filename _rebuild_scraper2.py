"""
Full rebuild of scraper.py - fix ALL triple-quote issues
"""
import re, ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')

# Remove replacement chars
content = content.replace('\ufffd', '')

# ── Find ALL unclosed triple-quotes and fix them ──────────────
lines = content.split('\n')
result = []
in_docstring = False
docstring_start = -1

i = 0
while i < len(lines):
    line = lines[i]
    
    # Count """ in this line
    count = line.count('"""')
    
    if not in_docstring:
        if count == 1:
            # Opening a docstring that doesn't close on same line
            in_docstring = True
            docstring_start = i
            result.append(line)
        elif count == 2:
            # Opens and closes on same line - fine
            result.append(line)
        elif count == 0:
            result.append(line)
        else:
            # 3+ on same line - unusual but ok
            result.append(line)
    else:
        # We're inside a docstring
        if count >= 1:
            # This line closes the docstring
            in_docstring = False
            result.append(line)
        else:
            result.append(line)
    i += 1

# If still in docstring at end, add closing
if in_docstring:
    result.append('"""')
    print(f"Added missing closing triple-quote (docstring started at line {docstring_start+1})")

content = '\n'.join(result)

# ── Remove ALL fake email generation ─────────────────────────
# Pattern 1: "email": f"careers@{safe_company...}.com"
content = re.sub(
    r'"email":\s*f"careers@\{[^"{}]+\}\.com"',
    '"email": ""',
    content
)
# Pattern 2: "email": f"info@{...}.com"
content = re.sub(
    r'"email":\s*(?:email or )?f"info@\{[^"{}]+\}\.com"',
    '"email": email or ""',
    content
)
# Pattern 3: valid_emails.append(f"careers@{domain}")
content = re.sub(
    r'valid_emails\.append\(f"careers@\{[^}]+\}"\)',
    'pass  # No fake emails - recon surge finds real contact',
    content
)

# ── Verify ────────────────────────────────────────────────────
try:
    ast.parse(content)
    print('OK - syntax clean')
    with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved successfully')
    
    # Count fake emails removed
    remaining = content.count('careers@') + content.count('info@{safe')
    print(f'Remaining fake email patterns: {remaining}')
    
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines2 = content.split('\n')
    for j in range(max(0, e.lineno-5), min(len(lines2), e.lineno+3)):
        print(f'  {j+1}: {repr(lines2[j][:90])}')
