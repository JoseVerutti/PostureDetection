import tkinter as tk
from PIL import Image, ImageTk
import subprocess
import threading

# Definir el color beige
BEIGE_COLOR = "#F5F5DC"

# Definir el estilo de botón
BUTTON_STYLE = {
    "bg": "#4A90E2",
    "fg": "white",
    "font": ("Helvetica", 12),
    "relief": "raised",
    "bd": 2,
    "padx": 10,
    "pady": 5
}

# Crear la ventana principal de Tkinter
def abrir_ventana_principal():
    root = tk.Tk()
    root.title("EI4work - Inicio")
    root.configure(bg=BEIGE_COLOR)
    root.geometry("400x350")

    # Cargar la imagen del logo
    logo_image = Image.open("logo.png")
    logo_image = logo_image.resize((200, 200))
    logo_photo = ImageTk.PhotoImage(logo_image)

    # Crear un widget Label para mostrar la imagen
    logo_label = tk.Label(root, image=logo_photo, bg=BEIGE_COLOR)
    logo_label.pack(pady=20)

    # Función para iniciar la detección (ejecutar el archivo main.py)
    def iniciar_deteccion():
        # Mostrar la pantalla de carga en un nuevo hilo
        thread = threading.Thread(target=mostrar_splash_y_ejecutar)
        thread.start()

    # Crear un botón que ejecuta la detección
    start_button = tk.Button(root, text="Iniciar detección", command=iniciar_deteccion, **BUTTON_STYLE)
    start_button.pack(pady=20)

    # Ejecutar la ventana principal
    root.mainloop()

# Función para mostrar la pantalla de carga y luego ejecutar el archivo main.py
def mostrar_splash_y_ejecutar():
    splash = tk.Tk()
    splash.title("Cargando...")
    splash.geometry("300x200")
    splash.configure(bg=BEIGE_COLOR)

    splash_label = tk.Label(splash, text="Abriendo la aplicación...", font=("Helvetica", 16), bg=BEIGE_COLOR)
    splash_label.pack(expand=True)

    # Ejecutar el archivo main.py en un hilo separado para no bloquear la UI
    def ejecutar_aplicacion():
        subprocess.Popen([r"venv\Scripts\python.exe", "main.py"])
        # Cerrar la ventana de splash una vez que el proceso se haya iniciado
        splash.after(1000, splash.destroy)

    # Crear un hilo para ejecutar el proceso de la aplicación
    hilo_aplicacion = threading.Thread(target=ejecutar_aplicacion)
    hilo_aplicacion.start()

    splash.mainloop()

# Crear ventana de splash screen inicial
def mostrar_splash_screen():
    splash = tk.Tk()
    splash.title("Cargando...")
    splash.geometry("300x200")
    splash.configure(bg=BEIGE_COLOR)

    splash_label = tk.Label(splash, text="Cargando la aplicación...", font=("Helvetica", 16), bg=BEIGE_COLOR)
    splash_label.pack(expand=True)

    # Simular un tiempo de carga de 3 segundos
    splash.after(3000, lambda: [splash.destroy(), abrir_ventana_principal()])

    splash.mainloop()

# Ejecutar el splash screen inicial
mostrar_splash_screen()
