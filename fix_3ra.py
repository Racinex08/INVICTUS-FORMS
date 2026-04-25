with open('index.html', encoding='utf-8') as f:
    text = f.read()

# Fix all remaining "4ta" references in visible text
text = text.replace('En 4ta Asistencia', 'En 3ra Asistencia')
text = text.replace('4ta Asistencia', '3ra Asistencia')
text = text.replace("total === '4'", "total === '3'")

# Make the 3ra card clickable
text = text.replace(
    '<div style="background:linear-gradient(135deg,#6f42c1,#e83e8c);border-radius:12px;padding:16px;color:white;text-align:center;">',
    '<div onclick="show3raPopup()" style="background:linear-gradient(135deg,#6f42c1,#e83e8c);border-radius:12px;padding:16px;color:white;text-align:center;cursor:pointer;transition:transform 0.15s;" onmouseenter="this.style.transform=\'scale(1.03)\'" onmouseleave="this.style.transform=\'scale(1)\'" title="Toca para ver los nombres">'
)

# Add the popup modal for 3ra asistencia (before </body>)
popup_html = '''
    <!-- Modal 3ra Asistencia -->
    <div class="modal-overlay" id="popup3raModal" style="z-index:3000;">
        <div class="modal-content" style="max-width:420px;max-height:80vh;overflow-y:auto;">
            <button class="modal-close" onclick="closeModal('popup3raModal')">&times;</button>
            <h3 style="margin-top:0;">🌟 En su 3ra Asistencia</h3>
            <p style="color:#888;font-size:0.85rem;margin-bottom:16px;">Estas personas han asistido 3 o más veces. ¡Son candidatos de conexión profunda!</p>
            <div id="lista3ra" style="display:flex;flex-direction:column;gap:10px;">
                <p style="color:#999;text-align:center;">Cargando...</p>
            </div>
        </div>
    </div>
'''
text = text.replace('</body>', popup_html + '\n</body>')

# Add JS function for 3ra popup — insert right before the closing </script> of the main script block
fn_3ra = """
        // ---- POPUP 3RA ASISTENCIA ----
        let personas3ra = []; // populated when dashboard loads

        function show3raPopup() {
            openModal('popup3raModal');
            const lista = document.getElementById('lista3ra');
            if (personas3ra.length === 0) {
                lista.innerHTML = '<p style="color:#888;text-align:center;padding:20px;">No hay datos cargados aún.<br>Abre el Dashboard primero.</p>';
                return;
            }
            lista.innerHTML = personas3ra.map(p => `
                <div style="background:#f8f9fa;border-radius:10px;padding:12px;display:flex;justify-content:space-between;align-items:center;border-left:4px solid #6f42c1;box-shadow:0 1px 3px rgba(0,0,0,0.06);">
                    <div>
                        <strong style="font-size:0.95rem;">${p.nombre}</strong>
                        <div style="font-size:0.78rem;color:#555;margin-top:3px;">
                            ${p.sexo === 'M' ? '👨' : '👩'} ${p.sexo === 'M' ? 'Masculino' : 'Femenino'} &nbsp;|&nbsp; 🔗 ${p.conector || '—'}
                        </div>
                        <div style="font-size:0.78rem;color:#888;">🌟 ${p.totalAsistencias} asistencias</div>
                    </div>
                    <a href="https://wa.me/${(p.telefono||'').replace(/[^\\d]/g,'')}" target="_blank" class="whatsapp-btn" style="width:36px;height:36px;font-size:1rem;flex-shrink:0;margin-left:10px;">💬</a>
                </div>
            `).join('');
        }
"""

# Insert before the closing </script> tag of the inline script
text = text.replace(
    '        // Inicialización\n        requestNotificationPermission();',
    fn_3ra + '\n        // Inicialización\n        requestNotificationPermission();'
)

# Now update loadDashboardData to also populate personas3ra
# Find the line where we store total3ra value and add storage of personas3ra
text = text.replace(
    "                const total3raVal   = data.total3ra || 0;",
    "                const total3raVal   = data.total3ra || 0;\n                personas3ra = data.personas3ra || [];"
)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
