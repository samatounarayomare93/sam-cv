import re
import ast

with open('core/scrapers/scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

print("File length:", len(content))

# Find all occurrences of the broken pattern
# Pattern 1: "email": ""  # No guessing ... real email,
# Pattern 2: "email": email or ""  # No guessing ... real email,

lines = content.split('\n')
for i, line in enumerate(lines, 1):
    if 'No guessing' in line:
        print(f"Line {i}: {repr(line)}")
