"""Fix scraper.py - fix broken docstring and remove fake emails."""
import re

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')

# ── Fix 1: The broken docstring at line 290 ──────────────────────────────────
# The emoji \U0001f451 (crown) got mojibake'd to ðŸ'' which contains a ' char
# This breaks the triple-quote parser
# Replace the broken emoji sequence in docstrings with safe text
content = content.replace(
    '"""[ðŸ\'\' BYPASS MODE] Delegates to daleel_parallel_scan which uses search-engine queries.\r\n    Direct HTTP to daleel-madani.org returns 403 on every request."""',
    '"""BYPASS MODE: Delegates to daleel_parallel_scan (search-engine queries).\n    Direct HTTP to daleel-madani.org returns 403 on every request."""'
)

# Also fix any other broken emoji in docstrings/comments that contain quotes
# Replace all mojibake emoji patterns (sequences starting with ð) in comments/strings
# with safe ASCII equivalents
def fix_mojibake(text):
    # Fix common broken emoji patterns that contain quote chars
    replacements = [
        ("ðŸ''", "[crown]"),
        ("ðŸ›¡ï¸\x8f", "[shield]"),
        ("ðŸ›¡ï¸", "[shield]"),
        ("ðŸ\x8f", ""),
        ("\x8f", ""),
        ("\xc3\xb0\xc5\xb8\xc5\x92\xc2\x8d", "[globe]"),
    ]
    for broken, fixed in replacements:
        text = text.replace(broken, fixed)
    return text

content = fix_mojibake(content)

# ── Fix 2: Remove fake email generation ──────────────────────────────────────
# Replace: "email": f"careers@{safe_company.lower().replace(' ', '')}.com"
# With:    "email": ""
content = re.sub(
    r'"email":\s*f"careers@\{safe_company\.lower\(\)\.replace\([^)]+\)\}\.com"',
    '"email": ""',
    content
)

# Replace: "email": f"info@{safe_company.lower().replace(' ', '')}.com"  
content = re.sub(
    r'"email":\s*f"info@\{safe_company\.lower\(\)\.replace\([^)]+\)\}\.com"',
    '"email": ""',
    content
)

# Replace: "email": email or f"info@{...}.com"
content = re.sub(
    r'"email":\s*email or f"info@\{safe_company\.lower\(\)\.replace\([^)]+\)\}\.com"',
    '"email": email or ""',
    content
)

# Replace blind extract fake email: valid_emails.append(f"careers@{domain}")
content = re.sub(
    r'valid_emails\.append\(f"careers@\{domain\}"\)',
    'pass  # Skip fake domain email',
    content
)

# ── Write back ────────────────────────────────────────────────────────────────
with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

# ── Verify ────────────────────────────────────────────────────────────────────
import ast
try:
    ast.parse(content)
    print('OK  scraper.py - syntax clean')
    
    # Count remaining fake emails
    remaining = len(re.findall(r'careers@.*replace|info@.*replace', content))
    print(f'Fake email patterns remaining: {remaining}')
    
    # Count empty emails
    empty = len(re.findall(r'"email":\s*""', content))
    print(f'Clean empty email fields: {empty}')
    
except SyntaxError as e:
    print(f'ERR line {e.lineno}: {e.msg}')
    lines = content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+3)):
        print(f'  {i+1}: {repr(lines[i][:100])}')
