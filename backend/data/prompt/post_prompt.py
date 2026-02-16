def post_prompt(post, full_name, telephone):
    return f"""
    Prends en compte les instructions suivantes : {post} et génére un post sur LinkedIn en tant que cabinet de conseil, le message doit etre court et pret a être posté sur LinkedIn sans parenthèses
    ou autres caractères spéciaux.
    Indique mes coordonnées : {full_name} - {telephone}
""".strip()
