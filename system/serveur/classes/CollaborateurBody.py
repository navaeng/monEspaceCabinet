from pydantic import BaseModel

class CollaborateurBody(BaseModel):
    email: str
    password: str
    nom: str
    role: str
    admin_id: str
    # cabinet_id: str
    # current_user_id: str