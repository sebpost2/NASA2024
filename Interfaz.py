import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import cv2
import mediapipe as mp
import torch
import os

# Función para redondear las esquinas de una imagen
def round_image_corners(image, radius):
    mask = Image.new('L', image.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, image.size[0], image.size[1]), radius=radius, fill=255)
    rounded_image = Image.new('RGBA', image.size)
    rounded_image.paste(image, (0, 0), mask)
    return rounded_image

# Función para mostrar los créditos del proyecto
def show_credits():
    messagebox.showinfo("Créditos", "Proyecto de Estimación de Poses\nDesarrollado por: [Fabian Concha, Justo Peres, Abimael Guzman, Giulia Nava, Sebastian Postigo, Gabriel Valdivia]")

# Función para mostrar información extra sobre el proyecto
def show_info():
    messagebox.showinfo("Información del Proyecto", "Este proyecto utiliza OpenCV para capturar video y estimar poses corporales.")

# Función que inicia el código de tracking al hacer clic en Start
def iniciar_deteccion():
    root.destroy()  # Cerrar el menú principal

    # Inicializar MediaPipe para la detección de poses
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose

    # Iniciar la captura de video desde la cámara web
    cap = cv2.VideoCapture(0)

    # Configuración del modelo de pose
    with mp_pose.Pose(static_image_mode=False, 
                      model_complexity=2, 
                      enable_segmentation=False,
                      min_detection_confidence=0.5,
                      min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Convertir la imagen de BGR a RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False  # Marca la imagen como no editable

            # Realizar la detección de la pose
            results = pose.process(image)

            # Marcar la imagen como editable nuevamente
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Dibujar las anotaciones de la pose en la imagen
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    h, w, _ = image.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)

                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Mostrar el video en tiempo real
            cv2.imshow('Pose Estimation', image)

            if cv2.waitKey(5) & 0xFF == 27:  # Presiona 'Esc' para salir
                break

    # Liberar la captura y cerrar ventanas
    cap.release()
    cv2.destroyAllWindows()

# Función para crear botones con estilo
def create_button(parent, text, command):
    style = ttk.Style()
    style.configure('my.TButton', font=("Sixtyfour Convergence", 14), foreground="white", background="#000033", borderwidth=0)
    button = ttk.Button(parent, text=text, command=command, style='my.TButton', width=15)
    button.pack(pady=5)
    return button

# Función para mostrar el menú principal
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    bg_image = Image.open("C:/Users/Usuario/Desktop/Nasa-SpaceApp/NASA2024/bckgrnd.jpg")
    bg_image = bg_image.resize((1000, 700), Image.LANCZOS)
    bg_image_tk = ImageTk.PhotoImage(bg_image)
    background_label = tk.Label(root, image=bg_image_tk)
    background_label.image = bg_image_tk
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    title_label = ttk.Label(root, text="Galactic Games", font=("Sixtyfour Convergence", 35), foreground="#663399")
    title_label.pack()
    title_label2 = ttk.Label(root, text="Fun in a Microgravity", font=("Sixtyfour Convergence", 40), foreground="#663399")
    title_label2.pack()
    title_label3 = ttk.Label(root, text="Environment!", font=("Sixtyfour Convergence", 40), foreground="#663399")
    title_label3.pack()

    button_frame = ttk.Frame(root)
    button_frame.pack(pady=20)
    create_button(button_frame, "Start", iniciar_deteccion)  # Inicia la detección
    create_button(button_frame, "More Info.", show_info)
    create_button(button_frame, "Credits", show_credits)

    img_path = "C:/Users/Usuario/Desktop/Nasa-SpaceApp/NASA2024/logo.jpg"
    img = Image.open(img_path)
    img = img.resize((200, 200), Image.LANCZOS)
    img = round_image_corners(img, radius=30)
    img_tk = ImageTk.PhotoImage(img)
    image_label = ttk.Label(root, image=img_tk)
    image_label.image = img_tk
    image_label.pack(pady=20)

# Crear la interfaz gráfica
def create_gui():
    global root
    root = ttk.Window(themename="superhero")
    root.title("Galactic Games: Fun in a Microgravity Environment!")
    root.geometry("1000x700")
    show_main_menu()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
