with open('index.html', encoding='utf-8') as f:
    text = f.read()

# ---- 1. Fix "4ta" -> "3ra" in dashboard card HTML ----
text = text.replace('🌟 En 4ta Asistencia', '🌟 En 3ra Asistencia')
text = text.replace('En 4ta Asistencia', 'En 3ra Asistencia')

# ---- 2. Insert month/year filter UI right after <h3>📊 Desempeño Invictus</h3> ----
filter_html = '''
            <!-- Filtro por mes y año -->
            <div style="background:linear-gradient(135deg,#e8f0fe,#f3e5f5);border-radius:12px;padding:14px 16px;display:flex;gap:10px;align-items:center;flex-wrap:wrap;border:1px solid #d0d7f0;">
                <span style="font-weight:700;color:#333;font-size:0.9rem;">📅 Período:</span>
                <select id="filterMes" onchange="applyDashFilter()" style="padding:8px 12px;border-radius:8px;border:1px solid #c5cbe0;font-size:0.88rem;background:white;flex:1;min-width:110px;">
                    <option value="1">Enero</option>
                    <option value="2">Febrero</option>
                    <option value="3">Marzo</option>
                    <option value="4">Abril</option>
                    <option value="5">Mayo</option>
                    <option value="6">Junio</option>
                    <option value="7">Julio</option>
                    <option value="8">Agosto</option>
                    <option value="9">Septiembre</option>
                    <option value="10">Octubre</option>
                    <option value="11">Noviembre</option>
                    <option value="12">Diciembre</option>
                </select>
                <select id="filterAño" onchange="applyDashFilter()" style="padding:8px 12px;border-radius:8px;border:1px solid #c5cbe0;font-size:0.88rem;background:white;width:90px;">
                    <option value="2025">2025</option>
                    <option value="2026">2026</option>
                    <option value="2027">2027</option>
                </select>
                <button onclick="clearDashFilter()" style="padding:8px 14px;border-radius:8px;border:none;background:#6c757d;color:white;font-size:0.82rem;font-weight:700;cursor:pointer;">↩ Esta semana</button>
            </div>
            <!-- Etiqueta del periodo activo -->
            <div id="periodoLabel" style="text-align:center;font-size:0.82rem;color:#666;font-style:italic;margin-top:-8px;">Mostrando: últimos 7 días</div>
'''

text = text.replace(
    '<div id="dashboardContent" style="display:flex; flex-direction:column; gap:18px;">',
    '<div id="dashboardContent" style="display:flex; flex-direction:column; gap:18px;">' + filter_html
)

# ---- 3. Change card label for metric id ----
# The card already has id="total4ta", rename to total3ra
text = text.replace('id="total4ta"', 'id="total3ra"')

