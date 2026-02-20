def prompt_message_sourcing(
    job_title, details, telephone, full_name, candidatrecherche
):
    return f"""
Nous sommes un cabinet de conseil pécialisé en ingénierie,
nous recherchons des talents pour un besoin en {job_title}. Rédige un message LinkedIn naturel pour approcher de futur candidats potentiel.

Contexte :
- Informations complémentaires : {details}
- Les compétences recherchées sont : {candidatrecherche}

Consignes STRICTES :
3. Ton moderne et direct (pas de "Cher/Chère", "Madame", "Monsieur")
4. Change à chaque fois ce que tu dis car j'appelle ce prompt plusieurs fois.
5. Objectif : donner envie d'échanger sans être insistant.
6. Terminer par les coordonnées : {telephone} - {full_name}
7. CRUCIAL : Le message doit être prêt à envoyer TEL QUEL sans aucune modification
8. INTERDIT : crochets [], accolades {{}}, placeholders type [nom]/[entreprise], texte explicatif, formules génériques

Le message doit sembler rédigé spontanément par un recruteur humain, pas généré par une IA.
Soit preudent car le message sera envoyé directement sans vérification.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
