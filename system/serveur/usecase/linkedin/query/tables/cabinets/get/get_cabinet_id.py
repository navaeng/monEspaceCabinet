from data.database import supabase_client


async def get_cabinet_id(current_user_id):
    try:
        res_cabinet = (
            supabase_client().table("profiles")
            .select("cabinet_id")
            .eq("user_id", current_user_id)
            .limit(1)
            .execute()
        )

        if res_cabinet.data and len(res_cabinet.data) > 0:
            return res_cabinet.data[0].get("cabinet_id")

    except Exception as e:
        print(f"ERREUR RÉCUPÉRATION CABINET_ID : {e}")

    return None