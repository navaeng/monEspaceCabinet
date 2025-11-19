import json
from data.prompt.simple_prompt.prompt_experiences import prompt_experiences
from data.read_cv import read_cv
from data.call_groq import call_groq
import html
from treatment.json.extract_json import  extract_json


def extract_experiences_from_cv(file_path):
    print("Début de extract_experiences_from_cv")
    cv_text = read_cv(file_path)
    cv_size = len(cv_text.split())
    print("CV lu, longueur :", cv_size)

    prompt = prompt_experiences(cv_text)
    print("⚡ travail en cours du modele (experiences)…")
    output = call_groq(prompt)

    json_text = extract_json(output).strip()
    print("JSON extrait :", json_text)
    json_text = json_text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    
    try:
        data_experiences = json.loads(json_text)
        data_experiences = {k: html.escape(v) if isinstance(v, str) else v for k, v in data_experiences.items()}
    except json.JSONDecodeError as e:
        print(f"Erreur JSON : {e}")
        print("JSON brut (repr) :", repr(json_text))
        data_experiences = {}

    print("envoi de la data experiences")
    return data_experiences