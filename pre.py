import random
import string
from tkinter import messagebox, simpledialog

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
from matplotlib.widgets import Button

from input import procesarDatos

TAM_NODO = 800
ESTILO_ARISTA = 'arc3,rad=0.1'

# Ford-Fulkerson funciona con ciclos. Si tu profesor NO exige grafo acíclico,
# pon esto en True y se permitirán aristas que cierren ciclos.
PERMITIR_CICLOS = False

ARISTAS_POR_LINEA = 3
MAX_LINEAS_PANEL = 28


def crearGrafo(numNodos):
    letras = list(string.ascii_uppercase)[:numNodos]
    grafoI = nx.DiGraph()
    grafoI.add_nodes_from(letras)
    return grafoI


def generarGrafoAleatorio(grafo, densidad=0.15):
    """Modo automático: cadena A->B->...->última (siempre hay camino s->t)
    más aristas extra solo 'hacia adelante', así el grafo sigue siendo acíclico."""
    nodos = list(grafo.nodes)
    for u, v in zip(nodos, nodos[1:]):
        grafo.add_edge(u, v, capacity=random.randint(1, 20))
    for i in range(len(nodos)):
        for j in range(i + 2, len(nodos)):
            if random.random() < densidad:
                grafo.add_edge(nodos[i], nodos[j], capacity=random.randint(1, 20))
    return nodos[0], nodos[-1]


def nodoMasCercano(x, y, posDict, maxDistancia=0.12):
    """Devuelve el nodo más cercano al punto (x, y), o None si ninguno está dentro del radio."""
    mejor, mejorDist = None, maxDistancia
    for node, (nx_x, nx_y) in posDict.items():
        dist = np.hypot(x - nx_x, y - nx_y)
        if dist <= mejorDist:
            mejor, mejorDist = node, dist
    return mejor


