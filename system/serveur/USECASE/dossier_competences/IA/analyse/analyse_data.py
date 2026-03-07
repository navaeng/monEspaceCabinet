from services.api_externes.groq.call_groq import call_groq
from USECASE.dossier_competences.IA.prompt.clean.clean_prompt import clean_prompt
from USECASE.dossier_competences.services.data.read_cv import read_cv

def analyse_data(file_path):
    cv_text = read_cv(file_path)
    if not cv_text:
        print("Erreur : Impossible de lire le texte du CV")
        return ""
    prompt = clean_prompt(cv_text)
    output = call_groq(prompt)

    if output:
        print(" CV ordonné et nettoyé avec succès.")
        print(output)
        return output

    return cv_text
