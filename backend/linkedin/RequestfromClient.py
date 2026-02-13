from typing import Optional

from pydantic import BaseModel


class RequestfromClient(BaseModel):  # contrat
    intitule: str
    mode: str
    details: str
    offre: Optional[str]
