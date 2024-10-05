import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw

# Función para redondear las esquinas de una imagen
def round_image_corners(image, radius):
    # Crear una máscara circular
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
    
    # Aplicar la máscara a la imagen
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

# Función para mostrar los créditos del proyecto
def show_credits():
    messagebox.showinfo("Créditos", "Proyecto de Estimación de Poses\nDesarrollado por: [Fabian Concha, Justo Peres, Abimael Guzman, Giulia Nava, Sebastian Postigo, Gabriel Valdivia]")

# Función para mostrar información extra sobre el proyecto
def show_info():
    messagebox.showinfo("Información del Proyecto", "Este proyecto utiliza OpenCV para capturar video y estimar poses corporales.")

# Función para mostrar la ventana de estimación de poses
def open_pose_estimation_window():
    pose_window = tk.Toplevel(root)  # Crear una nueva ventana
    pose_window.title("Estimación de Poses")
    pose_window.geometry("300x800")  # Definir tamaño de la ventana

    # Mensaje en la nueva ventana
    label = ttk.Label(pose_window, text="Aquí habrá la estimación", font=("Helvetica", 14))
    label.pack(pady=50)

    # Botón para cerrar la ventana
    close_button = ttk.Button(pose_window, text="Cerrar", command=pose_window.destroy, style="danger.TButton")
    close_button.pack(pady=10)

# Función para crear botones con estilo similar a la imagen
def create_button(parent, text, command):
    style = ttk.Style()
    style.configure('my.TButton', font=("Courier New", 14), foreground="white", background="#000033", borderwidth=0)  # Cambiar color de fondo aquí
    button = ttk.Button(parent, text=text, command=command, style='my.TButton', width=15)
    button.pack(pady=5)
    return button

# Función para mostrar el menú principal con diseño similar a la imagen
def show_main_menu():
    # Limpiar la ventana principal
    for widget in root.winfo_children():
        widget.destroy()

    # Cargar la imagen de fondo
    bg_image = Image.open("C:/Users/Usuario/Desktop/Nasa-SpaceApp/NASA2024/bckgrnd.jpg")  # Cambia la ruta aquí
    bg_image = bg_image.resize((1000, 700), Image.LANCZOS)  # Ajusta el tamaño de la imagen a la ventana
    bg_image_tk = ImageTk.PhotoImage(bg_image)

    # Crear una etiqueta para el fondo
    background_label = tk.Label(root, image=bg_image_tk)
    background_label.image = bg_image_tk  # Mantener una referencia a la imagen
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Establecer la etiqueta para que cubra toda la ventana

    # Títulos del menú principal
    title_label = ttk.Label(root, text="Galactic Games", font=("Courier New", 50), foreground="#663399", background="#000033")
    title_label.pack()

    title_label2 = ttk.Label(root, text="Fun in a Microgravity", font=("Courier New", 40), foreground="#663399", background="#000033")
    title_label2.pack()

    title_label3 = ttk.Label(root, text="Environment!", font=("Courier New", 40), foreground="#663399", background="#000033")
    title_label3.pack()

    # Marco para los botones con fondo igual al fondo de la ventana
    button_frame = ttk.Frame(root)  # No especificamos un estilo
    button_frame.pack(pady=20)

    # Botones del menú
    create_button(button_frame, "Start", open_pose_estimation_window)  # Abre la ventana de estimación de poses
    create_button(button_frame, "More Info.", show_info)  # Muestra información extra sobre el proyecto
    create_button(button_frame, "Credits", show_credits)  # Muestra los créditos

    # Cargar la imagen adicional debajo de los botones
    img_path = "C:/Users/Usuario/Desktop/Nasa-SpaceApp/NASA2024/logo.jpg"  # Cambia la ruta aquí
    img = Image.open(img_path)
    img = img.resize((200, 200), Image.LANCZOS)  # Ajustar tamaño según sea necesario

    # Redondear esquinas
    img = round_image_corners(img, radius=30)  # Cambia el radio según lo que desees

    img_tk = ImageTk.PhotoImage(img)

    # Etiqueta para mostrar la imagen
    image_label = ttk.Label(root, image=img_tk)
    image_label.image = img_tk  # Mantener una referencia a la imagen
    image_label.pack(pady=20)  # Ajustar el espacio vertical como sea necesario

# Crear la interfaz gráfica
def create_gui():
    global root
    root = ttk.Window(themename="darkly")  # Ventana con estilo oscuro
    root.title("Galactic Games: Fun in a Microgravity Environment!")
    root.geometry("1000x700")  # Tamaño de la ventana

    # Mostrar el menú principal al inicio
    show_main_menu()

    # Ejecutar el bucle de la ventana
    root.mainloop()

if __name__ == "__main__":
    create_gui()
