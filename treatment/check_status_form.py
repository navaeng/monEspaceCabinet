from treatment.save_cv import save_cv

def check_status_form(self):
    self.selected_file = save_cv(self)

    if not (self.cv_simple.isChecked() or self.cv_complex.isChecked()):
             self.file_label.setText("Selectionnez le type de cv")