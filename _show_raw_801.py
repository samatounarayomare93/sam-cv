with open('core/scrapers/scraper.py', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
line = lines[800]  # line 801 (0-indexed)
print(f"Line 801 repr: {repr(line)}")
print(f"Line 801 hex: {line.encode('utf-8').hex()}")
print()
# Check each char
for i, c in enumerate(line):
    if ord(c) > 127 or c == '"':
        print(f"  pos {i}: char={repr(c)} ord={ord(c)} hex={ord(c):04x}")
