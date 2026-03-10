def main_prompt(temp_output, json_template):
    return f"""TU ES UN EXPERT EN EXTRACTION DE DONNÉES. TON BUT EST DE STRUCTURER DANS LE JSON : {json_template} 
    TOUTES LES DONNÉES DANS LEUR INTÉGRALITÉ, SANS COMMENTAIRES.
DATA:
{temp_output}
"""