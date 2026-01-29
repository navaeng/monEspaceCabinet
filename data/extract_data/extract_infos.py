import json

from data.prompt.dc.simple_prompt.prompt_infos import prompt_infos
from data.extract_data.
from treatment.json.extract_json import extract_json

from data.call_groq import call_groq
from backend.data.read_cv import read_cv


def extract_infos_from_cv(file_path):
    print("Début de extract_experiences_from_cv")
    doc_text = read_cv(file_path)
    doc_size = len(doc_text.split())
    print("CV lu, longueur :", doc_size)

    prompt = prompt_infos(doc_text)
    print("⚡  travail en cours du modele (infos)…")
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

        print("envoi de la data infos...")
        return data_skills
