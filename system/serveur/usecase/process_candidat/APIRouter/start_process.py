from pydantic import BaseModel
from fastapi import APIRouter, HTTPException
from services.api_externes.openrouter.call_openrouter import call_openrouter
from usecase.process_candidat.IA.prompt.prompt_mail import prompt_mail
# from usecase.process_candidat.classes.UserMailSchema import UserMailSchema
from usecase.process_candidat.mail.send_mail import send_mail

router_start_process = APIRouter()

class UserMailSchema(BaseModel):
    nom: str
    email: str
    notes_mail: str

@router_start_process.post("/envoyer-email")
async def root_start_process(data: UserMailSchema):
    try:

        prompt = prompt_mail(data.nom, data.notes_mail)
        ai_response = call_openrouter(prompt, "google/gemini-2.0-flash-001", json_mode=True)
        await send_mail(data, ai_response)

        return {"status": "success", "ai_msg": ai_response}

    except Exception as e:
        print(f"Erreur : {e}")
        raise HTTPException(status_code=500, detail=str(e))