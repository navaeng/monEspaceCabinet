from core.query import config_db


def fill_email(find_email_input, slow_type):
    email_user = config_db.get("linkedin_email")
    if email_user:
        print(f"DEBUG: Saisie de l'email: {email_user}")
        find_email_input.click()
        slow_type(find_email_input, email_user)
    else:
        print("Email manquant dans config_db")
        yield "Email linkedin non trouvé dans vos infos..."
        return