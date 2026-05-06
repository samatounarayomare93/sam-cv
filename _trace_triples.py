with open('core/scrapers/scraper.py', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

# Manually trace triple-quote state line by line
in_triple = False
triple_char = None

for line_num, line in enumerate(lines, 1):
    if line_num > 810:
        break
    
    i = 0
    while i < len(line):
        if not in_triple:
            if line[i:i+3] in ('"""', "'''"):
                triple_char = line[i:i+3]
                in_triple = True
                i += 3
                continue
        else:
            if line[i:i+3] == triple_char:
                in_triple = False
                triple_char = None
                i += 3
                continue
        i += 1
    
    # After processing line, if we're in a triple quote that spans lines, it continues
    # But single-line docstrings open and close on same line
    
    if in_triple and line_num >= 285:
        print(f"Line {line_num}: OPEN triple ({triple_char}) | {line[:80]}")
    elif not in_triple and line_num >= 285 and line_num <= 295:
        print(f"Line {line_num}: closed | {line[:80]}")

print(f"\nFinal state: in_triple={in_triple}, char={triple_char}")
