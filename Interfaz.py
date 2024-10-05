import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import cv2
import mediapipe as mp
import numpy as np
import time

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
    credits_window = tk.Toplevel(root)
    credits_window.title("Créditos")
    credits_window.geometry("400x300")
    credits_window.configure(bg="#000033")
    
    frame = ttk.Frame(credits_window, padding=20, bootstyle="primary", relief="solid", borderwidth=3)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    developers = ["Fabian Concha", "Justo Peres", "Abimael Guzman", "Giulia Nava", "Sebastian Postigo", "Gabriel Valdivia"]
    for dev in developers:
        dev_label = ttk.Label(frame, text=dev, font=("Helvetica", 12), foreground="white")
        dev_label.pack(anchor="w", padx=10, pady=2)

    close_button = ttk.Button(frame, text="Cerrar", command=credits_window.destroy, bootstyle="danger")
    close_button.pack(pady=(20, 0))

# Función para mostrar información extra sobre el proyecto
def show_info():
    messagebox.showinfo("Información del Proyecto", "Este proyecto utiliza OpenCV para capturar video y estimar poses corporales.")

# Función para dibujar la silueta cargada
def draw_silhouette(frame):
    pts = np.loadtxt("shapeCoords/sil01.txt", dtype=int)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=(0, 0, 255), thickness=5)  # Dibuja en rojo
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)  # Máscara en escala de grises
    cv2.fillPoly(mask, [pts], 255)
    return pts, mask

# Función para calcular el porcentaje de puntos dentro de la silueta
def calculate_points_inside_shape(pts_silhouette, points):
    inside_count = 0
    for point in points:
        # Utilizamos pointPolygonTest para comprobar si el punto está dentro (resultado > 0)
        result = cv2.pointPolygonTest(pts_silhouette, (point[0], point[1]), False)
        if result >= 0:
            inside_count += 1
    return inside_count

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

        # Variable para controlar el tiempo de actualización
        last_update_time = time.time()

        while cap.isOpened():
            # Leer el frame de la cámara
            ret, frame = cap.read()

            if not ret:
                print("Error al acceder a la cámara.")
                break

            # Convertir la imagen de BGR a RGB
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False  # Marca la imagen como no editable

            # Realizar la detección de la pose
            results = pose.process(image_rgb)

            # Marcar la imagen como editable nuevamente
            image_rgb.flags.writeable = True
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            # Dibujar la silueta en el frame
            pts_silhouette, silhouette_mask = draw_silhouette(image_bgr)

            # Generar puntos a partir de los landmarks de la pose
            points = []
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    h, w, _ = image_bgr.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    points.append((cx, cy))  # Guardar las coordenadas de los landmarks

            # Comprobar cuántos puntos están dentro de la silueta
            inside_count = calculate_points_inside_shape(pts_silhouette, points)
            
            # Calcular el porcentaje de puntos que están dentro
            total_points = len(points)
            if total_points > 0:
                match_percentage = (inside_count / total_points) * 100
                cv2.putText(image_bgr, f"Coincidencia: {match_percentage:.2f}%", (10, 30), 
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Dibujar los puntos en el frame (para visualización)
            for point in points:
                cv2.circle(image_bgr, point, 5, (255, 255, 0), -1)  # Dibuja los puntos en color azul

            cv2.imshow("Hole in the Wall", image_bgr)

            # Presiona 'q' para salir
            if cv2.waitKey(1) & 0xFF == ord('q'):
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
