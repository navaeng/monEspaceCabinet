def prompt_diplomes(doc_text):
    return f"""
Extrais les diplômes et formations du CV et retourne un JSON valide.

Règle a respecter :

- Rerouper correctement les informations de chaque diplôme : Titre, Ecole, Annee, Lieu sans mélanger les informations entre différents diplômes.

CV :
{doc_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires, en français) :
{{
  "Diplomes": [
    {{
      "Titre": "",
      "École": "",
      "Année": "",
      "Lieu": ""
    }}
  ]
}}
"""