class EditorGrafo:
    def __init__(self, grafo, pos, fig, axis, axisTexto,
                 nodoS=None, nodoT=None, historial=None):
        self.grafo = grafo
        self.pos = pos
        self.fig = fig
        self.axis = axis
        self.axisTexto = axisTexto

        self.nodoS = nodoS
        self.nodoT = nodoT
        self.nodoSeleccionado = None
        # cada entrada: (u, v, capacidadAnterior); capacidadAnterior es None si la arista era nueva
        self.historial = historial if historial is not None else []

        self.mensaje = None      # (texto, color) temporal que reemplaza el título
        self.idMensaje = 0
        self.timers = []         # se guardan para que no los borre el recolector de basura
        self.botones = []        # idem con los botones
        self.resultado = None    # (grafo, nodoS, nodoT, pos) al pulsar "Iniciar Algoritmo"

        self.crearBotones()
        fig.canvas.mpl_connect('button_press_event', self.manejarClics)
        fig.canvas.mpl_connect('close_event', self.alCerrar)
        self.dibujar()

    # ------------------------------------------------------------------ utilidades
    def ventana(self):
        """Ventana Tk de la figura (para usarla como padre de los diálogos)."""
        manager = getattr(self.fig.canvas, 'manager', None)
        return getattr(manager, 'window', None)

    def alCerrar(self, event):
        for timer in self.timers:
            timer.stop()

    def crearBotones(self):
        definiciones = [
            ([0.04, 0.05, 0.21, 0.06], 'Limpiar última arista', 'lightgray', 'yellow', self.limpiarConexiones),
            ([0.27, 0.05, 0.21, 0.06], 'Reasignar s / t', 'lightgray', 'yellow', self.reasignar),
            ([0.50, 0.05, 0.21, 0.06], 'Verificar grafo', 'lightgray', 'aquamarine', self.verificarGrafo),
            ([0.73, 0.05, 0.21, 0.06], 'Iniciar Algoritmo', 'lightgreen', 'lime', self.arrancarAlgoritmo),
        ]
        for rect, texto, color, hover, accion in definiciones:
            boton = Button(self.fig.add_axes(rect), texto, color=color, hovercolor=hover)
            boton.on_clicked(accion)
            self.botones.append(boton)

    def mostrarMensaje(self, texto, color):
        """Muestra un mensaje 3 segundos en el título SIN bloquear la ventana (reemplaza plt.pause)."""
        self.mensaje = (texto, color)
        self.idMensaje += 1
        miId = self.idMensaje
        self.dibujar()

        def borrar():
            if self.idMensaje == miId and plt.fignum_exists(self.fig.number):
                self.mensaje = None
                self.dibujar()

        timer = self.fig.canvas.new_timer(interval=3000)
        timer.single_shot = True
        timer.add_callback(borrar)
        timer.start()
        self.timers.append(timer)

    # ------------------------------------------------------------------ dibujo
    def dibujar(self):
        axis, grafo, pos = self.axis, self.grafo, self.pos
        axis.clear()
        self.axisTexto.clear()
        self.axisTexto.axis('off')

        colores = []
        for n in grafo.nodes:
            if n == self.nodoSeleccionado:
                colores.append('yellow')
            elif n == self.nodoS:
                colores.append('limegreen')
            elif n == self.nodoT:
                colores.append('darkorange')
            else:
                colores.append('cyan')

        nx.draw_networkx_nodes(grafo, pos, ax=axis, node_color=colores, node_size=TAM_NODO)
        nx.draw_networkx_edges(grafo, pos, ax=axis, arrowstyle='->', arrowsize=25,
                               edge_color='gray', connectionstyle=ESTILO_ARISTA,
                               node_size=TAM_NODO)

        edge_labels = nx.get_edge_attributes(grafo, 'capacity')
        try:
            # NetworkX >= 3.2: la etiqueta sigue la curva de la arista
            nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, ax=axis,
                                         label_pos=0.5, connectionstyle=ESTILO_ARISTA)
        except TypeError:
            nx.draw_networkx_edge_labels(grafo, pos, edge_labels=edge_labels, ax=axis,
                                         label_pos=0.5)

        nx.draw_networkx_labels(grafo, pos, ax=axis, font_weight='bold', font_size=9)

        x_vals = [c[0] for c in pos.values()]
        y_vals = [c[1] for c in pos.values()]
        axis.set_xlim(min(x_vals) - 0.25, max(x_vals) + 0.25)
        axis.set_ylim(min(y_vals) - 0.25, max(y_vals) + 0.25)
        axis.set_aspect('equal')

        if self.mensaje is not None:
            texto, color = self.mensaje
            axis.set_title(texto, color=color, fontweight='bold', fontsize=10)
        elif self.nodoS is None:
            axis.set_title("PASO 1: Haz clic en un nodo para definir la FUENTE (s)",
                           color='green', fontweight='bold', fontsize=10)
        elif self.nodoT is None:
            axis.set_title(f"Fuente (s): {self.nodoS} | PASO 2: Clic para definir el SUMIDERO (t)",
                           color='darkorange', fontweight='bold', fontsize=10)
        else:
            axis.set_title(f"Fuente (s): {self.nodoS} | Sumidero (t): {self.nodoT}\n"
                           "Clic 1: Origen | Clic 2: Destino (crear arista)",
                           color='black', fontsize=10)

        # Panel lateral: aristas en filas compactas para que quepan con 16 nodos
        textoPanel = "--- ESTADO DEL GRAFO ---\n"
        textoPanel += f"Fuente (s): {self.nodoS if self.nodoS else 'Pendiente'}\n"
        textoPanel += f"Sumidero (t): {self.nodoT if self.nodoT else 'Pendiente'}\n\n"
        textoPanel += "Aristas (capacidad):\n"

        aristas = [f"{u}->{v}:{c}" for u, v, c in grafo.edges(data='capacity')]
        if aristas:
            filas = ["  ".join(aristas[i:i + ARISTAS_POR_LINEA])
                     for i in range(0, len(aristas), ARISTAS_POR_LINEA)]
            if len(filas) > MAX_LINEAS_PANEL:
                ocultas = len(aristas) - MAX_LINEAS_PANEL * ARISTAS_POR_LINEA
                filas = filas[:MAX_LINEAS_PANEL] + [f"... (+{ocultas} más)"]
            textoPanel += "\n".join(filas)
        else:
            textoPanel += " (sin conexiones)"

        self.axisTexto.text(0.05, 0.95, textoPanel, transform=self.axisTexto.transAxes,
                            fontsize=8, verticalalignment='top', family='monospace')
        self.fig.canvas.draw_idle()

    # ------------------------------------------------------------------ eventos
    def manejarClics(self, event):
        if event.inaxes is not self.axis or event.xdata is None or event.ydata is None:
            return
        if event.button != 1:    # solo clic izquierdo
            return
        toolbar = getattr(self.fig.canvas, 'toolbar', None)
        if toolbar is not None and toolbar.mode != '':    # lupa o mano activas
            return

        nodo = nodoMasCercano(event.xdata, event.ydata, self.pos)
        if nodo is None:
            return

        self.mensaje = None

        if self.nodoS is None:
            self.nodoS = nodo
            print(f"Nodo Fuente (s) asignado: {nodo}")

        elif self.nodoT is None:
            if nodo != self.nodoS:
                self.nodoT = nodo
                print(f"Nodo Sumidero (t) asignado: {nodo}")
            else:
                self.mostrarMensaje("El sumidero (t) no puede ser igual a la fuente (s)", 'red')
                return

        elif self.nodoSeleccionado is None:
            self.nodoSeleccionado = nodo
            print(f"Origen seleccionado: {nodo}")

        else:
            origen = self.nodoSeleccionado
            self.nodoSeleccionado = None
            if origen != nodo:
                self.crearArista(origen, nodo)

        self.dibujar()

    def crearArista(self, u, v):
        if not PERMITIR_CICLOS and nx.has_path(self.grafo, v, u):
            messagebox.showwarning(
                "Ciclo", f"La arista {u} -> {v} cerraría un ciclo.\nNo se creó.",
                parent=self.ventana())
            return

        capAnterior = self.grafo[u][v]['capacity'] if self.grafo.has_edge(u, v) else None
        capacidad = simpledialog.askinteger(
            "Capacidad", f"Ingrese capacidad para la arista {u} -> {v}:",
            minvalue=1, initialvalue=capAnterior, parent=self.ventana())
        if capacidad is None:
            return

        self.grafo.add_edge(u, v, capacity=capacidad)
        self.historial.append((u, v, capAnterior))
        print(f"Arista creada: {u} -> {v} con capacidad {capacidad}")

    def validarGrafo(self):
        """Devuelve un texto de error, o None si el grafo está listo."""
        if self.nodoS is None or self.nodoT is None:
            return "Primero define la fuente (s) y el sumidero (t)."
        if not PERMITIR_CICLOS and not nx.is_directed_acyclic_graph(self.grafo):
            return "El grafo tiene ciclos. Elimina alguna arista."
        if not nx.has_path(self.grafo, self.nodoS, self.nodoT):
            return f"No existe camino de {self.nodoS} a {self.nodoT}. Agrega aristas."
        return None

    def verificarGrafo(self, event):
        error = self.validarGrafo()
        if error:
            self.mostrarMensaje(error, 'red')
        else:
            self.mostrarMensaje("Grafo listo para Ford-Fulkerson", 'green')

    def arrancarAlgoritmo(self, event):
        error = self.validarGrafo()
        if error:
            messagebox.showwarning("Error", error + "\nCorrige antes de iniciar.",
                                   parent=self.ventana())
            return
        self.resultado = (self.grafo, self.nodoS, self.nodoT, self.pos)
        plt.close(self.fig)

    def limpiarConexiones(self, event):
        self.nodoSeleccionado = None
        if not self.historial:
            self.mostrarMensaje("No hay conexiones para eliminar", 'red')
            return

        u, v, capAnterior = self.historial.pop()
        if capAnterior is None:
            if self.grafo.has_edge(u, v):
                self.grafo.remove_edge(u, v)
                print(f"Arista eliminada: {u} -> {v}")
        else:
            # la arista ya existía: se restaura su capacidad anterior en vez de borrarla
            self.grafo[u][v]['capacity'] = capAnterior
            print(f"Capacidad de {u} -> {v} restaurada a {capAnterior}")
        self.dibujar()

    def reasignar(self, event):
        self.nodoS = None
        self.nodoT = None
        self.nodoSeleccionado = None
        self.mensaje = None
        self.dibujar()


def preAlgoritmo():
    resultado = procesarDatos()
    if resultado is None:
        print("Operación cancelada o ventana cerrada sin datos procesados.")
        return None, None, None, None
    cantidadNodos, modo, nombre = resultado

    grafo = crearGrafo(cantidadNodos)
    pos = nx.circular_layout(grafo)

    nodoS = nodoT = None
    historial = []
    if modo == 2:    # automático: grafo aleatorio listo (se puede seguir editando)
        nodoS, nodoT = generarGrafoAleatorio(grafo)
        historial = [(u, v, None) for u, v in grafo.edges]

    fig = plt.figure(figsize=(10, 7))
    manager = getattr(fig.canvas, 'manager', None)
    if manager is not None and hasattr(manager, 'set_window_title'):
        manager.set_window_title(f"Ford-Fulkerson - {nombre}")

    axis = fig.add_axes([0.05, 0.2, 0.65, 0.75])
    axisTexto = fig.add_axes([0.72, 0.2, 0.26, 0.75])

    editor = EditorGrafo(grafo, pos, fig, axis, axisTexto, nodoS, nodoT, historial)
    plt.show()

    if editor.resultado is not None:
        return editor.resultado
    return None, None, None, None