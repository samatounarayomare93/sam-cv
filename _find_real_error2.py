"""Find the REAL unclosed string - check salary.replace lines"""
with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')
lines = content.split('\n')

# Show ALL lines from 395-420 (where salary.replace was before)
print("=== Lines 395-430 ===")
for i in range(394, 430):
    if i < len(lines):
        print(f"{i+1:4}: {repr(lines[i][:100])}")
