from fastapi import Depends

from core.query.user.get_user_id import get_user_id
from data.database import supabase_client


async def get_cabinet_id(current_user_id: str = Depends(get_user_id)):
    cabinet_id = None
    res_cabinet = (
        supabase_client.table("profiles")
        .select("cabinet_id")
        .eq("id", current_user_id)
        .limit(1)
        .execute()
    )

    if res_cabinet.data and isinstance(res_cabinet.data, dict):
        cabinet_id = res_cabinet.data[0].get("cabinet_id")

    return cabinet_id
