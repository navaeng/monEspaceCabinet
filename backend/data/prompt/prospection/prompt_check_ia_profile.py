# import groq
from backend.data.call_groq import call_groq


def prompt_check_ia_profile(job_title, profile_main_content):

    prompt = f"""
        Analyse ce profil LinkedIn : {profile_main_content}
        Est-ce qu'il correspond à un poste de {job_title} ?
        Réponds uniquement par 'OUI' ou 'NON'.
        """

    response_ia = call_groq(prompt) or ""
    response_clear = response_ia.strip().lower()

    return "OUI" in response_clear
