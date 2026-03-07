def prompt_message_sourcing(
    job_title, details, telephone, full_name, candidatrecherche, previous_message
):
    print(f"Prompt message sourcing : job_title: {job_title}, details: {details}, telephone: {telephone}, full_name: {full_name}, previous_message: {previous_message}")

    return f"""
Nous sommes un cabinet de conseil pécialisé en ingénierie et nous souhaitons placer des candidats sur des besoins que nous reçevons,
nous recherchons des talents pour un besoin en {job_title}. Rédige un message LinkedIn naturel pour approcher de futur candidats potentiel.

Contexte :
- Informations complémentaires : {details}
- Les compétences recherchées sont : {candidatrecherche}

Consignes :
1. Soi court, fait 2 phrases maximum.
2. Ton moderne et professionnel, vouvoiement.
3. Rédige autre chose que les messages précedent : {previous_message}
4. Objectif : donner envie d'échanger sans être insistant.
5. Terminer par les coordonnées : {telephone} - {full_name}
6. CRUCIAL : Le message doit être prêt à envoyer TEL QUEL sans aucune modification
7. INTERDIT : crochets [], accolades {{}}, placeholders type [nom]/[entreprise], texte explicatif, formules génériques

Le message doit sembler rédigé spontanément par un recruteur humain, pas généré par une IA.
Soit preudent car le message sera envoyé directement sans vérification.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
