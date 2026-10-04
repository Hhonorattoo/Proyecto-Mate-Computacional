import textwrap
import matplotlib
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.widgets import Button

TAM_NODO = 800
ESTILO_ARISTA = 'arc3,rad=0.1'


def dibujarPasoAlgoritmo(axis, axisTexto, fig, grafo, pos, etiquetas, titulo, flujo_max,
                         nodoS, nodoT, camino_azul=None, es_final=False,
                         conjunto_S=None, aristas_corte=None):
    axis.clear()
    axisTexto.clear()
    axisTexto.axis('off')

    camino_azul = camino_azul or []
    conjunto_S = conjunto_S or []
    aristas_corte = aristas_corte or []

    # 1. Nodos
    #    Relleno: verde/rojo = conjuntos S/T (al final), amarillo = etiquetado, cian = sin etiquetar
    #    Borde grueso: verde oscuro = fuente (s), naranja = sumidero (t)
    colores, bordes, grosores = [], [], []
    for n in grafo.nodes:
        if es_final:
            colores.append('lightgreen' if n in conjunto_S else 'lightcoral')
        elif n in etiquetas:
            colores.append('yellow')
        else:
            colores.append('cyan')

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

    # 2. Aristas (rojo = corte mínimo, azul = camino de aumento)
    colores_arista, anchos = [], []
    for u, v in grafo.edges():
        if es_final and (u, v) in aristas_corte:
            colores_arista.append('red')
            anchos.append(3.0)
        elif (u, v) in camino_azul:
            colores_arista.append('blue')
            anchos.append(2.5)
        else:
            colores_arista.append('gray')
            anchos.append(1.0)

    nx.draw_networkx_edges(grafo, pos, ax=axis, arrowstyle='->', arrowsize=20,
                           edge_color=colores_arista, width=anchos,
                           connectionstyle=ESTILO_ARISTA, node_size=TAM_NODO)

    # 3. Flujo / Capacidad en cada arista
    edge_labels = {(u, v): f"{grafo[u][v]['flow']}/{grafo[u][v]['capacity']}"
                   for u, v in grafo.edges()}
    try:
        # NetworkX >= 3.2: la etiqueta sigue la curva de la arista
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, ax=axis,
                                     font_size=8, connectionstyle=ESTILO_ARISTA)
    except TypeError:
        # NetworkX más viejo: no acepta connectionstyle
        nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, ax=axis,
                                     font_size=8)

    # 4. Etiquetas Ford-Fulkerson en los nodos: [predecesor+/-, incremento]
    node_labels = {}
    for n in grafo.nodes:
        if n in etiquetas:
            p = etiquetas[n]['pred']
            s = etiquetas[n]['signo']
            inc = etiquetas[n]['inc']
            node_labels[n] = f"{n}\n(-, ∞)" if p == '-' else f"{n}\n[{p}{s}, {inc}]"
        else:
            node_labels[n] = str(n)

    nx.draw_networkx_labels(grafo, pos, labels=node_labels, ax=axis,
                            font_weight='bold', font_size=8)

    x_vals = [c[0] for c in pos.values()]
    y_vals = [c[1] for c in pos.values()]
    axis.set_xlim(min(x_vals) - 0.25, max(x_vals) + 0.25)
    axis.set_ylim(min(y_vals) - 0.25, max(y_vals) + 0.25)
    axis.set_aspect('equal')
    axis.set_title(titulo, fontweight='bold', fontsize=10)

    # 5. Panel lateral
    textoPanel = f"Flujo máximo: {flujo_max}\n"
    textoPanel += f"Fuente (s): {nodoS}\n"
    textoPanel += f"Sumidero (t): {nodoT}\n\n"

    if es_final:
        conjunto_T = [n for n in grafo.nodes if n not in conjunto_S]
        capCorte = sum(grafo[u][v]['capacity'] for u, v in aristas_corte)
        textoPanel += "--- FIN DEL ALGORITMO ---\n"
        textoPanel += textwrap.fill(f"S (verde): {', '.join(conjunto_S)}", 30) + "\n"
        textoPanel += textwrap.fill(f"T (rojo): {', '.join(conjunto_T)}", 30) + "\n\n"
        textoPanel += "Flechas rojas gruesas =\ncorte mínimo (saturadas).\n"
        textoPanel += f"Capacidad del corte = {capCorte}\n"
        textoPanel += f"Flujo máximo        = {flujo_max}\n"
    else:
        textoPanel += "Etiquetas activas:\n"
        for k, v in etiquetas.items():
            textoPanel += f" • {k}: ({v['pred']}{v['signo']}, {v['inc']})\n"

    textoPanel += "\nBorde verde = s\nBorde naranja = t"

    axisTexto.text(0.05, 0.95, textoPanel, transform=axisTexto.transAxes,
                   fontsize=9, verticalalignment='top', family='monospace')
    fig.canvas.draw_idle()


