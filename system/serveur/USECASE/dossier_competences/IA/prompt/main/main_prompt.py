def main_prompt(cv_text):
    template = json_template()

    return f"""Extrais les informations du CV suivant et retourne un JSON valide.

CV :
{cv_text}

JSON uniquement : {template}
"""