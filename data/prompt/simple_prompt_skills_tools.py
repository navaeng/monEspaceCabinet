def simple_prompt_skills_tools(cv_text):
    return f"""
Extrais les compétences et les outils, logiciels du CV, retourne un JSON valide.

Englobe les par domaines avec un titre précis à chaque fois, N'ouvre AUCUNE parenthèse ou accolade de + que le JSON.

CV :
{cv_text}

Format de sortie (JSON uniquement sans commentaires) :
{{
  "Competences_par_titre": [
    {{
      "titre": "",
      "competences": []
    }}
  ],
  "Logiciels_par_titre": [
    {{
      "titre": "",
      "logiciels_outils": []
    }}
  ]
}}
"""