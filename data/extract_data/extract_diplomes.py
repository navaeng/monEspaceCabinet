import json

from data.prompt.dc.simple_prompt.prompt_diplomes import prompt_diplomes
from data.read_doc import read_doc
from treatment.json.extract_json import extract_json

from backend.data.read_cv import read_cv
from data.call_groq import call_groq


def extract_diplomes_from_cv(file_path):
    print("Début de extract_diplomes_from_cv")
    doc_text = read_cv(file_path)
    doc_size = len(doc_text.split())
    print("CV lu, longueur :", doc_size)

    prompt = prompt_diplomes(doc_text)
    print(" extraction (diplomes)…")
    output = call_groq(prompt)

    if output:
        json_text = extract_json(output).strip()
        print("JSON extrait :", json_text)

        try:
            data_diplomes = json.loads(json_text)
        except json.JSONDecodeError as e:
            print(f"Erreur JSON : {e}")
            print("JSON brut (repr) :", repr(json_text))
            data_diplomes = {}

        print("envoi de la data diplomes")
        return data_diplomes
