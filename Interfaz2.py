import sys
import subprocess
import cv2
import fitz
import mediapipe as mp
import pygame
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QSizePolicy, QSpacerItem, QGraphicsOpacityEffect, QScrollArea
from PySide6.QtCore import Qt, QTimer, QRect
from PySide6.QtGui import QFont, QPixmap, QPalette, QBrush, QFontDatabase, QPainter, QPen

# Rutas de la fuente, imágenes
FONT_PATH = "static/SixtyfourConvergence-Regular.ttf"
LOGO_PATH = "Images/logo.jpg"
TEAM_LOGO_PATH = "Images/team.jpg"
BACKGROUND_PATH = "Images/bckgrnd.jpg"
PDF_PATH = "Images/info.pdf"
AUDIO_PATH = "Images/menuSong.mp3"
BUTTON_SOUND_PATH = "Images/button-pressed-38129.mp3"

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
        self.setGeometry(100, 100, 1920, 1080)  # Cambiado a 1920x1080
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
        self.blink_timer = QTimer(self)
        self.blink_timer.timeout.connect(self.blink_title)
        self.blink_timer.start(500)
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.start_button = QPushButton("Start", self)
        self.start_button.setFont(custom_font)
        self.start_button.clicked.connect(self.on_button_click)
        layout.addWidget(self.start_button, alignment=Qt.AlignCenter)
        self.credits_button = QPushButton("Credits", self)
        self.credits_button.setFont(custom_font)
        self.credits_button.clicked.connect(self.on_button_click)
        layout.addWidget(self.credits_button, alignment=Qt.AlignCenter)
        self.info_button = QPushButton("More Info", self)
        self.info_button.setFont(custom_font)
        self.info_button.clicked.connect(self.on_button_click)
        layout.addWidget(self.info_button, alignment=Qt.AlignCenter)
        image_layout = QHBoxLayout()
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(LOGO_PATH)
        rounded_logo_pixmap = round_pixmap(logo_pixmap, 60)
        logo_label.setPixmap(rounded_logo_pixmap.scaled(130, 130, Qt.KeepAspectRatio))
        image_layout.addWidget(logo_label, alignment=Qt.AlignCenter)
        team_label = QLabel(self)
        team_pixmap = QPixmap(TEAM_LOGO_PATH)
        rounded_team_pixmap = round_pixmap(team_pixmap, 60)
        team_label.setPixmap(rounded_team_pixmap.scaled(150, 130, Qt.KeepAspectRatio))
        image_layout.addWidget(team_label, alignment=Qt.AlignCenter)
        layout.addLayout(image_layout)

    def blink_title(self):
        current_opacity = self.opacity_effect.opacity()
        self.opacity_effect.setOpacity(1.0 if current_opacity == 0.0 else 0.0)

    def on_button_click(self):
        self.button_sound.play()
        clicked_button = self.sender()
        if clicked_button == self.start_button:
            start_detection()
        elif clicked_button == self.credits_button:
            show_credits()
        elif clicked_button == self.info_button:
            show_info()

    def closeEvent(self, event):
        for proc in subprocess._active:
            proc.terminate()
        event.accept()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
