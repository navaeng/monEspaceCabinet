def prompt_mail(nom, notes_mail):

    return f"""En tant qu'expert pour un cabinet de conseil, je dois transmettre un email à mon candidat pour l'informer
    de la suite du process, ecris un mail PRET à etre envoyé attention il sera tranmis immédiatement il ne faut pas
    que tu insére des éléments à modifier, donc pas de crochet ni rien de similaire.
      prends en compte les instructions suivant pour rédiger l'email : {notes_mail} nom du candidat : {nom}.
"""