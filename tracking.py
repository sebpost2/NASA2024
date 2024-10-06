import sys
import cv2
import mediapipe as mp
import random
import time
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap
from silhouettes import draw_silhouette, calculate_points_inside_shape

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hole in the Wall")
        self.setGeometry(100, 100, 1920, 1080)  # Cambiado a 1920x1080

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout para centrar la cámara
        self.camera_layout = QHBoxLayout()
        self.layout.addLayout(self.camera_layout)

        # Label para mostrar la cámara, ocupa casi toda la ventana
        self.camera_label = QLabel()
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)  # Política de tamaño expandible
        self.camera_layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)  # Centra el QLabel

        # Botón "Volver al Inicio"
        self.back_button = QPushButton("Volver al Inicio")
        self.back_button.clicked.connect(self.close_camera)

        # Usamos un layout horizontal para centrar el botón
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        
        # Añadir el layout del botón debajo de la cámara
        self.layout.addLayout(button_layout)

        # Iniciar detección
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.cap = cv2.VideoCapture(0)
        self.pose = mp.solutions.pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        self.shape_files = ["shapeCoords/sil01.txt", "shapeCoords/sil02.txt", "shapeCoords/sil03.txt"]
        self.shape_file = random.choice(self.shape_files)
        self.start_time = time.time()
        self.score = 0
        self.score_incremented = False
        self.freeze_time = 2000  # tiempo de pausa en milisegundos
        self.timer.start(30)
        self.interface_opened = False

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error al acceder a la cámara.")
            return

        frame = cv2.flip(frame, 1)  # Reflejar la imagen para que sea más intuitiva
        results = self.pose.process(frame)

        if results.pose_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

        points = []
        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                points.append((cx, cy))

        pts_silhouette, silhouette_mask = draw_silhouette(frame, self.shape_file, match_percentage=0)
        inside_count = calculate_points_inside_shape(pts_silhouette, points)
        total_points = len(points)
        match_percentage = (inside_count / total_points) * 100 if total_points > 0 else 0

        pts_silhouette, silhouette_mask = draw_silhouette(frame, self.shape_file, match_percentage)

        if match_percentage >= 50 and not self.score_incremented:
            cv2.putText(frame, "SUCCESS", (frame.shape[1] // 2 - 100, frame.shape[0] // 2),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)  # Cambiamos a verde
            self.display_image(frame)

            self.score += 1
            self.score_incremented = True
            self.shape_file = random.choice(self.shape_files)
            self.start_time = time.time()

            # Pausar por 2 segundos antes de continuar
            QTimer.singleShot(self.freeze_time, self.timer.start)  # reanuda el timer después de 2s
            self.timer.stop()
            return

        if match_percentage < 50:
            self.score_incremented = False

        cv2.putText(frame, f"Puntaje: {self.score}", (10, frame.shape[0] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        cv2.putText(frame, f"Coincidencia: {match_percentage:.2f}%", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        elapsed_time = time.time() - self.start_time
        countdown = max(0, 10 - int(elapsed_time))

        timer_text = f"{countdown}s"
        text_size = cv2.getTextSize(timer_text, cv2.FONT_HERSHEY_SIMPLEX, 2.5, 5)[0]
        text_x = (frame.shape[1] - text_size[0]) // 2
        cv2.putText(frame, timer_text, (text_x, 60),
                    cv2.FONT_HERSHEY_SIMPLEX, 2.5, (0, 0, 255), 5)

        if countdown == 0:
            self.shape_file = random.choice(self.shape_files)
            self.start_time = time.time()

        # Mostrar el frame en el QLabel
        self.display_image(frame)

    def display_image(self, frame):
        # Convierte el frame en formato QImage para QLabel
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        self.camera_label.setPixmap(QPixmap.fromImage(image))

    def close_camera(self):
        self.cap.release()
        self.timer.stop()
        if not self.interface_opened:
            subprocess.Popen([sys.executable, "Interfaz2.py"])
            self.interface_opened = True  # Cambia el estado a True
        self.close()

    def closeEvent(self, event):
        self.close_camera()
        event.accept()

# Ejecutar la aplicación
app = QApplication(sys.argv)
window = CameraWindow()
window.show()
sys.exit(app.exec())
