with open('index.html', encoding='utf-8') as f:
    t = f.read()

idx = t.find('dashboardModal')
section = t[idx:idx+4000]
print('total3ra in modal:', 'total3ra' in section)
print('total4ta in file:', 'total4ta' in t)
print('genderChart canvas:', 'id="genderChart"' in t)
print('connectorChart canvas:', 'id="connectorChart"' in t)
print('periodoLabel in modal:', 'periodoLabel' in section)
print('filterMes in modal:', 'filterMes' in section)

# Also show the part of the dashboard
start = section.find('total3ra') if 'total3ra' in section else -1
if start >= 0:
    print("total3ra context:", repr(section[start-50:start+80]))
