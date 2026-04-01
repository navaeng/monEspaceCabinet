def extract_subject(ai_response):
    for line in ai_response.split("\n"):
        if line.startswith("Objet :"):
            return line.replace("Objet :", "").strip()
    return "Suivi de votre candidature"