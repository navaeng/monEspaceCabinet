import os

from PyQt6.QtWidgets import QFileDialog


def save_doc(self, doc_type):
    if doc_type == "cv":
        files, _ = QFileDialog.getOpenFileNames(
            self,
            "Sélectionner des cv",
            "",
            "PDF Files (*.pdf);;Word Files (*.docx);;All Files (*)",
        )
        if files:
            self.selected_cv = files
            self.file_label.setText("\n".join([os.path.basename(f) for f in files]))
            self.upload_offer_btn.setEnabled(True)
    elif doc_type == "offer":
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Sélectionner des offres",
            "",
            "PDF Files (*.pdf);;Word Files (*.docx);;All Files (*)",
        )
        if file_path:
            self.selected_offer = file_path
            self.selected_label.setText(os.path.basename(file_path))

        if self.selected_cv and self.selected_offer:
            self.valider_btn.setEnabled(True)
        else:
            self.valider_btn.setEnabled(False)
