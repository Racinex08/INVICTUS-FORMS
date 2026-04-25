import re

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Patrón original exacto
old_code = """        function openNewcomers() {
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
        }"""

new_code = """        function openNewcomers() {
            closeModal('historyMenuModal');
            openModal('newcomersModal');
            const list = document.getElementById('newcomersList');
            list.innerHTML = '<div style="text-align:center;"><p>Cargando datos...</p></div>';
            
            fetch(SCRIPT_URL, {
                method: 'POST',
                mode: 'cors',
                headers: { 'Content-Type': 'text/plain;charset=utf-8' },
                body: JSON.stringify({ action: 'getNewcomers' })
            })
            .then(res => res.json())
            .then(data => {
                if (data.success && data.nuevos && data.nuevos.length > 0) {
                    list.innerHTML = data.nuevos.map(n => `
                        <div class="newcomer-card" style="display:flex; flex-direction:column; align-items:flex-start;">
                            <div style="display:flex; justify-content:space-between; width:100%; align-items:center; border-bottom:1px solid #ebebeb; padding-bottom:8px; margin-bottom:8px;">
                                <h4 style="margin:0;">${n.nombre}</h4>
                                <a href="https://wa.me/${(n.telefono || '').replace(/[^\\d]/g, '')}" target="_blank" class="whatsapp-btn" style="width:35px; height:35px; font-size:1.1rem;">💬</a>
                            </div>
                            <small style="color:#555; margin-bottom: 2px;"><strong>Asociado (Conector):</strong> ${n.conector}</small>
                            <small style="color:#555; margin-bottom: 2px;"><strong>Invitado por:</strong> ${n.invitadoPor || 'N/A'}</small>
                            <small style="color:#555; margin-bottom: 2px;"><strong>Sexo:</strong> ${n.sexo === 'M' ? '👨 Masculino' : (n.sexo === 'F' ? '👩 Femenino' : 'N/A')}</small>
                            <small style="color:#555; margin-bottom: 2px;"><strong>Asiste a Iglesia:</strong> ${n.asisteIglesia === 'SÍ' ? 'Sí, a ' + (n.iglesiaNombre || '') : 'No'}</small>
                        </div>
                    `).join('');
                } else {
                    list.innerHTML = '<p>No hay nuevos registrados en los últimos 7 días.</p>';
                }
            }).catch(e => {
                list.innerHTML = '<p>Error cargando los datos. Por favor revisa la conexión.</p>';
                console.error("Fetch Error:", e);
            });
        }"""

text = text.replace(old_code, new_code)

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'w', encoding='utf-8') as f:
    f.write(text)
