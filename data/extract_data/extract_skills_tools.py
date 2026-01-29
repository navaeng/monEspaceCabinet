import json

from data.prompt.dc.simple_prompt.prompt_skills_tools import prompt_skills_tools
from data.prompt.dc.special_prompt.add_skills import add_skills
from data.read_doc import read_doc
from treatment.json.extract_json import extract_json

from backend.data.read_cv import read_cv
from data.call_groq import call_groq


def extract_skills_tools_from_cv(file_path, self):
    print("Début de extract_skills_from_cv")
    doc_text = read_cv(file_path)
    doc_size = len(doc_text.split())
    print("CV lu, longueur :", doc_size)

    if hasattr(self, "add_skills_yes") and self.add_skills_yes.isChecked():
        prompt = add_skills(doc_text)
    else:
        prompt = prompt_skills_tools(doc_text)

    print("⚡  travail en cours du modele (compétences)…")
    output = call_groq(prompt)

    if output:
        json_text = extract_json(output).strip()
        print("JSON extrait :", json_text)

        try:
            data_skills = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Erreur JSON : {e}")
            print("JSON brut (repr) :", repr(json_text))
            data_skills = {}

        print("envoi de la data compétences")
        return data_skills
