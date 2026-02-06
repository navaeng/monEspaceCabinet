def send_mail(argument, url):
    print(f"✅ [MAIL] Sent email with URL: {url}")
    import yagmail

    yag = yagmail.SMTP("contact.kcc0@gmail.com", "jhhvrhyusnhneyuu")
    yag.send(
        to="kouicicontact@yahoo.com",
        subject="Profil Top",
        contents=f"{argument}, {url}",
    )
    print("✅ [MAIL] Email sent successfully")
