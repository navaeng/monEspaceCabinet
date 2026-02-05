# import groq
from data.call_groq import call_groq


def prompt_check_ia_profile(offre, profile_main_content):

    prompt = f"""
        Analyse ce profil LinkedIn : {profile_main_content}
        Est-ce qu'il correspond à cette {offre} ?
        Réponds uniquement par 'OUI' ou 'NON'.
        """

    response_ia = call_groq(prompt) or ""
    response_clear = response_ia.strip().lower()
    print(f"Reponse IA: {response_clear}")
    print(
        f"✅ [IA CHECK] Verdict: {'Accepté' if 'OUI' in response_clear else 'Refusé'}"
    )

    return "OUI" in response_clear
