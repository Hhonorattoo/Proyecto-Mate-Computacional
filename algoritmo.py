import textwrap
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button

TAM_NODO = 800
ESTILO_ARISTA = 'arc3,rad=0.1'


def motorFordFulkerson(grafo, nodoS, nodoT): 
    flujoMaximo = 0
    historialRutas = []

    while True:
        # Fase 1: etiquetado (BFS)
        cola = [nodoS]
        etiquetas = {nodoS : {'pred': '-', 'signo': '', 'inc': float('inf')}}
        encontrado = False

        while cola and not encontrado:
            u = cola.pop(0)
            deltaU = etiquetas[u]['inc']

            # busqueda hacia adelante
            for v in grafo.successors(u):
                residuo = grafo[u][v]['capacity'] - grafo[u][v]['flow']
                if v not in etiquetas and residuo > 0:
                    etiquetas[v] = {'pred': u, 'signo':'+', 'inc': min(deltaU, residuo)}
                    cola.append(v)
                    if v == nodoT:
                        encontrado = True
                        break

            # busqueda hacia atrás
            if not encontrado:
                for v in grafo.predecessors(u):
                    flujo = grafo[v][u]['flow']
                    if v not in etiquetas and flujo > 0:
                        etiquetas[v] = {'pred': u, 'signo': '-', 'inc': min(deltaU, flujo)}
                        cola.append(v)
                        if v == nodoT:
                            encontrado = True
                            break

        if not encontrado:
            conjuntoS = list(etiquetas.keys())
            conjuntoT = [n for n in grafo.nodes if n not in conjuntoS]
            aristasCorte = []
            for u in conjuntoS:
                for v in grafo.successors(u):
                    if v in conjuntoT:
                        aristasCorte.append((u, v))
            capCorte = sum(grafo[u][v]['capacity'] for u, v in aristasCorte)

            yield {
                "estado" : "FIN",
                "flujo_max" : flujoMaximo,
                "conjunto_S" : conjuntoS,
                "conjunto_T" : conjuntoT,
                "aristas_corte" : aristasCorte,
                "cap_corte" : capCorte,
                "historial": historialRutas
            }
            break

       # Fase 2: camino encontrado (reconstrucción)
        deltaT = etiquetas[nodoT]['inc']
        caminoEncontrado = []
        curr = nodoT
        nodos_en_camino = {nodoT} # Guardamos los nodos que sí pertenecen a la ruta
        
        while curr != nodoS:
            pred = etiquetas[curr]['pred']
            signo = etiquetas[curr]['signo']

            if signo == "+":
                caminoEncontrado.insert(0, (pred, curr, '+'))
            else:
                caminoEncontrado.insert(0, (curr, pred, '-'))
            
            curr = pred
            nodos_en_camino.add(curr)

        rutaStr = str(nodoS)
        for u, v, signo in caminoEncontrado:
            # Agregamos cada nodo destino de la arista
            rutaStr += f" -> {v}"

        paso_num = len(historialRutas) + 1
        historialRutas.append(f"Paso {paso_num}: {rutaStr} (Δ={deltaT})")

        etiquetasFiltradas = {k: v for k, v in etiquetas.items() if k in nodos_en_camino}
        aristasDibujo = [(u, v) for u, v, _ in caminoEncontrado]

        yield {
            "estado": "CAMINO_ENCONTRADO",
            "flujo_max": flujoMaximo,
            "etiquetas": etiquetasFiltradas,
            "camino": aristasDibujo,
            "delta": deltaT,
            "historial": historialRutas
        }

        # Fase 3: actualizar flujo
        for u, v, signo in caminoEncontrado:
            if signo == "+":
                grafo[u][v]['flow'] += deltaT
            else:
                grafo[u][v]['flow'] -= deltaT
        flujoMaximo += deltaT

        yield {
            "estado": "FLUJO_ACTUALIZADO",
            "flujo_max": flujoMaximo,
            "delta_agregado": deltaT,
            "etiquetas": {nodoS: {'pred': '-', 'signo': '', 'inc': float('inf')}},
            "historial": historialRutas
        }


