import resend

resend.api_key = "re_KNzSW2NY_4DUhnNFD3qayPRs7BWwgZxtT"

def envoyer_mail(email_utilisateur, nom_utilisateur):
    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": "kouicicontact@yahoo.com",
            "subject": f"Confirmation pour {nom_utilisateur}",
            "html": f"<strong>Bravo {nom_utilisateur} !</strong> Ton clic a bien été enregistré pour l'adresse {email_utilisateur}."
        }

        r = resend.Emails.send(params)
        print(f"Mail envoyé avec succès ! ID: {r['id']}")

    except Exception as e:
        print(f"Erreur lors de l'envoi : {e}")