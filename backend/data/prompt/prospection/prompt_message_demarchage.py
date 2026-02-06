def prompt_message_demarchage(job_title, details):
    return f"""
    Nous somme un cabinet et on fais du démarchage
    Rédige un message d'approche LinkedIn ultra-court (2 phrases max) pour démarcher des futurs clients
    Prends en compte les détails suivants : {details}
    Le but est de susciter la curiosité sans avoir l'air d'un robot.
    Pas de "Cher/Chère", sois direct et moderne.
    INTERDICTION : Ne mets pas d'accolades, de crochets [ ] ou de texte explicatif.
    Il ne faut pas qu'on sache que c'est généré par une IA, Il doit être prêt à être envoyé.
    Réponds UNIQUEMENT avec le texte du message.
    """.strip()
