import json
from data.prompt.simple_prompt.prompt_infos import prompt_infos
from data.read_cv import read_cv
from data.call_groq import call_groq
from treatment.json.extract_json import  extract_json

def extract_infos_from_cv(file_path):
    print("Début de extract_experiences_from_cv")
    cv_text = read_cv(file_path)
    cv_size = len(cv_text.split())
    print("CV lu, longueur :", cv_size)

    prompt = prompt_infos(cv_text)
    print("⚡  travail en cours du modele (infos)…")
    output = call_groq(prompt)

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