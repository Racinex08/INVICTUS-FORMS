import re
with open('index.html', encoding='utf-8') as f:
    t = f.read()
for m in re.finditer(r'id="(dashboardModal|newcomersModal|historyMenuModal)"', t):
    line = t[:m.start()].count('\n')+1
    print(f'{m.group(1)} at line {line}')
