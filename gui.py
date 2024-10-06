from PIL import Image, ImageTk  # Asegúrate de que esta línea esté presente
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from tracking import iniciar_deteccion

def show_credits():
    credits_window = tk.Toplevel(root)
    credits_window.title("Credits")
    credits_window.geometry("400x300")
    credits_window.configure(bg="#060606")

    style = ttk.Style()
    style.configure('my.TFrame', font=("Helvetica", 12), foreground="white", background="#060606", borderwidth=0)
    frame = ttk.Frame(credits_window, style='my.TFrame', padding=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    developers = ["Fabian Concha", "Justo Perez", "Abimael Ruiz", "Giulia Naval", "Sebastian Postigo", "Gabriel Valdivia"]
    for dev in developers:
        dev_label = ttk.Label(frame, text=dev, font=("Helvetica", 12), foreground="white", background='#060606')
        dev_label.pack(anchor="w", padx=10, pady=2)

    close_button = tk.Button(frame, text="Cerrar", command=credits_window.destroy, bg='#060606', fg='#b00000')
    close_button.pack(pady=(20, 0))

def show_info():
    messagebox.showinfo("Project Information", "This project uses OpenCV to capture video and estimate body poses.")

def show_main_menu(root):
    for widget in root.winfo_children():
        widget.destroy()

    bg_image = Image.open("Images/bckgrnd.jpg")  # Actualiza la ruta aquí
    bg_image = bg_image.resize((1000, 700), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(root, image=bg_image_tk)
    background_label.image = bg_image_tk
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = ttk.Label(root, text="Galactic Pose Challenge", font=("Helvetica", 24), foreground="white", background="#000033")
    title_label.pack(pady=(20, 0))

    start_button = create_button(root, "Iniciar", iniciar_deteccion)
    credits_button = create_button(root, "Créditos", show_credits)
    info_button = create_button(root, "Información", show_info)

def create_button(parent, text, command):
    style = ttk.Style()
    style.configure('my.TButton', font=("Sixtyfour Convergence", 14), foreground="white", background="#000033", borderwidth=0)
    button = ttk.Button(parent, text=text, command=command, style='my.TButton', width=15)
    button.pack(pady=5)
    return button
