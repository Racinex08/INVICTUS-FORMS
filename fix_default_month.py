with open('index.html', encoding='utf-8') as f:
    text = f.read()

# Change openDashboard() to default to current month/year instead of week
old_open = """        function openDashboard() {
            closeModal('historyMenuModal');
            openModal('dashboardModal');
            dashFilterMode = 'week';
            setDefaultFilter();
            document.getElementById('periodoLabel').textContent = 'Mostrando: últimos 7 días';
            loadDashboardData({});
        }"""

new_open = """        function openDashboard() {
            closeModal('historyMenuModal');
            openModal('dashboardModal');
            dashFilterMode = 'month';
            setDefaultFilter();
            // Default: load current month automatically
            const now = new Date();
            const mes = String(now.getMonth() + 1);
            const año = String(now.getFullYear());
            const meses = ['','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
            document.getElementById('periodoLabel').textContent = `Mostrando: ${meses[parseInt(mes)]} ${año}`;
            loadDashboardData({ mes, año });
        }"""

text = text.replace(old_open, new_open)

# Also fix "Nuevos esta semana" card label to "Nuevos del mes"
text = text.replace('Nuevos esta semana</div>', 'Nuevos del mes</div>')

# Also update "clearDashFilter" to show week label
old_clear = """        function clearDashFilter() {
            dashFilterMode = 'week';
            document.getElementById('periodoLabel').textContent = 'Mostrando: últimos 7 días';
            loadDashboardData({});
        }"""

new_clear = """        function clearDashFilter() {
            dashFilterMode = 'week';
            document.getElementById('periodoLabel').textContent = 'Mostrando: últimos 7 días';
            loadDashboardData({ semana: true });
        }"""

text = text.replace(old_clear, new_clear)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
