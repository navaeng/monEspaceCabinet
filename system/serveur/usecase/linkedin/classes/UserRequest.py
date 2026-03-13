from typing import Optional

from pydantic import BaseModel

class UserRequest(BaseModel):  # contrat
    id: Optional[int] = None
    intitule: str
    mode: str
    details: str
    segment: Optional[str] = ""
    candidatrecherche: str
    post: Optional[str]
    telephone: Optional[str] = ""
    full_name: Optional[str] = ""
    is_manual: Optional[bool] = False
