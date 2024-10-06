import sys
import cv2
import mediapipe as mp
import random
import time
import subprocess
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QSizePolicy
from PySide6.QtCore import QTimer, Qt
from PySide6.QtGui import QImage, QPixmap, QFont
from silhouettes import draw_silhouette, calculate_points_inside_shape

class CameraWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hole in the Wall")
        self.setGeometry(100, 100, 1920, 1080)

        # Layout principal
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Layout para centrar la cámara
        self.camera_layout = QHBoxLayout()
        self.layout.addLayout(self.camera_layout)

        # Label para mostrar la cámara
        self.camera_label = QLabel()
        self.camera_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.camera_layout.addWidget(self.camera_label, alignment=Qt.AlignCenter)

        # Layout para las estadísticas
        self.stats_layout = QHBoxLayout()
        self.layout.addLayout(self.stats_layout)

        # Labels para puntaje, coincidencia y fallos
        self.score_label = QLabel("Puntaje: 0")
        self.match_label = QLabel("Coincidencia: 0%")
        self.fail_label = QLabel("Fallos: 0")

        # Configuración de fuentes
        self.score_label.setFont(QFont("Arial", 20))
        self.match_label.setFont(QFont("Arial", 20))
        self.fail_label.setFont(QFont("Arial", 20))

        self.stats_layout.addWidget(self.score_label, alignment=Qt.AlignLeft)
        self.stats_layout.addWidget(self.match_label, alignment=Qt.AlignCenter)
        self.stats_layout.addWidget(self.fail_label, alignment=Qt.AlignRight)

        # Label para el temporizador
        self.timer_label = QLabel("10s")
        self.timer_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.timer_label)

        # Label para mostrar el mensaje de éxito
        self.success_label = QLabel("")
        self.success_label.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(self.success_label)

        # Botón "Volver al Inicio"
        self.back_button = QPushButton("Volver al Inicio")
        self.back_button.clicked.connect(self.close_camera)

        # Layout para centrar el botón
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.layout.addLayout(button_layout)

        # Configuración inicial para detección y puntajes
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
        self.fails = 0
        self.freeze_time = 2000
        self.timer.start(30)
        self.interface_opened = False
        self.required_landmarks = [0, 11, 12, 23, 24, 31, 32]
        self.body_detected = False
        self.last_success_time = 0  # Para evitar puntajes dobles
        self.success_time = 0  # Para contar tiempo de éxito

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            print("Error al acceder a la cámara.")
            return

        frame = cv2.flip(frame, 1)
        results = self.pose.process(frame)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            self.body_detected = all(landmarks[i].visibility > 0.5 for i in self.required_landmarks)

            if self.body_detected or True:
                mp.solutions.drawing_utils.draw_landmarks(frame, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)

                points = []
                for landmark in landmarks:
                    h, w, _ = frame.shape
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    points.append((cx, cy))

                pts_silhouette, silhouette_mask = draw_silhouette(frame, self.shape_file, match_percentage=0)
                inside_count = calculate_points_inside_shape(pts_silhouette, points)
                total_points = len(points)
                match_percentage = (inside_count / total_points) * 100 if total_points > 0 else 0

                pts_silhouette, silhouette_mask = draw_silhouette(frame, self.shape_file, match_percentage)

                current_time = time.time()

                if match_percentage >= 75:
                    self.success_time += self.timer.interval() / 1000  # Contar el tiempo de coincidencia
                    cv2.putText(frame, "SUCCESS", (frame.shape[1] // 2 - 100, frame.shape[0] // 2),
                                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 5)
                    self.success_label.setText(f"<font color='blue'>Success en {0.75 - self.success_time:.2f} segundos</font>")  # Mostrar el mensaje
                else:
                    self.success_time = 0  # Reiniciar si no se mantiene la coincidencia
                    self.success_label.clear()  # Limpiar el mensaje si no hay éxito

                if self.success_time >= 0.75:  # Solo contar puntaje si se mantiene por 0.75 segundos
                    if self.last_success_time == 0 or (current_time - self.last_success_time >= 0.75):  # Evitar puntaje doble
                        self.score += 1
                        self.last_success_time = current_time  # Registrar el tiempo del éxito
                        self.shape_file = random.choice(self.shape_files)
                        self.start_time = time.time()
                        self.success_time = 0  # Reiniciar contador de éxito

                # Actualizar etiquetas
                self.score_label.setText(f"<font color='green'>Puntaje: {self.score}</font>")
                self.match_label.setText(f"<font color='yellow'>Coincidencia: {match_percentage:.2f}%</font>")
                self.fail_label.setText(f"<font color='red'>Fallos: {self.fails}</font>")

                # Aplicar el formato de la etiqueta
                self.score_label.setOpenExternalLinks(True)
                self.match_label.setOpenExternalLinks(True)
                self.fail_label.setOpenExternalLinks(True)

                elapsed_time = time.time() - self.start_time
                countdown = max(0, 10 - int(elapsed_time))

                # Actualizar temporizador
                self.timer_label.setText(f"{countdown}s")

                if countdown == 0:
                    self.fails += 1
                    self.shape_file = random.choice(self.shape_files)
                    self.start_time = time.time()
            else:
                cv2.putText(frame, "Detectando cuerpo completo...", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        self.display_image(frame)

    def display_image(self, frame):
        image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_BGR888)
        self.camera_label.setPixmap(QPixmap.fromImage(image))

    def close_camera(self):
        self.cap.release()
        self.timer.stop()
        if not self.interface_opened:
            subprocess.Popen([sys.executable, "Interfaz2.py"])
            self.interface_opened = True
        self.close()

    def closeEvent(self, event):
        self.close_camera()
        event.accept()

# Ejecutar la aplicación
app = QApplication(sys.argv)
window = CameraWindow()
window.show()
sys.exit(app.exec())
