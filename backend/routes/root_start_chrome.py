from fastapi import Depends, APIRouter

from core.USECASE.linkedin.classes.UserRequest import  UserRequest
from core.USECASE.linkedin.components.generate_hour import generate_hour
from core.query.cabinets.get_cabinet_id import get_cabinet_id
from core.query.cabinets.insert_prospection_settings import insert_prospection_settings
from core.query.user.get_user_id import get_user_id

router_start_chrome = APIRouter()

@router_start_chrome.post("/backend/linkedin/start_chrome")
async def root_start_chrome(
    body: UserRequest,
    current_user_id: str = Depends(get_user_id),
    cabinet_id: str = Depends(get_cabinet_id),
):

    generate_next_hour = generate_hour()

    insert_prospection_settings(body, cabinet_id, current_user_id, generate_next_hour)
