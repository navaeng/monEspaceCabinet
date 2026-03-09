import ast
import re

from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv
from services.api_externes.openrouter.call_openrouter import call_openrouter
import json

def analyse_data(file_path):
    cv_text = read_cv(file_path)
    if not cv_text:
        print("Erreur : Impossible de lire le texte du CV")
        return {}

    output = call_openrouter(main_prompt(cv_text), model="nousresearch/hermes-4-405b", json_mode=True)

    json_match = re.search(r'\{.*\}', output, re.DOTALL)
    if json_match:
        output = json_match.group(0)

    try:
        print(output)
        return json.loads(output)
    except json.JSONDecodeError:
        return ast.literal_eval(output)