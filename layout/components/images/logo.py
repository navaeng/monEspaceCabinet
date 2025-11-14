from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from treatment.path_ressources import ressources_path

class LogoWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("logoWidget")
        logo_path = ressources_path('ressources/logo.ico')
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
        logo_label = QLabel()
        pixmap = QPixmap(logo_path).scaled(150, 150, Qt.AspectRatioMode.KeepAspectRatio)
        logo_label.setPixmap(pixmap)
        layout.addWidget(logo_label)