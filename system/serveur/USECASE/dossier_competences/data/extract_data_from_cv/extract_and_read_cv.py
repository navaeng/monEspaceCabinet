from services.api_externes.groq import call_groq
from USECASE.dossier_competences.services.prompt.clean_prompt import clean_prompt
from USECASE.dossier_competences.services.cv.read_cv import read_cv

def extract_and_read_cv(file_path):
    print("Début de extract_diplomes_from_cv")
    cv_text = read_cv(file_path)
    if not cv_text:
        print("Erreur : Impossible de lire le texte du CV")
        return ""
    prompt = clean_prompt(cv_text)
    output = call_groq(prompt)

    if output:
        print(" CV ordonné et nettoyé avec succès.")
        return output

    return cv_text
