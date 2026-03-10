def main_prompt(cv_text, curren_template):
    return f"""TU ES UN EXPERT EN EXTRACTION DE DONNÉES. TON BUT EST DE STRUCTURER DANS LE JSON : {curren_template} 
    TOUTES LES DONNÉES DANS LEUR INTÉGRALITÉ, SANS COMMENTAIRES.
DATA:
{cv_text}
"""