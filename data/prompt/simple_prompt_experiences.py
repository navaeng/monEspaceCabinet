def simple_prompt_experiences(cv_text):
    return f"""
Extrais toutes les expériences professionnelles du CV suivant et retourne un JSON valide.

Règles à respecter :

- Extrait les tâches entièrement tel qu'ils ont été mentionnés sans émoji.
- Ne mélange pas les informations entre différentes expériences.
- Retourne le résultat de la plus récente à la plus ancienne expérience.
- Attention à n'oublier aucune expérience.
- Si tu ne trouve pas un éléments laisse le vide.
- Retourne sans fautes d'ortographe ou de grammaire.

CV :
{cv_text}

Format de sortie (JSON uniquement, sans commentaires) :
{{
  "Experiences": [
    {{
      "Nom_Entreprise": "",
      "Poste": "",
      "Dates": "",
      "Durée_expérience": "",
      "Mission",
      "Clients",
      "Taches": [],
      "Logiciels_outils": []
    }}
  ]
}}
"""