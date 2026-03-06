from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse

from core.USECASE.linkedin.chrome.stream_generator import stream_generator
from core.USECASE.linkedin.classes.UserRequest import  UserRequest
from core.USECASE.linkedin.classes.object_user_data import object_user_data
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
    user_data = object_user_data(body, current_user_id)
    generate_next_hour = generate_hour()

    insert_prospection_settings(body, cabinet_id, current_user_id, generate_next_hour)

    return StreamingResponse(stream_generator(body, user_data), media_type="text/plain")
