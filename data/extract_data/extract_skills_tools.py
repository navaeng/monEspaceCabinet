import json
from data.prompt.simple_prompt.prompt_skills_tools import prompt_skills_tools
from data.read_cv import read_cv
from data.call_groq import call_groq
from treatment.json.extract_json import  extract_json
from data.prompt.special_prompt.add_skills import add_skills


def extract_skills_tools_from_cv(file_path, self):
    print("Début de extract_skills_from_cv")
    cv_text = read_cv(file_path)
    cv_size = len(cv_text.split())
    print("CV lu, longueur :", cv_size)

    if self.add_skills_yes.isChecked():
        prompt = add_skills(cv_text)
    else:
        prompt = prompt_skills_tools(cv_text)

    print("⚡  travail en cours du modele (compétences)…")
    output = call_groq(prompt)

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