"""
Rebuild scraper.py cleanly:
1. Fix unclosed triple-quote at line 290
2. Remove all fake email generation
3. Fix encoding issues
"""
import re, ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')

# ── Step 1: Fix the broken docstring at line 290 ──────────────
# The issue: line 290 has a docstring that starts with """ but
# the content has """ inside it without proper escaping
lines = content.split('\n')

# Find and fix line 290 area
for i in range(285, 300):
    if i < len(lines) and '"""' in lines[i]:
        print(f"Line {i+1}: {repr(lines[i][:80])}")

# The broken docstring - replace with single-line comment
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    # Fix the broken multi-line docstring at line ~290
    # It starts with """ and has content that breaks parsing
    if i == 289 and '"""' in line:  # line 290 (0-indexed: 289)
        # Convert to a comment instead
        fixed_lines.append('    # [BYPASS MODE] Delegates to daleel_parallel_scan')
        # Skip until we find the closing """
        i += 1
        while i < len(lines) and '"""' not in lines[i]:
            i += 1
        i += 1  # skip the closing """
        continue
    fixed_lines.append(line)
    i += 1

content = '\n'.join(fixed_lines)

# ── Step 2: Remove ALL fake email generation ──────────────────
# Pattern: "email": f"careers@{...}.com"
content = re.sub(
    r'"email":\s*f"careers@\{[^}]+\}\.com"',
    '"email": ""',
    content
)
# Pattern: "email": f"info@{...}.com"  
content = re.sub(
    r'"email":\s*(?:email or )?f"info@\{[^}]+\}\.com"',
    '"email": email or ""',
    content
)
# Pattern: valid_emails.append(f"careers@{domain}")
content = re.sub(
    r'valid_emails\.append\(f"careers@\{[^}]+\}"\)',
    'pass  # No fake emails',
    content
)

# ── Step 3: Fix broken emoji (mojibake) in comments/strings ───
# Replace broken UTF-8 sequences with plain text
mojibake = [
    ('\xc3\xb0\xc5\xb8\xc5\x92\x8d', ''),   # broken globe emoji
    ('\xc3\xb0\xc5\xb8\xe2\x80\x98\x8f', ''), # broken shield
    ('\xc3\xb0\xc5\xb8\xe2\x80\x99\x8f', ''), # broken shield variant
]
for broken, fixed in mojibake:
    content = content.replace(broken, fixed)

# Also fix replacement chars
content = content.replace('\ufffd', '')

# ── Step 4: Verify and write ──────────────────────────────────
try:
    ast.parse(content)
    print('OK - syntax clean after fixes')
    with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Written successfully')
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines2 = content.split('\n')
    for j in range(max(0, e.lineno-3), min(len(lines2), e.lineno+3)):
        print(f'  {j+1}: {repr(lines2[j][:80])}')
