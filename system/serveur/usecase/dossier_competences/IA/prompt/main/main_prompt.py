def main_prompt(cv_text, current_template):

    return f"""Tu es un expert en extraction de données. Consigne strict : ton but est d'extraire tout le contenu de {cv_text} dans le json : {current_template} 
    dans son intégralité sans commentaires.
    Si une clé contient 'à définir', tu dois générer toi-même une valeur.
"""