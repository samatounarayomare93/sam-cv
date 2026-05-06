"""Find exact syntax error location in scraper.py"""
import ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')
lines = content.split('\n')

# Show lines 840-860
print("=== Lines 840-860 ===")
for i in range(839, min(860, len(lines))):
    print(f"{i+1:4}: {repr(lines[i][:100])}")

print()

# Find all lines with non-standard chars
print("=== Lines with non-ASCII issues ===")
for i, line in enumerate(lines):
    if any(ord(c) > 127 and ord(c) < 160 for c in line):
        print(f"{i+1:4}: {repr(line[:100])}")
