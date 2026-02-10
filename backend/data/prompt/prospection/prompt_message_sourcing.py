def prompt_message_sourcing(job_title, details, telephone, full_name):
    return f"""
Tu es un expert en recrutement et sourcing de talents. Rédige un message LinkedIn naturel pour approcher un candidat potentiel.

Contexte :
- Poste ciblé : {job_title}
- Informations complémentaires : {details}

Consignes STRICTES :
1. Maximum 2 phrases courtes et engageantes et ne tutoie pas
2. Indique que nous avons des profils de candidats qualifiés prêts à être présentés.
3. Ton moderne et direct (pas de "Cher/Chère", "Madame", "Monsieur")
4. Change à chaque fois ce que tu dis car j'appelle ce prompt plusieurs fois
5. Objectif : donner envie d'échanger sans être insistant
6. Terminer par les coordonnées : {telephone} - {full_name}
7. CRUCIAL : Le message doit être prêt à envoyer TEL QUEL sans aucune modification
8. INTERDIT : crochets [], accolades {{}}, placeholders type [nom]/[entreprise], texte explicatif, formules génériques

Le message doit sembler rédigé spontanément par un recruteur humain, pas généré par une IA.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
