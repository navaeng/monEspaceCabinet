def prompt_message_prospection(job_title, details, telephone, full_name):
    return f"""
Tu es un expert en prospection B2B. Rédige un message LinkedIn naturel et direct.

Contexte :
- Poste du prospect : {job_title}
- Informations complémentaires : {details}

Consignes STRICTES :
1. Maximum 2 phrases courtes et percutantes
2. Ton moderne et professionnel (pas de "Cher/Chère", "Madame", "Monsieur")
3. Objectif : piquer la curiosité sans être intrusif
4. Terminer par : {telephone} - {full_name}
5. CRUCIAL : Le message doit être prêt à envoyer TEL QUEL
6. INTERDIT : crochets [], accolades {{}}, placeholders, texte explicatif, formules génériques type [prénom]

Le message doit sembler écrit par un humain, pas généré par une IA.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
