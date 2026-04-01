import resend

resend.api_key = "re_KNzSW2NY_4DUhnNFD3qayPRs7BWwgZxtT"

params = {
    "from": "onboarding@resend.dev",
    "to": "kouicicontact@yahoo.com",
    "subject": "Test Resend Python",
    "html": "<strong>Ça marche !</strong>"
}

email = resend.Emails.send(params)
print(email)