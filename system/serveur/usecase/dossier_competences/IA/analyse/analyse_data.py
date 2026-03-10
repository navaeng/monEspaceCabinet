from json_repair import repair_json
import json

from services.api_externes.openrouter.call_openrouter import call_openrouter
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv


def analyse_data(file_path):
    cv_text = read_cv(file_path)
    output = call_openrouter(main_prompt(cv_text), model="nousresearch/hermes-4-405b", json_mode=True)
    print(output)

    # transforme une chaîne corrompue en JSON valide
    repaired_output = repair_json(output)

    try:
        return json.loads(repaired_output)
    except:
        print("Échec critique du parsing malgré la réparation.")
        return {}