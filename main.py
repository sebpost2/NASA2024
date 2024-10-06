import tkinter as tk
from gui import show_main_menu

# Crear la ventana principal
root = tk.Tk()
root.title("Galactic Pose Challenge")
root.geometry("1000x700")
root.configure(bg="#000033")

# Mostrar el menú principal
show_main_menu(root)

# Iniciar el bucle principal de la aplicación
root.mainloop()
