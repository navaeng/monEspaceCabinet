from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QCheckBox, QHBoxLayout, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt
from treatment.upload_cv import upload_cv
from treatment.fill_template import fill_template
from layout.components.buttons.backbutton import backbutton
from layout.components.images.logo import LogoWidget

class CVUploadForm(QWidget):
    def __init__(self, navigate_home=None):
        super().__init__() 
        self.navigate_home = navigate_home
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)

        logo_widget = LogoWidget()
        main_layout.addWidget(logo_widget, alignment=Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        main_layout.addStretch()

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)  

        self.upload_btn = QPushButton("Sélectionner un cv")
        self.upload_btn.setEnabled(True)
        self.upload_btn.clicked.connect(lambda: upload_cv(self))
        center_layout.addWidget(self.upload_btn)

        cv_type_layout = QHBoxLayout()

        self.cv_simple = QRadioButton("CV simple", self)
        self.cv_complex = QRadioButton("CV complex", self)
        
        self.english_cv = QCheckBox("CV anglais", self)
        self.cv_simple.setEnabled(False)
        self.cv_complex.setEnabled(False)
        self.english_cv.setEnabled(False)
        self.english_cv.setChecked(False)

        self.cv_type_group = QButtonGroup(self)
        self.cv_type_group.addButton(self.cv_simple)
        self.cv_type_group.addButton(self.cv_complex)

        cv_type_layout.addStretch()
        cv_type_layout.addWidget(self.cv_simple)
        cv_type_layout.addWidget(self.cv_complex)
        cv_type_layout.addWidget(self.english_cv)
        cv_type_layout.addStretch()
        center_layout.addLayout(cv_type_layout)

        self.valider_btn = QPushButton("Générer un dossier")
        self.valider_btn.clicked.connect(lambda: fill_template(self))
        center_layout.addWidget(self.valider_btn)
        main_layout.addLayout(center_layout)

        main_layout.addStretch()
