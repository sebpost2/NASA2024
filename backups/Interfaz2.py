import sys
import subprocess
import cv2
import mediapipe as mp
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QSizePolicy, QSpacerItem
from PySide6.QtCore import Qt, QThread, Signal, QRect
from PySide6.QtGui import QFont, QPixmap, QPalette, QBrush, QFontDatabase, QPainter, QPen

# Rutas de la fuente y las imágenes
FONT_PATH = "Sixtyfour_Convergence/static/SixtyfourConvergence-Regular.ttf"
LOGO_PATH = "Images/logo.jpg"
TEAM_LOGO_PATH = "Images/team.png"  # Nueva ruta
BACKGROUND_PATH = "Images/bckgrnd.jpg"

# Función para redondear las esquinas de un pixmap
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

# Función que se ejecuta al hacer clic en el botón "Start"
def start_detection():
    print("Starting detection...")
    # Ocultar la ventana principal
    window.hide()
    
    # Ejecutar el archivo Tracking2.py
    subprocess.Popen([sys.executable, "backups\Tracking2.py"])
    
    # Mostrar la ventana principal nuevamente al terminar el hilo
    window.show()

# Función para mostrar los créditos del proyecto
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

# Función para mostrar información adicional del proyecto
def show_info():
    info_dialog = QDialog()
    info_dialog.setWindowTitle("More Info")
    info_dialog.setGeometry(400, 400, 300, 100)

    layout = QVBoxLayout()

    info_label = QLabel("This project uses OpenCV and MediaPipe for pose detection.")
    info_label.setFont(QFont("Arial", 10))
    info_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(info_label)

    close_button = QPushButton("Close")
    close_button.clicked.connect(info_dialog.close)
    layout.addWidget(close_button)

    info_dialog.setLayout(layout)
    info_dialog.exec()

# Clase principal para la interfaz
class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("Galactic Games")
        self.setGeometry(100, 100, 800, 600)

        # Establecer la fuente personalizada
        font_id = QFontDatabase.addApplicationFont(FONT_PATH)
        if font_id == -1:
            print("Error: No se pudo cargar la fuente personalizada. Usando fuente predeterminada.")
            custom_font = QFont("Arial", 24)
            family = ["Arial"]
        else:
            family = QFontDatabase.applicationFontFamilies(font_id)
            if family:
                custom_font = QFont(family[0], 24)
            else:
                print("Error: No se encontró ninguna familia de fuentes. Usando fuente predeterminada.")
                custom_font = QFont("Arial", 24)
                family = ["Arial"]

        # Crear un widget central
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Crear un layout vertical
        layout = QVBoxLayout(central_widget)

        # Establecer imagen de fondo
        palette = QPalette()
        background = QPixmap(BACKGROUND_PATH)
        palette.setBrush(QPalette.Window, QBrush(background.scaled(self.size(), Qt.IgnoreAspectRatio)))
        self.setPalette(palette)

        # Espaciador vertical para separar las imágenes del borde superior
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Título principal
        title_label = QLabel("ASTRO·SHAPE", self)
        title_label.setFont(QFont(family[0], 36))
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)

        # Espaciador vertical para separar las imágenes del borde superior
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Botón "Start"
        start_button = QPushButton("Start", self)
        start_button.setFont(QFont(family[0], 14))
        start_button.setFixedWidth(120)
        start_button.clicked.connect(start_detection)
        layout.addWidget(start_button, alignment=Qt.AlignCenter)

        # Botón "Credits"
        credits_button = QPushButton("Credits", self)
        credits_button.setFont(QFont(family[0], 14))
        credits_button.setFixedWidth(170)
        credits_button.clicked.connect(show_credits)
        layout.addWidget(credits_button, alignment=Qt.AlignCenter)

        # Botón "More Info"
        info_button = QPushButton("More Info", self)
        info_button.setFont(QFont(family[0], 14))
        info_button.setFixedWidth(190)
        info_button.clicked.connect(show_info)
        layout.addWidget(info_button, alignment=Qt.AlignCenter)

        # Espaciador vertical para separar las imágenes del borde superior
        layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        # Crear un layout horizontal para las imágenes
        image_layout = QHBoxLayout()
        
        # Imagen del logo
        logo_label = QLabel(self)
        logo_pixmap = QPixmap(LOGO_PATH)
        rounded_logo_pixmap = round_pixmap(logo_pixmap, 60)
        logo_label.setPixmap(rounded_logo_pixmap.scaled(130, 130, Qt.KeepAspectRatio))
        image_layout.addWidget(logo_label, alignment=Qt.AlignCenter)

        # Imagen del equipo
        team_label = QLabel(self)
        team_pixmap = QPixmap(TEAM_LOGO_PATH)
        rounded_team_pixmap = round_pixmap(team_pixmap, 60)
        team_label.setPixmap(rounded_team_pixmap.scaled(130, 130, Qt.KeepAspectRatio))  # Ajustar tamaño según sea necesario
        image_layout.addWidget(team_label, alignment=Qt.AlignCenter)

        layout.addLayout(image_layout)

        # Espaciador vertical para separar las imágenes del borde superior
        layout.addSpacerItem(QSpacerItem(20, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

# Iniciar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