def renderizarEstado(axis, axisTexto, fig, grafo, pos, estado_dict, nodoS, nodoT):
    # dibuja todo según lo que dicet el estado_dict
    axis.clear()
    axisTexto.clear()
    axisTexto.axis('off')

    estado = estado_dict.get("estado")
    flujoMax = estado_dict.get("flujo_max", 0)
    
    # Extraer variables dinámicas de forma segura
    etiquetas = estado_dict.get("etiquetas", {})
    caminoAzul = estado_dict.get("camino", [])
    conjuntoS = estado_dict.get("conjunto_S", [])
    aristasCorte = estado_dict.get("aristas_corte", [])

    # 1. Configurar Títulos según el estado
    if estado == "CAMINO_ENCONTRADO":
        titulo = f"¡Camino encontrado! Cuello de botella (Δt) = {estado_dict.get('delta')}"
    elif estado == "FLUJO_ACTUALIZADO":
        titulo = f"Flujo actualizado (+{estado_dict.get('delta_agregado')}). Pulsa para buscar otro camino."
    elif estado == "FIN":
        titulo = f"Fin: flujo máximo = {flujoMax} | corte mínimo = {estado_dict.get('cap_corte')}"
    else:
        titulo = f"Inicio: fuente {nodoS} etiquetada (-, ∞) | Pulsa 'Siguiente Paso'"

    # 2. Asignar Colores a Nodos y Bordes
    colores, bordes, grosores = [], [], []
    for n in grafo.nodes:
        # Lógica de relleno
        if estado == "FIN":
            colores.append('lightgreen' if n in conjuntoS else 'lightcoral')
        elif n in etiquetas:
            colores.append('yellow')
        else:
            colores.append('cyan')

        # Lógica de borde para s y t
        if n == nodoS:
            bordes.append('darkgreen')
            grosores.append(3)
        elif n == nodoT:
            bordes.append('darkorange')
            grosores.append(3)
        else:
            bordes.append('black')
            grosores.append(1)

    nx.draw_networkx_nodes(grafo, pos, ax=axis, node_color=colores, node_size=TAM_NODO,
                           edgecolors=bordes, linewidths=grosores)

    # 3. Asignar Colores a Aristas
    colores_arista, anchos = [], []
    for u, v in grafo.edges():
        if estado == "FIN" and (u, v) in aristasCorte:
            colores_arista.append('red')
            anchos.append(3.0)
        elif estado == "CAMINO_ENCONTRADO" and (u, v) in caminoAzul:
            colores_arista.append('blue')
            anchos.append(2.5)
        else:
            colores_arista.append('gray')
            anchos.append(1.0)

    nx.draw_networkx_edges(grafo, pos, ax=axis, arrowstyle='->', arrowsize=20,
                           edge_color=colores_arista, width=anchos,
                           connectionstyle=ESTILO_ARISTA, node_size=TAM_NODO)

    aristas_residuales = []
    for u, v in grafo.edges():
        # Si hay flujo pasando, significa que podemos "devolverlo" (capacidad residual inversa)
        if grafo[u][v]['flow'] > 0 and estado != "FIN":
            aristas_residuales.append((v, u))  # Invertimos el orden de u, v

    if aristas_residuales:
        nx.draw_networkx_edges(
            grafo, pos, ax=axis, edgelist=aristas_residuales,
            arrowstyle='->', arrowsize=15,
            edge_color='magenta', style='dashed', width=1.5,
            connectionstyle='arc3,rad=0.25', node_size=TAM_NODO
        )

    # 4. Dibujar Capacidades y Flujos
    edge_labels = {(u, v): f"{grafo[u][v]['flow']}/{grafo[u][v]['capacity']}" for u, v in grafo.edges()}
    try:
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, ax=axis, font_size=8, connectionstyle=ESTILO_ARISTA)
    except TypeError:
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, ax=axis, font_size=8)

    # 5. Dibujar Etiquetas de Nodos (Ford-Fulkerson)
    node_labels = {}
    for n in grafo.nodes:
        if n in etiquetas and estado != "FIN":
            p = etiquetas[n]['pred']
            s = etiquetas[n]['signo']
            inc = "∞" if etiquetas[n]['inc'] == float('inf') else etiquetas[n]['inc']
            node_labels[n] = f"{n}\n(-, ∞)" if p == '-' else f"{n}\n[{p}{s}, {inc}]"
        else:
            node_labels[n] = str(n)

    nx.draw_networkx_labels(grafo, pos, labels=node_labels, ax=axis, font_weight='bold', font_size=8)

    # Encuadre
    x_vals, y_vals = [c[0] for c in pos.values()], [c[1] for c in pos.values()]
    axis.set_xlim(min(x_vals) - 0.25, max(x_vals) + 0.25)
    axis.set_ylim(min(y_vals) - 0.25, max(y_vals) + 0.25)
    axis.set_aspect('equal')
    axis.set_title(titulo, fontweight='bold', fontsize=10)

    # 6. Panel de Texto Lateral
    textoPanel = f"Flujo máximo: {flujoMax}\nFuente (s): {nodoS}\nSumidero (t): {nodoT}\n\n"

    #Extraemos el historial del estado actual
    historial = estado_dict.get("historial", [])

    if estado == "FIN":
        textoPanel += "--- FIN DEL ALGORITMO ---\n"
        textoPanel += textwrap.fill(f"S (verde): {', '.join(map(str, conjuntoS))}", 30) + "\n"
        textoPanel += textwrap.fill(f"T (rojo): {', '.join(map(str, estado_dict.get('conjunto_T', [])))}", 30) + "\n\n"
        textoPanel += "Flechas rojas gruesas =\ncorte mínimo (saturadas).\n"
        textoPanel += f"Cap. del corte = {estado_dict.get('cap_corte')}\n\n"

        textoPanel += "--- RUTAS UTILIZADAS ---\n"
        if historial:
            textoPanel += "\n".join(historial)
        else:
            textoPanel += "Ninguna ruta encontrada."

    else:
        textoPanel += "Etiquetas activas:\n"
        for k, v in etiquetas.items():
            inc_val = "∞" if v['inc'] == float('inf') else v['inc']
            textoPanel += f" • {k}: ({v['pred']}{v['signo']}, {inc_val})\n"

        textoPanel += "\n--- BITÁCORA ---\n"
        if historial:
            textoPanel += "\n".join(historial)

    textoPanel += "\n\nBorde verde = s\nBorde naranja = t"
    if estado != "FIN":
        textoPanel += "\nFlecha magenta = Red residual (atrás)"

    axisTexto.text(0.05, 0.95, textoPanel, transform=axisTexto.transAxes,
                   fontsize=9, verticalalignment='top', family='monospace')
    fig.canvas.draw_idle()

