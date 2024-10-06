import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import cv2
import mediapipe as mp
import numpy as np
import time
import random

# Function to round image corners
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

# Function to show extra project information
def show_info():
    messagebox.showinfo("Project Information", "This project uses OpenCV to capture video and estimate body poses.")

# Función para dibujar la silueta cargada con color dinámico
def draw_silhouette(frame, shape_file, match_percentage):
    color = (0, 255, 0) if match_percentage >= 50 else (0, 0, 255)  # Cambiar a verde al 50%
    pts = np.loadtxt(shape_file, dtype=int)
    pts = pts.reshape((-1, 1, 2))
    cv2.polylines(frame, [pts], isClosed=True, color=color, thickness=5)
    mask = np.zeros(frame.shape[:2], dtype=np.uint8)
    cv2.fillPoly(mask, [pts], 255)
    return pts, mask

# Función para calcular el porcentaje de puntos dentro de la silueta
def calculate_points_inside_shape(pts_silhouette, points):
    inside_count = 0
    for point in points:
        result = cv2.pointPolygonTest(pts_silhouette, (point[0], point[1]), False)
        if result >= 0:
            inside_count += 1
    return inside_count

# Función que inicia el código de tracking al hacer clic en Start
def iniciar_deteccion():
    root.destroy()
    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)

    # Lista de archivos de siluetas
    shape_files = ["shapeCoords/sil01.txt", "shapeCoords/sil02.txt", "shapeCoords/sil03.txt"]
    shape_file = random.choice(shape_files)
    start_time = time.time()
    score = 0
    score_incremented = False  # Variable para controlar el incremento del puntaje

    with mp_pose.Pose(static_image_mode=False, model_complexity=2, enable_segmentation=False,
                      min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("Error al acceder a la cámara.")
                break

            # Invertir horizontalmente la imagen de la cámara
            frame = cv2.flip(frame, 1)

            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image_rgb.flags.writeable = False
            results = pose.process(image_rgb)
            image_rgb.flags.writeable = True
            image_bgr = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(image_bgr, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Generar puntos a partir de los landmarks de la pose
            points = []
            if results.pose_landmarks:
                for landmark in results.pose_landmarks.landmark:
                    h, w, _ = image_bgr.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    points.append((cx, cy))

            pts_silhouette, silhouette_mask = draw_silhouette(image_bgr, shape_file, match_percentage=0)
            inside_count = calculate_points_inside_shape(pts_silhouette, points)
            total_points = len(points)
            match_percentage = (inside_count / total_points) * 100 if total_points > 0 else 0

            # Dibujar la silueta en el frame con color dinámico según el porcentaje
            pts_silhouette, silhouette_mask = draw_silhouette(image_bgr, shape_file, match_percentage)

            # Incrementar puntaje solo una vez por pose
            if match_percentage >= 50 and not score_incremented:
                # Mostrar texto de éxito antes de congelar la pantalla
                cv2.putText(image_bgr, "SUCCESS", (frame.shape[1] // 2 - 100, frame.shape[0] // 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 5)  # Color amarillo
                cv2.imshow("Hole in the Wall", image_bgr)  # Mostrar imagen con el texto
                cv2.waitKey(2000)  # Esperar 2 segundos

                score += 1  # Incrementar puntaje
                score_incremented = True  # Marcar que se ha incrementado el puntaje
                shape_file = random.choice(shape_files)  # Cambiar a una nueva silueta

            if match_percentage < 50:
                score_incremented = False  # Reiniciar el estado si no hay coincidencia

            # Mostrar el puntaje en la parte inferior izquierda
            cv2.putText(image_bgr, f"Puntaje: {score}", (10, frame.shape[0] - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            # Muestra el porcentaje de coincidencia en la pantalla
            cv2.putText(image_bgr, f"Coincidencia: {match_percentage:.2f}%", (10, 30), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            # Temporizador y cambio de archivo cada 10 segundos
            elapsed_time = time.time() - start_time
            countdown = max(0, 10 - int(elapsed_time))

            # Mostrar temporizador centrado en la parte superior
            timer_text = f"{countdown}s"
            text_size = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 2.5, 5)[0]
            text_x = (frame.shape[1] - text_size[0]) // 2
            cv2.putText(image_bgr, timer_text, (text_x, 60),
                        cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 5)

            if countdown == 0:
                shape_file = random.choice(shape_files)
                start_time = time.time()

            cv2.imshow("Hole in the Wall", image_bgr)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    cap.release()
    cv2.destroyAllWindows()


# Function to create styled buttons
def create_button(parent, text, command):
    style = ttk.Style()
    style.configure('my.TButton', font=("Sixtyfour Convergence", 14), foreground="white", background="#000033", borderwidth=0)
    button = ttk.Button(parent, text=text, command=command, style='my.TButton', width=15)
    button.pack(pady=5)
    return button

# Function to show the main menu
def show_main_menu():
    for widget in root.winfo_children():
        widget.destroy()

    bg_image = Image.open("Images/bckgrnd.jpg")
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
    create_button(button_frame, "Start", iniciar_deteccion)
    create_button(button_frame, "More Info.", show_info)
    create_button(button_frame, "Credits", show_credits)

    img_path = "Images/logo.jpg"
    img = Image.open(img_path)
    img = img.resize((200, 200), Image.LANCZOS)
    img = round_image_corners(img, radius=30)
    img_tk = ImageTk.PhotoImage(img)
    image_label = ttk.Label(root, image=img_tk)
    image_label.image = img_tk
    image_label.pack(pady=20)

# Create GUI
def create_gui():
    global root
    root = ttk.Window(themename="superhero")
    root.title("Astro·")
    root.geometry("1000x700")
    show_main_menu()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
