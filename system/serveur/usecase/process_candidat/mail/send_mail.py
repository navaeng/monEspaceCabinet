import os

import resend
from fastapi import HTTPException

from usecase.process_candidat.classes.UserMailSchema import UserMailSchema
from usecase.process_candidat.mail.extract.extract_subject import extract_subject

resend.api_key = os.environ.get("RESEND_API")

async def send_mail(data: UserMailSchema, ai_response: str):

    try:
        # html_response = ai_response.replace("\n", "<br>")
        body = ai_response.split("\n", 2)[-1].strip()

        params = {
            "from": "onboarding@resend.dev",
            "to": "kouicicontact@yahoo.com",
            "subject": extract_subject(ai_response),
            "html_response" : body.replace("\n", "<br>")
        }
        resend.Emails.send(params)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))