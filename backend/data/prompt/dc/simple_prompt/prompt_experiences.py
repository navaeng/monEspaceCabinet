def prompt_experiences(doc_text):
    return f"""
Extrais toutes les expériences professionnelles du CV suivant et retourne un JSON valide.

Règles à respecter :

- Extrait les tâches entièrement tel qu'ils ont été mentionnés en corrigant les potentiels fautes de grammaires ou d'ortographes.
- Ne mélange pas les informations entre différentes expériences.
- Pour poste retourne l'intitulé tel qu'il apparait sans ajouter de tiret ou autre ajout.
- Retourne le résultat de la plus récente à la plus ancienne expérience.
- Attention à n'oublier aucune expérience.
- Retourne sans fautes d'ortographe ou de grammaire.
- Concernant Nom_Entreprise, une seule entreprise est attendue à chaque fois, retourne celle pour qui il a travaillé pour chaque expériences.
- Concernant "Titre" :
                    Poste regroupant des expériences.
                    -Information identifiable car aucune taches en lien avec le poste n'est indiqué, elle est suivie par un intitulé de poste indiquant plus d'informations.

CV :
{doc_text}

Format de sortie (JSON uniquement MEME SYNTAXE, sans commentaires, en français) :
{{
  "Expériences": [
    {{
      "Titre": "",
      "Poste": "",
      "Nom_Entreprise": "",
      "Dates": "",
      "Durée_expérience": "",
      "Mission",
      "Clients",
      "Tâches": [],
      "Logiciels_outils": []
    }}
  ]
}}
"""
