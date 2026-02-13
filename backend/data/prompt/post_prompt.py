def post_prompt(post):
    return f"""
    Prends en compte les instructions suivantes : {post} et génére un post sur LinkedIn en tant que cabinet de conseil, le message doit etre court et pret a être posté sur LinkedIn sans parenthèses
    ou autres caractères spéciaux.
""".strip()
