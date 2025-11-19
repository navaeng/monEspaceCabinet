def prompt_diplomes(cv_text):
    return f"""
Extrais les diplômes et formations du CV et retourne un JSON valide.

Règle a respecter : 

- Rerouper correctement les informations de chaque diplôme : Titre, Ecole, Annee, Lieu sans mélanger les informations entre différents diplômes.

CV :  
{cv_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires) :
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