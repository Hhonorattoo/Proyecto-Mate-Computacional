import tkinter as tk
from tkinter import messagebox

# 1. Función para procesar y trabajar con los datos recibidos
def procesar_datos():
    # Obtener el texto de los campos de entrada (.get())
    nombre = entrada_nombre.get()
    edad_texto = entrada_edad.get()
    
    # Validar que los campos no estén vacíos
    if not nombre or not edad_texto:
        messagebox.showwarning("Error", "Por favor, llena todos los campos.")
        return
        
    try:
        # Convertir la edad a número para poder trabajar con ella
        edad = int(edad_texto)
        edad_futura = edad + 10
        
        # Trabajar con los datos: Crear el mensaje final
        resultado = f"¡Hola, {nombre}!\nEn 10 años tendrás {edad_futura} años."
        
        # Mostrar el resultado en una ventana emergente
        messagebox.showinfo("Resultado", resultado)
        
    except ValueError:
        # Control de errores si el usuario no ingresa un número en la edad
        messagebox.showerror("Error", "Por favor, introduce una edad válida (número entero).")

# 2. Configuración de la ventana principal
ventana = tk.Tk()
ventana.title("Formulario Interactivo")
ventana.geometry("640x480")  # Ancho x Alto

# 3. Creación de los elementos (Widgets)

# Etiqueta y Campo para el Nombre
titulo_visual = tk.Label(ventana, text="REGISTRO DE USUARIOS", font=("Times New Roman", 16, "bold"), fg="black")
titulo_visual.pack(pady=50)

etiqueta_nombre = tk.Label(ventana, text="Introduce tu nombre:")
etiqueta_nombre.pack(pady=5)

entrada_nombre = tk.Entry(ventana, width=30)
entrada_nombre.pack(pady=5)

# Etiqueta y Campo para la Edad
etiqueta_edad = tk.Label(ventana, text="Introduce tu edad:")
etiqueta_edad.pack(pady=5)

entrada_edad = tk.Entry(ventana, width=30)
entrada_edad.pack(pady=5)

# Botón para enviar y activar la función
boton_enviar = tk.Button(ventana, text="Procesar Datos", command=procesar_datos)
boton_enviar.pack(pady=15)


# 4. Iniciar el bucle de la aplicación (mantiene la ventana abierta)
ventana.mainloop()
