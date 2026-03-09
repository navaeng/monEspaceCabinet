from usecase.dossier_competences.json.json_template import json_template

def main_prompt(temp_output):
    return f"""TU ES UN EXPERT EN EXTRACTION DE DONNÉES. TON BUT EST DE STRUCTURER DANS LE JSON : {json_template()} LA DATA DANS SON INTEGRALITE SANS COMMENTAIRES.
DATA:
{temp_output}
"""