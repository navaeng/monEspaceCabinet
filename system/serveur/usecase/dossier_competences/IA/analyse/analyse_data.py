# from json_repair import repair_json
# import json
#
# from services.api_externes.openrouter.call_openrouter import call_openrouter
# from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
# from usecase.dossier_competences.services.data.reading.read_cv import read_cv
#
#
# def analyse_data(file_path):
#     cv_text = read_cv(file_path)
#     output = call_openrouter(main_prompt(cv_text), model, json_mode=True)
#     print(output)
#
#     repaired_output = repair_json(output)
#
#
#     try:
#         data = json.loads(repaired_output)
#     except:
#         print("Échec critique du parsing.")
#         return {}
#
#
#
# def analyse_data(file_path):
#     cv_text = read_cv(file_path)
#
#     identite = extract_with_gemini(cv_text)
#     outils = extract_with_hermes3(cv_text)
#     competences = extract_with_gpt(cv_text)
#     formations = extract_with_llama(cv_text)
#     experiences = extract_with_hermes4(cv_text)
#
#     data = {}
#     for block in [identite, outils, competences, formations, experiences]:
#         if isinstance(block, dict):
#             data.update(block)
#         else:
#             try:
#                 data.update(json.loads(repair_json(block)))
#             except:
#                 print(f"Erreur de fusion pour un bloc : {block[:50]}...")
#
#     return data
import json

from json_repair import repair_json

from services.api_externes.openrouter.call_openrouter import call_openrouter
from usecase.dossier_competences.IA.configurations.config_model_ia import config_ia
from usecase.dossier_competences.IA.prompt.main.main_prompt import main_prompt
from usecase.dossier_competences.services.data.reading.read_cv import read_cv


def analyse_data(file_path):
    cv_text = read_cv(file_path)
    final_data = {}
    config = config_ia()

    for model_name, json_template in config:
        output = call_openrouter(main_prompt(cv_text, json_template), model=model_name, json_mode=True)
        try:
            repaired = repair_json(output)
            final_data.update(json.loads(repaired))
        except:
            print("Erreur")

    return final_data