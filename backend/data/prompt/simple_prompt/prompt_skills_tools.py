def prompt_skills_tools(cv_text):
    return f"""
Extrais et synthétise les compétences techniques et les outils du CV en JSON.

MÉTHODE :

1. ANALYSE DES COMPÉTENCES :
   - Identifie les savoir-faire clés du candidat.
   - Synthétise chaque groupe de compétences par une phrase professionnelle impersonelle.

2. CLASSIFICATION DES OUTILS :
   - Regroupe les logiciels, langages ou outils par catégories logiques.
   - Chaque catégorie doit avoir un "titre" précis et une liste "logiciels_outils".

3. QUALITÉ :
   - Correction orthographique et grammaticale irréprochable.
   - Supprime les doublons.

RÈGLES CRITIQUES :
- Ne crée pas de catégories d'outils vides.
- Le champ "logiciels_outils" doit être une LISTE de chaînes de caractères.
- Garde un ton professionnel et synthétique.

CV :
{cv_text}

JSON uniquement (respecte strictement cette structure) :
{{
  "compétences": [
    "",
    ""
  ],
  "Logiciels_par_titre": [
    {{
      "titre": "",
      "logiciels_outils": []
    }}
  ]
}}
"""
