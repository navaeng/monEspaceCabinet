from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog
)
from PyQt6.QtCore import Qt
import sys
from treatment.fill_template import fill_template

class Treatment_cv_form(QWidget):

    def upload_cv(self):
        file_dialog = QFileDialog(self)
        file_dialog.setOption(QFileDialog.Option.DontUseNativeDialog, False)
        file_dialog.setNameFilter("Documents (*.pdf *.doc *.docx)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            self.selected_file = file_dialog.selectedFiles()[0]
            self.file_label.setText("Fichier sélectionné ✅")
            print(f"File selected: {self.selected_file}")
        else:
            self.selected_file = None
            self.file_label.setText("Aucun fichier sélectionné.")

    def valider(self):
        if not hasattr(self, "selected_file") and self.selected_file:
            self.file_label.setText("Veuillez sélectionner un fichier avant de valider.")
            return

        if not (self.add_skills_yes.isChecked() or self.add_skills_no.isChecked()):
            self.file_label.setText("Veuillez remplir les informations")
            return