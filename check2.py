with open('index.html', encoding='utf-8') as f:
    t = f.read()

# Find ALL total4ta instances
import re
for m in re.finditer('total4ta', t):
    line = t[:m.start()].count('\n') + 1
    ctx = t[m.start()-40:m.start()+60].replace('\n',' ').replace('\r','')
    print(f"Line {line}: {repr(ctx)}")

print("---")
# Find total3ra instances
for m in re.finditer('total3ra', t):
    line = t[:m.start()].count('\n') + 1
    ctx = t[m.start()-40:m.start()+60].replace('\n',' ').replace('\r','')
    print(f"Line {line}: {repr(ctx)}")
