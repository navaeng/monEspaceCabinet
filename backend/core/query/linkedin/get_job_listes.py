from data.database import supabase_client


def get_listes(current_user_id):
    try:
        print(
            f"DEBUG: get_prospection_list a reçu : '{current_user_id}' (type: {type(current_user_id)})"
        )
        if not current_user_id or current_user_id == "None":
            print("id user invalide")
            return []

        res = (
            supabase_client.table("prospection_settings")
            .select("id, job_title, created_at, is_active, hour_start")
            .eq("user_id", current_user_id)
            .order("created_at", desc=True)
            .execute()
        )

        return res.data if res.data else []

    except Exception as e:
        print(f"Erreur Supabase: {e}")
        return []
