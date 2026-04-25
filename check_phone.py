import re
with open('index.html', encoding='utf-8') as f:
    t = f.read()

for m in re.finditer(r'id="(phone|phoneCheck)"', t):
    line = t[:m.start()].count('\n')+1
    print(f'Line {line}: {repr(t[m.start()-30:m.start()+60])}')
