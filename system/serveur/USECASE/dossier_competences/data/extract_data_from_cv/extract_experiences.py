import html
import json

from USECASE.dossier_competences.json.extract_json import extract_json

from services.api_externes.groq import call_groq
from USECASE.dossier_competences.services.prompt.prompt_experiences import prompt_experiences


def extract_experiences_from_cv(cv_text):
    print("Début de extract_experiences_from_cv")

    prompt = prompt_experiences(cv_text)
    print("⚡ travail en cours du modele (experiences)…")
    output = call_groq(prompt)

    if output:
        json_text = extract_json(output).strip()
        print("JSON extrait :", json_text)
        json_text = (
            json_text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        )

        try:
            data_experiences = json.loads(json_text)
            data_experiences = {
                k: html.escape(v) if isinstance(v, str) else v
                for k, v in data_experiences.items()
            }
        except json.JSONDecodeError as e:
            print(f"Erreur JSON : {e}")
            print("JSON brut (repr) :", repr(json_text))
            data_experiences = {}

        print("envoi de la data experiences")
        return data_experiences
