from data.database import supabase_client


def insert_prospection_settings(body, cabinet_id, current_user_id):
    try:
        supabase_client().table("prospection_settings").insert(
            {
                "job_title": body.intitule,
                "query": body.intitule,
                "is_active": True,
                "details": body.details,
                "cabinet_id": cabinet_id,
                "mode": body.mode,
                "user_id": current_user_id,
            }
        ).execute()
    except Exception as e:
        print(f" ERREUR SUPABASE INSERT DANS LA TABLE PROSPECTION_SETTINGS : {e}")
