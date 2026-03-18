from fastapi import APIRouter, Depends

from classes.CollaborateurBody import CollaborateurBody
from query.collaborateurs.ajouter_collaborateur import query_ajouter_collaborateur
from usecase.linkedin.query.tables.cabinets.get.get_cabinet_id import get_cabinet_id

router_add_collaborator = APIRouter()

@router_add_collaborator.post("/endpoint/add_collaborator")
async def root_add_collaborator(body: CollaborateurBody):

    current_user_id = body.admin_id
    print(current_user_id)
    cabinet_id = get_cabinet_id(current_user_id)

    return query_ajouter_collaborateur(body, cabinet_id)