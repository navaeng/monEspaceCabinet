import os

import yagmail


def send_mail(argument, url, config_db):
    print(f"✅ [MAIL] Sent email with URL: {url}")

    email = os.environ.get("our_email")
    password = os.environ.get("our_pass")
    email_user = config_db.get("email")

    print(f"Email: {email}, Password: {password}, Email User: {email_user}")

    yag = yagmail.SMTP(email, password)
    yag.send(
        to=email_user,
        subject="Profil Top",
        contents=f"{argument}, {url}",
    )
    print("✅ [MAIL] Email sent successfully")
