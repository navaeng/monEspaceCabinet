from pydantic import BaseModel

class UserMailSchema(BaseModel):
    nom: str
    email: str
    notes_mail: str