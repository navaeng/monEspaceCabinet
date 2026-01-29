from PyQt6.QtWidgets import QFileDialog

from treatment.buttons.enabled_true_all_buttons import enabled_true_all_buttons


def save_cv(self):
    file_dialog = QFileDialog(self)

    file_dialog.setNameFilter("Documents (*.pdf *.doc *.docx)")
    file_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
    if file_dialog.exec():
        self.selected_file = file_dialog.selectedFiles()[0]
        self.file_label.setText("Fichier sélectionné ✅")
        enabled_true_all_buttons(self)
        return self.selected_file
    else:
        self.selected_file = None
        self.file_label.setText("Aucun fichier sélectionné.")
