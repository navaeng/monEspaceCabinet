import json

from core.USECASE.dossier_competences.json import extract_json

from data.call_groq import call_groq
from data.prompt.simple_prompt.prompt_infos import prompt_infos


def extract_infos_from_cv(cv_text):
    print("Début de extract_experiences_from_cv")

    prompt = prompt_infos(cv_text)
    print("⚡  travail en cours du modele (infos)…")
    output = call_groq(prompt)
    if output:
        json_text = extract_json(output).strip()
        print("JSON extrait :", json_text)

        try:
            data_infos = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Erreur JSON : {e}")
            print("JSON brut (repr) :", repr(json_text))
            data_infos = {}

        print("envoi de la data infos...")
        return data_infos
