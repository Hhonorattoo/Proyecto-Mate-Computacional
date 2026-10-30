# 🌊 Simulador Interactivo: Algoritmo de Ford-Fulkerson

Un simulador gráfico e interactivo desarrollado en Python para modelar redes de flujo y visualizar el cálculo del **Flujo Máximo** y el **Corte Mínimo** utilizando el algoritmo de Ford-Fulkerson.

Este proyecto permite a estudiantes, profesores y entusiastas de las matemáticas computacionales comprender paso a paso cómo se construyen las redes residuales y cómo se identifican los caminos aumentantes en tiempo real.

## ✨ Características Principales

* **Generación de Grafos (7 a 16 nodos):** Crea redes de flujo de manera totalmente manual (dibujando aristas y asignando capacidades) o genera redes aleatorias de forma automática.
* **Soporte Multifuente y Multisumidero:** Inyección automática de nodos ficticios (súper-fuente y súper-sumidero) para resolver problemas logísticos complejos.
* **Prevención de Ciclos:** Validación en tiempo real durante la edición manual para garantizar grafos dirigidos acíclicos (DAG) si la configuración lo requiere.
* **Ejecución Paso a Paso:** Controla el avance del algoritmo con un clic. Observa la búsqueda BFS, el etiquetado de vértices y la actualización de cuellos de botella ($\Delta t$).
* **Visualización de Red Residual:** Representación gráfica de las aristas directas (azul) y las aristas de flujo inverso (magenta punteado) para devolver flujo.
* **Teorema Max-Flow / Min-Cut:** Al finalizar, el programa resalta en rojo grueso el corte mínimo que particiona la red (Conjuntos $S$ y $T$) y confirma el flujo máximo alcanzado.
* **Bitácora Integrada:** Panel lateral que documenta cada camino aumentante utilizado y las capacidades modificadas en el proceso.

## 🛠️ Tecnologías Utilizadas

* **Python 3.x** - Lenguaje base.
* **NetworkX** - Lógica de estructuras de datos para grafos dirigidos y validación interna.
* **Matplotlib** - Renderizado interactivo del motor gráfico (nodos, aristas, layouts y eventos de clic).
* **Tkinter** - Interfaces gráficas nativas para la recolección de parámetros iniciales y pop-ups.
* **NumPy** - Operaciones espaciales para el cálculo de distancias al hacer clic en los nodos.

## ⚙️ Instalación y Requisitos

Asegúrate de tener Python instalado en tu sistema. Luego, instala las dependencias necesarias ejecutando el siguiente comando en tu terminal:

```bash
pip install networkx matplotlib numpy
```

## 🚀 Cómo usar el simulador

1. Clona este repositorio o descarga los archivos fuente.
2. Abre una terminal en la carpeta del proyecto.
3. Ejecuta el archivo principal:

```bash
python input.py
```

4. **Menú de Inicio:** Introduce un nombre para tu red y elige el modo (1 para Manual, 2 para Automático). Si es manual, ingresa cuántos nodos deseas (entre 7 y 16).
5. **Editor de Grafo:** 
   * Selecciona tus fuentes (color verde) y sumideros (color naranja).
   * Haz clic en un nodo origen y luego en un nodo destino para crear una arista.
   * Ingresa la capacidad cuando el sistema te lo pida.
   * Haz clic en "Iniciar Algoritmo" cuando la red esté lista.
6. **Simulación:** Utiliza el botón "Siguiente Paso" para ver la magia de Ford-Fulkerson en acción.

## 📂 Estructura del Proyecto

El código está modularizado bajo una arquitectura de *pipeline* para separar la captura de datos del motor de renderizado:

* `input.py`: Punto de entrada de la aplicación. Maneja la interfaz gráfica inicial con Tkinter y captura los parámetros base.
* `pre.py`: Motor de edición espacial. Carga el entorno de Matplotlib, procesa los eventos de ratón para dibujar conexiones, inyecta nodos ficticios y valida que el grafo sea resoluble.
* `algoritmo.py`: Contiene el generador matemático de Ford-Fulkerson. Maneja la máquina de estados del programa, actualiza los colores, flujos y capacidades, y controla el historial de la bitácora.

## 📝 Licencia

Este proyecto fue desarrollado con fines académicos. Siéntete libre de clonarlo, estudiarlo y modificarlo.