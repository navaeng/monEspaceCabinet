def prompt_infos(cv_text):
    return f"""
Extrais les informations suivantes du CV et retourne un JSON valide.

Concernant "Experience_totale" Calcule la durée totale d'expérience professionnelle, si les périodes se chevauchent, ne double pas la durée, 
Additionne les années de toutes les périodes d'emploi mentionnées, format de rendu : ".. ans d'expériences".
Concernant les secteurs d'activité, il s'agit de ciblé là où il est spécialisé ou les secteurs des entreprises pour lesquelles il a travaillé.

CV :
{cv_text}

Format de sortie (JSON uniquement sans commentaires) :
{{"Nom_Prénom": "", "POSTE": "", "Secteurs_activites": [], "Langues": [], "Experience_totale": ""}}
"""