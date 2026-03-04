def prompt_message_prospection(job_title, details, telephone, full_name, previous_message):
    print(f"Prompt message proespection : job_title: {job_title}, details: {details}, telephone: {telephone}, full_name: {full_name}, previous_message: {previous_message}")

    return f"""
Tu nous aide à généré un message LinkedIn, nous sommes un cabinet de conseil pécialisé en ingénierie,
nous recherchons de nouvelles enseignes afin de leurs proposer des talents pour leurs besoins.
Rédige un message LinkedIn naturel et direct.

Contexte :
- Informations complémentaires : {details}

Consignes STRICTES :
1. Soi court, fait 2 phrases maximum.
2. Ton moderne et professionnel, vouvoiement.
3. Rédige autre chose que les messages précedent : {previous_message}
4. Terminer par : {telephone} - {full_name} si indiqué sinon pas grave n'indique rien
5. CRUCIAL : Le message doit être prêt à envoyer TEL QUEL
6. INTERDIT : crochets [], accolades {{}}, placeholders, texte explicatif, formules génériques type [prénom]

Le message doit sembler écrit par un humain, pas généré par une IA.
Soit preudent car le message sera envoyé directement sans vérification.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
