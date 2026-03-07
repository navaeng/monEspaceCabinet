import json

from USECASE.dossier_competences.json.extract_json import extract_json

from services.api_externes.groq import call_groq
from USECASE.dossier_competences.services.prompt.prompt_infos import prompt_infos


def analyse_infos_tools_with_model(cv_text):

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
