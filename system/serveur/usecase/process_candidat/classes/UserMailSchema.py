from pydantic import BaseModel

class UserMailSchema(BaseModel):
    nom: str
    email: str
    notes_mail: str
    remuneration: str
    poste: str
    doc: str
    prochaine_etape: str
    lieu: str