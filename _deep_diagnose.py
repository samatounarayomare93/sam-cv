with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

# Try to find the actual unterminated string
# The error says line 801 starts a triple-quoted string that never ends
# Let's find all triple-quote positions
content_str = raw.decode('utf-8', errors='replace')
lines = content_str.split('\n')

# Count triple quotes
triple_count = 0
for i, line in enumerate(lines):
    stripped = line.strip()
    if '"""' in stripped:
        count = stripped.count('"""')
        triple_count += count
        if count % 2 != 0:  # Odd number means it opens/closes
            print(f"Line {i+1}: {count} triple-quote(s) | running total: {triple_count} | {stripped[:60]}")

print(f"\nTotal triple-quote markers: {triple_count}")
if triple_count % 2 != 0:
    print("ODD COUNT - there's an unclosed triple-quoted string!")
else:
    print("Even count - triple quotes are balanced")

# Also check line 809 fully
print(f"\nLine 809 full: {repr(lines[808])}")
print(f"Line 810 full: {repr(lines[809])}")
