import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import tkinter as tk
import random
import string

def pedirEntero(mensaje, minimo, maximo):
    while True:
        try:
            valor = int(input(mensaje))
            if minimo <= valor <= maximo:
                return valor
            print(f"Por favor, ingresa un número entre {minimo} y {maximo}.")
        except ValueError:
            print("Entrada inválida. Debes ingresar un número entero.")


def crearGrafo():
    modo = pedirEntero("Manual o automático? (1 o 2):", 1, 2)
    numNodos  = 0
    match modo:
        case 1:
            numNodos = pedirEntero("Cantidad de nodos entre 7 a 16: ", 7, 16)
        case 2:
            numNodos = random.randint(7, 16)

    letras = list(string.ascii_uppercase)[:numNodos]
    grafo = nx.DiGraph()
    grafo.add_nodes_from(letras)

    nx.draw(grafo,
        with_labels=True,
        node_color='skyblue',
        node_size=700,
        edge_color='gray'
    )
    plt.show()

if __name__ == "__main__":
    crearGrafo()