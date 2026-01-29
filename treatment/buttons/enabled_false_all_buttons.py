def enabled_false_all_buttons(self):
    if hasattr(self, "english_cv"):
        self.english_cv.setEnabled(False)
    if hasattr(self, "valider_btn"):
        self.valider_btn.setEnabled(False)
    if hasattr(self, "upload_btn"):
        self.upload_btn.setEnabled(False)
    if hasattr(self, "add_skills_yes"):
        self.add_skills_yes.setEnabled(False)
    if hasattr(self, "add_skills_no"):
        self.add_skills_no.setEnabled(False)
    if hasattr(self, "upload_offer_btn"):
        self.upload_offer_btn.setEnabled(False)
