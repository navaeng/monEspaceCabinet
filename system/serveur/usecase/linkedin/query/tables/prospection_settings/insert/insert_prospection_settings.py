from data.database import supabase_client


def insert_prospection_settings(body, cabinet_id, current_user_id, new_hour):
    try:
        res = supabase_client().table("prospection_settings").insert(
            {
                "job_title": body.intitule,
                "query": body.intitule,
                "hour_start": new_hour.isoformat(),
                "is_active": True,
                "details": body.details,
                "cabinet_id": cabinet_id,
                "mode": body.mode,
                "user_id": current_user_id,
            }
        ).execute()

        return res.data[0]['id']

    except Exception as e:
            print(f" ERREUR SUPABASE INSERT : {e}")
            return None