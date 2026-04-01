import os

import resend

resend.api_key = os.environ.get("RESEND_API")
from usecase.process_candidat.classes.UserMailSchema import UserMailSchema

async def send_mail(data: UserMailSchema, ai_response: str):

    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": "kouicicontact@yahoo.com",
            "subject": f"Nouveau process : {data.nom}",
            "html": f"<p>{ai_response}</p>"
        }
        resend.Emails.send(params)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))