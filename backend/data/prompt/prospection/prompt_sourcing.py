def prompt_sourcing(candidatrecherche):
    return f"""
    ### ROLE
    Expert en Sourcing Recrutement (LinkedIn Boolean Search).

    ### MISSION
    Si {candidatrecherche} n'est pas vide !
    Génère une URL de recherche LinkedIn optimisée pour ces critères :
    "{candidatrecherche}"

    ### CONTRAINTES
    1. Utilise les opérateurs booléens (AND, OR, NOT) pour les compétences.
    2. L'URL doit pointer vers 'https://www.linkedin.com/search/results/people/'.
    3. Ajoute les mots-clés dans le paramètre 'keywords'.
    4. Si certains filtres ne peuvent pas être appliqué sur l'url ne la casse pas et garde une url valide.

    ### FORMAT DE SORTIE
    Réponds UNIQUEMENT avec un JSON brut (pas de markdown, pas de texte) :
    {{
      "target_url": "https://www.linkedin.com/search/results/people/?keywords=..."
    }}
    """.strip()
