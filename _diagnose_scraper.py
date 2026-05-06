with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

lines = raw.split(b'\n')
print(f"Total lines: {len(lines)}")
print(f"Total bytes: {len(raw)}")
print()

# Show lines 798-810 as raw bytes
print("=== Raw bytes lines 798-810 ===")
for i in range(797, min(812, len(lines))):
    print(f"{i+1:4}: {lines[i][:120]}")

print()
# Find the actual broken spot
print("=== Lines 845-852 ===")
for i in range(844, min(853, len(lines))):
    print(f"{i+1:4}: {lines[i][:120]}")
