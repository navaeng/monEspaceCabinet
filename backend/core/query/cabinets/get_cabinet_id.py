from data.database import supabase_client


def get_cabinet_id(current_user_id, cabinet_id):
    cabinet_id = None
    res_cabinet = (
        supabase_client.table("profiles")
        .select("cabinet_id")
        .eq("id", current_user_id)
        .single()
        .execute()
    )

    if res_cabinet.data and isinstance(res_cabinet.data, dict):
        cabinet_id = res_cabinet.data.get("cabinet_id")

    return cabinet_id
