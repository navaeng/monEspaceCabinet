def main_prompt(cv_text, current_template):

    return f"""Tu es un expert en extraction de données. ton but est de structurer dans le json : {current_template} 
    tout le contenu dans son intégralité sans commentaires ,
    si une clé contient 'à définir', tu dois générer toi-même une valeur
DATA:
{cv_text}
"""