# ---- 4. Replace the entire openDashboard + renderChart JS block ----
old_js = '''        let chartGender = null;
        let chartConnector = null;

        function animateCount(el, target, dur=1000) {
            const start = performance.now();
            (function step(now) {
                const p = Math.min((now - start) / dur, 1);
                const ease = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.floor(ease * target);
                if (p < 1) requestAnimationFrame(step);
                else el.textContent = target;
            })(start);
        }

        function openDashboard() {
            closeModal('historyMenuModal');
            openModal('dashboardModal');
            document.getElementById('dashLoading').style.display = 'block';
            document.getElementById('dashboardContent').style.display = 'none';

            fetch(SCRIPT_URL, {
                method: 'POST',
                mode: 'cors',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify({ action: 'getNewcomers' })
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('dashLoading').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'flex';

                const nuevos = data.nuevos || [];
                // Conteos desde los nuevos (semana)
                const hombresS = nuevos.filter(n => n.sexo === 'M').length;
                const mujeresS = nuevos.filter(n => n.sexo === 'F').length;
                const iglesiaS = nuevos.filter(n => n.asisteIglesia && n.asisteIglesia !== 'N/A' && n.asisteIglesia !== 'No').length;

                // Animar métricas
                animateCount(document.getElementById('totalNuevosSemana'), nuevos.length);
                animateCount(document.getElementById('totalHombres'), hombresS);
                animateCount(document.getElementById('totalMujeres'), mujeresS);
                animateCount(document.getElementById('totalIglesia'), iglesiaS);
                animateCount(document.getElementById('totalRegistrados'), nuevos.length);
                animateCount(document.getElementById('total3ra'), 0);

                // Gráfico circular Géneros
                if (chartGender) chartGender.destroy();
                chartGender = new Chart(document.getElementById('genderChart'), {
                    type: 'doughnut',
                    data: {
                        labels: ['👨 Masculino', '👩 Femenino'],
                        datasets: [{ data: [hombresS, mujeresS],
                            backgroundColor: ['#0d6efd','#fd7e14'],
                            borderWidth: 0 }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        animation: { animateRotate: true, duration: 1500, easing: 'easeOutQuart' },
                        plugins: { legend: { position: 'bottom' } }
                    }
                });

                // Gráfico de barras por Conector
                const connCount = {};
                nuevos.forEach(n => { connCount[n.conector || 'Sin asignar'] = (connCount[n.conector || 'Sin asignar'] || 0) + 1; });
                const connLabels = Object.keys(connCount);
                const connData   = Object.values(connCount);
                const barColors  = ['#007bff','#6610f2','#28a745','#fd7e14','#dc3545','#20c997','#ffc107'];
                if (chartConnector) chartConnector.destroy();
                chartConnector = new Chart(document.getElementById('connectorChart'), {
                    type: 'bar',
                    data: {
                        labels: connLabels,
                        datasets: [{ label: 'Personas', data: connData,
                            backgroundColor: connLabels.map((_, i) => barColors[i % barColors.length]),
                            borderRadius: 8, borderSkipped: false }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        animation: { duration: 1500, easing: 'easeOutQuart' },
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
                    }
                });

                // Lista de nuevos detallada
                const dashNuevos = document.getElementById('dashNuevos');
                if (nuevos.length === 0) {
                    dashNuevos.innerHTML = '<p style="color:#888;text-align:center;">No hay nuevos esta semana aún.</p>';
                } else {
                    dashNuevos.innerHTML = nuevos.map(n => `
                        <div style="background:white;border-radius:10px;padding:12px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;border-left:4px solid #007bff;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                            <div>
                                <strong style="font-size:0.95rem;">${n.nombre}</strong>
                                <div style="font-size:0.78rem;color:#555;margin-top:3px;">
                                    ${n.sexo === 'M' ? '👨' : '👩'} ${n.sexo === 'M' ? 'Masculino' : 'Femenino'} &nbsp;|&nbsp;
                                    🔗 ${n.conector || '—'} &nbsp;|&nbsp;
                                    ⛪ ${(n.asisteIglesia && n.asisteIglesia !== 'N/A') ? 'Sí — ' + (n.iglesiaNombre || '') : 'No'}
                                </div>
                                <div style="font-size:0.78rem;color:#888;">Invitado por: ${n.invitadoPor || 'N/A'}</div>
                            </div>
                            <a href="https://wa.me/${(n.telefono || '').replace(/[^\\d]/g, '')}" target="_blank" class="whatsapp-btn" style="width:38px;height:38px;font-size:1.1rem;flex-shrink:0;">💬</a>
                        </div>
                    `).join('');
                }
            })
            .catch(e => {
                document.getElementById('dashLoading').innerHTML = '<p style="color:red;">Error cargando datos. Verifica la conexión.</p>';
                console.error(e);
            });
        }'''

