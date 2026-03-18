from fastapi import APIRouter

from classes.CollaborateurBody import CollaborateurBody
from query.collaborateurs.ajouter_collaborateur import query_ajouter_collaborateur

router_add_collaborator = APIRouter()

@router_add_collaborator.post("/endpoint/add_collaborator")
async def root_add_collaborator(body: CollaborateurBody):

    return query_ajouter_collaborateur(body)

