from treatment.dc.save_cv import save_cv


def check_status_form(self):
    self.selected_file = save_cv(self)

    if not (self.add_skills_yes.isChecked() or self.add_skills_no.isChecked()):
        self.file_label.setText("Selectionnez le type de cv")
