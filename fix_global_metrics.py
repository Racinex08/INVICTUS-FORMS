with open('index.html', encoding='utf-8') as f:
    text = f.read()

# Update the metrics section to use new global fields from AppScript
old_metrics = """                const nuevos        = data.nuevos || [];
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
                const nuevosSub = document.querySelector('#totalNuevosSemana + div, #totalNuevosSemana ~ div');"""

new_metrics = """                const nuevos        = data.nuevos || [];
                // Métricas globales (todos los tiempos, sin filtro de fecha)
                const totalGlobal   = data.totalGlobal || 0;
                const globalHombres = data.globalHombres || 0;
                const globalMujeres = data.globalMujeres || 0;
                const totalIglesia  = data.totalIglesia  || 0;
                const total3raVal   = data.total3ra      || 0;
                const connGlobal    = data.conectoresGlobal || {};
                personas3ra         = data.personas3ra   || [];

                // Animate metric cards — siempre con datos globales reales
                animateCount(document.getElementById('totalRegistrados'),  totalGlobal);
                animateCount(document.getElementById('totalNuevosSemana'), nuevos.length);
                animateCount(document.getElementById('totalHombres'),      globalHombres);
                animateCount(document.getElementById('totalMujeres'),      globalMujeres);
                animateCount(document.getElementById('totalIglesia'),      totalIglesia);
                animateCount(document.getElementById('total3ra'),          total3raVal);"""

text = text.replace(old_metrics, new_metrics)

# Also remove the old personas3ra line that was already there to avoid duplicate
text = text.replace(
    'personas3ra         = data.personas3ra   || [];\n\n                // Animate metric cards — siempre con datos globales reales',
    '// Animate metric cards — siempre con datos globales reales'
)

# Clean the connector chart source — always use global data
old_conn = """                // Connector bar chart — use global connectors for richer data
                const connSource = Object.keys(connGlobal).length > 0 ? connGlobal
                    : nuevos.reduce((acc, n) => { const k = n.conector||'Sin asignar'; acc[k]=(acc[k]||0)+1; return acc; }, {});"""
new_conn = """                // Connector bar chart — datos globales históricos
                const connSource = Object.keys(connGlobal).length > 0 ? connGlobal
                    : { 'Sin datos': 0 };"""
text = text.replace(old_conn, new_conn)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(text)

print("Done!")
