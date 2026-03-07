import json

from USECASE.dossier_competences.json.extract_json import extract_json

from services.api_externes.groq import call_groq


def analyse_skills_tools_with_model(cv_text):

    print("⚡  travail en cours du modele (compétences)…")
    output = call_groq(cv_text)

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
