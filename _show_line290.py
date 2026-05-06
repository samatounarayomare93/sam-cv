with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

lines = raw.split(b'\n')

# Show line 290 as exact hex
line = lines[289]  # 0-indexed
print(f"Line 290 hex: {line.hex()}")
print(f"Line 290 repr: {repr(line)}")
print()
line291 = lines[290]
print(f"Line 291 repr: {repr(line291)}")
print()

# Find the exact bytes of the broken emoji
# Look for the pattern that contains quote chars
for i, l in enumerate(lines[285:300], start=286):
    if b"''" in l or b'\x27\x27' in l or b'\x92' in l:
        print(f"Line {i} has quote issue: {repr(l[:120])}")
