from pydantic import BaseModel

class CollaborateurBody(BaseModel):
    email: str
    password: str
    # cabinet_id: str
    # current_user_id: str