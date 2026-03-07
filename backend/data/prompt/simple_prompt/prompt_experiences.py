def prompt_experiences(cv_text):
    return f"""
Extrais les expériences du CV en JSON.

MÉTHODE :

1. REPÉRAGE :
   Liste tous les blocs : [Entreprise | Dates | Poste]

2. EXTRACTION PAR BLOC :
   Pour chaque bloc :
   - Cherche TOUTES les tâches (lignes avec -, • ou sans point) dans sa zone.
   - Zone = depuis l'en-tête du bloc jusqu'au prochain bloc
   - Si aucune tâche dans la zone → cherche avant/après si elles ont été déplacées

3. RATTACHEMENT :
   - Poste sans entreprise ? → rattache à l'entreprise la plus proche logiquement
   - Tâches orphelines ? → rattache au bloc correspondant thématiquement
   - Blocs avec Tâches:[] ? → cherche si des tâches existent ailleurs dans le CV
   - Logiciels et outils : Extrais uniquement ceux mentionnés dans la zone de l'expérience ou explicitement liés à celle-ci.
   - Calcule la "Durée_expérience" pour chaque bloc (ex: "1 an et 6 mois").
   - Si la date de fin est "Aujourd'hui" ou "Présent", utilise la date actuelle (Janvier 2026).

4. VÉRIFICATION :
   - Chaque tâche n'apparaît qu'UNE SEULE fois
   - Aucun bloc vide si des tâches existent dans le CV
   - Ordre chronologique inverse

5 RÈGLES :
    - Ne mélange JAMAIS les tâches entre blocs
    - N'oublie AUCUNE tâche du CV
    - Ne laisse PAS de Tâches:[] si le CV contient des tâches pour ce bloc

CV :
{cv_text}

JSON uniquement :
{{
  "Expériences": [
    {{
      "Poste": "",
      "Nom_Entreprise": "",
      "Dates": "",
      "Durée_expérience": "",
      "Mission": "",
      "Masse_achat": "",
      "Périmètre": "",
      "Tâches": [],
      "Logiciels_outils": []
    }}
  ]
}}
"""