def iniciarAlgoritmo(grafo, nodoS, nodoT, pos):
    if nodoS is None or nodoT is None:
        raise ValueError("Falta definir la fuente (s) o el sumidero (t).")
    
    # inicialización de flujos en 0
    for u, v in grafo.edges():
        grafo[u][v]['flow'] = 0

    # Inicializar la figura
    fig = plt.figure(figsize=(10, 7))
    axis = fig.add_axes([0.05, 0.2, 0.65, 0.75])
    axisTexto = fig.add_axes([0.72, 0.2, 0.26, 0.75])

    # Instanciar el motor matemático
    generador = motorFordFulkerson(grafo, nodoS, nodoT)
    
    # Estado inicial estático antes del primer clic
    estado_inicial = {
        "estado": "INICIO", 
        "flujo_max": 0, 
        "etiquetas": {nodoS: {'pred': '-', 'signo': '', 'inc': float('inf')}}
    }
    renderizarEstado(axis, axisTexto, fig, grafo, pos, estado_inicial, nodoS, nodoT)

    def on_siguiente_paso(event):
        try:
            nuevo_estado = next(generador)
            renderizarEstado(axis, axisTexto, fig, grafo, pos, nuevo_estado, nodoS, nodoT)
            
            # Si el algoritmo llega a su fin, deshabilitar botón y verificar contra NetworkX
            if nuevo_estado.get("estado") == "FIN":
                btnSiguiente.label.set_text('Terminado')
                btnSiguiente.color = 'lightgray'
                btnSiguiente.hovercolor = 'lightgray'
                btnSiguiente.ax.set_facecolor('lightgray')
                
                # Verificación silenciosa en consola
                esperado = nx.maximum_flow_value(grafo, nodoS, nodoT)
                calculado = nuevo_estado['flujo_max']
                print(f"[Check] Flujo calculado: {calculado} | NetworkX: {esperado}")
                
        except StopIteration:
            plt.close(fig)

    # Crear botón
    axBtn = fig.add_axes([0.35, 0.05, 0.25, 0.08])
    btnSiguiente = Button(axBtn, 'Siguiente Paso', color='lightblue', hovercolor='skyblue')
    btnSiguiente.on_clicked(on_siguiente_paso)
    fig._btnSiguiente = btnSiguiente
    
    plt.show()

if __name__ == "__main__":
    matplotlib.use("TkAgg")
    from pre import preAlgoritmo

    nGrafo, nNodoS, nNodoT, nPos = preAlgoritmo()
    if nGrafo is not None:
        iniciarAlgoritmo(nGrafo, nNodoS, nNodoT, nPos)

