import json
from data.prompt.simple_prompt_infos import simple_prompt_infos
from data.read_cv import read_cv
from data.call_groq import call_groq


def extract_json(text):
    start = text.find('{')
    end = text.rfind('}')
    if start != -1 and end != -1 and end > start:
        return text[start:end+1]
    return text

def extract_infos_from_cv(file_path):
    print("Début de extract_infos_from_cv")
    cv_text = read_cv(file_path)
    cv_size = len(cv_text.split())
    print("CV lu, longueur :", cv_size)

    prompt = simple_prompt_infos(cv_text)
    print("⚡  travail en cours du model (infos)…")
    output = call_groq(prompt)

    json_text = extract_json(output).strip()
    print("JSON extrait :", json_text)
    
    try:
        data_infos = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Erreur JSON : {e}")
        print("JSON brut (repr) :", repr(json_text))
        data_infos = {}

    print("envoi de la data infos")
    return data_infos