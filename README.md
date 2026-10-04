# Proyecto de Matemática Computacional: Algoritmo de Ford-Fulkerson
Programa desarrollado con Python usando librerías gráficas

## 1. Introducción
El problema del flujo máximo es un concepto fundamental en la optimización de redes, con aplicaciones prácticas cruciales en el transporte de recursos, telecomunicaciones y logística. Este proyecto presenta el desarrollo de una herramienta gráfica e interactiva diseñada para modelar redes y resolver este problema de manera didáctica. A través de este documento, se detalla el contenido del informe y el funcionamiento del sistema, despertando el interés en cómo las matemáticas computacionales pueden simular y resolver cuellos de botella en tiempo real[cite: 6].

## 2. Objetivo General
**Desarrollar** una aplicación interactiva en Python que permita modelar grafos dirigidos, ingresar datos de forma dinámica y ejecutar paso a paso el algoritmo de Ford-Fulkerson, con el fin de hallar el flujo máximo y el corte mínimo de la red de manera visual y comprobable[cite: 6].

## 3. Marco Metodológico y Desarrollo del Código
El algoritmo utilizado es el de **Ford-Fulkerson**, el cual resuelve el problema iterando sobre la red para encontrar "caminos aumentantes" desde el nodo fuente ($s$) hasta el nodo sumidero ($t$). Sus etapas principales incluyen:
1.  **Etiquetado (Búsqueda BFS):** Se evalúan las aristas hacia adelante (con capacidad residual) y hacia atrás (con flujo que se puede devolver) asignando etiquetas a los nodos (predecesor, signo e incremento).
2.  **Actualización de flujo:** Al encontrar un camino, se calcula el cuello de botella (flujo máximo posible por esa ruta) y se actualiza el flujo del sistema.
3.  **Corte Mínimo:** Cuando el sumidero ya no puede ser etiquetado, el algoritmo termina y determina qué aristas saturadas dividen la red, confirmando el flujo máximo[cite: 6].

### Desarrollo del Código y Librerías Utilizadas
El programa presenta un avance funcional significativo, permitiendo interactuar con el usuario y ejecutar el algoritmo de manera gráfica[cite: 6]. Se utilizaron las siguientes librerías principales[cite: 6]:
*   **Python:** Lenguaje de programación base.
*   **NetworkX:** Utilizada para la creación de la estructura del grafo dirigido, almacenamiento de nodos, aristas, capacidades y verificación de grafos acíclicos.
*   **Matplotlib:** Implementada para renderizar la interfaz gráfica, dibujar el progreso del algoritmo, cambiar colores de los nodos (fuente, sumidero, etiquetados) y manejar los botones de interacción.
*   **Tkinter:** Usada para las ventanas emergentes que permiten recolectar los datos iniciales (como el número de nodos, entre 7 y 16) y el modo de generación.

El código se estructuró en tres módulos fundamentales para asegurar su legibilidad[cite: 6]:
*   `input.py`: Gestiona la interfaz de inicio y la captura de parámetros.
*   `pre.py`: Editor interactivo donde el usuario define manualmente las conexiones y valida el grafo.
*   `algoritmo.py`: Contiene el motor matemático y controla los pasos de ejecución y el panel lateral informativo.

*(Nota para el informe: Las figuras del código y capturas de pantalla de la interfaz deben presentarse con el formato APA, incluyendo número, título y nota)*[cite: 6].

## 4. Diagrama de Flujo
*(En este apartado de tu informe deberás insertar la imagen de tu diagrama de flujo. Asegúrate de que sea claro, completo y coherente con el funcionamiento real del programa `input.py -> pre.py -> algoritmo.py`)*[cite: 6].

## 5. Resultados
El sistema permite ingresar datos, interactuar con el usuario y ejecutar parcialmente (paso a paso) o totalmente el algoritmo[cite: 6]. Como resultado, la aplicación visualiza en tiempo real las etiquetas activas y, al finalizar, devuelve la red particionada:
*   Muestra el valor cuantitativo del **Flujo Máximo**.
*   Identifica visualmente (con flechas rojas gruesas) las aristas saturadas correspondientes al **Corte Mínimo**.
*   Imprime en el panel lateral los conjuntos $S$ (verde) y $T$ (rojo).

## 6. Conclusiones
*   Se logró desarrollar con éxito una herramienta que cumple con las funcionalidades principales previstas, permitiendo evaluar redes desde 7 hasta 16 nodos de forma manual o automática[cite: 6].
*   La separación gráfica por colores y la ejecución controlada (botón de "Siguiente Paso") demostró ser un método sumamente efectivo para comprender la actualización del flujo y el comportamiento de la red residual, cumpliendo directamente con el objetivo general del proyecto[cite: 6].
