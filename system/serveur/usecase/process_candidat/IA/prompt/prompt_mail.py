def prompt_mail(nom, poste, remuneration, doc, prochaine_etape, notes_email, lieu):
    return f"""
    Rôle : Expert en recrutement pour un cabinet de conseil.
    Mission : Rédiger l'email de suivi pour {nom}.

    Interdiction formelle d'utiliser des crochets [], des parenthèses () ou des champs à remplir. 
    L'email doit être prêt à l'envoi immédiat.

    Infos :
    - Candidat : {nom}
    - Poste pour lequel il est en process : {poste}
    - Rémunération : {remuneration}
    - Document attendu : {doc}
    - Prochaine étape : {prochaine_etape}
    - Instructions spécifiques : {notes_email}
    - Lieu de l'offre : {lieu}
    
    """