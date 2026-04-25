import re

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Quitar el historyBtn del welcomeScreen
text = text.replace('<button id="historyBtn" class="history-btn">📋</button>\\n        <button id="langToggle">ES</button>', '<button id="langToggle">ES</button>')

# 2. Agregar el botón estilo flotante al mismo nivel que notificationCenter
new_history_btn = """
    <!-- Botón de Historial (Flotante) -->
    <div style="position: fixed; top: 20px; left: 20px; z-index: 1000;">
        <div id="historyBtn"
            style="background: white; width: 50px; height: 50px; border-radius: 50%; display: flex; align-items: center; justify-content: center; cursor: pointer; box-shadow: 0 4px 10px rgba(0,0,0,0.2); transition: transform 0.2s;">
            <span style="font-size: 24px;">📋</span>
        </div>
    </div>
"""
# Insertar justo después de <body>
text = text.replace('<body>\\n\\n    <!-- Centro de Notificaciones -->', '<body>\\n' + new_history_btn + '\\n    <!-- Centro de Notificaciones -->')

# Fallback por si la estructura anterior no funciona exactamente
if "<!-- Botón de Historial (Flotante) -->" not in text:
    text = text.replace('<body>\\n    <!-- Centro de Notificaciones -->', '<body>\\n' + new_history_btn + '\\n    <!-- Centro de Notificaciones -->')

if "<!-- Botón de Historial (Flotante) -->" not in text:
    text = text.replace('<body>', '<body>\\n' + new_history_btn)


# 3. Eliminar la clase .history-btn de estilos ya que los pusimos inline
text = re.sub(r'\\.history-btn {[^}]+}', '', text, flags=re.MULTILINE)

with open('c:\\Users\\Isaac Racines\\Downloads\\Invictus Form\\index.html', 'w', encoding='utf-8') as f:
    f.write(text)
