import ast

with open('core/scrapers/scraper.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')

print("Lines around 405-412:")
for i in range(403, 415):
    print(f"  {i+1}: {repr(lines[i])}")

# Find and fix the broken salary line
# The broken pattern is two consecutive lines:
#   line N:   "salary": salary.replace('
#   line N+1: $', '').replace(',', ''),
# Should be merged into:
#   "salary": salary.replace('$', '').replace(',', ''),

fixed_lines = []
i = 0
skip_next = False
while i < len(lines):
    if skip_next:
        skip_next = False
        i += 1
        continue
    
    line = lines[i]
    # Check if this line ends with salary.replace(' (with possible trailing whitespace/newline)
    stripped = line.rstrip()
    if stripped.endswith("salary.replace('") and i + 1 < len(lines):
        next_line = lines[i + 1]
        next_stripped = next_line.strip()
        # The next line should start with $', '').replace(',', ''),
        if next_stripped.startswith("$', '').replace(',', ''),"):
            # Merge: replace the broken end with the full expression
            merged = stripped + "$', '').replace(',', ''),"
            fixed_lines.append(merged)
            skip_next = True
            print(f"Fixed broken salary at line {i+1}")
            i += 1
            continue
    
    fixed_lines.append(line)
    i += 1

content = '\n'.join(fixed_lines)

# Verify
try:
    ast.parse(content)
    print("SYNTAX OK after salary fix")
except SyntaxError as e:
    print(f"Still broken: {e}")
    err_line = e.lineno
    if err_line:
        start = max(0, err_line - 10)
        end = min(len(fixed_lines), err_line + 5)
        for j in range(start, end):
            marker = ">>>" if j + 1 == err_line else "   "
            print(f"{marker} {j+1}: {repr(fixed_lines[j])}")

with open('core/scrapers/scraper.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("File written.")
