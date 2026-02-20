def prompt_sourcing(candidatrecherche, target_url):
    return f"""
    Génére l'url linkedin filtré pour rechercher des candidats selon les critères suivants :
    - Les compétences recherchées sont : {candidatrecherche}

    Format de sortie (JSON uniquement sans commentaires) :

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
return target_url
""".strip()
