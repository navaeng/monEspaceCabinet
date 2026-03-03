def prompt_relance_message(job_title, details, telephone, full_name, candidatrecherche):
    return """
Nous sommes un cabinet de conseil pécialisé en ingénierie et nous avons contacté des personnes sur linkedin, génére un message de relance simple et
pas long.

INTERDIT : crochets [], accolades {{}}, placeholders type [nom]/[entreprise], texte explicatif, formules génériques

Le message doit sembler rédigé spontanément par un recruteur humain, pas généré par une IA.
Soit preudent car le message sera envoyé directement sans vérification.

Réponds UNIQUEMENT avec le texte final du message, rien d'autre.
""".strip()
