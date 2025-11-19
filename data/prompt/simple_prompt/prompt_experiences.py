def prompt_experiences(cv_text):
    return f"""
Extrais toutes les expériences professionnelles du CV suivant et retourne un JSON valide.

Règles à respecter :

- Extrait les tâches entièrement tel qu'ils ont été mentionnés en corrigant les potentiels fautes de grammaires ou d'ortographes.
- Ne mélange pas les informations entre différentes expériences.
- Pour poste retourne l'intitulé tel qu'il apparait sans ajouter de tiret ou autre ajout.
- Retourne le résultat de la plus récente à la plus ancienne expérience.
- Attention à n'oublier aucune expérience.
- Retourne sans fautes d'ortographe ou de grammaire.
- Si tu ne trouve pas un éléments laisse le vide.
- Respecte la syntaxe du json.

CV :
{cv_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires) :
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