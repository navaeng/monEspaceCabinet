from usecase.dossier_competences.IA.prompt.clean.clean_prompt import clean_prompt
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv
from services.api_externes.openrouter.call_openrouter import call_openrouter
import json

def analyse_data(file_path):
    cv_text = read_cv(file_path)
    if not cv_text:
        print("Erreur : Impossible de lire le texte du CV")
        return ""

    prompt = main_prompt(cv_text)
    output = call_openrouter(prompt, model="nousresearch/hermes-3-llama-3.1-405b")
    output_clean = output.strip().removeprefix("```json").removesuffix("```").strip()
    print(output_clean)
    return json.loads(output_clean)
