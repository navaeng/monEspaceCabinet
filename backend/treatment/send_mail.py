def send_mail(argument, url, config_db):
    print(f"✅ [MAIL] Sent email with URL: {url}")
    import os

    import yagmail

    email = os.environ.get("our_email")
    password = os.environ.get("our_password")
    email_user = config_db.get("linkedin_email")

    yag = yagmail.SMTP(email, password)
    yag.send(
        to=email_user,
        subject="Profil Top",
        contents=f"{argument}, {url}",
    )
    print("✅ [MAIL] Email sent successfully")
