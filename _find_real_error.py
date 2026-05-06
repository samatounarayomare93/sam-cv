"""Find the REAL unclosed string before line 801"""
import re

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')
lines = content.split('\n')

# Manually track string state line by line
# Look for f-strings or regular strings that open but don't close
print("Scanning for unclosed strings before line 801...")
print()

# Check every line from 700-800 for unclosed quotes
for i in range(699, 801):
    if i >= len(lines):
        break
    line = lines[i]
    
    # Check for f-string with { that might contain """
    if 'f"' in line or "f'" in line:
        # Check if it has unbalanced braces
        open_b = line.count('{')
        close_b = line.count('}')
        if open_b != close_b:
            print(f"Line {i+1} UNBALANCED BRACES ({open_b} open, {close_b} close): {repr(line[:80])}")
    
    # Check for lines ending mid-string
    # Count single quotes (not in triple)
    stripped = line.rstrip('\r\n')
    if stripped.endswith('\\'):
        print(f"Line {i+1} LINE CONTINUATION: {repr(stripped[:80])}")

print()
print("=== Lines 750-802 checking for issues ===")
for i in range(749, 802):
    if i >= len(lines):
        break
    line = lines[i]
    if any(x in line for x in ['salary.replace', "replace('", 'replace("']):
        print(f"Line {i+1}: {repr(line[:100])}")
