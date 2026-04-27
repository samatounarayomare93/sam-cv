import re
with open('core/pdf_generator.py', 'r', encoding='utf-8') as f: content = f.read()
content = re.sub(r'ln=True', 'new_x="LMARGIN", new_y="NEXT"', content)
with open('core/pdf_generator.py', 'w', encoding='utf-8') as f: f.write(content)
