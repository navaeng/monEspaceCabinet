from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QCheckBox, QRadioButton, QButtonGroup, QHBoxLayout
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

        layout.addStretch()

        self.file_label = QLabel("")
        layout.addWidget(self.file_label, alignment=Qt.AlignmentFlag.AlignCenter)

        self.upload_btn = QPushButton("Sélectionner un fichier")
        self.upload_btn.setEnabled(True)
        self.upload_btn.clicked.connect(lambda: save_cv(self))
        layout.addWidget(self.upload_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        label_qst = QLabel("Ajouter plus de compétences en lien avec le profil ?")
        layout.addWidget(label_qst, alignment=Qt.AlignmentFlag.AlignCenter)

        radio_layout = QHBoxLayout()
        radio_layout.addStretch()  

        self.add_skills_yes = QRadioButton("Oui", self)
        self.add_skills_yes.setEnabled(False)
        radio_layout.addWidget(self.add_skills_yes)

        self.add_skills_no = QRadioButton("Non", self)
        self.add_skills_no.setEnabled(False)
        radio_layout.addWidget(self.add_skills_no)

        radio_layout.addStretch() 
        layout.addLayout(radio_layout)

        self.cv_type_group = QButtonGroup(self)
        self.cv_type_group.addButton(self.add_skills_yes)
        self.cv_type_group.addButton(self.add_skills_no)
        self.cv_type_group.buttonClicked.connect(lambda: self.valider_btn.setEnabled(True))
    

        self.add_skills_yes.setChecked(False)
        self.add_skills_no.setChecked(False)

        self.english_cv = QCheckBox("CV anglais", self)
        self.english_cv.setEnabled(False)
        layout.addWidget(self.english_cv, alignment=Qt.AlignmentFlag.AlignCenter)
        self.english_cv.setChecked(False)

        self.valider_btn = QPushButton("Générer un dossier")
        self.valider_btn.setEnabled(False)
        self.valider_btn.clicked.connect(lambda: fill_template(self))

        layout.addWidget(self.valider_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        layout.addStretch()
        