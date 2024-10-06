import sys
import subprocess
import cv2
import fitz
import mediapipe as mp
import pygame
import logging
import os
import psutil  # Asegúrate de tener psutil instalado
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QSizePolicy, QSpacerItem, QGraphicsOpacityEffect, QScrollArea
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QFont, QPixmap, QPalette, QBrush, QFontDatabase, QPainter, QPen

# Silenciar mensajes de advertencia
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Para TensorFlow
logging.getLogger('absl').setLevel(logging.ERROR)  # Para Mediapipe

# Rutas de la fuente, imágenes
FONT_PATH = "static/SixtyfourConvergence-Regular.ttf"
LOGO_PATH = "Images/logo.jpg"
TEAM_LOGO_PATH = "Images/team.jpg"
BACKGROUND_PATH = "Images/bckgrnd.jpg"
PDF_PATH = "Images/info.pdf"
AUDIO_PATH = "Images/menuSong.mp3"
BUTTON_SOUND_PATH = "Images/button-pressed-38129.mp3"

class InstructionsScreen(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Instructions")
        self.setGeometry(100, 100, 1000, 600)
        layout = QVBoxLayout(self)

        # Texto de instrucciones
        instructions_text = """
        Welcome to ASTRO·SHAPE!
        Please follow the instructions below:
        - Step back far enough for the camera to detect your full body.
        - You must match the silhouette that will appear on the screen.
        - You need at least 70% accuracy for 0.75 seconds to succeed.
        - Perform the poses shown on the screen within 10 seconds.
        - The green color indicates you're doing well.
        - A successfully matched pose will show "Success".
        - Then, a new pose will appear.
        THANK YOU FOR USING ASTRO·SHAPE!
        """
        
        # Crear QLabel para mostrar el texto de instrucciones
        instructions_label = QLabel(instructions_text, self)
        instructions_label.setFont(QFont("Arial", 20))
        instructions_label.setAlignment(Qt.AlignCenter)
        instructions_label.setWordWrap(True)
        layout.addWidget(instructions_label)
        
        # Agregar espaciador vertical
        layout.addSpacerItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Crear botón para continuar
        continue_button = QPushButton("Continue to Pose Detection", self)
        continue_button.setFont(QFont("Arial", 18))
        continue_button.clicked.connect(self.start_detection)
        layout.addWidget(continue_button, alignment=Qt.AlignCenter)

    def start_detection(self):
        self.close()  # Cerrar la ventana de instrucciones
        subprocess.Popen([sys.executable, "tracking.py"])  # Ejecutar tracking.py

def show_instructions(parent):
    parent.close()
    instructions_screen = InstructionsScreen(parent)
    instructions_screen.exec()

class PDFViewer(QDialog):
    def __init__(self, pdf_path):
        super().__init__()
        self.setWindowTitle("More Info")
        self.setGeometry(100, 100, 800, 600)
        self.layout = QVBoxLayout(self)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.layout.addWidget(self.scroll_area)
        self.pdf_widget = QWidget()
        self.pdf_layout = QVBoxLayout(self.pdf_widget)
        self.zoom_level = 1.0
        self.load_pdf(pdf_path)
        self.scroll_area.setWidget(self.pdf_widget)
        zoom_in_button = QPushButton("Zoom In")
        zoom_out_button = QPushButton("Zoom Out")
        close_button = QPushButton("Close")
        zoom_in_button.clicked.connect(self.zoom_in)
        zoom_out_button.clicked.connect(self.zoom_out)
        close_button.clicked.connect(self.close)
        button_layout = QHBoxLayout()
        button_layout.addWidget(zoom_in_button)
        button_layout.addWidget(zoom_out_button)
        button_layout.addWidget(close_button)
        self.layout.addLayout(button_layout)

    def load_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            pix = page.get_pixmap()
            img = QPixmap()
            img.loadFromData(pix.tobytes())
            img = img.scaled(img.size() * self.zoom_level, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pdf_label = QLabel()
            pdf_label.setPixmap(img)
            pdf_label.setAlignment(Qt.AlignCenter)
            self.pdf_layout.addWidget(pdf_label)

    def zoom_in(self):
        self.zoom_level *= 1.2
        self.update_pdf_images()

    def zoom_out(self):
        self.zoom_level /= 1.2
        self.update_pdf_images()

    def update_pdf_images(self):
        for i in reversed(range(self.pdf_layout.count())):
            self.pdf_layout.itemAt(i).widget().deleteLater()
        self.load_pdf(PDF_PATH)

def round_pixmap(pixmap, radius):
    rounded_pixmap = QPixmap(pixmap.size())
    rounded_pixmap.fill(Qt.transparent)
    painter = QPainter(rounded_pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setPen(QPen(Qt.transparent))
    rect = QRect(0, 0, pixmap.width(), pixmap.height())
    painter.drawRoundedRect(rect, radius, radius)
    painter.setClipRect(rect)
    painter.drawPixmap(0, 0, pixmap)
    painter.end()
    return rounded_pixmap

def start_detection():
    app.quit()
    subprocess.Popen([sys.executable, "tracking.py"])

def show_credits():
    credits_dialog = QDialog()
    credits_dialog.setWindowTitle("Credits")
    credits_dialog.setGeometry(400, 400, 300, 200)
    layout = QVBoxLayout()
    credits = ["CREDITS:", "Fabian Concha", "Giulia Naval", "Justo Perez", "Abimael Ruiz", "Sebastian Postigo", "Gabriel Valdivia"]
    for credit in credits:
        label = QLabel(credit)
        label.setFont(QFont("Arial", 12))
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)
    close_button = QPushButton("Close")
    close_button.clicked.connect(credits_dialog.close)
    layout.addWidget(close_button)
    credits_dialog.setLayout(layout)
    credits_dialog.exec()

def show_info():
    pdf_viewer = PDFViewer(PDF_PATH)
    pdf_viewer.exec()

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("ASTRO·SHAPE")
        self.setGeometry(100, 100, 1920, 1080)
        pygame.mixer.init()
        pygame.mixer.music.load(AUDIO_PATH)
        pygame.mixer.music.play(-1)
        self.button_sound = pygame.mixer.Sound(BUTTON_SOUND_PATH)
        font_id = QFontDatabase.addApplicationFont(FONT_PATH)
        family = QFontDatabase.applicationFontFamilies(font_id)
        custom_font = QFont(family[0], 24) if family else QFont("Arial", 24)
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        palette = QPalette()
        background = QPixmap(BACKGROUND_PATH)
        palette.setBrush(QPalette.Window, QBrush(background.scaled(self.size(), Qt.IgnoreAspectRatio)))
        self.setPalette(palette)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.title_label = QLabel("ASTRO·SHAPE", self)
        self.title_label.setFont(QFont(family[0], 36))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.opacity_effect = QGraphicsOpacityEffect()
        self.title_label.setGraphicsEffect(self.opacity_effect)
        layout.addWidget(self.title_label)
        
        # Temporizador para parpadeo del título
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_title)
        self.blink_timer.start(500)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Crear una lista para contener los botones
        self.buttons = []
        for button_text in ["Start", "Credits", "More Info"]:
            button = QPushButton(button_text, self)
            button.setFont(custom_font)
            button.clicked.connect(self.on_button_click)
            layout.addWidget(button, alignment=Qt.AlignCenter)
            self.buttons.append(button)
            self.create_blinking_effect(button)

        image_layout = QHBoxLayout()
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(LOGO_PATH)
        rounded_logo_pixmap = round_pixmap(logo_pixmap, 60)
        logo_label.setPixmap(rounded_logo_pixmap.scaled(130, 130, Qt.KeepAspectRatio))
        image_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        team_label = QLabel(self)
        team_pixmap = QPixmap(TEAM_LOGO_PATH)
        rounded_team_pixmap = round_pixmap(team_pixmap, 60)
        team_label.setPixmap(rounded_team_pixmap.scaled(130, 130, Qt.KeepAspectRatio))
        image_layout.addWidget(team_label, alignment=Qt.AlignCenter)
        layout.addLayout(image_layout)

        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

    def create_blinking_effect(self, button):
        effect = QGraphicsOpacityEffect()
        button.setGraphicsEffect(effect)
        timer = QTimer(self)
        timer.timeout.connect(lambda: self.blink_button(button, effect))
        timer.start(500)

    def blink_button(self, button, effect):
        current_opacity = effect.opacity()
        new_opacity = 0.0 if current_opacity == 1.0 else 1.0
        effect.setOpacity(new_opacity)

    def on_button_click(self):
        button = self.sender()
        self.button_sound.play()  # Reproducir sonido al presionar
        if button.text() == "Start":
            show_instructions(self)
        elif button.text() == "Credits":
            show_credits()
        elif button.text() == "More Info":
            show_info()

    def blink_title(self):
        current_opacity = self.opacity_effect.opacity()
        new_opacity = 0.0 if current_opacity == 1.0 else 1.0
        self.opacity_effect.setOpacity(new_opacity)

    def closeEvent(self, event):
        self.terminate_subprocesses()  # Llama a terminate_subprocesses al cerrar
        pygame.mixer.music.stop()  # Detener la música
        event.accept()  # Aceptar el evento de cierre

    def terminate_subprocesses(self):
        # Revisa todos los procesos activos y termina los que se iniciaron desde este script
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                if proc.name() == "python" and proc.pid != os.getpid():
                    proc.terminate()  # Termina el proceso
                    try:
                        proc.wait(timeout=1)  # Espera a que el proceso termine
                    except psutil.TimeoutExpired:
                        proc.kill()  # Si no termina, forzar su cierre
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
    