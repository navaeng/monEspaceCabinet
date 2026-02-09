def prompt_message_sourcing(job_title, details, telephone, full_name):
    return f"""
Tu es un expert en recrutement et sourcing de talents. Rédige un message LinkedIn naturel pour approcher un candidat potentiel.

Contexte :
- Poste ciblé : {job_title}
- Informations complémentaires : {details}

Consignes STRICTES :
1. Maximum 2 phrases courtes et engageantes
2. Ton moderne et direct (pas de "Cher/Chère", "Madame", "Monsieur")
3. Objectif : donner envie d'échanger sans être insistant
4. Terminer par les coordonnées : {telephone} - {full_name}
5. CRUCIAL : Le message doit être prêt à envoyer TEL QUEL sans aucune modification
6. INTERDIT : crochets [], accolades {{}}, placeholders type [nom]/[entreprise], texte explicatif, formules génériques

Le message doit sembler rédigé spontanément par un recruteur humain, pas généré par une IA.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
