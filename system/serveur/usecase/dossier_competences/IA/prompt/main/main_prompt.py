from usecase.dossier_competences.json.json_template import json_template


def main_prompt(cv_text):

    return f""" 
CV :
{cv_text}

"""