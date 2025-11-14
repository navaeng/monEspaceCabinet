def simple_prompt_diplomes(cv_text):
    return f"""
Extrais les diplômes et formations du CV et retourne un JSON valide.

- Groupe correctement les informations de chaque diplôme : Titre, Ecole, Annee, Lieu
- Ne mélange jamais les informations entre différents diplômes

CV :  
{cv_text}

Format de sortie (JSON uniquement sans commentaires) :
{{
  "Diplomes": [
    {{
      "Titre": "",
      "Ecole": "",
      "Annee": "",
      "Lieu": ""
    }}
  ]
}}
"""