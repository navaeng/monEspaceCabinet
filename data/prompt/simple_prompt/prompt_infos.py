def prompt_infos(cv_text):
    return f"""
Extrais les informations suivantes du CV et retourne un JSON valide.

Règles à respecter :

- Concernant Iinitial", ceci n'est pas indiqué dans le cv, retourne 3 lettres ciblant le candidat selon son nom.
- Concernant "Experience_totale", il s'agit du nombre d'année global d'expériences du candidat, si ce n'est pas mentionné additionne donc les périodes d'emploi. Format de rendu : ".. ans d'expériences".
- Concernant les secteurs d'activité il s'agit du/des secteur des entreprises dans lequel il a évolué. 
- Concernant le niveau des langues si le niveau est mentionné avec l'échelle d'évaluation du CERCL traduit ! 

CV :
{cv_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires) :
{{"Nom_prénom", "Initial": "", "POSTE": "", "Secteurs_activites": [], "Langues": [], "Experience_totale": ""}}
"""