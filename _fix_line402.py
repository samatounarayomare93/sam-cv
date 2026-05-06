"""Fix the broken string on line 402 of scraper.py"""
import ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')
lines = content.split('\n')

# Show lines 400-415 to understand the full context
print("=== Lines 400-415 ===")
for i in range(399, 415):
    print(f"{i+1:4}: {repr(lines[i])}")

print()

# Fix line 402: the string ' -' is broken across lines
# Find and fix it
fixed_lines = []
i = 0
while i < len(lines):
    line = lines[i]
    
    # Fix broken safe_company line: c in ' -\n').strip()
    if "c in ' -" in line and not line.rstrip().endswith("' -').strip()"):
        # Check if next line has the closing
        if i + 1 < len(lines) and "').strip()" in lines[i+1]:
            # Merge the two lines
            merged = line.rstrip() + "').strip()"
            fixed_lines.append(merged)
            i += 2  # skip next line
            print(f"Fixed broken string at line {i}: merged with next line")
            continue
        else:
            # Just close the string on this line
            fixed = line.rstrip() + "').strip()"
            fixed_lines.append(fixed)
            print(f"Fixed broken string at line {i+1}")
            i += 1
            continue
    
    fixed_lines.append(line)
    i += 1

content = '\n'.join(fixed_lines)

# Also fix the email comment issue
import re
content = re.sub(r'"email":\s*""[^\n"]*,', '"email": "",', content)
content = re.sub(r'"email":\s*email or ""[^\n"]*,', '"email": email or "",', content)
content = re.sub(r'valid_emails\.append\(f"careers@\{[^}]+\}"\)', 'pass  # No fake emails', content)
content = content.replace('\u2014', '-').replace('\u2013', '-')

# Verify
try:
    ast.parse(content)
    print('OK - syntax clean!')
    with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print('Saved successfully')
except SyntaxError as e:
    print(f'Still broken at line {e.lineno}: {e.msg}')
    lines2 = content.split('\n')
    for j in range(max(0, e.lineno-5), min(len(lines2), e.lineno+3)):
        print(f'  {j+1}: {repr(lines2[j][:90])}')
