import json
import os

import resend
from fastapi import HTTPException

from usecase.process_candidat.classes.UserMailSchema import UserMailSchema
from usecase.process_candidat.mail.extract.extract_subject import extract_subject

resend.api_key = os.environ.get("RESEND_API")

async def send_mail(data: UserMailSchema, ai_response: str):

    try:
        try:
            res = json.loads(ai_response)
            email_text = res.get("email", res).get("body", ai_response)
        except:
            email_text = ai_response

        html_response = email_text.replace("\n", "<br>")

        params = {
            "from": "onboarding@resend.dev",
            "to": data.email,
            "subject": extract_subject(ai_response),
            "html": f'<p style="font-family: "Helvetica Neue", Arial, sans-serif; font-size: 15px; line-height: 1.7;">{html_response}</p>'
        }
        resend.Emails.send(params)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))