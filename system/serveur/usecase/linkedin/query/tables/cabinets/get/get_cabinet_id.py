from data.database import supabase_client
from data.get_admin_client import get_admin_client


def get_cabinet_id(current_user_id: str):
    cabinet_id = None
    try:

        res_cabinet = (
            get_admin_client().table("profiles")
            .select("cabinet_id")
            .eq("id", current_user_id)
            .limit(1)
            .execute()
        )

        if res_cabinet.data and len(res_cabinet.data) > 0:
            cabinet_id = res_cabinet.data[0].get("cabinet_id")


    except Exception as e:
        print(f"Erreur lors de la récupération du cabinet: {e}")
        cabinet_id = None

    return cabinet_id