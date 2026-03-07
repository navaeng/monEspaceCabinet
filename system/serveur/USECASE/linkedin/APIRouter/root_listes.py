from fastapi import Depends, APIRouter
from query.get_job_listes import get_listes
from query.user.get_user_id import get_user_id

router_listes = APIRouter()

@router_listes.get("/backend/prospection/list")
async def root_listes(current_user_id: str = Depends(get_user_id)):
    return get_listes(current_user_id)
