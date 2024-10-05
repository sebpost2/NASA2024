import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from PIL import Image, ImageTk, ImageDraw
import cv2
import mediapipe as mp
import torch

# Función para redondear las esquinas de una imagen
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
    # Crear una nueva ventana para los créditos
    credits_window = tk.Toplevel(root)
    credits_window.title("Créditos")
    credits_window.title("Credits")
    credits_window.geometry("400x300")
    credits_window.configure(bg="#060606")

    
    style = ttk.Style()
    style.configure('my.TFrame', font=("Helvetica", 12), foreground="white", background="#060606", borderwidth=0)
    # Using tk.Frame with black background
    frame = ttk.Frame(credits_window, style='my.TFrame', padding=20)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Developers list with tk.Label for custom colors
    developers = ["Fabian Concha", "Justo Perez", "Abimael Ruiz", "Giulia Naval", "Sebastian Postigo", "Gabriel Valdivia"]
    for dev in developers:
        dev_label = ttk.Label(frame, text=dev, font=("Helvetica", 12), foreground="white", background='#060606')
        dev_label.pack(anchor="w", padx=10, pady=2)

    # Botón de cerrar ventana
    close_button = tk.Button(frame, text="Cerrar", command=credits_window.destroy,  bg='#060606',
                fg='#b00000')
    close_button.pack(pady=(20, 0))


# Function to show extra project information
def show_info():
    messagebox.showinfo("Project Information", "This project uses OpenCV to capture video and estimate body poses.")

# Function to start detection on 'Start' button click
def iniciar_deteccion():
    root.destroy()
    yolo_model = torch.hub.load('ultralytics/yolov5', 'yolov5s')
    yolo_model.classes = [0]

    mp_drawing = mp.solutions.drawing_utils
    mp_pose = mp.solutions.pose
    cap = cv2.VideoCapture(0)

    with mp_pose.Pose(min_detection_confidence=0.3, min_tracking_confidence=0.3) as pose:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            result = yolo_model(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            MARGIN = 10

            for (xmin, ymin, xmax, ymax, confidence, clas) in result.xyxy[0].tolist():
                crop_image = image[int(ymin) + MARGIN:int(ymax) + MARGIN, int(xmin) + MARGIN:int(xmax) + MARGIN]
                crop_rgb = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
                results = pose.process(crop_rgb)

                if results.pose_landmarks:
                    mp_drawing.draw_landmarks(crop_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                              mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                              mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))

                image[int(ymin) + MARGIN:int(ymax) + MARGIN, int(xmin) + MARGIN:int(xmax) + MARGIN] = crop_image

            cv2.imshow('Real-Time Person and Pose Detection', image)
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

    bg_image = Image.open("/home/sebpost02/Documents/NASA2024/NASA2024/bckgrnd.jpg")
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

    img_path = "/home/sebpost02/Documents/NASA2024/NASA2024/logo.jpg"
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
    root.title("Galactic Games: Fun in a Microgravity Environment!")
    root.geometry("1000x700")
    show_main_menu()
    root.mainloop()

if __name__ == "__main__":
    create_gui()
