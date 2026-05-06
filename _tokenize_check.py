import tokenize, io

with open('core/scrapers/scraper.py', 'rb') as f:
    raw = f.read()

content = raw.decode('utf-8', errors='replace').replace('\ufffd', '')

try:
    tokens = list(tokenize.generate_tokens(io.StringIO(content).readline))
    print(f"OK - {len(tokens)} tokens, no syntax errors")
except tokenize.TokenError as e:
    msg, (line, col) = e.args
    print(f"TokenError at line {line}, col {col}: {msg}")
    lines = content.split('\n')
    for i in range(max(0, line-5), min(len(lines), line+3)):
        print(f"  {i+1}: {repr(lines[i][:90])}")
except Exception as e:
    print(f"Error: {e}")
