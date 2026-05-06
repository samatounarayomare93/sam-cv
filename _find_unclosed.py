with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace')
lines = content.split('\n')

# Track open/close state
in_triple = False
triple_start = None

for i, line in enumerate(lines):
    stripped = line.strip()
    # Count """ occurrences
    pos = 0
    while True:
        idx = stripped.find('"""', pos)
        if idx == -1:
            break
        if not in_triple:
            in_triple = True
            triple_start = i + 1
        else:
            in_triple = False
            triple_start = None
        pos = idx + 3

# Show the problematic area
print(f"Unclosed triple-quote started at line: {triple_start}")
print()

# Show lines around it
if triple_start:
    start = max(0, triple_start - 2)
    end = min(len(lines), triple_start + 5)
    for i in range(start, end):
        marker = " <-- UNCLOSED" if i + 1 == triple_start else ""
        print(f"{i+1:4}: {lines[i][:100]}{marker}")
