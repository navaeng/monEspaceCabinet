from PyQt6.QtWidgets import (QFileDialog)

def upload_cv(self):
        file_dialog = QFileDialog(self)
        file_dialog.setNameFilter("Documents (*.pdf *.doc *.docx)")
        file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)

        if file_dialog.exec():
            self.selected_file = file_dialog.selectedFiles()[0]
            self.file_label.setText("Fichier sélectionné ✅")
            self.english_cv.setEnabled(True)
            self.valider_btn.setEnabled(True)
            self.cv_simple.setEnabled(True)
            self.cv_complex.setEnabled(True)
        else:
            self.selected_file = None
            self.file_label.setText("Aucun fichier sélectionné.")