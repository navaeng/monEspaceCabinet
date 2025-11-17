def simple_prompt_infos(cv_text):
    return f"""
Extrais les informations suivantes du CV et retourne un JSON valide.

Règles à respecter :

- Concernant "trois_lettre_nom", ceci n'est pas indiqué dans le cv, retourne 3 lettres ciblant le candidat.
- Concernant "Experience_totale" additionne les années de toutes les périodes d'emploi mentionnées, format de rendu : ".. ans d'expériences".
- Concernant les secteurs d'activité il s'agit du/des secteur des entreprises dans lequel il a évolué. 
- Concernant le niveau des langues si le niveau est mentionné avec l'échelle d'évaluation du CERCL traduit le de la sorte : bon niveau, avancé, intermédiaire ou autre.
- Retourne sans fautes d'ortographe ou de grammaire.

CV :
{cv_text}

Format de sortie (JSON uniquement sans commentaires) :
{{"Nom_prénom", "trois_lettre_nom": "", "POSTE": "", "Secteurs_activites": [], "Langues": [], "Experience_totale": ""}}
"""