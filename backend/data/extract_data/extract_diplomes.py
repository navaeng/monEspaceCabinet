import json

from treatment.json.extract_json import extract_json

from data.call_groq import call_groq
from data.prompt.simple_prompt.prompt_diplomes import prompt_diplomes


def extract_diplomes_from_cv(cv_text):
    print("Début de extract_diplomes_from_cv")

    prompt = prompt_diplomes(cv_text)
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
