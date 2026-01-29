def prompt_offre(doc_text, cvs_texts):
    cvs_joined = "\n\n--- CV ---\n\n".join(cvs_texts)
    return f"""
Je travail dans un cabinet de recrutement et je dois trouver un candidat pour cette offre d'emploi.
Analyse les informations de l'offre d'emploi.
Après avoir analysé les informations de l'offre d'emploi, compare les candidats et retourne un classement des candidats avec le format JSON demandé.
Soit concret et réaliste.
L'interêt est que tu me fasse gagner du temps, soi direct.
Apporte moi des conseils dans ma recherche de candidat.

doc :
{doc_text}
{cvs_joined}


Format de sortie (JSON uniquement sans commentaires) :
{{"nom": ,"forces": "", "faiblesses": "", "risques_réticences_recruteur": "" , "elements_à_confirmer_avec_le_candidat": "", "classement": "", "conseils": ""}} même rendu pour chaque candidat
"""