class ControlFordFulkerson:
    def __init__(self, grafo, nodoS, nodoT, pos, axis, axisTexto, fig):
        self.grafo = grafo
        self.nodoS = nodoS
        self.nodoT = nodoT
        self.pos = pos
        self.axis = axis
        self.axisTexto = axisTexto
        self.fig = fig
        self.boton = None   # se asigna desde iniciarAlgoritmo

        self.flujoMaximo = 0
        self.esFinal = False
        self.fase = "EVALUAR_ETIQUETADO"   # o ACTUALIZAR_FLUJO

        self.etiquetas = {self.nodoS: {'pred': '-', 'signo': '', 'inc': float('inf')}}
        self.caminoEncontrado = []   # lista de (u, v, signo)
        self.deltaT = 0
        self.conjuntoS = []
        self.aristasCorte = []

        self.titulo = f"Inicio: fuente {self.nodoS} etiquetada (-, ∞) | Pulsa 'Siguiente Paso'"
        self.render()

    def render(self):
        etiquetasRender = {}
        for k, v in self.etiquetas.items():
            incValores = "∞" if v['inc'] == float('inf') else v['inc']
            etiquetasRender[k] = {'pred': v['pred'], 'signo': v['signo'], 'inc': incValores}

        camino_dibujo = [(u, v) for u, v, _ in self.caminoEncontrado]

        dibujarPasoAlgoritmo(
            self.axis, self.axisTexto, self.fig, self.grafo, self.pos,
            etiquetas=etiquetasRender,
            titulo=self.titulo,
            flujo_max=self.flujoMaximo,
            nodoS=self.nodoS,
            nodoT=self.nodoT,
            camino_azul=camino_dibujo,
            es_final=self.esFinal,
            conjunto_S=self.conjuntoS,
            aristas_corte=self.aristasCorte
        )

    def etiquetar(self):
        """Fase de etiquetado (BFS). Devuelve True si el sumidero quedó etiquetado."""
        cola = [self.nodoS]
        self.etiquetas = {self.nodoS: {'pred': '-', 'signo': '', 'inc': float('inf')}}

        while cola and self.nodoT not in self.etiquetas:
            u = cola.pop(0)
            deltaU = self.etiquetas[u]['inc']

            # Hacia adelante (forward): arista u -> v con capacidad residual
            for v in self.grafo.successors(u):
                residuo = self.grafo[u][v]['capacity'] - self.grafo[u][v]['flow']
                if v not in self.etiquetas and residuo > 0:
                    self.etiquetas[v] = {'pred': u, 'signo': '+', 'inc': min(deltaU, residuo)}
                    cola.append(v)
                    if v == self.nodoT:
                        return True

            # Hacia atrás (backward): arista v -> u con flujo que se puede devolver
            for v in self.grafo.predecessors(u):
                flujo = self.grafo[v][u]['flow']
                if v not in self.etiquetas and flujo > 0:
                    self.etiquetas[v] = {'pred': u, 'signo': '-', 'inc': min(deltaU, flujo)}
                    cola.append(v)
                    if v == self.nodoT:
                        return True

        return self.nodoT in self.etiquetas

    def siguientePaso(self, event=None):
        if self.esFinal:
            return

        if self.fase == "EVALUAR_ETIQUETADO":
            if self.etiquetar():
                self.deltaT = self.etiquetas[self.nodoT]['inc']

                # Reconstruir el camino de t hacia s guardando el signo de cada arista
                curr = self.nodoT
                self.caminoEncontrado = []
                while curr != self.nodoS:
                    pred = self.etiquetas[curr]['pred']
                    signo = self.etiquetas[curr]['signo']
                    if signo == '+':
                        self.caminoEncontrado.insert(0, (pred, curr, '+'))
                    else:
                        self.caminoEncontrado.insert(0, (curr, pred, '-'))
                    curr = pred

                self.titulo = f"¡Camino encontrado! Cuello de botella (Δt) = {self.deltaT}"
                self.fase = "ACTUALIZAR_FLUJO"
            else:
                self.esFinal = True
                self.conjuntoS = list(self.etiquetas.keys())
                conjuntoT = [n for n in self.grafo.nodes if n not in self.conjuntoS]
                self.aristasCorte = [
                    (u, v) for u, v in self.grafo.edges()
                    if u in self.conjuntoS and v in conjuntoT
                ]
                capCorte = sum(self.grafo[u][v]['capacity'] for u, v in self.aristasCorte)

                self.caminoEncontrado = []
                self.titulo = f"Fin: flujo máximo = {self.flujoMaximo} | corte mínimo = {capCorte}"

                # Verificación contra la implementación de NetworkX
                esperado = nx.maximum_flow_value(self.grafo, self.nodoS, self.nodoT)
                estado = "OK" if esperado == self.flujoMaximo == capCorte else "NO COINCIDE"
                print(f"[Verificación] tu flujo = {self.flujoMaximo} | corte = {capCorte} "
                      f"| NetworkX = {esperado} -> {estado}")

                if self.boton is not None:
                    self.boton.label.set_text('Algoritmo terminado')
                    self.boton.color = 'lightgray'
                    self.boton.hovercolor = 'lightgray'
                    self.boton.ax.set_facecolor('lightgray')

        elif self.fase == "ACTUALIZAR_FLUJO":
            for u, v, signo in self.caminoEncontrado:
                if signo == '+':
                    self.grafo[u][v]['flow'] += self.deltaT
                else:
                    self.grafo[u][v]['flow'] -= self.deltaT

            self.flujoMaximo += self.deltaT
            self.titulo = f"Flujo actualizado (+{self.deltaT}). Pulsa para buscar otro camino."

            self.caminoEncontrado = []
            self.etiquetas = {self.nodoS: {'pred': '-', 'signo': '', 'inc': float('inf')}}
            self.fase = "EVALUAR_ETIQUETADO"

        self.render()


def iniciarAlgoritmo(grafo, nodoS, nodoT, pos):
    if nodoS is None or nodoT is None:
        raise ValueError("Falta definir la fuente (s) o el sumidero (t).")

    for u, v in grafo.edges():
        grafo[u][v]['flow'] = 0

    fig = plt.figure(figsize=(10, 7))

    axis = fig.add_axes([0.05, 0.2, 0.65, 0.75])
    axisTexto = fig.add_axes([0.72, 0.2, 0.26, 0.75])

    motor = ControlFordFulkerson(grafo, nodoS, nodoT, pos, axis, axisTexto, fig)

    axBtn = fig.add_axes([0.35, 0.05, 0.25, 0.08])
    btnSiguiente = Button(axBtn, 'Siguiente Paso', color='lightblue', hovercolor='skyblue')
    motor.boton = btnSiguiente
    btnSiguiente.on_clicked(motor.siguientePaso)
    plt.show()


if __name__ == "__main__":
    matplotlib.use("TkAgg")
    from pre import preAlgoritmo

    nGrafo, nNodoS, nNodoT, nPos = preAlgoritmo()
    if nGrafo is not None:
        iniciarAlgoritmo(nGrafo, nNodoS, nNodoT, nPos)