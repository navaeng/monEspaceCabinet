# import openai
from openai import AsyncOpenAI
import os
async def faire_recherche_openrouter(nom_entreprise):
    if not nom_entreprise or len(nom_entreprise) < 2:
        return ""

    client = AsyncOpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.environ.get("OPENROUTERAPI"))
    print(client)

    try:
        print('lancement de recherche en ligne...')
        completion = await client.chat.completions.create(
        model="google/gemini-2.0-flash-001:online",
            messages=[{
                "role": "user",
                "content": (
                    f"Recherche le secteur d'activité de l'entreprise '{nom_entreprise}'. "
                    f"Réponds UNIQUEMENT en JSON valide, sans texte autour, sans balises markdown, dans ce format exact : "
                    f'{{"Secteur_entreprise": "valeur en une phrase courte"}}'
                )
            }]
        )
        res = completion.choices[0].message.content.strip()
        print(f"Brut reçu: {res}")
        return res
    except Exception as e:
        print(f"Erreur: {e}")
        return "Erreur recherche"