# import groq
from data.call_groq import call_groq


def prompt_check_ia_profile(offre, profile_main_content):

    prompt = f"""
        Analyse ce profil LinkedIn : {profile_main_content}
        Est-ce qu'il correspond à cette {offre} ?
        Réponds uniquement par 'OUI' ou 'NON'.
        Si le profil semble être d'une correspondance réellement idéal, réponds 'OUI TOP'
        """

    response_ia = call_groq(prompt) or ""
    response_clear = response_ia.strip().lower()
    parts = response_clear.split()
    is_match = "oui" in parts
    is_top = "top" in parts
    print(f"Reponse IA: {response_clear}")
    print(f"✅ [IA CHECK] Verdict: {'Accepté' if is_match else 'Refusé'}")
    print(f"✅ [IA CHECK] Top: {'Oui' if is_top else 'Non'}")
    return is_match, is_top
