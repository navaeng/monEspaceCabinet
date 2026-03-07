def prompt_infos(doc_text):
    return f"""
Extrais les informations suivantes du CV et retourne un JSON valide.

Règles à respecter :
- Concernant Iinitial", ceci n'est pas indiqué dans le cv, retourne 3 lettres ciblant le candidat selon son nom.
- Concernant "Experience_totale", il s'agit du nombre d'année global d'expériences du candidat, si ce n'est pas mentionné additionne donc les périodes d'emploi. Format de rendu : ".. ans d'expériences".
- Concernant les secteurs d'activité il s'agit du/des secteur des entreprises dans lequel il a évolué.
- Format attendu : langues : (niveau)

- Concernant Iinitial", ceci n'est pas indiqué dans le cv, retourne 3 lettres pour l'identifier selon son nom et prénom.
- Concernant "Experience_totale", il s'agit du nombre d'année global d'expériences du candidat, additionne donc les périodes d'emploi. Format de rendu : ".. ans d'expériences".
- Concernant les secteurs d'activité il s'agit du/des secteur des entreprises dans lequel il a évolué.
- Format attendu : langues : niveau

CV :
{doc_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires, en français) :

{{"Nom_prénom", "Initial": "", "POSTE": "", "Secteurs_activités": [], "Langues": [], "Experience_totale": ""}}

{{"Nom_prénom", "Initial": "", "Poste": "", "Secteurs_activités": [], "Langues": [{{"langue": "", "niveau": ""}}], "Experience_totale": ""}}

"""
