def prompt_diplomes(cv_text):
    return f"""
Extrais les diplômes et formations du CV et retourne un JSON valide.

Règle a respecter :

- Rerouper correctement les informations de chaque diplôme : Titre, Option_diplome (Si spécifié), Ecole, Annee, Lieu sans mélanger les informations entre différents diplômes.
- Pour chaque diplôme, vérifier que les informations sont correctement renseignées et cohérentes.
- Pour l'année, il s'agit de l'année d'obtention du diplôme.
- Pour diplôme, trouve l'intitulé du diplôme.
CV :
{cv_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires, en français) :
{{
  "Diplômes": [
    {{
      "Diplôme": "",
      "École": "",
      "Année": "",
      "Lieu": ""
    }}
  ]
}}
"""
