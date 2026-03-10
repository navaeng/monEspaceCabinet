def generate_initial(data):
    nom_prenom = data.get('Nom_Prénom', '').split()
    if len(nom_prenom) >= 2:
        initiales = (nom_prenom[0][0] + nom_prenom[1][:2]).upper()
    else:
        initiales = ""
    return initiales