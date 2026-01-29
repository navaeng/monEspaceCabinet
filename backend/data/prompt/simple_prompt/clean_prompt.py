def clean_prompt(cv_text):
    return f"""
Tu es un expert en restructuration de données. Ton but est de remettre ce CV en ordre de manière logique et linéaire.

CONSIGNES :
1. REGROUPEMENT : Si des tâches sont séparées de leur entreprise à cause de la mise en page, recolle-les ensemble.
2. ZÉRO PERTE : Ne résume rien. Garde chaque mot, chaque chiffre et chaque compétence technique.
3. STRUCTURE : Utilise des sections claires (EXPÉRIENCES, FORMATION, COMPÉTENCES).
4. CHRONOLOGIE : Range les expériences de la plus récente à la plus ancienne.

TEXTE DU CV :
{cv_text}
"""
