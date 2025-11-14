def simple_prompt_experiences(cv_text):
    return f"""
Extrais TOUTES les expériences professionnelles du CV suivant et retourne un JSON valide.

- Une expérience = un poste dans une entreprise sur une période.
- Extrait les tâches entièrement tel qu'ils ont été mentionnés sans émoji.
- Retourne le résultat de la plus récente à la plus ancienne expérience.
- Si tu ne trouve pas un élément laisse le vide.
- Parfois un intitulé peut contenir plusieurs expériences.
- Prends en compte le context du cv. Le plus important est de retourner toutes lex expériences.

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
      "Logiciels": []
    }}
  ]
}}
"""