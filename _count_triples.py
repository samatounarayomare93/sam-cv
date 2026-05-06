with open('core/scrapers/scraper.py', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
in_triple = False
triple_char = None
open_line = None

i = 0
while i < len(content):
    if not in_triple:
        if content[i:i+3] == '"""':
            in_triple = True
            triple_char = '"""'
            # Find which line
            line_num = content[:i].count('\n') + 1
            open_line = line_num
            i += 3
            continue
        elif content[i:i+3] == "'''":
            in_triple = True
            triple_char = "'''"
            line_num = content[:i].count('\n') + 1
            open_line = line_num
            i += 3
            continue
    else:
        if content[i:i+3] == triple_char:
            in_triple = False
            triple_char = None
            open_line = None
            i += 3
            continue
    i += 1

if in_triple:
    print(f"UNCLOSED triple-quote ({triple_char}) opened at line {open_line}")
    # Show context
    for j in range(max(0, open_line-2), min(len(lines), open_line+3)):
        print(f"  {j+1}: {lines[j][:100]}")
else:
    print("All triple-quotes are balanced!")
