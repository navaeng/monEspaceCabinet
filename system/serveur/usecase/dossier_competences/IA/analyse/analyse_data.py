from json_repair import repair_json
import json

from services.api_externes.openrouter.call_openrouter import call_openrouter
from usecase.dossier_competences.IA.configurations.config_model_ia import config_ia
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv


# def analyse_data(file_path):
#     cv_text = read_cv(file_path)
#     config = config_ia()
#     final_data = {}
#
#     for model_name, current_template, in config:
#         output = call_openrouter(main_prompt(cv_text, current_template), model=model_name, json_mode=True)
#
#         try:
#             repaired = repair_json(output)
#             final_data.update(json.loads(repaired))
#         except Exception as e:
#             print(f"Erreur {e}")
#     return final_data
#

import json
from concurrent.futures import ThreadPoolExecutor
from json_repair import repair_json

from services.api_externes.openrouter.call_openrouter import call_openrouter
from usecase.dossier_competences.IA.configurations.config_model_ia import config_ia
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv


def analyse_data(file_path):
    cv_text = read_cv(file_path)
    config = config_ia()
    final_data = {}

    def fetch_ai_data(conf):
        model_name, current_template = conf
        return call_openrouter(main_prompt(cv_text, current_template), model=model_name, json_mode=True)

    with ThreadPoolExecutor() as executor:
        outputs = list(executor.map(fetch_ai_data, config))

    for output in outputs:
        try:
            clean_output = output.replace('\xa0', ' ').replace('\u2019', "'")
            repaired = repair_json(clean_output)
            final_data.update(json.loads(repaired))
        except Exception as e:
            print(f"Erreur {e}")

    return final_data
