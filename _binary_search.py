"""Binary search for the broken line"""
import ast

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')
lines = content.split('\n')
total = len(lines)
print(f"Total lines: {total}")

# Binary search
lo, hi = 0, total
while lo < hi - 1:
    mid = (lo + hi) // 2
    chunk = '\n'.join(lines[:mid])
    try:
        ast.parse(chunk)
        lo = mid  # first half is OK, problem is in second half
    except SyntaxError:
        hi = mid  # problem is in first half

print(f"Problem is around line {hi}")
print()
print(f"Lines {max(1,hi-5)} to {min(total,hi+5)}:")
for i in range(max(0,hi-6), min(total,hi+5)):
    print(f"  {i+1:4}: {repr(lines[i][:100])}")
