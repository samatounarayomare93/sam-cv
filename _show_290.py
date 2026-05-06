with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()
content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')
lines = content.split('\n')

print("=== Lines 285-300 (raw repr) ===")
for i in range(284, 302):
    if i < len(lines):
        print(f"{i+1:4}: {repr(lines[i])}")
