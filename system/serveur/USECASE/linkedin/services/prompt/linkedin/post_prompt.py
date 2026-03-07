def post_prompt(post, full_name, telephone, cabinet_name):
    print("nom du cabinet ", cabinet_name)
    return f"""
    Nous sommes un cabinet de conseil et nous postons sur LinkedIn, aidez-nous à créer un message court et prêt à être posté sur LinkedIn.
    L'objectif du post est d'avoir de nouveaux clients.
    Ne fait pas de fautes de frappe ou d'orthographe.
    Prends en compte les instructions suivantes : {post}
    Attention aucun caractère spéciaux, le message doit être prêt à être posté sur LinkedIn.
    Indique mes coordonnées : {full_name} - {telephone} - {cabinet_name}
""".strip()
