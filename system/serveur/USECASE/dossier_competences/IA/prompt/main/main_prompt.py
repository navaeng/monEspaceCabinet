def main_prompt(cv_text):
    return f"""Extrais les informations du CV suivant et retourne un JSON valide en français.

CV :
{cv_text}

JSON uniquement :
{{
  "Nom_prénom": "",
  "Initial": "",
  "Poste": "",
  "Secteurs_activités": [],
  "Langues": [{{"langue": "", "niveau": ""}}],
  "Experience_totale": "",
  "compétences": [],
  "Logiciels_par_titre": [{{"titre": "", "logiciels_outils": []}}],
  "Diplômes": [{{"Diplôme": "", "École": "", "Année": "", "Lieu": ""}}],
  "Expériences": [{{
    "Poste": "",
    "Nom_Entreprise": "",
    "Dates": "",
    "Durée_expérience": "",
    "Mission": "",
    "Tâches": [],
    "Logiciels_outils": []
  }}]
}}

Règles :
- Initial = 3 lettres du nom/prénom
- Experience_totale = somme des périodes d'emploi en "X ans d'expérience"
- Ne mélange jamais les tâches entre expériences
- Aucune liste vide si des données existent dans le CV
"""