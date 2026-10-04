import random
import tkinter as tk
from tkinter import messagebox

def procesarDatos():
    """Devuelve (cantidadNodos, modo, nombre), o None si se cierra la ventana sin terminar.
    modo: 1 = manual, 2 = automático."""
    configGrafo = {"nodos": None, "modo": None, "nombre": None}

    ventanaPrincipal = tk.Tk()
    ventanaPrincipal.title("Proyecto Mate Computacional")
    ventanaPrincipal.geometry("640x480")

    def validarPaso():
        nombre = entradaNombre.get().strip()
        modo_texto = entradaModo.get().strip()

        if not nombre or not modo_texto:
            messagebox.showwarning("Error", "Por favor, llena todos los campos.")
            return

        try:
            modo = int(modo_texto)
        except ValueError:
            messagebox.showerror("Error", "El modo debe ser 1 (Manual) o 2 (Automático).")
            return

        if modo not in (1, 2):
            messagebox.showerror("Error", "El modo debe ser 1 (Manual) o 2 (Automático).")
            return

        configGrafo["nombre"] = nombre
        configGrafo["modo"] = modo

        if modo == 1:
            abrirVentanas()
        else:
            configGrafo["nodos"] = random.randint(7, 16)
            messagebox.showinfo("Éxito", f"Generación automática: {configGrafo['nodos']} nodos.")
            ventanaPrincipal.destroy()

    def abrirVentanas():
        ventana2 = tk.Toplevel(ventanaPrincipal)
        ventana2.title("Procedimiento Manual")
        ventana2.geometry("450x200")
        ventana2.grab_set()   # evita abrir varias ventanas pulsando "Siguiente" repetidamente

        tk.Label(ventana2, text="Introduce la cantidad de nodos (7 a 16)",
                 font=("Times New Roman", 16, "bold"), fg="black").pack(pady=40)
        entradaCantidadNodos = tk.Entry(ventana2, width=30)
        entradaCantidadNodos.pack(pady=5)
        entradaCantidadNodos.focus_set()

        def guardarNodos():
            try:
                cantidadNodos = int(entradaCantidadNodos.get())
            except ValueError:
                messagebox.showerror("Error.", "Ingresar números enteros válidos.", parent=ventana2)
                return

            if 7 <= cantidadNodos <= 16:
                configGrafo["nodos"] = cantidadNodos
                messagebox.showinfo("Éxito.", f"Configurado para {cantidadNodos} nodos", parent=ventana2)
                ventana2.destroy()
                ventanaPrincipal.destroy()
            else:
                messagebox.showwarning("Error.", "La cantidad debe estar entre 7 y 16", parent=ventana2)

        tk.Button(ventana2, text="Terminar", command=guardarNodos).pack(pady=15)
        # sin ventana2.mainloop(): el mainloop de la ventana principal ya atiende a esta

    tk.Label(ventanaPrincipal, text="ALGORITMO DE FORD FULKERSON",
             font=("Times New Roman", 20, "bold"), fg="black").pack(pady=40)

    tk.Label(ventanaPrincipal, text="Introduce el nombre del grafo: ").pack(pady=5)
    entradaNombre = tk.Entry(ventanaPrincipal, width=30)
    entradaNombre.pack(pady=5)

    tk.Label(ventanaPrincipal, text="Manual o automático? (1 o 2): ").pack(pady=5)
    entradaModo = tk.Entry(ventanaPrincipal, width=30)
    entradaModo.pack(pady=5)

    tk.Button(ventanaPrincipal, text="Siguiente", command=validarPaso).pack(pady=30)

    ventanaPrincipal.mainloop()

    if configGrafo["nodos"] is None:
        return None
    return configGrafo["nodos"], configGrafo["modo"], configGrafo["nombre"]