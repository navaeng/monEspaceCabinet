from usecase.dossier_competences.IA.prompt.clean.clean_prompt import clean_prompt
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv
from services.api_externes.openrouter.call_openrouter import call_openrouter
import json
import ast

def analyse_data(file_path):
    cv_text = read_cv(file_path)
    if not cv_text:
        print("Erreur : Impossible de lire le texte du CV")
        return ""

    temp_output = call_openrouter(clean_prompt(cv_text), model="nousresearch/hermes-3-llama-3.1-405b", json_mode=False)
    prompt_main = main_prompt(temp_output)
    output = call_openrouter(prompt_main, model="nousresearch/hermes-4-405b", json_mode=True)
    return json.loads(output)