import json

from USECASE.dossier_competences.json.extract_json import extract_json

from services.api_externes.groq import call_groq
from USECASE.dossier_competences.services.prompt.prompt_skills_tools import prompt_skills_tools
from USECASE.dossier_competences.services.prompt.special_prompt.add_skills import prompt_add_skills


def extract_skills_tools_from_cv(cv_text, self):
    if self.add_skills_yes.isChecked():
        prompt = prompt_add_skills(cv_text)
    else:
        prompt = prompt_skills_tools(cv_text)

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
