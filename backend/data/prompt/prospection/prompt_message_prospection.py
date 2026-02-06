def prompt_message_prospection(job_title, details, offre):
    return f"""
    On fais de la prospection
    Rédige un message d'approche LinkedIn ultra-court (2 phrases max)
    On recherche un {job_title}.
    Prends en compte les détails suivants : {details}
    Adapte le message à l'offre {offre}.
    Le but est de susciter la curiosité sans avoir l'air d'un robot.
    Pas de "Cher/Chère", sois direct et moderne.
    INTERDICTION : Ne mets pas d'accolades, de crochets [ ] ou de texte explicatif.
    Il ne faut pas qu'on sache que c'est généré par une IA, Il doit être prêt à être envoyé.
    Réponds UNIQUEMENT avec le texte du message.
    """.strip()
