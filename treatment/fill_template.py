from docxtpl import DocxTemplate
import threading
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from treatment.replace_empersand import replace_ampersand
from treatment.path_ressources import ressources_path
from treatment.jinra.create_jinra_env import create_jinra_env
from treatment.buttons.enabled_false_all_buttons import enabled_false_all_buttons
from data.extract.extract_and_call_prompt import extract_and_call_prompt
from treatment.translate.translate import translate
import traceback

def fill_template(self):

    QMessageBox.information(self,"Génération du dossier de compétences", "Vous allez choisir où sera généré le dossier de compétences")
    
    output_path, _ = QFileDialog.getSaveFileName(
        self,
        "Enregistrer le dossier de compétences",
        "dossier_competences.docx",
        "Documents Word (*.docx)"
    )
    if not output_path:
        return

    enabled_false_all_buttons(self)

    def worker(selected_file, file_label):
        try:

            print(f"Checkbox english: {self.english_cv.isChecked()}")
                            
            data_skills_tools, data_infos, data_diplomes, data_experiences = extract_and_call_prompt(selected_file, file_label, self)

            data = {**data_skills_tools, **data_infos, **data_diplomes, **data_experiences}
            if not data:
                raise ValueError("Les données du CV n'ont pas pu être extraites.")

            print(f"Checkbox add skills yes: {self.add_skills_yes.isChecked()}")
            print(f"Checkbox add skills no: {self.add_skills_no.isChecked()}")

            if hasattr(self, 'english_cv') and self.english_cv.isChecked():
                data = translate(data)
                
            template_path = ressources_path("ressources/template.docx")

            doc = DocxTemplate(template_path)
            create_jinra_env(doc)

            self.file_label.setText("Ecriture du dossier...")
            data = replace_ampersand(data)
            doc.render(data)
            doc.save(output_path)
            self.file_label.setText("✅ Dossier généré avec succès !")
            self.upload_btn.setEnabled(True)

        except Exception as e:

            error_msg = f"Erreur: {str(e)}\n{traceback.format_exc()}"
            self.file_label.setText(error_msg[:600])
            self.upload_btn.setEnabled(True)
            print(error_msg)


            
    threading.Thread(target=worker,args=(self.selected_file, self.file_label), daemon=True).start()