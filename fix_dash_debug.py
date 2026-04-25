with open('index.html', encoding='utf-8') as f:
    text = f.read()

# Fix dashboard to show data even if totalGlobal is 0 from AppScript
# Also add a console.log to debug what the server returns
old_then = """            .then(r => r.json())
            .then(data => {
                document.getElementById('dashLoading').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'flex';

                const nuevos        = data.nuevos || [];
                const totalGlobal   = data.totalGlobal || nuevos.length;
                const total3raVal   = data.total3ra || 0;
                const connGlobal    = data.conectoresGlobal || {};"""

new_then = """            .then(r => r.json())
            .then(data => {
                console.log('Dashboard data:', JSON.stringify(data));
                document.getElementById('dashLoading').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'flex';

                const nuevos        = data.nuevos || [];
                const totalGlobal   = data.totalGlobal || nuevos.length;
                const total3raVal   = data.total3ra || 0;
                const connGlobal    = data.conectoresGlobal || {};"""

text = text.replace(old_then, new_then)

# Fix: make sure dashboardContent is properly shown
# It sometimes gets stuck at display:none due to CSS specificity
old_show = "document.getElementById('dashboardContent').style.display = 'flex';"
new_show = "const dc = document.getElementById('dashboardContent'); dc.style.cssText = dc.style.cssText.replace('display: none', ''); dc.style.display = 'flex';"
# Only replace in the loadDashboardData function (first occurrence after the fetch)
text = text.replace(old_show, new_show, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
