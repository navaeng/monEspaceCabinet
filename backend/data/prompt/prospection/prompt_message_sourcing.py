def prompt_message_sourcing(job_title, details):
    return f"""
    Nous somme un cabinet et on fais du sourcing
    Rédige un message d'approche LinkedIn ultra-court (2 phrases max) pour tenter de trouver des candidats.
    Prends en compte les détails suivants : {details}
    Le but est de susciter la curiosité sans avoir l'air d'un robot.
    Pas de "Cher/Chère", sois direct et moderne.
    Laisse les informations de contact à la fin du message.
    INTERDICTION : Ne mets pas d'accolades, de crochets [ ] ou de texte explicatif.
    Il ne faut pas qu'on sache que c'est généré par une IA, Il doit être prêt à être envoyé.
    Réponds UNIQUEMENT avec le texte du message.
    """.strip()
