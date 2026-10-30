# Proyecto de Matemática Computacional: Algoritmo de Ford-Fulkerson

## 1. Introducción
El problema del flujo máximo es un concepto fundamental en la optimización de redes, con aplicaciones prácticas cruciales en el transporte de recursos, telecomunicaciones y logística. Este proyecto presenta el desarrollo de una herramienta gráfica e interactiva diseñada para modelar redes y resolver este problema de manera didáctica. A través de este documento, se detalla el contenido del informe y el funcionamiento del sistema, despertando el interés en cómo las matemáticas computacionales pueden simular y resolver cuellos de botella en tiempo real.

## 2. Objetivo General
**Desarrollar** una aplicación interactiva en Python que permita modelar grafos dirigidos, ingresar datos de forma dinámica y ejecutar paso a paso el algoritmo de Ford-Fulkerson, con el fin de hallar el flujo máximo y el corte mínimo de la red de manera visual y comprobable.

## 3. Marco Metodológico y Desarrollo del Código
El algoritmo utilizado es el de **Ford-Fulkerson**, el cual resuelve el problema iterando sobre la red para encontrar "caminos aumentantes" desde el nodo fuente ($s$) hasta el nodo sumidero ($t$). Sus etapas principales incluyen:
1. **Etiquetado (Búsqueda BFS):** Se evalúan las aristas hacia adelante (con capacidad residual) y hacia atrás (con flujo que se puede devolver) asignando etiquetas a los nodos, incluyendo predecesor, signo e incremento.
2. **Actualización de flujo:** Al encontrar un camino, se calcula el cuello de botella (flujo máximo posible por esa ruta) y se actualiza el flujo del sistema.
3. **Corte Mínimo:** Cuando el sumidero ya no puede ser etiquetado, el algoritmo termina y determina qué aristas saturadas dividen la red, confirmando el flujo máximo.

### Librerías Utilizadas
El programa presenta un avance funcional significativo, permitiendo interactuar con el usuario y ejecutar el algoritmo de manera gráfica. Se utilizaron las siguientes librerías principales:
* **Python:** Lenguaje de programación base.
* **NetworkX:** Utilizada para la creación de la estructura del grafo dirigido, almacenamiento de nodos, aristas, capacidades y verificación de grafos acíclicos.
* **Matplotlib:** Implementada para renderizar la interfaz gráfica, dibujar el progreso del algoritmo, cambiar colores de los nodos (fuente, sumidero, etiquetados) y manejar los botones de interacción.
* **Tkinter:** Usada para las ventanas emergentes que permiten recolectar los datos iniciales, como el número de nodos (entre 7 y 16) y el modo de generación manual o automático.

### Estructura de Módulos
El código se estructuró en tres módulos fundamentales para asegurar su legibilidad y cumplir con los requerimientos del proyecto:
* `input.py`: Gestiona la interfaz de inicio y la captura de parámetros iniciales mediante ventanas de Tkinter.
* `pre.py`: Editor interactivo donde el usuario define manualmente las conexiones, valida que exista camino entre fuente y sumidero, y en caso de haber múltiples orígenes o destinos, inyecta automáticamente nodos ficticios (súper-fuente y súper-sumidero) con capacidades simuladas infinitas.
* `algoritmo.py`: Contiene el motor matemático de Ford-Fulkerson implementado como un generador, controlando los pasos de ejecución (BFS, reconstrucción de camino, actualización) y el renderizado del panel lateral informativo con el historial de rutas.

## 4. Diagrama de Flujo
*(Nota: Insertar aquí la figura del diagrama de flujo formateada según normas APA, incluyendo número de figura, título descriptivo y nota explicativa en la parte inferior, que represente el ciclo de inicio, edición gráfica, validación de ciclos y ejecución paso a paso del algoritmo)*.

## 5. Resultados
El sistema permite ingresar datos, interactuar con el usuario y ejecutar parcialmente (paso a paso) o totalmente el algoritmo. Como resultado, la aplicación visualiza en tiempo real las etiquetas activas y, al finalizar, devuelve la red particionada:
* Muestra el valor cuantitativo del **Flujo Máximo** calculado por el motor propio y verificado de forma silenciosa contra la función nativa de NetworkX.
* Identifica visualmente (con flechas rojas gruesas) las aristas saturadas correspondientes al **Corte Mínimo**.
* Imprime en el panel lateral los conjuntos $S$ (verde) y $T$ (rojo), junto con el historial completo de rutas utilizadas.

## 6. Conclusiones
* Se logró desarrollar con éxito una herramienta que cumple con las funcionalidades principales previstas, permitiendo evaluar redes desde 7 hasta 16 nodos de forma manual o automática, logrando así el objetivo general del proyecto.
* La separación gráfica por colores, el uso de nodos ficticios para múltiples fuentes/sumideros, y la ejecución controlada (botón de "Siguiente Paso") demostró ser un método sumamente efectivo para comprender la actualización del flujo y el comportamiento de la red residual.

## 7. Instrucciones de Ejecución
Para iniciar el proyecto, asegúrese de tener instaladas las dependencias requeridas (`networkx`, `matplotlib`, `numpy`) y ejecute el módulo principal:
```bash
python input.py
```