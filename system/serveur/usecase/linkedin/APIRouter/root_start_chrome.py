from fastapi import Depends, APIRouter
from starlette.responses import StreamingResponse

from usecase.linkedin.generator.streaming.stream_generator import stream_generator
from usecase.linkedin.classes.user.UserRequest import  UserRequest
from usecase.linkedin.objects.user.object_user_data import object_user_data
from usecase.linkedin.query.tables.cabinets.get.get_cabinet_id import get_cabinet_id
from usecase.linkedin.query.tables.prospection_settings.insert.insert_prospection_settings import insert_prospection_settings
from usecase.linkedin.query.tables.user.get.get_user_id import get_user_id
from usecase.linkedin.query.tables.user.get.get_user_informations import get_user_informations
from usecase.linkedin.services.python_functions.generate_next_hour import generate_next_hour

router_start_chrome = APIRouter()


@router_start_chrome.post("/backend/linkedin/start_chrome")
async def root_start_chrome(
    body: UserRequest,
    current_user_id: str = Depends(get_user_id),
):
    cabinet_id =  await get_cabinet_id(current_user_id)
    user_data = object_user_data(body, current_user_id)
    user_data = get_user_informations(user_data)
    next_hour = generate_next_hour()

    if body.is_manual:
        insert_prospection_settings(body, cabinet_id, current_user_id, next_hour)

    return StreamingResponse(stream_generator(body, user_data), media_type="text/plain")
