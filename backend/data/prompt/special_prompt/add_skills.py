def prompt_add_skills(cv_text):
    return f"""
Extrais, synthétise et enrichis les compétences techniques et les outils du CV en JSON.

MÉTHODE :

1. ANALYSE ET SYNTHÈSE DES COMPÉTENCES :
   - Identifie les savoir-faire fondamentaux du candidat.
   - Formule chaque compétence par une phrase courte, percutante et impersonnelle.

2. CLASSIFICATION STRATÉGIQUE DES OUTILS :
   - Regroupe les logiciels et outils par "titre" de catégorie métier (ex: "Bureautique", "ERP", "CAO").
   - Ne liste pas les outils en vrac, range-les intelligemment.

3. CONTRÔLE QUALITÉ :
   - Zéro faute d'orthographe et suppression des doublons.

RÈGLES CRITIQUES :
- Ne crée JAMAIS de catégories d'outils vides.
- "logiciels_outils" doit être une LISTE d'items (ex: ["Excel", "SAP"]).
- Le ton doit être celui d'un cabinet de recrutement premium.
- Ajoute 5 compétences en plus qui sont en lien avec le domaine et le niveau d'expérience du candidat qui ne sont pas forcément spécifiées dans le CV.

CV :
{cv_text}

JSON uniquement :
{{
  "compétences": [],
  "Logiciels_par_titre": [
    {{
      "titre": "",
      "logiciels_outils": []
    }}
  ]
}}
"""
