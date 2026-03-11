def main_prompt(cv_text, current_template):

    return f"""En tant qu'expert pour un cabinet de conseil, analyse ce CV pour générer un dossier de compétences 
    valorisant en complétant
      le JSON suivant, applique strictement l'instruction de formatage contenue dans chaque nom de clé JSON. 
      CV: {cv_text}
      JSON: {current_template}
"""