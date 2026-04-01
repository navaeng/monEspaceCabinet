def prompt_mail(nom, notes_mail):
    return f"""Rédige un email pro pour {nom} basé sur : {notes_mail}.
    CONTEXT : Cabinet de conseil, email suite processus.
    IMPORTANT : Texte brut uniquement, pas de JSON, pas de crochets, pas de blabla d'intro.
    L'email doit être prêt à l'envoi immédiat avec des sauts de ligne clairs."""