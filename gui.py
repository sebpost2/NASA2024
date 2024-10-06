from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QDialog, QHBoxLayout, QMessageBox
from PySide6.QtGui import QPixmap, QPalette, QBrush
from tracking import iniciar_deteccion
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Galactic Pose Challenge")
        self.setGeometry(100, 100, 1000, 700)
        self.setStyleSheet("background-color: #000033;")
        
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        self.show_main_menu()

    def show_main_menu(self):
        # Limpiar el layout
        for i in reversed(range(self.layout.count())): 
            widget = self.layout.itemAt(i).widget()
            if widget is not None: 
                widget.deleteLater()

        # Establecer imagen de fondo
        bg_image_path = "Images/bckgrnd.jpg"
        if os.path.exists(bg_image_path):
            bg_image = QPixmap(bg_image_path)
            self.setFixedSize(1000, 700)
            background_label = QLabel(self)
            background_label.setPixmap(bg_image.scaled(1000, 700))
            self.layout.addWidget(background_label)

        # Título
        title_label = QLabel("Galactic Pose Challenge")
        title_label.setStyleSheet("font-size: 24px; color: white;")
        self.layout.addWidget(title_label)

        # Botones
        start_button = self.create_button("Iniciar", iniciar_deteccion)
        credits_button = self.create_button("Créditos", self.show_credits)
        info_button = self.create_button("Información", self.show_info)

        self.layout.addWidget(start_button)
        self.layout.addWidget(credits_button)
        self.layout.addWidget(info_button)

    def create_button(self, text, callback):
        button = QPushButton(text)
        button.setStyleSheet("font-size: 14px; color: white; background-color: #000033;")
        button.clicked.connect(callback)
        return button

    def show_credits(self):
        credits_window = QDialog(self)
        credits_window.setWindowTitle("Créditos")
        credits_window.setGeometry(100, 100, 400, 300)
        credits_window.setStyleSheet("background-color: #060606;")

        layout = QVBoxLayout(credits_window)

        developers = ["Fabian Concha", "Justo Perez", "Abimael Ruiz", "Giulia Naval", "Sebastian Postigo", "Gabriel Valdivia"]
        for dev in developers:
            dev_label = QLabel(dev)
            dev_label.setStyleSheet("color: white; font-size: 12px;")
            layout.addWidget(dev_label)

        close_button = QPushButton("Cerrar")
        close_button.clicked.connect(credits_window.accept)
        layout.addWidget(close_button)

        credits_window.exec()

    def show_info(self):
        QMessageBox.information(self, "Información del Proyecto", "Este proyecto utiliza OpenCV para capturar video y estimar poses corporales.")
