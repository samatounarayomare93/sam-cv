"""Fix scraper.py - remove fake emails and fix encoding issues."""
import re, ast

# Read raw bytes
with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

# Try to decode - if it has encoding issues, fix them
try:
    content = raw.decode('utf-8')
except UnicodeDecodeError:
    content = raw.decode('latin-1')

# Fix broken emoji mojibake (latin-1 interpreted as utf-8)
mojibake_fixes = {
    'ðŸŒ': '🌍',
    'ðŸ"‹': '📋',
    'ðŸ›¡': '🛡',
    'âš ': '⚠',
    'âœ…': '✅',
    'ðŸš€': '🚀',
    'ðŸ"§': '🔧',
    'ðŸ"Š': '📊',
    'ðŸ"¥': '🔥',
    'ðŸ"': '📝',
    'ðŸ¤–': '🤖',
    'ðŸ§¹': '🧹',
    'ðŸŽ¯': '🎯',
    'ðŸ§ ': '🧠',
    'ðŸ"¤': '📤',
    'ðŸ"': '🔄',
    'ðŸ'¥': '💥',
    'ðŸ"': '🔐',
    'ðŸŒ': '🌐',
    'ðŸ•µ': '🕵',
    'ðŸ›°': '🛰',
    'ðŸ§¬': '🧬',
    'ðŸ'»': '💻',
    'ðŸ"': '📡',
    'ðŸ'": '💓',
    'ðŸ"': '📥',
    'ðŸ'¡': '💡',
    'ðŸ—': '🗑',
    'ðŸ¦…': '🦅',
    'ðŸ—º': '🗺',
    'â¤': '❤',
    'ðŸ'¥': '💥',
    'ðŸ"': '📡',
    'ï¸': '',  # variation selector leftover
}
for broken, fixed in mojibake_fixes.items():
    content = content.replace(broken, fixed)

# Fix broken email comment pattern: "email": ""  # comment,
# The comment got embedded inside the dict incorrectly
content = re.sub(
    r'"email":\s*""[^,\n"]*,',
    '"email": "",',
    content
)

# Also fix: "email": email or ""  # comment
content = re.sub(
    r'"email":\s*email or ""[^,\n"]*,',
    '"email": email or "",',
    content
)

# Write back clean
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
        print(f'  {i+1}: {repr(lines[i])}')
