def simple_prompt_skills_tools(cv_text):
    return f"""
Extrais les compétences et les outils du CV, retourne un JSON valide.

Règles à respecter : 

-Prends en compte le context du cv et retournes les compétences du candidat synthétisés par des phrases.
-Englobe les logiciels et outils avec un titre précis à chaque fois.
- Retourne sans fautes d'ortographe ou de grammaire.

CV :
{cv_text}

Format de sortie (JSON UNIQUEMENT sans commentaires ou caractère spécial) :
{{
  "compétences": []
  ],
  "Logiciels_par_titre": [
    {{
      "titre": "",
      "logiciels_outils": 
    }}
  ]
}}
"""