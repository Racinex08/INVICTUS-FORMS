import re

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Replace translations
text = text.replace('🏷️ Nombre y Apellido:', '🏷️ Nombre:')
text = text.replace('🏷️ Nombre y Apellido', '🏷️ Nombre')
text = text.replace('Tu nombre completo', 'Tu nombre')

# Add history button
text = text.replace('<button id="langToggle">ES</button>', '<button id="historyBtn" class="history-btn">📋</button>\n        <button id="langToggle">ES</button>')

# Add CSS
css_to_add = """
        .history-btn {
            position: absolute;
            top: 15px;
            left: 15px;
            background-color: #f0f0f0;
            border: 1px solid #ddd;
            color: #555;
            padding: 8px 12px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 1.2rem;
            z-index: 100;
        }
        
        .modal-overlay {
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 2000;
            opacity: 0;
            pointer-events: none;
            transition: opacity 0.3s ease;
            backdrop-filter: blur(5px);
        }
        .modal-overlay.active {
            opacity: 1;
            pointer-events: auto;
        }
        .modal-content {
            background: white;
            padding: 2rem;
            border-radius: 16px;
            width: 90%;
            max-width: 400px;
            transform: translateY(20px);
            transition: transform 0.3s ease;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            position: relative;
        }
        .modal-overlay.active .modal-content {
            transform: translateY(0);
        }
        .modal-close {
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #888;
        }

        .dashboard-container {
            max-width: 800px;
            width: 95%;
        }

        .chart-wrapper {
            position: relative;
            height: 300px;
            width: 100%;
            margin-top: 20px;
        }

        .newcomer-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 15px;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-left: 4px solid var(--primary-color);
        }
        .whatsapp-btn {
            background: #25D366;
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px; height: 40px;
            display: flex; align-items: center; justify-content: center;
            text-decoration: none;
            font-size: 1.2rem;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }
"""
text = text.replace('/* --- INICIO ESTILOS NUEVO LOADER --- */', css_to_add + '\n        /* --- INICIO ESTILOS NUEVO LOADER --- */')

# Add Modals HTML
modals_html = """
    <!-- Modals -->
    <div class="modal-overlay" id="pinModal">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('pinModal')">&times;</button>
            <h3>🔒 Acceso Restringido</h3>
            <p>Ingresa el PIN de conexión:</p>
            <input type="password" id="pinInput" style="width:100%; padding: 10px; border-radius: 8px; border: 1px solid #ccc; font-size: 1.2rem; text-align: center; margin-bottom: 15px;">
            <button class="btn-primary" onclick="verifyPin()">Entrar</button>
            <p id="pinError" style="color: red; display: none; margin-top: 10px;">PIN Incorrecto</p>
        </div>
    </div>

    <div class="modal-overlay" id="historyMenuModal">
        <div class="modal-content" style="text-align: center;">
            <button class="modal-close" onclick="closeModal('historyMenuModal')">&times;</button>
            <h3>📋 Menú de Historial</h3>
            <div style="display: flex; flex-direction: column; gap: 15px; margin-top: 20px;">
                <button class="btn-primary" onclick="openDashboard()" style="background: linear-gradient(135deg, #007bff, #6610f2); border: none;">📊 Ver Resultados</button>
                <button class="btn-primary" onclick="openNewcomers()" style="background: linear-gradient(135deg, #ffc107, #fd7e14); border: none; color: #fff;">🆕 Nuevos Semanales</button>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="dashboardModal">
        <div class="modal-content dashboard-container">
            <button class="modal-close" onclick="closeModal('dashboardModal')">&times;</button>
            <h3>📊 Desempeño Invictus</h3>
            <div class="chart-wrapper">
                <canvas id="statsChart"></canvas>
            </div>
        </div>
    </div>

    <div class="modal-overlay" id="newcomersModal">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal('newcomersModal')">&times;</button>
            <h3>🆕 Nuevos Semanales</h3>
            <div id="newcomersList" style="margin-top: 15px; max-height: 300px; overflow-y: auto;">
                <p>Cargando...</p>
            </div>
        </div>
    </div>
"""

text = text.replace('</body>', modals_html + '\n</body>')

# Add Chart.js
text = text.replace('</head>', '<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>\n</head>')

# Add JS Logic
js_logic = """
        // --- LOGICA DE HISTORIAL Y DASHBOARD ---
        function openModal(id) { document.getElementById(id).classList.add('active'); }
        function closeModal(id) { document.getElementById(id).classList.remove('active'); }

        document.getElementById('historyBtn').addEventListener('click', () => {
            document.getElementById('pinInput').value = '';
            document.getElementById('pinError').style.display = 'none';
            openModal('pinModal');
        });

        function verifyPin() {
            const pin = document.getElementById('pinInput').value;
            if (pin === 'JesusRey') {
                closeModal('pinModal');
                openModal('historyMenuModal');
            } else {
                document.getElementById('pinError').style.display = 'block';
            }
        }

        let myChart = null;

        function openDashboard() {
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
        }

        function openNewcomers() {
            closeModal('historyMenuModal');
            openModal('newcomersModal');
            const list = document.getElementById('newcomersList');
            list.innerHTML = '<div style="text-align:center;"><p>Cargando datos...</p></div>';
            
            fetch(SCRIPT_URL, {
                method: 'POST',
                body: JSON.stringify({ action: 'getNewcomers' })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && data.nuevos && data.nuevos.length > 0) {
                    list.innerHTML = data.nuevos.map(n => `
                        <div class="newcomer-card">
                            <div>
                                <h4 style="margin:0 0 5px 0;">${n.nombre}</h4>
                                <small style="color:#666;">Conector: ${n.conector}</small>
                            </div>
                            <a href="https://wa.me/${n.telefono.replace(/[^\\d]/g, '')}" target="_blank" class="whatsapp-btn">💬</a>
                        </div>
                    `).join('');
                } else {
                    list.innerHTML = '<p>No hay nuevos registrados en los últimos 7 días.</p>';
                }
            }).catch(e => {
                list.innerHTML = '<p>Error cargando los datos.</p>';
            });
        }
"""

text = text.replace('// --- LÓGICA DE NOTIFICACIONES PUSH & AUTOMÁTICAS ---', js_logic + '\n        // --- LÓGICA DE NOTIFICACIONES PUSH & AUTOMÁTICAS ---')

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'w', encoding='utf-8') as f:
    f.write(text)
