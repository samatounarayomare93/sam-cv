import ast, re
with open('core/scrapers/scraper.py', encoding='utf-8') as f:
    content = f.read()
try:
    ast.parse(content)
    fake = len(re.findall(r'careers@.*replace|info@.*replace', content))
    empty = content.count('"email": ""')
    print(f'OK  scraper.py - syntax clean')
    print(f'    Fake email patterns: {fake} (should be 0)')
    print(f'    Empty email fields: {empty}')
except SyntaxError as e:
    print(f'ERR line {e.lineno}: {e.msg}')
    lines = content.split('\n')
    for i in range(max(0, e.lineno-3), min(len(lines), e.lineno+3)):
        print(f'  {i+1}: {repr(lines[i][:100])}')
