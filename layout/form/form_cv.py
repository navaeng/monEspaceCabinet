from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QRadioButton, QButtonGroup
from PyQt6.QtCore import Qt
from treatment.save_cv import save_cv
from treatment.fill_template import fill_template
from layout.components.buttons.backbutton import backbutton
from layout.components.images.logo import LogoWidget
from treatment.check_status_form import check_status_form

class CVUploadForm(QWidget):
    def __init__(self, navigate_home=None):
        super().__init__()
        self.selected_file = None

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(25)

        logo_widget = LogoWidget()
        layout.addWidget(logo_widget, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)

        backbutton(navigate_home)

        """
                warning_label = QLabel("Il s'agit d'une première version, veillez à verifier le dossier généré")
                layout.addWidget(warning_label, alignment=Qt.AlignmentFlag.AlignCenter)
        """


        layout.addStretch()


        self.file_label = QLabel("")
        layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.upload_btn = QPushButton("Sélectionner un cv")
        self.upload_btn.setEnabled(True)
        self.upload_btn.clicked.connect(lambda: save_cv(self))
        layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        label_qst = QLabel("Ajouter plus de compétences en lien avec le profil ?")
        layout.addWidget(label_qst, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cv_complex = QRadioButton("Oui", self)
        self.cv_complex.setEnabled(False)
        layout.addWidget(self.cv_complex, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cv_simple = QRadioButton("Non", self)
        self.cv_simple.setEnabled(False)
        layout.addWidget(self.cv_simple, alignment=Qt.AlignmentFlag.AlignCenter)
        
        self.valider_btn = QPushButton("Générer un dossier")
        self.valider_btn.setEnabled(False)
        self.valider_btn.clicked.connect(lambda: fill_template(self))

        layout.addWidget(self.valider_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.cv_type_group = QButtonGroup(self)
        self.cv_type_group.addButton(self.cv_simple)
        self.cv_type_group.addButton(self.cv_complex)
        self.cv_type_group.buttonClicked.connect(lambda: self.valider_btn.setEnabled(True))

        self.cv_simple.setChecked(False)
        self.cv_complex.setChecked(False)

        self.english_cv = QCheckBox("CV anglais", self)
        self.english_cv.setEnabled(False)
        layout.addWidget(self.english_cv, alignment=Qt.AlignmentFlag.AlignCenter)
        self.english_cv.setChecked(False)

        layout.addStretch()
        