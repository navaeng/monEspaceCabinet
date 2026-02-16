def post_prompt(post, full_name, telephone, cabinet_name):
    return f"""
    Nous sommes un cabinet de conseil et nous postons sur LinkedIn, aidez-nous à créer un message court et prêt à être posté sur LinkedIn.
    Prends en compte les instructions suivantes : {post}
    Attention aucun caractère spéciaux, le message doit être prêt à être posté sur LinkedIn.
    Indique mes coordonnées : {full_name} - {telephone} - {cabinet_name}
""".strip()
