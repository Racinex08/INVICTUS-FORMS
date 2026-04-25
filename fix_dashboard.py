import re

with open('index.html', encoding='utf-8') as f:
    text = f.read()

# Fix 1: The <body>\n literal text corruption
text = text.replace('<body>\\n\r\n', '<body>\r\n')
text = text.replace('<body>\\n\n', '<body>\n')

# Fix 2: Remove any lingering history-btn class style blocks from CSS
text = re.sub(r'\s*\.history-btn\s*\{[^}]*\}', '', text)

# Fix 3: Replace the broken dashboard modal with a proper content-rich one
old_dash = '''    <div class="modal-overlay" id="dashboardModal">
        <div class="modal-content dashboard-container">
            <button class="modal-close" onclick="closeModal('dashboardModal')">&times;</button>
            <h3>📊 Desempeño Invictus</h3>
            <div class="chart-wrapper">
                <canvas id="statsChart"></canvas>
            </div>
        </div>
    </div>'''

new_dash = '''    <div class="modal-overlay" id="dashboardModal">
        <div class="modal-content dashboard-container" style="max-width:600px; max-height:90vh; overflow-y:auto;">
            <button class="modal-close" onclick="closeModal('dashboardModal')">&times;</button>
            <h3 style="margin-top:0;">📊 Desempeño Invictus</h3>
            <div id="dashboardContent" style="display:flex; flex-direction:column; gap:18px;">
                <!-- Tarjetas de métricas -->
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;" id="metricCards">
                    <div style="background:linear-gradient(135deg,#007bff,#6610f2);border-radius:12px;padding:16px;color:white;text-align:center;">
                        <div style="font-size:2rem;font-weight:800;" id="totalRegistrados">—</div>
                        <div style="font-size:0.8rem;opacity:0.9;">Total Registrados</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#28a745,#20c997);border-radius:12px;padding:16px;color:white;text-align:center;">
                        <div style="font-size:2rem;font-weight:800;" id="totalNuevosSemana">—</div>
                        <div style="font-size:0.8rem;opacity:0.9;">Nuevos esta semana</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#0dcaf0,#0d6efd);border-radius:12px;padding:16px;color:white;text-align:center;">
                        <div style="font-size:2rem;font-weight:800;" id="totalHombres">—</div>
                        <div style="font-size:0.8rem;opacity:0.9;">👨 Hombres</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#fd7e14,#dc3545);border-radius:12px;padding:16px;color:white;text-align:center;">
                        <div style="font-size:2rem;font-weight:800;" id="totalMujeres">—</div>
                        <div style="font-size:0.8rem;opacity:0.9;">👩 Mujeres</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#ffc107,#fd7e14);border-radius:12px;padding:16px;color:white;text-align:center;">
                        <div style="font-size:2rem;font-weight:800;" id="totalIglesia">—</div>
                        <div style="font-size:0.8rem;opacity:0.9;">⛪ Asisten a Iglesia</div>
                    </div>
                    <div style="background:linear-gradient(135deg,#6f42c1,#e83e8c);border-radius:12px;padding:16px;color:white;text-align:center;">
                        <div style="font-size:2rem;font-weight:800;" id="total4ta">—</div>
                        <div style="font-size:0.8rem;opacity:0.9;">🌟 En 4ta Asistencia</div>
                    </div>
                </div>
                <!-- Gráfico de Géneros -->
                <div style="background:#f8f9fa;border-radius:12px;padding:16px;">
                    <h4 style="margin:0 0 12px 0;color:#333;">📊 Distribución por Género</h4>
                    <div style="position:relative;height:220px;"><canvas id="genderChart"></canvas></div>
                </div>
                <!-- Gráfico por Conectores -->
                <div style="background:#f8f9fa;border-radius:12px;padding:16px;">
                    <h4 style="margin:0 0 12px 0;color:#333;">🔗 Personas por Conector</h4>
                    <div style="position:relative;height:250px;"><canvas id="connectorChart"></canvas></div>
                </div>
                <!-- Lista de nuevos semanales -->
                <div style="background:#f8f9fa;border-radius:12px;padding:16px;">
                    <h4 style="margin:0 0 12px 0;color:#333;">🆕 Nuevos esta semana</h4>
                    <div id="dashNuevos" style="max-height:300px;overflow-y:auto;"></div>
                </div>
            </div>
            <div id="dashLoading" style="text-align:center;padding:40px 0;display:none;">
                <div style="font-size:2rem;margin-bottom:10px;">⏳</div>
                <p style="color:#888;">Cargando datos en tiempo real...</p>
            </div>
        </div>
    </div>'''

text = text.replace(old_dash, new_dash)

# Fix 4: Replace renderChart() JS function with a rich dashboard loader
old_fn = """        function openDashboard() {
            closeModal('historyMenuModal');
            openModal('dashboardModal');
            renderChart();
        }

        function renderChart() {
            const ctx = document.getElementById('statsChart').getContext('2d');
            if (myChart) myChart.destroy();
            
            // Datos de ejemplo para animar el dashboard al estilo apple (suave)
            myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4'],
                    datasets: [{
                        label: 'Asistencia General',
                        data: [12, 19, 25, 30],
                        borderColor: '#007bff',
                        backgroundColor: 'rgba(0,123,255,0.2)',
                        tension: 0.4, // apple style curves
                        fill: true
                    }, {
                        label: 'Personas Nuevas',
                        data: [5, 2, 8, 4],
                        borderColor: '#28a745',
                        backgroundColor: 'rgba(40,167,69,0.2)',
                        tension: 0.4,
                        fill: true
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    animation: {
                        duration: 2500,
                        easing: 'easeOutQuart'
                    },
                    plugins: {
                        legend: { position: 'bottom' }
                    }
                }
            });
        }"""

new_fn = """        let chartGender = null;
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
                animateCount(document.getElementById('total4ta'), 0);

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
        }"""

text = text.replace(old_fn, new_fn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
