def prompt_mail(nom, notes_mail):
    return f"""Rédige un email professionnel pour {nom}.

CONTEXTE : Cabinet de conseil, email suite à un processus de recrutement.

Les notes ci-dessous sont des points à intégrer naturellement dans l'email, pas le sujet unique :
Notes : {notes_mail}

Voici le format exact à respecter :

Objet : Suivi de votre candidature

Bonjour {nom},

Nous espérons que vous allez bien. Suite à nos échanges, nous revenons vers vous concernant votre candidature.

Pourriez-vous nous transmettre votre pièce d'identité dans les meilleurs délais afin de finaliser votre dossier ?

Nous restons disponibles pour toute question.

Cordialement,
L'équipe de recrutement"""