import os

import resend

resend.api_key = os.environ.get("RESEND_API")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import resend

router_envoyer_mail = APIRouter()

class EmailSchema(BaseModel):
    nom: str
    email: str
    points: str

@router_envoyer_mail.post("/envoyer-email")
async def root_envoyer_mail(data: EmailSchema):
    try:
        params = {
            "from": "onboarding@resend.dev",
            "to": "kouicicontact@yahoo.com",
            "subject": f"Nouveau process : {data.nom}",
            "html": f"<p><strong>Candidat :</strong> {data.nom}</p><p><strong>Notes :</strong> {data.points}</p>"
        }
        resend.Emails.send(params)
        return {"status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))