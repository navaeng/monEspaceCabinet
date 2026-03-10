def main_prompt(cv_text, current_template):

    return f"""TU ES UN EXPERT EN EXTRACTION DE DONNÉES. TON BUT EST DE STRUCTURER DANS LE JSON : {current_template} 
    TOUT LE CONTENU DANS SON INTÉGRALITÉ SANS COMMENTAIRES.
DATA:
{cv_text}
"""