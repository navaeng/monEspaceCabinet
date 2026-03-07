import os

import yagmail


def send_mail(argument, url, user_data):
    print(f"✅ [MAIL] Sent email with URL: {url}")

    email = os.environ.get("our_email")
    password = os.environ.get("our_pass")
    email_user = user_data.get("email")

    print(f"Email: {email}, Password: {password}, Email User: {email_user}")

    yag = yagmail.SMTP(email, password)
    yag.send(
        to=email_user,
        subject="Profil Top",
        contents=f"{argument}, {url}",
    )
    print("✅ [MAIL] Email sent successfully")