new_js = '''        let chartGender = null;
        let chartConnector = null;
        let dashFilterMode = 'week'; // 'week' or 'month'

        function animateCount(el, target, dur=1000) {
            if (!el) return;
            const start = performance.now();
            (function step(now) {
                const p = Math.min((now - start) / dur, 1);
                const ease = 1 - Math.pow(1 - p, 3);
                el.textContent = Math.floor(ease * target);
                if (p < 1) requestAnimationFrame(step);
                else el.textContent = target;
            })(start);
        }

        function setDefaultFilter() {
            const now = new Date();
            const mesEl = document.getElementById('filterMes');
            const añoEl = document.getElementById('filterAño');
            if (mesEl) mesEl.value = String(now.getMonth() + 1);
            if (añoEl) añoEl.value = String(now.getFullYear());
        }

        function openDashboard() {
            closeModal('historyMenuModal');
            openModal('dashboardModal');
            dashFilterMode = 'week';
            setDefaultFilter();
            document.getElementById('periodoLabel').textContent = 'Mostrando: últimos 7 días';
            loadDashboardData({});
        }

        function applyDashFilter() {
            const mes = document.getElementById('filterMes').value;
            const año = document.getElementById('filterAño').value;
            const meses = ['','Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre'];
            dashFilterMode = 'month';
            document.getElementById('periodoLabel').textContent = `Mostrando: ${meses[parseInt(mes)]} ${año}`;
            loadDashboardData({ mes, año });
        }

        function clearDashFilter() {
            dashFilterMode = 'week';
            document.getElementById('periodoLabel').textContent = 'Mostrando: últimos 7 días';
            loadDashboardData({});
        }

        function loadDashboardData(params) {
            document.getElementById('dashLoading').style.display = 'block';
            document.getElementById('dashboardContent').style.display = 'none';

            const body = { action: 'getNewcomers', ...params };

            fetch(SCRIPT_URL, {
                method: 'POST',
                mode: 'cors',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify(body)
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('dashLoading').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'flex';

                const nuevos        = data.nuevos || [];
                const totalGlobal   = data.totalGlobal || nuevos.length;
                const total3raVal   = data.total3ra || 0;
                const connGlobal    = data.conectoresGlobal || {};

                const hombresS = nuevos.filter(n => n.sexo === 'M').length;
                const mujeresS = nuevos.filter(n => n.sexo === 'F').length;
                const iglesiaS = nuevos.filter(n => n.asisteIglesia && n.asisteIglesia !== 'N/A' && n.asisteIglesia !== 'No').length;

                // Animate metric cards
                animateCount(document.getElementById('totalRegistrados'),   totalGlobal);
                animateCount(document.getElementById('totalNuevosSemana'),  nuevos.length);
                animateCount(document.getElementById('totalHombres'),       hombresS);
                animateCount(document.getElementById('totalMujeres'),       mujeresS);
                animateCount(document.getElementById('totalIglesia'),       iglesiaS);
                animateCount(document.getElementById('total3ra'),           total3raVal);

                // Update "nuevos" card label dynamically
                const nuevosSub = document.querySelector('#totalNuevosSemana + div, #totalNuevosSemana ~ div');

                // Gender doughnut chart
                if (chartGender) chartGender.destroy();
                chartGender = new Chart(document.getElementById('genderChart'), {
                    type: 'doughnut',
                    data: {
                        labels: ['👨 Masculino', '👩 Femenino'],
                        datasets: [{ data: [hombresS, mujeresS],
                            backgroundColor: ['#0d6efd','#fd7e14'], borderWidth: 0 }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        animation: { animateRotate: true, duration: 1500, easing: 'easeOutQuart' },
                        plugins: { legend: { position: 'bottom' } }
                    }
                });

                // Connector bar chart — use global connectors for richer data
                const connSource = Object.keys(connGlobal).length > 0 ? connGlobal
                    : nuevos.reduce((acc, n) => { const k = n.conector||'Sin asignar'; acc[k]=(acc[k]||0)+1; return acc; }, {});
                const connLabels = Object.keys(connSource);
                const connData   = Object.values(connSource);
                const barColors  = ['#007bff','#6610f2','#28a745','#fd7e14','#dc3545','#20c997','#ffc107'];
                if (chartConnector) chartConnector.destroy();
                chartConnector = new Chart(document.getElementById('connectorChart'), {
                    type: 'bar',
                    data: {
                        labels: connLabels,
                        datasets: [{ label: 'Personas', data: connData,
                            backgroundColor: connLabels.map((_, i) => barColors[i % barColors.length]),
                            borderRadius: 8, borderSkipped: false }]
                    },
                    options: {
                        responsive: true, maintainAspectRatio: false,
                        animation: { duration: 1500, easing: 'easeOutQuart' },
                        plugins: { legend: { display: false } },
                        scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } }
                    }
                });

                // Newcomers list
                const dashNuevos = document.getElementById('dashNuevos');
                if (nuevos.length === 0) {
                    dashNuevos.innerHTML = '<p style="color:#888;text-align:center;padding:20px 0;">No hay registros en este período.</p>';
                } else {
                    dashNuevos.innerHTML = nuevos.map(n => `
                        <div style="background:white;border-radius:10px;padding:12px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center;border-left:4px solid #007bff;box-shadow:0 1px 4px rgba(0,0,0,0.06);">
                            <div style="flex:1;min-width:0;">
                                <strong style="font-size:0.95rem;">${n.nombre}</strong>
                                <div style="font-size:0.78rem;color:#555;margin-top:3px;">
                                    ${n.sexo === 'M' ? '👨 Masculino' : '👩 Femenino'} &nbsp;|&nbsp; 🔗 ${n.conector || '—'}
                                </div>
                                <div style="font-size:0.78rem;color:#777;">
                                    ⛪ ${(n.asisteIglesia && n.asisteIglesia !== 'N/A' && n.asisteIglesia !== 'No') ? 'Sí — '+(n.iglesiaNombre||'') : 'No asiste'} &nbsp;|&nbsp; 👥 ${n.invitadoPor||'N/A'}
                                </div>
                            </div>
                            <a href="https://wa.me/${(n.telefono||'').replace(/[^\\d]/g,'')}" target="_blank" class="whatsapp-btn" style="width:38px;height:38px;font-size:1.1rem;flex-shrink:0;margin-left:10px;">💬</a>
                        </div>
                    `).join('');
                }
            })
            .catch(e => {
                document.getElementById('dashLoading').style.display = 'none';
                document.getElementById('dashboardContent').style.display = 'flex';
                document.getElementById('dashNuevos').innerHTML = '<p style="color:red;text-align:center;">Error cargando datos. Verifica la conexión.</p>';
                console.error(e);
            });
        }'''

text = text.replace(old_js, new_js)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
